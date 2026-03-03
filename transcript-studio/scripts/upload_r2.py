#!/usr/bin/env python3
"""Upload extracted frames to Cloudflare R2 for Notion embedding.

Uploads all frames from tmp/frames/<VIDEO_ID>/ to an R2 bucket,
preserving the VIDEO_ID/filename structure. Outputs the public
base URL for use with export_notion.py --image-base-url.

Required env vars:
  CF_ACCOUNT_ID       - Cloudflare account ID
  CF_R2_ACCESS_KEY    - R2 API access key ID
  CF_R2_SECRET_KEY    - R2 API secret access key
  CF_R2_BUCKET        - R2 bucket name (default: transcript-frames)
  CF_R2_PUBLIC_URL    - Public URL prefix (e.g. https://pub-<hash>.r2.dev)

Optional env vars:
  CONTENT_SCOUT_WORKDIR - Working directory (default: cwd)
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from pathlib import Path
from typing import Any

# Load .env from workdir (via _common's auto-loader)
try:
    from . import _common as _  # noqa: F401 — triggers .env load
except ImportError:
    try:
        import _common as _  # noqa: F401 — direct script invocation
    except ImportError:
        pass  # standalone usage without _common

try:
    import boto3
    from botocore.config import Config as BotoConfig
except ImportError:
    boto3 = None  # type: ignore[assignment]
    BotoConfig = None  # type: ignore[assignment, misc]

LOGGER = logging.getLogger("content_scout.upload_r2")

DEFAULT_BUCKET = "transcript-frames"
FRAME_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--frames-dir",
        default="tmp/frames",
        help="Directory containing per-video frame folders (default: tmp/frames)",
    )
    parser.add_argument(
        "--video-id",
        help="Upload frames for a single video ID only",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List files that would be uploaded without uploading",
    )
    parser.add_argument("--verbose", action="store_true", help="Enable debug logs")
    return parser.parse_args()


def resolve_workdir() -> Path:
    workdir = os.environ.get("CONTENT_SCOUT_WORKDIR", "").strip()
    return Path(workdir) if workdir else Path.cwd()


def get_r2_client() -> Any:
    """Create an S3-compatible client for Cloudflare R2."""
    if boto3 is None:
        LOGGER.error("boto3 is required for R2 uploads. Install with: pip install boto3")
        sys.exit(1)

    account_id = os.environ.get("CF_ACCOUNT_ID", "").strip()
    access_key = os.environ.get("CF_R2_ACCESS_KEY", "").strip()
    secret_key = os.environ.get("CF_R2_SECRET_KEY", "").strip()

    if not account_id:
        LOGGER.error("CF_ACCOUNT_ID env var is required")
        sys.exit(1)
    if not access_key or not secret_key:
        LOGGER.error("CF_R2_ACCESS_KEY and CF_R2_SECRET_KEY env vars are required")
        sys.exit(1)

    endpoint_url = f"https://{account_id}.r2.cloudflarestorage.com"

    return boto3.client(
        "s3",
        endpoint_url=endpoint_url,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        config=BotoConfig(
            retries={"max_attempts": 3, "mode": "adaptive"},
            s3={"addressing_style": "path"},
        ),
        region_name="auto",
    )


def content_type_for(path: Path) -> str:
    suffix = path.suffix.lower()
    return {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
    }.get(suffix, "application/octet-stream")


def collect_frames(frames_dir: Path, video_id: str | None) -> list[tuple[Path, str]]:
    """Collect (local_path, r2_key) pairs for all frames to upload."""
    results: list[tuple[Path, str]] = []

    if video_id:
        video_dirs = [frames_dir / video_id]
    else:
        video_dirs = sorted(
            d for d in frames_dir.iterdir() if d.is_dir()
        )

    for video_dir in video_dirs:
        if not video_dir.exists():
            LOGGER.warning("Frame directory not found: %s", video_dir)
            continue

        vid = video_dir.name
        frame_files = sorted(
            f for f in video_dir.iterdir()
            if f.is_file() and f.suffix.lower() in FRAME_EXTENSIONS
        )

        for frame_file in frame_files:
            r2_key = f"{vid}/{frame_file.name}"
            results.append((frame_file, r2_key))

    return results


def upload_frames(
    client: Any,
    bucket: str,
    frames: list[tuple[Path, str]],
    dry_run: bool,
) -> tuple[int, int]:
    """Upload frames to R2. Returns (uploaded, failed) counts."""
    uploaded = 0
    failed = 0

    for local_path, r2_key in frames:
        if dry_run:
            LOGGER.info("DRY-RUN: would upload %s → s3://%s/%s", local_path, bucket, r2_key)
            uploaded += 1
            continue

        try:
            client.upload_file(
                str(local_path),
                bucket,
                r2_key,
                ExtraArgs={
                    "ContentType": content_type_for(local_path),
                    "CacheControl": "public, max-age=31536000, immutable",
                },
            )
            LOGGER.info("Uploaded %s → %s", local_path.name, r2_key)
            uploaded += 1
        except Exception as exc:  # noqa: BLE001
            LOGGER.error("Failed to upload %s: %s", r2_key, exc)
            failed += 1

    return uploaded, failed


def main() -> int:
    args = parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )

    workdir = resolve_workdir()
    frames_dir = workdir / args.frames_dir

    if not frames_dir.exists():
        LOGGER.error("Frames directory does not exist: %s", frames_dir)
        return 1

    public_url = os.environ.get("CF_R2_PUBLIC_URL", "").strip().rstrip("/")
    if not public_url:
        LOGGER.error("CF_R2_PUBLIC_URL env var is required (e.g. https://pub-<hash>.r2.dev)")
        return 1

    bucket = os.environ.get("CF_R2_BUCKET", DEFAULT_BUCKET).strip()

    frames = collect_frames(frames_dir, args.video_id)
    if not frames:
        LOGGER.warning("No frames found to upload")
        # Not an error — videos may have no visual frames
        result = {"uploaded": 0, "failed": 0, "baseUrl": public_url}
        print(json.dumps(result))
        return 0

    LOGGER.info(
        "Found %d frame(s) to upload to R2 bucket '%s'",
        len(frames), bucket,
    )

    if args.dry_run:
        client = None
    else:
        client = get_r2_client()

    uploaded, failed = upload_frames(client, bucket, frames, args.dry_run)

    result = {
        "uploaded": uploaded,
        "failed": failed,
        "bucket": bucket,
        "baseUrl": public_url,
        "dryRun": args.dry_run,
    }
    print(json.dumps(result))

    if failed > 0:
        LOGGER.error("%d upload(s) failed", failed)
        return 1

    LOGGER.info("✅ Uploaded %d frame(s) to %s", uploaded, public_url)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

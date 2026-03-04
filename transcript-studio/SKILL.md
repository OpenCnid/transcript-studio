---
name: transcript-studio
description: >
  Deep YouTube video processing into rich Notion pages with speaker-diarized transcripts,
  embedded visual frames, and AI-generated summaries. Use when: (1) user asks to process,
  transcribe, or analyze a YouTube video, (2) creating a Notion page from a video,
  (3) running the transcript studio pipeline, (4) generating summaries, chapters, or
  shorts candidates from video content, (5) setting up a Transcript Studio Notion database.
  Depends on content-scout skill for frame extraction and classification steps.
  Requires: Apple Silicon Mac (mlx-whisper), ffmpeg, yt-dlp, Python 3.10+.
---

# Transcript Studio

YouTube video → local transcription (mlx-whisper + speaker diarization) → visual frame
merging → LLM summary → rich Notion page with embedded images.

**Requires content-scout skill installed** for frame extraction (`extract_frames.py`)
and classification (`classify_annotate.py`) steps.

## ⚠️ Success Criteria — VERIFY BEFORE REPORTING DONE

**The pipeline is complete ONLY when the final JSON output contains `"verdict": "COMPLETE"`.**

After the pipeline finishes, check the state file (path relative to working directory):

```bash
python3 -c "
import json
state = json.load(open('tmp/_ts_pipeline_state.json'))
for name, info in state.get('steps', {}).items():
    s = info.get('status', '?')
    icon = '✅' if s == 'completed' else ('❌' if s == 'failed' else '⏳')
    msg = info.get('message', '')[:80]
    print(f'{icon} {name}: {s}  {msg}')
pending = [n for n,i in state.get('steps',{}).items() if i.get('status') != 'completed']
print()
print('PIPELINE COMPLETE ✅' if not pending else f'INCOMPLETE ❌ — {len(pending)} steps remaining: {pending}')
"
```

**All 3 must be true:**
1. Pipeline JSON output shows `"verdict": "COMPLETE"`
2. All 12 steps show `"status": "completed"` in the state file
3. Export step message contains a Notion page ID

**If any check fails, do NOT report success.** Report which steps failed, their error
messages, and whether `--force` or manual intervention is needed.

## Quick Start

```bash
# Process a single video (full pipeline, default finance domain)
python3 scripts/run_transcript_pipeline.py \
  --video-url "https://youtube.com/watch?v=VIDEO_ID" \
  --preset default

# Process a video with a different analysis domain
python3 scripts/run_transcript_pipeline.py \
  --video-url "https://youtube.com/watch?v=VIDEO_ID" \
  --domain openclaw

# Process latest from monitored channels
python3 scripts/run_transcript_pipeline.py --date 2026-02-24

# Resume a failed run (auto-skips completed steps from state file)
python3 scripts/run_transcript_pipeline.py --date 2026-02-24
```

## Pipeline Steps

12 steps, run by `scripts/run_transcript_pipeline.py`:

| Step | Script | Phase | What it does |
|------|--------|-------|-------------|
| select | `select_transcript_videos.py` | Prep | Pick videos from channels/playlists config |
| download | *(content-scout)* `download.py` | Prep | Download via yt-dlp |
| extract | *(content-scout)* `extract_frames.py` | Prep | Extract frames, deduplicate |
| transcribe | `transcribe_local.py` | 1 | mlx-whisper + pyannote diarization |
| window | *(content-scout)* `window_transcripts.py` | 1 | Split transcript into windows |
| classify | *(content-scout)* `classify_annotate.py` | 1 | LLM frame classification |
| merge | `merge_visuals.py` | 2 | Interleave frames into transcript |
| summarize | `summarize_video.py` | 2 | LLM: takeaways, chapters, shorts, slides |
| upload | `upload_r2.py` | 2 | Upload frames to Cloudflare R2 *(optional)* |
| export | `export_notion.py` | 3 | Build Notion page with images |
| log | *(shared)* `update_log.py` | 3 | Update processing log |
| archive | *(shared)* `archive_transcripts.py` | 3 | Archive transcripts |
| cleanup | *(shared)* `cleanup_tmp.py` | 3 | Clean temp files |

Steps marked *(content-scout)* require the content-scout skill's scripts on `sys.path`
or in the same scripts directory.

## Domains

Domains control the **analysis persona, output schema, and Notion page layout** via the
`--domain` flag. All other pipeline steps (download, transcribe, frames, etc.) are shared.

If the user specifies a domain (e.g. "in finance", "in openclaw", "analyze this as an
OpenClaw video"), pass `--domain <name>`. Default: `finance`.

| Domain | Persona | Analysis Section | Best for |
|--------|---------|-----------------|----------|
| `finance` | Macro strategist | 🔥 Signal Extraction Layer (tickers, macro, scores) | Stock/market videos |
| `openclaw` | AI systems architect | 🤖 Tool Analysis (features, setup, scores) | AI tool/framework videos |

Domain prompt files live in `prompts/{domain}/`:

```
prompts/
  finance/
    persona.md          ← System prompt (analyst persona)
    instructions.md     ← Output JSON schema + requirements
  openclaw/
    persona.md          ← System prompt (AI tools evaluator)
    instructions.md     ← Output JSON schema + requirements
```

**Adding a new domain:** Copy an existing domain folder, edit the markdown files to define
the new persona and output schema, and use `--domain <name>` to activate it. No Python
code changes required unless the Notion page needs a custom analysis section layout.

## Presets

Presets in `config/presets/` control frame intervals and whisper model:

| Preset | Frame Interval | Whisper Model | Best for |
|--------|---------------|---------------|----------|
| default | 15s | large-v3-turbo | Finance/trading videos |
| podcast | 30s | large-v3-turbo | Long-form conversation |
| presentation | 5s | large-v3-turbo | Slide-heavy content |
| suno | 10s | large-v3-turbo | Music/feature reviews |

## Notion Page Output

Each video produces a Notion page with:

1. **Metadata callout** — source URL, speakers, duration, date
2. **🔥 Signal Extraction Layer** — macro/stock signal analysis for show production:
   - **Quick Verdict** — 2-3 blunt sentences: is this worth your time and why? (🎯 callout)
   - **Speaker Assessment** — credibility, angle, conviction level, conflicts of interest (🔍 callout)
   - **Scores Dashboard** — 5 metrics rated 0-5 with visual bars (📊 callout):
     Macro Impact · Stock Idea Density · Contrarian Value · AI/Infra Relevance · Show Utility
   - **Market Bias** — tone (Bullish/Bearish/Neutral/Mixed), regime, risk tilt, cycle position
   - **Macro Signals** — rates, credit, liquidity, volatility, structural shifts (or "No meaningful macro signal")
   - **Ticker Mentions** — table: Ticker | Direction | Context | Horizon | Timestamp | Signal Strength
   - **Catalysts** — upcoming events, data releases, or triggers that could move markets
   - **Show Relevance** — 5 active theses (AI 2.0, Software Repricing, Infrastructure, Rate Regime,
     Liquidity Cycle), contradictions, segment potential
3. **TL;DR** — one-paragraph summary
4. **Key Takeaways** — numbered list with timestamps (visible, not toggled)
5. **Chapters** — bulleted timeline with descriptions (visible)
6. **Shorts & Clip Ideas** — toggle with hook/payoff pairs
7. **Slide/Graphic Notes** — toggle with suggestions
8. **Full Transcript** — paragraphs grouped by chapter, visuals inline as images
9. **Visual Index** — toggle with timestamp/type/description table
10. **Raw Transcript** — toggle with full unformatted text

The Signal Extraction Layer is the key differentiator — it turns the pipeline from a content
processor into a **macro/stock signal classifier** that helps decide what to build a show around.

The LLM analyst persona is a 30-year veteran macro strategist with a 4-step analytical framework:
Speaker Assessment → Signal Extraction → Thesis Mapping → Show Utility. It uses a calibrated
0-5 scoring rubric with anchor examples to ensure consistent scoring across videos. System prompt
is sent separately from task instructions for maximum output quality.

Videos with no macro signal are explicitly flagged and scored accordingly so you can skip or
file them differently. The speaker assessment catches promotional content, conflicts of interest,
and conviction levels.

### Image Hosting (Cloudflare R2)

Notion requires public URLs for embedded images. The pipeline includes an `upload` step
that pushes frames to Cloudflare R2 automatically before the export step.

The upload step is **optional** — if `CF_R2_PUBLIC_URL` is not set, it's skipped and
images won't be embedded in Notion pages (callout placeholders are used instead).

Frame paths like `tmp/frames/VIDEO_ID/frame_125s.png` are uploaded preserving the
`VIDEO_ID/filename` structure → `{base_url}/VIDEO_ID/frame_125s.png`.

**R2 Setup:**
1. Cloudflare dashboard → **R2 Object Storage** → **Create bucket** (e.g. `transcript-frames`)
2. Enable **public access** on the bucket (Settings → Public Access → Allow)
3. Create an R2 API token (R2 → Manage R2 API Tokens) with Object Read & Write
4. Set the env vars below

**Standalone usage:**
```bash
python3 scripts/upload_r2.py --frames-dir tmp/frames
python3 scripts/upload_r2.py --video-id VIDEO_ID --dry-run
```

## Working Directory

Set `CONTENT_SCOUT_WORKDIR` to control where output goes (tmp/, transcripts, frames).
Defaults to `cwd`. Config and presets always resolve from the skill installation.

```bash
export CONTENT_SCOUT_WORKDIR=/path/to/project
python3 scripts/run_transcript_pipeline.py --video-url "https://youtube.com/watch?v=..."
```

## Setup

### Notion Database

Run once to create the Transcript Studio database:

```bash
NOTION_TOKEN=ntn_... python3 scripts/setup_transcript_db.py --parent-page-id PAGE_ID
```

Creates database with properties: Name, Date, Channel, Preset, Status, Source URL,
Video ID, Duration, Speakers, Tags, Playlist.

**Note:** Use Notion API version `2022-06-28` for database creation. The `2025-09-03`
version silently drops properties via the Python client.

### Environment Variables

| Variable | Required | Purpose |
|----------|----------|---------|
| `NOTION_TOKEN` | Yes | Notion API integration token |
| `ANTHROPIC_API_KEY` | For summaries | Claude for summarization + classification |
| `OPENAI_API_KEY` | Fallback | Whisper API fallback if mlx-whisper unavailable |
| `HF_TOKEN` | For diarization | HuggingFace token for pyannote speaker model |
| `CF_ACCOUNT_ID` | For images | Cloudflare account ID |
| `CF_R2_ACCESS_KEY` | For images | R2 S3-compatible access key ID |
| `CF_R2_SECRET_KEY` | For images | R2 S3-compatible secret access key |
| `CF_R2_BUCKET` | For images | R2 bucket name (default: `transcript-frames`) |
| `CF_R2_PUBLIC_URL` | For images | Public URL prefix (e.g. `https://pub-<hash>.r2.dev`) |

### Mac Studio Dependencies

```bash
pip install mlx-whisper pyannote-audio notion-client imagehash Pillow \
  python-slugify anthropic openai yt-dlp boto3
brew install ffmpeg
# HuggingFace login for pyannote
huggingface-cli login --token $HF_TOKEN
```

## Running Tests

```bash
cd tests && python3 test_transcript_studio.py
```

98 tests covering all scripts, preset configs, and E2E merge→export flow.
No external API calls needed.

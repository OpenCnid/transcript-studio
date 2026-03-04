# Transcript Studio — Status

**Phase:** Pipeline built, awaiting Mac Studio deployment
**Last Session:** 2026-02-25
**Health:** 🟡 Paused

## Current State
Deep YouTube video processing into rich Notion pages with speaker-diarized transcripts, embedded visual frames, and AI-generated summaries. 7 Python scripts, 4 presets, 128/128 tests passing. Depends on Content Scout for frame extraction/classification. Packaged as .skill file. Supabase Storage configured for frame hosting.

## Next
- [ ] Mac Studio setup: mlx-whisper, pyannote-audio, ffmpeg, yt-dlp, HuggingFace token
- [ ] Hans's Notion API token
- [ ] Anthropic API key for scripts (standard key, not OAuth token)
- [ ] End-to-end test on Mac Studio with real video

## Blockers
- Mac Studio not set up for local inference
- Hans's Notion API token
- Anthropic standard API key (scripts can't use OpenClaw's OAuth token)

## Key Files
- `skills/transcript-studio/scripts/run_transcript_pipeline.py` — pipeline orchestrator
- `skills/transcript-studio/scripts/transcribe_local.py` — mlx-whisper transcription
- `skills/transcript-studio/scripts/export_notion.py` — Notion page builder
- `skills/transcript-studio/SKILL.md` — skill definition
- Supabase Storage bucket: `transcript-frames` on `skleqjejhrtrhlvhyirk`

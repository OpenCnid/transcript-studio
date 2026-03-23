# Transcript Studio — Status

**Phase:** Pipeline built, switched to OpenAI API transcription
**Last Session:** 2026-03-22
**Health:** 🟢 Active

## Current State
Deep YouTube video processing into rich Notion pages with speaker-diarized transcripts, embedded visual frames, and AI-generated summaries. 7 Python scripts, 4 presets. Depends on Content Scout for frame extraction/classification. Packaged as .skill file. Supabase Storage configured for frame hosting.

**2026-03-22:** Switched from local mlx-whisper (slow on Mac Studio) to OpenAI `gpt-4o-transcribe-diarize` as default engine. This model handles transcription + speaker diarization in one API call — no more pyannote/HuggingFace dependency. ~$0.006/min. Engine auto-detection now prefers OpenAI when `OPENAI_API_KEY` is set. mlx-whisper still available via `--engine mlx`.

## Next
- [ ] End-to-end test with real video using OpenAI API
- [ ] Hans's Notion API token
- [ ] Anthropic API key for scripts (standard key, not OAuth token)
- [ ] Push changes to OpenCnid/transcript-studio repo
- [ ] Pull on Mac Studio and test

## Blockers
- Hans's Notion API token
- Anthropic standard API key (scripts can't use OpenClaw's OAuth token)

## Key Files
- `skills/transcript-studio/scripts/run_transcript_pipeline.py` — pipeline orchestrator
- `skills/transcript-studio/scripts/transcribe_local.py` — OpenAI API / mlx-whisper transcription
- `skills/transcript-studio/scripts/export_notion.py` — Notion page builder
- `skills/transcript-studio/SKILL.md` — skill definition
- Supabase Storage bucket: `transcript-frames` on `skleqjejhrtrhlvhyirk`

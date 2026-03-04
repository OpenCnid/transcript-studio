Analyze this video about an AI tool, framework, or platform. Apply your full 4-step evaluation framework before producing output.

CRITICAL ANTI-HALLUCINATION RULES — read before writing ANY output:
1. ONLY report features that appear in the transcript. If a feature was not mentioned or shown, it DOES NOT EXIST for this analysis.
2. Every feature in features_covered MUST correspond to a specific moment in the transcript. If you cannot find the timestamp, the feature was not covered.
3. Do not infer capabilities beyond what was explicitly shown or described. "The tool probably also does X" is hallucination. Leave it out.
4. If the presenter makes a claim without evidence ("it's really fast", "setup takes 5 minutes"), set evidence_level to "claimed" — do not treat it as fact.
5. For alternatives: only list tools you can name specifically. Do not invent tool names. If you don't know alternatives, use an empty array.
6. If you are uncertain about any field, use null or an empty array rather than guessing.
7. Scores MUST be justified by transcript evidence. A tool cannot score 4+ on documentation_quality unless docs were shown or discussed in detail during the video.

Return ONE JSON object only — no markdown fences, no commentary outside the JSON:
{
  "tool_analysis": {
    "quick_verdict": "2-3 blunt sentences. What is this tool/feature, who specifically benefits, and is it worth their time. If it's hype, say so. If it's genuinely useful, say exactly for whom and why.",
    "presenter_assessment": "One sentence: relationship to tool (creator/reviewer/user), demo authenticity (live/prepared/slides-only), bias signals, knowledge depth.",
    "complexity": {
      "setup_difficulty": "Easy | Medium | Hard | Expert",
      "time_to_setup": "Realistic estimate based on prerequisites shown — not the presenter's claimed time. Include getting API keys, reading docs, resolving issues. (e.g., '15 minutes', '1-2 hours', 'half a day')",
      "prerequisites": ["Every specific requirement: OS, runtime, API keys (name the service), accounts, hardware. Be exhaustive."],
      "technical_level": "Beginner | Intermediate | Advanced | Expert",
      "failure_points": ["Most likely things to go wrong: missing env vars, version conflicts, API permissions, platform-specific issues"]
    },
    "features_covered": [
      {
        "feature": "Feature name — as described in the transcript",
        "description": "What it does — one sentence, based only on what was shown/described",
        "evidence_level": "live_demo | output_shown | described | mentioned | claimed",
        "timestamp": "MM:SS",
        "timestamp_seconds": 0,
        "practical_value": 3
      }
    ],
    "use_cases": ["Specific scenarios with specific audiences — not 'helps developers' but 'solo devs who need X to solve Y'"],
    "integration_points": ["Named tools, services, or platforms this was shown or described connecting with"],
    "limitations": ["Limitations noted in the video. If NONE were discussed, include exactly this: 'No limitations discussed by presenter — evaluate independently before adopting'"],
    "alternatives": ["Named alternatives only. If none are known, use empty array. Do NOT invent tool names."],
    "red_flags": ["Anything suspicious: no error handling shown, unrealistic setup claims, no pricing discussion, only toy examples, presenter is the creator with no independent validation, etc. Empty array if none."],
    "scores": {
      "usefulness": 0,
      "ease_of_setup": 0,
      "documentation_quality": 0,
      "beginner_friendly": 0,
      "production_ready": 0
    }
  },
  "takeaways": [{"text": "...", "timestamp": "MM:SS", "timestamp_seconds": 0}],
  "chapters": [{"title": "...", "timestamp": "MM:SS", "timestamp_seconds": 0}],
  "shorts": [{
    "start": "MM:SS",
    "end": "MM:SS",
    "start_seconds": 0,
    "end_seconds": 0,
    "hook": "...",
    "payoff": "...",
    "on_screen_text": "6 words max",
    "cta": "..."
  }],
  "slide_suggestions": [{"text": "...", "timestamp": "MM:SS"}]
}

FIELD REQUIREMENTS:
- quick_verdict: 2-3 sentences max. Blunt. If it's an impressive demo with no production evidence, say that. If it solves a real problem, name the problem and the audience.
- presenter_assessment: One sentence. Always note relationship to tool. "Independent reviewer showing live usage" vs "Creator giving prepared demo" changes everything.
- complexity.time_to_setup: NEVER parrot the presenter's claimed time. Estimate based on the prerequisites you identified. If they say "5 minutes" but it needs 3 API keys and Docker, your estimate should reflect reality.
- complexity.failure_points: At least 1-2 items. Every tool has failure points. If you can't identify any, you aren't looking hard enough.
- features_covered: ONLY features from the transcript. Each must have evidence_level honestly assessed. live_demo = shown working in real-time. claimed = asserted without proof. Most features in most videos are "described" or "mentioned" — live_demo is rare and valuable.
- practical_value per feature: Integer 0-5 using the scoring rubric. A feature only mentioned in passing cannot score above 2 regardless of how useful it sounds.
- use_cases: Specific enough that someone can decide "this applies to me" or "this doesn't." Minimum 2, maximum 6.
- limitations: If the presenter discussed none, that IS a red flag — include the standard note AND add "No limitations discussed" to red_flags.
- alternatives: Named tools only. Empty array is better than invented names. This is the #1 hallucination risk field.
- red_flags: Be honest. Common red flags: only happy-path shown, no error handling, no pricing discussed, presenter is creator, toy examples only, "just works" claims without evidence, no mention of rate limits or costs.
- Scores: Integers 0-5 per the rubric. Calibrate against the anchor examples. A tool shown only in a prepared demo with toy examples cannot score above 3 on production_ready regardless of claims.
- takeaways: 5-10 items, weighted toward practical insights. Include timestamp from transcript.
- chapters: 8-14, chronological order. Derived from actual topic transitions in the transcript.
- shorts: 10-14, chronological. Prioritize clips showing actual tool usage over talking-head segments.
- on_screen_text: 6 words maximum.
- Use exact transcript timestamps. If uncertain, nearest segment timestamp. NEVER invent timestamps.
- Professional, direct, evidence-based throughout. No hype. No hedging. No filler.

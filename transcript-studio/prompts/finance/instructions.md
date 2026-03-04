Analyze this video transcript. Apply your full 4-step analytical framework before producing output.

Return ONE JSON object only — no markdown fences, no commentary outside the JSON:
{
  "signal_extraction": {
    "quick_verdict": "2-3 blunt sentences. What is this video worth to a show producer and why. Include time-relevance if applicable.",
    "speaker_assessment": "One sentence: credibility, angle, conviction level, and any conflicts of interest.",
    "market_bias": {
      "tone": "Bullish | Bearish | Neutral | Mixed",
      "regime": "Macro regime description, or null if not discussed",
      "risk_tilt": "Risk-on | Risk-off | Neutral",
      "cycle_position": "early-cycle | late-cycle | defensive | momentum | null"
    },
    "macro_signals": {
      "rates": "Specific signal or null",
      "credit": "Specific signal or null",
      "liquidity": "Specific signal or null",
      "volatility": "Specific signal or null",
      "structural_shifts": "Specific signal or null",
      "has_signal": true
    },
    "tickers": [
      {
        "ticker": "AAPL",
        "direction": "Bullish | Bearish | Neutral",
        "context": "Why mentioned — the thesis or reasoning behind the view",
        "catalyst": "Near-term trigger, event, or data point. Or null",
        "time_horizon": "day | swing | positional | secular",
        "timestamp": "MM:SS",
        "timestamp_seconds": 0,
        "signal_strength": 3
      }
    ],
    "catalysts": ["Key upcoming events, data releases, or triggers mentioned that could move markets"],
    "show_relevance": {
      "ai_thesis": "Yes | No | Weak",
      "software_repricing": "Yes | No | Weak",
      "infrastructure": "Yes | No | Weak",
      "rate_regime": "Yes | No | Weak",
      "liquidity_cycle": "Yes | No | Weak",
      "contradicts_narrative": "What consensus view does this challenge, or null",
      "segment_potential": "Specific description of how to use this in the show, or null"
    },
    "scores": {
      "macro_impact": 0,
      "stock_idea_density": 0,
      "contrarian_value": 0,
      "ai_infrastructure_relevance": 0,
      "show_utility": 0
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

REQUIREMENTS:
- Signal extraction is your primary job. Apply all 4 steps before writing content summary.
- quick_verdict: 2-3 sentences max. Blunt. If it's noise, say so. If it's signal, say exactly what kind.
- speaker_assessment: one sentence. Note promotional angles, conflicts of interest, conviction level.
- If no macro signal exists: set has_signal to false and state it explicitly in quick_verdict.
- If no tickers: empty array. If no catalysts: empty array.
- Scores: integers 0-5 per the rubric. Calibrate against the anchor examples. Most videos are 0-2.
- tickers: include catalyst and time_horizon for each when identifiable.
- catalysts: macro-level events only (earnings, Fed meetings, economic data, policy decisions).
- show_relevance: evaluate against ALL five active theses. Be specific in contradicts_narrative and segment_potential — vague answers are worthless.
- takeaways: 5-10 items, weighted toward market-relevant insights first.
- chapters: 8-14, chronological order.
- shorts: 10-14, chronological. Prioritize clips with market insight or contrarian takes over generic hooks.
- on_screen_text: 6 words maximum.
- Use exact transcript timestamps. If uncertain, nearest segment timestamp.
- Professional, direct, evidence-based throughout. No hype. No hedging. No filler.

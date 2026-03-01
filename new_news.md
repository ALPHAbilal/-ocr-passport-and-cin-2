Qwen3.5-35B-A3B just dropped — 35B params, only 3B active, beats Qwen3-235B-A22B.

Trending #1 on Hugging Face right now.

This changes everything about how we think about model scaling.

━━━━━━━━━━

The headline:

3B active params now beats 22B active params.

Not through scaling.
Through architecture.

━━━━━━━━━━

What Alibaba did differently:

They replaced standard Transformer attention.

New architecture: Gated DeltaNet + MoE

→ 3 layers of linear attention (DeltaNet)
→ 1 layer of full attention
→ Repeat

3:1 ratio. Linear attention scales near-linearly with context.

Result: 1M token context. Fraction of the compute.

━━━━━━━━━━

The numbers that matter:

• 35B total parameters
• 3B activated per token (91% sparsity)
• 256 experts, 9 active per token
• 262K native context → 1M with YaRN
• 201 languages supported
• Vision + Text unified (early fusion)

━━━━━━━━━━

Benchmarks vs GPT-5-mini:

• MMLU-Pro: 85.3 vs 83.7 ✓
• SWE-bench: 69.2 vs 72.0 (close)
• TAU2-Bench: 81.2 vs 69.8 ✓
• BFCL-V4 (tool use): 67.3 vs 55.5 ✓

A 3B-active open model competing with GPT-5-mini on agents.

━━━━━━━━━━

Vision benchmarks:

• MMMU: 81.4 (vs Claude Sonnet 4.5: 79.6)
• MathVision: 83.9 (vs GPT-5-mini: 71.9)
• VideoMME: 86.6 (with subs)
• AndroidWorld: 71.1

Native multimodal. Not bolted on.

━━━━━━━━━━

Why this architecture matters:

Standard attention: O(n²) with sequence length
Gated DeltaNet: Near-linear scaling

You can now run 1M context without melting your GPUs.

NVIDIA co-developed this. It's production-ready.

━━━━━━━━━━

Cost comparison:

Qwen3.5-Flash: $0.10/M input tokens
Claude Sonnet 4.6: $1.30/M input tokens

13x cheaper. Comparable quality on agents.

━━━━━━━━━━

Run it yourself:

ollama run qwen3.5:35b-a3b

Works on 8GB+ VRAM.
Apache 2.0. Full commercial use.

━━━━━━━━━━

🔗 https://lnkd.in/gkX4qrPN
🐙 github.com/QwenLM/Qwen3.5

━━━━━━━━━━

We've already deployed this for enterprise clients.

Self-hosted agentic RAG. Zero per-token API costs. 1M context running live.
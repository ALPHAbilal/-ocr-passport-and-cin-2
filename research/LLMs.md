Here is a comprehensive, research-backed guide for your CNIE extraction pipeline. **Qwen2.5-1.5B-Instruct** is the top recommendation for your use case: it has native Arabic support (explicitly in its training languages), strong JSON output, and runs comfortably within your latency budget on CPU.

***

## Model Comparison for Structured Extraction

The table below covers the primary candidates, scored on your exact requirements:

| Model | Params | Arabic Support | JSON Output | GGUF Q4_K_M RAM | Ollama Command |
|---|---|---|---|---|---|
| **Qwen2.5-1.5B-Instruct** | 1.5B | ✅ Native | ✅ Excellent | ~1.1 GB | `ollama pull qwen2.5:1.5b` |
| **Qwen2.5-0.5B-Instruct** | 0.5B | ✅ Native | ✅ Good | ~0.5 GB | `ollama pull qwen2.5:0.5b` |
| **Qwen2.5-3B-Instruct** | 3B | ✅ Native | ✅ Best in class | ~2.0 GB | `ollama pull qwen2.5:3b` |
| **Gemma-2-2B-Instruct** | 2B | ⚠️ Partial | ✅ Good | ~1.5 GB | `ollama pull gemma2:2b` |
| **SmolLM2-1.7B-Instruct** | 1.7B | ❌ Minimal | ✅ Good | ~1.1 GB | `ollama pull smollm2:1.7b` |
| **TinyLlama-1.1B** | 1.1B | ❌ None | ⚠️ Weak | ~0.7 GB | `ollama pull tinyllama` |

***

## Arabic Language Support (Critical)

**Qwen2.5 is the clear winner** for Arabic. The entire Qwen2.5 series explicitly lists Arabic (`ar`) among its 29+ natively trained languages, including training on AMMLU (Arabic MMLU) benchmarks. Qwen2-7B outperformed Gemma-2 and Phi-3 on Arabic tasks in multilingual benchmarks with an F1 of 85%+, and this heritage carries down to the 0.5B–3B sizes. [huggingface](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct)

**Gemma-2-2B** has partial Arabic from its base training, and the community reports surprisingly good multilingual performance for a 2B model. However, its Arabic is weaker than Qwen2.5 — you'd benefit from a fine-tune like **GemmAr** or Atlas-Chat. [arxiv](http://arxiv.org/pdf/2407.02147.pdf)

**SmolLM2** and **TinyLlama** are English-centric models. SmolLM2 outperforms Qwen2.5-1.5B on English benchmarks like MMLU-Pro by ~6 points and IFEval, but that advantage disappears for Arabic text. Skip these for your bilingual use case. [arxiv](https://arxiv.org/html/2502.02737v1)

***

## Recommended Models with Setup Details

### 🥇 Qwen2.5-1.5B-Instruct (Best Overall)
- **HuggingFace**: [Qwen/Qwen2.5-1.5B-Instruct-GGUF](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF)
- **Quantized size**: ~1.1 GB (Q4_K_M), ~1.3 GB (Q5_K_M)
- **Arabic support**: Native — trained on Arabic, French, Chinese, and 26 other languages [huggingface](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct)
- **Expected CPU speed**: ~25–40 tokens/sec on a modern laptop (8-core CPU), well under your 5s latency target for short extraction prompts
- **Structured output**: Explicitly designed for reliable JSON generation in post-training [qwenlm.github](https://qwenlm.github.io/blog/qwen2.5/)

```bash
# via Ollama
ollama pull qwen2.5:1.5b

# via llama-cpp-python
pip install llama-cpp-python
```
```python
from llama_cpp import Llama
llm = Llama.from_pretrained(
    repo_id="Qwen/Qwen2.5-1.5B-Instruct-GGUF",
    filename="qwen2.5-1.5b-instruct-q5_k_m.gguf",
    n_ctx=2048,
    n_threads=8,   # use all physical cores
    verbose=False
)
response = llm.create_chat_completion(
    messages=[{"role": "user", "content": your_prompt}],
    response_format={"type": "json_object"}  # enforce JSON mode
)
```

### 🥈 Qwen2.5-3B-Instruct (Best Quality Under 3B)
- **HuggingFace**: [Qwen/Qwen2.5-3B-Instruct-GGUF](https://huggingface.co/Qwen/Qwen2.5-3B-Instruct-GGUF)
- **Quantized size**: ~2.0 GB (Q4_K_M), ~2.4 GB (Q5_K_M)
- **Arabic support**: Native [huggingface](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct)
- **Expected CPU speed**: ~15–25 tokens/sec — still under 5s for short extraction tasks
- Qwen2.5-3B was highlighted as a standout model at its size for efficiency vs capability [qwenlm.github](https://qwenlm.github.io/blog/qwen2.5/)

```bash
ollama pull qwen2.5:3b
```

### 🥉 Qwen2.5-0.5B-Instruct (Ultra-fast / Edge Deploy)
- **HuggingFace**: [Qwen/Qwen2.5-0.5B-Instruct-GGUF](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF)
- **Quantized size**: ~0.5 GB (Q4_K_M)
- **Arabic support**: Native, but expect occasional hallucination on ambiguous OCR fragments [dataloop](https://dataloop.ai/library/model/qwen_qwen25-05b/)
- **Expected CPU speed**: ~50–80 tokens/sec — extremely fast
- Good for a first-pass extraction before a validation step [dataloop](https://dataloop.ai/library/model/qwen_qwen25-05b/)

```bash
ollama pull qwen2.5:0.5b
```

***

## Inference Framework: llama-cpp-python Wins for CPU

For pure CPU deployment, **llama-cpp-python is the best choice** over Ollama, ctransformers, or ONNX:

| Framework | CPU Speed | Control | Setup Complexity | Best For |
|---|---|---|---|---|
| **llama-cpp-python** | ~52 tok/s | Full | Medium | Production, scripting |
| **Ollama** | ~30 tok/s | Limited | Easy | Prototyping |
| **ctransformers** | ~20 tok/s | Medium | Easy | Legacy, deprecated |
| **ONNX Runtime** | Varies | Medium | Hard | Edge/mobile |

Benchmarks show llama.cpp generates ~52 tokens/sec vs Ollama's ~30 on identical hardware — roughly a **70% speed advantage**. This is because llama.cpp is pure C++ with fine-grained thread and memory control. Ollama is built on top of llama.cpp but adds an API layer with overhead and suboptimal GPU/CPU tensor allocation. For your use case (scripted Python pipeline with PaddleOCR output), llama-cpp-python gives you that speed with a clean Python API. [reddit](https://www.reddit.com/r/LocalLLaMA/comments/1q64f26/llamacpp_vs_ollama_70_higher_code_generation/)

***

## GGUF Quantization Level

Research on small models (<8B) reveals a critical **"quantization cliff"**: [arxiv](https://arxiv.org/html/2510.21970v1)

- **Q3_K_M**: Catastrophic accuracy collapse — accuracy drops from 0.99 to 0.60 in extraction tasks. **Avoid for structured output** [arxiv](https://arxiv.org/html/2510.21970v1)
- **Q4_K_M**: Peak inference speed (~48 tok/s), accuracy ~0.89. Good default for fast/low-RAM setups [arxiv](https://arxiv.org/html/2510.21970v1)
- **Q5_K_M**: Best balance — ~42 tok/s with accuracy ~0.99. **Recommended for your use case** [kaitchup.substack](https://kaitchup.substack.com/p/choosing-a-gguf-model-k-quants-i)
- **Q6_K**: Near-lossless quality, ~20% larger than Q5_K_M, marginal gain [kaitchup.substack](https://kaitchup.substack.com/p/choosing-a-gguf-model-k-quants-i)

**Use Q5_K_M for Qwen2.5-1.5B** on CNIE extraction. The JSON field accuracy improvement over Q4_K_M is significant for small models, and the speed difference (42 vs 48 tok/s) is negligible at your scale. [arxiv](https://arxiv.org/html/2510.21970v1)

***

## Fine-tuned Models for Arabic NER / Document Extraction

For a lightweight **non-generative** pipeline, consider these specialized models as an alternative or pre-processing step:

- **[NAMAA-Space/gliner_arabic-v2.1](https://huggingface.co/NAMAA-Space/gliner_arabic-v2.1)** — Arabic-specific NER built on GLiNER architecture, ideal for extracting entities (names, dates, CIN numbers) from Arabic text. Much faster than any LLM for pure NER, runs on CPU. [huggingface](https://huggingface.co/NAMAA-Space/gliner_arabic-v2.1)
- **[prakash-aryan/qwen-arabic-project](https://github.com/prakash-aryan/qwen-arabic-project)** — Qwen2-1.5B fine-tuned on Arabic with QLoRA (final loss 0.1083), strong on Arabic text classification and QA [github](https://github.com/prakash-aryan/qwen-arabic-project)
- **[Arabic-Nougat](https://arxiv.org/abs/2411.17835)** — OCR-to-structured-Markdown for Arabic documents, could serve as a pre-processor before your LLM step [arxiv](https://arxiv.org/abs/2411.17835)

***

## Recommended Pipeline for CNIE

A two-stage approach will give the best speed/accuracy tradeoff:

1. **PaddleOCR** → raw text fragments (Arabic + French mixed)
2. **Qwen2.5-1.5B-Instruct Q5_K_M** via llama-cpp-python with `response_format={"type": "json_object"}` and a well-structured system prompt listing all fields and example OCR patterns
3. Optional: **JSON schema validation** with Pydantic to catch hallucinations and retry with Qwen2.5-3B on failure

This keeps you well under 5 seconds per card on a modern 8-core CPU, with native Arabic/French handling and reliable JSON output. [qwenlm.github](https://qwenlm.github.io/blog/qwen2.5/)
# LLM Inference Fundamentals — Quick Reference

## What is a model file?

A model file (e.g. 5GB GGUF) is a frozen set of **billions of numbers (weights)**. These numbers were calculated during training (weeks of GPU time by the model creators). Once training is done, the weights **never change**. The model doesn't learn, doesn't grow, doesn't store data.

## What happens during inference (when you ask it a question)?

1. Model weights are loaded into RAM (once, at startup)
2. Your input text arrives
3. Text flows through the weights — billions of multiply-add operations
4. Output comes out (in our case: structured JSON)
5. Weights stay unchanged. RAM stays the same.

The model is like a calculator — input in, math through fixed numbers, answer out.

## Why does the model use exactly X GB of RAM?

The RAM usage = model file size + small KV cache (conversation memory).

- **Model weights**: fixed, never grows (e.g. 5GB stays 5GB forever)
- **KV cache**: grows with conversation length, capped by context window (n_ctx). For short tasks like ours (OCR text in → JSON out), it's ~50-200MB

There's nothing to grow. No learning, no accumulation. Same RAM from start to finish.

## Model size vs capability

| Parameter count | File size (Q5) | RAM needed | Speed on CPU | Intelligence |
|---|---|---|---|---|
| 1.5B parameters | ~1.2 GB | ~1.5 GB | ~5s | Basic tasks |
| 3B parameters | ~2.5 GB | ~3 GB | ~12s | Good for structured extraction |
| 4B parameters | ~3 GB | ~3.5 GB | ~15s | Good balance |
| 7B parameters | ~5 GB | ~5.5 GB | ~30s | Strong |
| 8B parameters | ~5.5 GB | ~6 GB | ~35s | Strongest at this tier |

More parameters = more weights = smarter model = but more math = slower.

## Why GPU is 10x faster (same model, same RAM)

It's not about memory — it's about **parallel math**.

- **CPU**: 4-16 cores, each very smart. Does 8-16 multiplications simultaneously.
- **GPU**: 4,000+ cores, each simple. Does 4,000+ multiplications simultaneously.

LLM inference = billions of independent multiply-add operations. Each GPU core handles one. More cores = more parallel math = faster.

```
CPU (8 cores):     7 billion multiplications → ~30 seconds
GPU (4000 cores):  7 billion multiplications → ~3 seconds
```

The GPU cores are individually dumber than CPU cores, but there are hundreds of times more of them, and LLM math is perfectly parallelizable.

## Quantization — making models smaller

The original model stores each weight as a 16-bit number (FP16). **Quantization** compresses weights to fewer bits:

| Quantization | Bits per weight | Size reduction | Accuracy |
|---|---|---|---|
| FP16 (original) | 16 bits | Baseline | 100% |
| Q8_K | 8 bits | 50% smaller | ~99.9% |
| Q5_K_M | 5 bits | 69% smaller | ~99% — **best balance** |
| Q4_K_M | 4 bits | 75% smaller | ~98% |
| Q3_K_M | 3 bits | 81% smaller | ~60% — **broken, avoid** |

For small models (<8B), Q5_K_M is the sweet spot. Q3_K_M causes catastrophic accuracy collapse.

## GGUF format

GGUF is the file format for quantized models, designed for llama.cpp. It contains:
- Model weights (quantized)
- Tokenizer (converts text → numbers and back)
- Metadata (model architecture, context size, etc.)

All in one file. Download it, load it, run it.

## Inference engines — what runs the model

| Engine | What it is | Best for |
|---|---|---|
| llama.cpp | C++ library, runs GGUF models | Core engine, fastest on CPU |
| llama-cpp-python | Python wrapper around llama.cpp | Developer testing, notebooks |
| Ollama | User-friendly app built on llama.cpp | Client deployment, one-click install |
| vLLM | Python server, GPU optimized | Server deployment with GPU |

llama-cpp-python and Ollama use the **exact same engine** (llama.cpp). Same speed. Ollama is just easier to install and manage for non-developers.

## Our architecture (CNIE OCR project)

```
Photo → Card Detection → PaddleOCR → Raw text → LLM → Structured JSON
         (OpenCV)        (Arabic model)          (Qwen via Ollama)
```

- **PaddleOCR**: extracts raw text from card image (Arabic + French)
- **LLM (Qwen2.5)**: takes noisy OCR text → outputs clean structured JSON
- **Why LLM?**: handles OCR errors, cross-references Arabic/French, identifies fields

## Key decisions and why

| Decision | Choice | Why |
|---|---|---|
| OCR engine | PaddleOCR v3.4 (PP-OCRv5) | Best Arabic support, free, local |
| Single vs dual OCR | Single Arabic model | Arabic model reads French at 0.99, dual adds garbage |
| Detection thresholds | text_det_box_thresh=0.4 | Default 0.6 was dropping French names |
| LLM model | Qwen2.5 1.5B-3B | Best Arabic at small size, fits any laptop |
| Quantization | Q5_K_M | Best accuracy/size balance for small models |
| Inference engine | Ollama (client) | One-click install, same speed as raw llama.cpp |
| Image preprocessing | No sharpening/CLAHE | Tested it — hurt Arabic recognition, not helped |
| JPEG temp files | Removed | JPEG compression degrades Arabic dots (ر vs ن) |

## Vocabulary cheat sheet

| Term | Plain English |
|---|---|
| **Parameters** | The numbers (weights) in the model. 3B = 3 billion numbers |
| **Inference** | Running the model to get an answer (not training) |
| **Quantization** | Compressing weights to use less RAM, slight accuracy tradeoff |
| **GGUF** | File format for quantized models |
| **Context window (n_ctx)** | How much text the model can see at once (measured in tokens) |
| **Tokens** | Chunks of text (~4 characters per token in English, ~1-2 chars in Arabic) |
| **KV cache** | Memory used to track the current conversation |
| **tok/s** | Tokens per second — how fast the model generates output |
| **System prompt** | Instructions given to the model before your question |
| **Temperature** | Randomness control. 0 = deterministic, 1 = creative. We use 0.1 |
| **Fine-tuning** | Retraining a model on your specific data to improve accuracy |

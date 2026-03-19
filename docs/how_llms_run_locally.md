# How LLMs Run on Your Machine

## The Problem

An LLM is a giant math file (billions of numbers = "weights").
Your computer needs software to READ that file and DO the math.

The file format and the software must match. That's it.


## The 3 Layers

```
 YOU (Python code)
  |
  v
 RUNTIME (the engine that runs the model)
  |
  v
 MODEL FILE (the weights on disk)
```

Each layer has options. They must be compatible.


## Layer 1: Model File Formats

The weights must be saved in some format. Think of it like video:
MP4, AVI, MKV — same movie, different container.

```
 Format        Who uses it         Size for 7B model
 ---------     ----------------    -----------------
 .safetensors  Transformers        ~14 GB (full precision)
 .gguf         llama.cpp / Ollama  ~4 GB  (quantized/compressed)
 .bin          PyTorch (old)       ~14 GB
```

GGUF is small because it's QUANTIZED — the numbers are rounded
to use less memory. Like JPEG vs RAW photo: smaller, almost same quality.


## Layer 2: Runtimes (the engine)

The runtime loads the model file and does the actual computation.

```
 Runtime          Reads format    Needs GPU?    How to use
 --------         ------------    ----------    ----------
 Transformers     .safetensors    Best with     Python library
                                  GPU           (import transformers)

 llama.cpp        .gguf           No            C++ program
                                  (CPU works)   (runs in terminal)

 llama-cpp-python .gguf           No            Python wrapper around
                                  (CPU works)   llama.cpp (import llama_cpp)

 Ollama           .gguf (auto)    No            Standalone app
                                  (CPU works)   (ollama run model-name)

 vLLM             .safetensors    YES           Python server
                                  (GPU only)    (fast, production use)
```

### When to use what:

```
 "I have a good GPU"          --> Transformers or vLLM
 "I only have CPU"            --> llama-cpp-python or Ollama
 "I want the easiest setup"   --> Ollama
 "I want control in Python"   --> llama-cpp-python or Transformers
```


## Layer 3: Your Code

Your Python code talks to the runtime:

```python
# Option A: llama-cpp-python (what we use now)
from llama_cpp import Llama
llm = Llama(model_path="model.gguf")
response = llm.create_chat_completion(messages=[...])

# Option B: Transformers
from transformers import AutoModelForCausalLM
model = AutoModelForCausalLM.from_pretrained("org/model-name")

# Option C: Ollama (call via HTTP)
import requests
requests.post("http://localhost:11434/api/chat", json={...})
```

All three do the same thing: send text in, get text out.


## Why So Many GGUF Repos on HuggingFace?

One model, many quantizations:

```
 Original model:  meta-llama/Llama-3.1-8B-Instruct  (.safetensors, ~16GB)
                          |
          People quantize it to GGUF:
                          |
          bartowski/Meta-Llama-3.1-8B-Instruct-GGUF
                Contains many files:
                  Q2_K   (~3 GB, lowest quality)
                  Q4_K_M (~5 GB, good balance)    <-- we usually pick this
                  Q6_K   (~7 GB, better quality)
                  Q8_0   (~9 GB, near original)
```

bartowski, TheBloke, unsloth = people who convert models to GGUF.
They don't make the models. They just repackage them.


## How It All Connects In Our Project

```
 PaddleOCR              GPT-OSS-20B
 (reads the image)      (understands the text)
      |                       |
      v                       v
 Image --> OCR text --> llama-cpp-python --> JSON fields
                             |
                        reads .gguf file
                        (~12 GB on disk)
                        runs on CPU
```


## What About GLM-OCR?

GLM-OCR is different: it's a VISION model.
It takes the IMAGE directly — no separate OCR step needed.

```
 Current pipeline:     Image --> PaddleOCR --> text --> LLM --> JSON
 GLM-OCR pipeline:     Image --> GLM-OCR --> JSON  (one step)
```

But GLM-OCR has no GGUF yet, so llama-cpp-python can't run it.
Options to run it:

```
 Ollama:         easiest, install Ollama, run "ollama run glm-ocr"
 Transformers:   needs GPU, more control, pip install transformers
```


## Summary Table

```
 What               Format         Runtime              GPU?
 ----               ------         -------              ----
 GPT-OSS-20B        .gguf          llama-cpp-python     No (slow on CPU)
 Mistral-Nemo       .gguf          llama-cpp-python     No
 Phi-4-mini         .gguf          llama-cpp-python     No
 GLM-OCR            .safetensors   Transformers/Ollama  Recommended
```

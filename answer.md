Here's the full breakdown. The short answer is: **llama-cpp-python's `Llama` class does NOT reliably support GLM-OCR vision yet** — the recommended path is `llama-server` with its HTTP API or Ollama. Here's every detail:

***

## 1. Does llama-cpp-python Support Vision?

Yes, but with caveats. llama-cpp-python supports vision models through a `chat_handler` + `mmproj` (multimodal projector) file pattern — the same architecture llama.cpp uses internally. Full vision support via the new `libmtmd` library was merged into llama.cpp in **May 2025**, but llama-cpp-python's Python bindings lag behind and don't always expose the latest llama.cpp multimodal changes immediately. [github](https://github.com/abetlen/llama-cpp-python)

For **GLM-OCR specifically**, the glm4v projector type caused a known error (`unknown projector type: glm4v`) even in the latest llama.cpp Docker images as of late 2025. The model uses the `glm4` architecture [ggml-org model card], and while there's a merged PR (`#19677`) adding GLM-OCR support to llama.cpp, community reports say **it works with `llama-cli` but not reliably with `llama-server`**. [reddit](https://www.reddit.com/r/LocalLLaMA/comments/1r8d4iq/model_support_glmocr_by_ngxson_pull_request_19677/)

***

## 2. Standard llama-cpp-python Vision Pattern

For models that ARE supported (LLaVA, Gemma3, Phi-3.5-Vision), the pattern is:

```python
from llama_cpp import Llama
from llama_cpp.llama_chat_format import Llava15ChatHandler

chat_handler = Llava15ChatHandler(clip_model_path="mmproj-model-f16.gguf")
llm = Llama(
    model_path="model-Q4_K_M.gguf",
    chat_handler=chat_handler,
    n_ctx=4096,
    n_gpu_layers=0  # CPU only
)

import base64
with open("image.jpg", "rb") as f:
    b64_image = base64.b64encode(f.read()).decode()

response = llm.create_chat_completion(messages=[{
    "role": "user",
    "content": [
        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_image}"}},
        {"type": "text", "text": "Extract all text from this image."}
    ]
}])
print(response["choices"][0]["message"]["content"])
```

The key requirement is always **two files**: the main `.gguf` (language model) + the `mmproj-*.gguf` (vision projector). [huggingface](https://huggingface.co/mradermacher/NuMarkdown-8B-Thinking-GGUF/discussions/1)

***

## 3. GLM-OCR Specific Chat Handler

There is **no dedicated `GLM4VChatHandler`** in llama-cpp-python's current release. The GLM-4V architecture requires its own projector handling, and the `unknown projector type: glm4v` error blocks it on standard builds. You cannot substitute `Llava15ChatHandler` or `Llava16ChatHandler` — those are hardcoded to CLIP-based projectors, not GLM's custom vision encoder. [huggingface](https://huggingface.co/ggml-org/GLM-4.6V-GGUF/discussions/1)

***

## 4. Recommended Alternative: llama-server HTTP API (✅ Working)

Based on community testing, `llama-server` (the binary, not the Python bindings) **does work** with GLM-OCR via the CLI image loader. The most reliable CPU-only workflow is: [reddit](https://www.reddit.com/r/LocalLLaMA/comments/1r8d4iq/model_support_glmocr_by_ngxson_pull_request_19677/)

**Step 1 — Start the server:**
```bash
llama-server -hf ggml-org/GLM-OCR-GGUF --no-mmproj-offload -c 4096
```

**Step 2 — Send image via Python (minimal working example for ID card OCR):**
```python
import requests, base64, json

with open("id_card.jpg", "rb") as f:
    b64 = base64.b64encode(f.read()).decode()

payload = {
    "model": "glm-ocr",
    "messages": [{
        "role": "user",
        "content": [
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
            {"type": "text", "text": (
                "Extract all text from this ID card. "
                "Return a JSON object with fields: name, dob, id_number, address."
            )}
        ]
    }],
    "temperature": 0.1,
    "max_tokens": 512
}

res = requests.post("http://127.0.0.1:8080/v1/chat/completions",
                    json=payload,
                    headers={"Content-Type": "application/json"})
print(json.dumps(res.json()["choices"][0]["message"]["content"], indent=2))
```

***

## 5. Simplest Alternative: Ollama API (✅ Easiest)

If you prefer zero binary management, Ollama's Python SDK makes it one-liner simple: [ollama](https://ollama.com/library/glm-ocr)

```python
import ollama, base64

with open("id_card.jpg", "rb") as f:
    b64 = base64.b64encode(f.read()).decode()

response = ollama.chat(
    model="glm-ocr",
    messages=[{
        "role": "user",
        "content": "Extract all text and return as JSON with name, dob, id_number, address.",
        "images": [b64]  # Ollama accepts raw base64
    }]
)
print(response["message"]["content"])
```

Install with `pip install ollama` and pull with `ollama pull glm-ocr` first.

***

## Decision Guide

| Method | Works with GLM-OCR | CPU-only | Complexity |
|---|---|---|---|
| `llama-cpp-python` Llama class | ⚠️ Unreliable (no GLM4V handler) | ✅ | Medium |
| `llama-server` + HTTP API | ✅ Confirmed via CLI | ✅ | Low |
| `ollama` Python SDK | ✅ Confirmed | ✅ | **Lowest** |
| `llama-cli` interactive | ✅ Works | ✅ | Manual only |

For a CPU-only production pipeline, go with **Ollama** if you want simplicity, or **llama-server + requests** if you need more control over quantization and context window. Skip the `llama-cpp-python` `Llama` class for GLM-OCR until a dedicated `GLM4VChatHandler` is added to the Python bindings. [huggingface](https://huggingface.co/ggml-org/GLM-4.6V-GGUF/discussions/1)
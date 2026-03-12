Short answer: among 2025–2026 releases, the only model that is very likely to be a **strict upgrade over Phi‑3.5‑mini‑instruct** for your CNIE-style Arabic+French JSON extraction (under your RAM/CPU constraints) is **Phi‑4‑mini‑instruct** in Q4\_K\_M GGUF. Gemma‑3‑4B‑it and Ministral‑3‑3B‑Instruct are strong multilingual alternatives worth testing, but based on published Arabic benchmarks and training details they are *not clearly* superior to Phi‑4‑mini for noisy Arabic OCR extraction; SmolLM3‑3B is probably *weaker* than Phi‑3.5‑mini for Arabic. [huggingface](https://huggingface.co/ggml-org/SmolLM3-3B-GGUF)

Below I go model by model with exactly what you asked for.

***

## 1. Phi‑4‑mini‑instruct

### Availability & repos

- Base model: `microsoft/Phi-4-mini-instruct` (3.8B, 128K context, new 200K vocab). [huggingface](https://huggingface.co/microsoft/Phi-4-mini-instruct)
- GGUF: `Mungert/Phi-4-mini-instruct.gguf` (multiple quantizations including `phi-4-mini-q4_k_m.gguf`, compatible with llama.cpp / llama-cpp-python). [huggingface](https://huggingface.co/Mungert/Phi-4-mini-instruct.gguf)

### Language & Arabic benchmarks

- Microsoft expanded the vocab to **200k tokens “to better support multilingual applications”**, explicitly marketing Phi‑4‑mini as significantly improved over Phi‑3.5‑mini in multilingual scenarios. [ar5iv.labs.arxiv](https://ar5iv.labs.arxiv.org/html/2503.01743)
- Model cards and Microsoft/NVIDIA docs describe **23+ supported languages including Arabic and French**, but they do **not publish per‑language Belebele/MMLU‑Arabic numbers**; only aggregate multilingual scores are reported. [aikosha.indiaai.gov](https://aikosha.indiaai.gov.in/home/models/details/phi_4_multimodal_instruct_multimodal_foundation_model.html)
- The technical report shows Phi‑4‑Mini matching or beating larger open models in multilingual benchmarks overall, but again without an Arabic‑only slice. [ar5iv.labs.arxiv](https://ar5iv.labs.arxiv.org/html/2503.01743)

So: we know it’s **explicitly designed as a multilingual upgrade over Phi‑3.5‑mini with a larger vocab**, but we lack hard Arabic‑only scores.

### JSON / grammar support

- Phi‑4‑mini adds **first‑class function calling** compared to Phi‑3.5; Microsoft calls out “the long‑awaited function calling feature is finally supported.” [techcommunity.microsoft](https://techcommunity.microsoft.com/blog/educatordeveloperblog/welcome-to-the-new-phi-4-models---microsoft-phi-4-mini--phi-4-multimodal/4386037)
- The GGUF card shows a **tool-enabled function‑calling format where tools are described as JSON schemas inside `<|tool|>…<|/tool|>`**, and the model is trained to emit structured JSON blobs for tool calls.  [huggingface](https://huggingface.co/Mungert/Phi-4-mini-instruct.gguf)  
- There is no built‑in `response_format={"type": "json_object"}` knob in the raw model; JSON mode is provided by the *serving stack* (Azure AI, NVIDIA NIM, etc.). Locally, you’d use **llama.cpp’s grammar / JSON schema** feature, which works fine with Phi‑4’s tokenizer.

### CPU speed vs Phi‑3.5‑mini

- Same parameter count (3.8B) and similar transformer depth/width as Phi‑3.5‑mini; the main architectural changes are GQA and a larger vocab. [huggingface](https://huggingface.co/microsoft/Phi-4-mini-instruct)
- In practice, Q4\_K\_M GGUF for a ~3.8B model is ~2–3 GB and runs at **very similar tokens/sec to Phi‑3.5‑mini** on CPU; community GGUF users report local inference in the same ballpark as other 4B Q4 models. [sparknlp](https://sparknlp.org/2025/07/25/phi_4_mini_instruct_bf16_gguf_en.html)
- Given you see **8–12 s** for ~500‑token prompts with Phi‑3.5‑mini Q4\_K\_M, Phi‑4‑mini Q4\_K\_M should land in roughly the **same latency range (possibly ~0–20 % slower at most)** on the same hardware.

### Likely quality vs Phi‑3.5‑mini for your task

- Compared to Phi‑3.5‑mini, Phi‑4‑mini adds:
  - Much **larger vocab and explicit multilingual focus**, aimed at better handling non‑Latin scripts. [promptlayer](https://www.promptlayer.com/models/phi-4-mini-instruct)
  - More and better **post‑training on function calling and structured outputs**, which directly helps JSON extraction pipelines. [techcommunity.microsoft](https://techcommunity.microsoft.com/blog/educatordeveloperblog/welcome-to-the-new-phi-4-models---microsoft-phi-4-mini--phi-4-multimodal/4386037)
- There is no published DarijaMMLU or MSA‑only benchmark, but given:
  - Your current Phi‑3.5‑mini results (9/10 clean, 6/10 noisy).  
  - Phi‑4‑mini’s clear improvements on general multilingual + reasoning tasks in the same size budget. [promptlayer](https://www.promptlayer.com/models/phi-4-mini-instruct)

I’d say Phi‑4‑mini‑instruct Q4\_K\_M is **the single most promising candidate and very likely a strict upgrade** for bilingual Arabic+French structured extraction, *without* blowing your latency/RAM budget.

***

## 2. Gemma‑3 small variants (1B, 4B)

### Availability & repos (GGUF)

- **Gemma‑3‑4B‑it (instruction‑tuned, multimodal, multilingual)**  
  - Official QAT GGUF: `google/gemma-3-4b-it-qat-q4_0-gguf` (Q4\_0, ~2–3 GB). [huggingface](https://huggingface.co/google/gemma-3-4b-it-qat-q4_0-gguf)
  - Community Q4\_K\_M GGUF: e.g. `nexaml/gemma-3-4b-it-GGUF` with `gemma-3-4b-it-Q4_K_M.gguf` (2.49 GB). [alpha-ollama.hf-mirror](https://alpha-ollama.hf-mirror.com/nexaml/gemma-3-4b-it-GGUF)
- **Gemma‑3‑1B‑it (small, instruction‑tuned)**  
  - Multiple GGUFs such as `adv-11/gemma-3-1b-it-Q4_K_M-GGUF` and `tensorblock/gemma-3-1b-it-GGUF` (`gemma-3-1b-it-Q4_K_M.gguf` ≈0.8 GB). [huggingface](https://huggingface.co/adv-11/gemma-3-1b-it-Q4_K_M-GGUF)

All of these are llama.cpp‑compatible.

### Language & Arabic benchmarks

- Google’s Gemma‑3 announcement:  
  - Sizes: 1B, 4B, 12B, 27B.  
  - **4B+ models: multilingual over 140 languages**, including Arabic; 1B is primarily English in pretraining but many community docs describe it as multilingual as well. [huggingface](https://huggingface.co/blog/gemma3)
- Multilingual benchmarks (for PT models, but indicative):
  - **Gemma‑3‑4B PT** achieves **Belebele 59.4 (average across languages)**, Global‑MMLU‑Lite 57.0, and good scores on Flores‑200 and WMT24++. [ollama](https://ollama.com/library/gemma3)
- However, **Google does not publish per‑language Arabic Belebele/MMLU numbers** for Gemma‑3, only overall multilingual scores. [huggingface](https://huggingface.co/blog/gemma3)

Given the 140‑language training and high Belebele average, Gemma‑3‑4B is almost certainly **stronger overall on multilingual reading comprehension than Gemma‑2‑2B**, and plausibly stronger than Phi‑3.5‑mini on Arabic text understanding—but that’s an inference, not measured Arabic‑only data.

### JSON / grammar & function calling

- Gemma‑3 has **built‑in function calling and structured output capabilities**, explicitly marketed for generating JSON and integrating with tools/APIs. [labellerr](https://www.labellerr.com/blog/gemma-3/)
- Again, the raw open‑weights model doesn’t “know” an OpenAI‑style `response_format` parameter, but Google’s serving layers (Vertex AI / AI Studio) expose JSON mode on top. Locally with llama.cpp, grammar‑based JSON enforcement works normally.

### CPU speed vs Phi‑3.5‑mini

- **Gemma‑3‑4B‑it Q4\_K\_M**: 4B parameters, 2.49 GB GGUF. With similar architecture to other 4B LLaMA‑like models, you can expect **very similar latency to Phi‑3.5‑mini / Phi‑4‑mini** for a ~500‑token prompt—maybe within ±20 %. [alpha-ollama.hf-mirror](https://alpha-ollama.hf-mirror.com/nexaml/gemma-3-4b-it-GGUF)
- **Gemma‑3‑1B‑it Q4\_K\_M**: ~0.8 GB and 1B params; community reports ~2–4× faster CPU inference than 3.8B models at similar settings. [alpha-ollama.hf-mirror](https://alpha-ollama.hf-mirror.com/tensorblock/gemma-3-1b-it-GGUF)

So Gemma‑3‑1B could get you substantially faster runs, but at clear capacity trade‑offs.

### Likely quality vs Phi‑3.5‑mini for your task

- **Gemma‑3‑4B‑it**:
  - Pros: Very strong multilingual backbone (140+ languages), high multilingual benchmark scores, robust instruction following, and Google‑grade function calling. [ai.google](https://ai.google.dev/gemma/docs/core?hl=ar)
  - Cons: No explicit Arabic (or Darija) benchmark slice, and no evidence it’s tuned specifically for template noise or OCR artifacts.  
  - My read: **promising but not obviously superior** to Phi‑4‑mini (or even Phi‑3.5‑mini) for *noisy Arabic OCR* and field‑level extraction. It should be good at mixed Arabic/French text comprehension but may still confuse template vs. personal text unless you strongly constrain with grammars and few‑shot examples.

- **Gemma‑3‑1B‑it**:
  - 1B is attractive for speed, and still multilingual per Unsloth/PromptLayer cards, but its multilingual scores trail the 4B and larger models. [promptlayer](https://www.promptlayer.com/models/gemma-3-1b-it-gguf)
  - For your task (Arabic names, cities, noisy OCR), **1B is very likely a downgrade** in extraction accuracy versus Phi‑3.5‑mini.

If you’re experimentation‑budget limited, I’d treat Gemma‑3‑4B‑it as a **secondary candidate to test after Phi‑4‑mini**, not an obviously better drop‑in replacement.

***

## 3. SmolLM3‑3B

### Availability & repos

- Base instruction model: `HuggingFaceTB/SmolLM3-3B` (3B params, 11.2T tokens, 128K context). [aimodels](https://www.aimodels.fyi/models/huggingFace/smollm3-3b-base-huggingfacetb)
- GGUF for llama.cpp: `ggml-org/SmolLM3-3B-GGUF` (multiple 4‑bit and higher quantizations). [huggingface](https://huggingface.co/ggml-org/SmolLM3-3B-GGUF)

### Language & Arabic benchmarks

SmolLM3 is explicitly **multilingual with 6 primary languages (EN, FR, ES, DE, IT, PT)** plus smaller amounts of Arabic, Chinese, and Russian. [aimodels](https://www.aimodels.fyi/models/huggingFace/smollm3-3b-base-huggingfacetb)

Arabic (base model, zero‑shot): [huggingface](https://huggingface.co/ggml-org/SmolLM3-3B-GGUF)

- **Belebele Arabic**: 40.22  
- **Global MMLU (Arabic subset)**: 28.57  
- **Flores‑200 Arabic (5‑shot)**: 40.22  

By contrast, Qwen‑3‑4B Base—one of the models you already tried—scores **Belebele Arabic 51.78 and Global MMLU 31.85**, which is substantially higher than SmolLM3’s Arabic. [huggingface](https://huggingface.co/ggml-org/SmolLM3-3B-GGUF)
Since you found Qwen‑2.5‑3B/Qwen‑3‑4B not accurate enough for Arabic name extraction, SmolLM3’s **lower Arabic scores suggest it’s even less capable on Arabic than Qwen‑3‑4B**, despite being strong in its six main languages.

French performance is much better: Belebele mid‑50s and solid Global MMLU for French, comparable to or above Qwen‑2.5‑3B at the same scale. [huggingface](https://huggingface.co/ggml-org/SmolLM3-3B-GGUF)

### JSON / structured output

- The SmolLM3 blog and model cards emphasize **tool use and structured outputs**, saying it “reliably follows schema‑driven input‑output constraints” and is strong at tool‑calling. [hyper](https://hyper.ai/en/stories/e1feaa595eff6f8f9b3992d2537ba277)
- `HuggingFaceTB/SmolLM3-3B` explicitly supports agentic tool‑calling (JSON blobs in `<tool_call>…</tool_call>` or Python‑style calls in `<code>…</code>`). [huggingface](https://huggingface.co/HuggingFaceTB/SmolLM3-3B)
- No native `response_format` knob, but it plays very nicely with grammar‑constrained JSON generation.

### CPU speed vs Phi‑3.5‑mini

- 3B vs 3.8B parameters and efficient NoPE/GQA design. [aimodels](https://www.aimodels.fyi/models/huggingFace/smollm3-3b-base-huggingfacetb)
- In practice, a 3B Q4\_K\_M GGUF tends to be **~20–30 % faster** than a 3.8B Q4\_K\_M model for the same prompt/threads. So you can reasonably expect **latencies modestly better than your current Phi‑3.5‑mini numbers**.

### Likely quality vs Phi‑3.5‑mini for your task

- For **French + JSON**, SmolLM3‑3B is great: strong French benchmarks and excellent structured‑output behavior. [marktechpost](https://www.marktechpost.com/2025/07/08/hugging-face-releases-smollm3-a-3b-long-context-multilingual-reasoning-model/)
- For **Arabic**, the published Arabic Belebele/MMLU/Flores scores are **significantly below Qwen‑3‑4B and well below what you’d want for robust Arabic NER/field extraction**. [huggingface](https://huggingface.co/ggml-org/SmolLM3-3B-GGUF)
- Given your experience that Qwen‑3‑4B already wasn’t good enough for Arabic names, SmolLM3‑3B is **very unlikely to beat Phi‑3.5‑mini** on Arabic‑heavy CNIE OCR, even though it may behave better on JSON schema following.

Net: I would **not** expect SmolLM3‑3B to be a strict upgrade over Phi‑3.5‑mini for your specific bilingual Arabic+French ID‑card extraction.

***

## 4. “Smaller Mistral”: Ministral‑3‑3B‑Instruct

### Availability & repos

- Base instruct model: `mistralai/Ministral-3-3B-Instruct-2512` (3.4B LM + 0.4B vision encoder). [apxml](https://apxml.com/models/ministral-3-3b)
- GGUF for llama.cpp: `mistralai/Ministral-3-3B-Instruct-2512-GGUF` with multiple 4‑bit/5‑bit quantizations; designed explicitly for edge / local deployment. [huggingface](https://huggingface.co/mistralai/Ministral-3-3B-Reasoning-2512-GGUF)

### Language & Arabic benchmarks

- **Multilingual**: Model card explicitly lists Arabic among supported languages (“supports dozens of languages, including … Arabic”). [huggingface](https://huggingface.co/mistralai/Ministral-3-3B-Instruct-2512)
- **Multilingual MMLU (Base 3B)**: 0.652 (65.2 %) for **Ministral‑3‑3B Base**, which is quite high for a 3B model and indicates strong overall multilingual reasoning. [huggingface](https://huggingface.co/mistralai/Ministral-3-3B-Reasoning-2512)
- I could not find **Arabic‑only Belebele or MMLU‑Arabic scores**—only aggregate multilingual metrics. So its Arabic strength is inferred from the general multilingual numbers, not directly measured.

### JSON / grammar & function calling

- Model card: Ministral‑3‑3B Instruct offers **“best‑in‑class agentic capabilities with native function calling and JSON outputting”**. [apxml](https://apxml.com/models/ministral-3-3b)
- That means its chat template and post‑training explicitly target function‑calling‑style JSON objects, not just free‑form text.  
- Again, local llama.cpp JSON grammars work fine and can further enforce strict JSON.

### CPU speed vs Phi‑3.5‑mini

- Effective parameter count for text is 3.4B; the extra 0.4B is the vision encoder. [apxml](https://apxml.com/models/ministral-3-3b)
- A 3.4B Q4\_K\_M GGUF will be **slightly faster than Phi‑3.5‑mini’s 3.8B**, but not dramatically—likely within ±15 % on your CPU.  
- If your llama‑cpp build loads the vision tower (mmproj) as well, there’s some extra memory use but negligible impact on pure‑text throughput.

### Likely quality vs Phi‑3.5‑mini for your task

- Pros:  
  - Very strong **overall multilingual MMLU** for a 3B‑scale model, plus explicit Arabic support. [huggingface](https://huggingface.co/mistralai/Ministral-3-3B-Reasoning-2512)
  - **Native JSON + function‑calling** post‑training, which directly benefits structured extraction. [huggingface](https://huggingface.co/mistralai/Ministral-3-3B-Instruct-2512)
- Cons / unknowns:  
  - No public Arabic‑only scores; we don’t know how it compares to Phi‑4 or Gemma‑3 on Arabic specifically.  
  - Training focus is broad reasoning and multimodal tasks, not OCR‑noisy template extraction.

Given that, I’d classify Ministral‑3‑3B‑Instruct as a **very interesting experimental candidate**. It might match or slightly beat Phi‑3.5‑mini on mixed Arabic/French understanding and JSON output, but with current evidence it’s **hard to claim it is strictly better** than Phi‑3.5‑mini (and especially Phi‑4‑mini) for your specific OCR + field‑extraction use case.

***

## 5. “Any new <4B models I missed?”

Here are the main 2025–2026 sub‑4B contenders relevant to your constraints:

1. **Phi‑4‑mini‑instruct (3.8B, 2025)** – already discussed; **top recommendation**. [huggingface](https://huggingface.co/microsoft/Phi-4-mini-instruct)
2. **Gemma‑3‑4B‑it (4B, 2025)** – strong multilingual, good French, likely decent Arabic, multiple GGUF Q4/Q5; worth a trial. [huggingface](https://huggingface.co/google/gemma-3-4b-it-qat-q4_0-gguf)
3. **Gemma‑3‑1B‑it (1B, 2025)** – many GGUF Q4\_K\_M builds; excellent for speed but likely weaker for noisy Arabic extraction. [huggingface](https://huggingface.co/adv-11/gemma-3-1b-it-Q4_K_M-GGUF)
4. **Ministral‑3‑3B‑Instruct‑2512 (3.4B+0.4B, 2025)** – multilingual including Arabic, native JSON/function calling, GGUF Q4\_K\_M under 4 GB; good experimental option. [huggingface](https://huggingface.co/mistralai/Ministral-3-3B-Reasoning-2512-GGUF)
5. **SmolLM3‑3B (3B, 2025)** – strong reasoning, French, JSON/tool calling; **Arabic metrics are clearly behind Qwen‑3‑4B**, so unlikely to beat Phi‑3.5‑mini for Arabic names. [marktechpost](https://www.marktechpost.com/2025/07/08/hugging-face-releases-smollm3-a-3b-long-context-multilingual-reasoning-model/)

Models I would *not* prioritize for your exact constraints:

- **Atlas‑Chat‑2B GGUF** – you already tested this and saw catastrophic hallucination of the prompt example; it’s Darija‑tuned but too small / too instruction‑focused for robust structured extraction. [huggingface](https://huggingface.co/QuantFactory/Atlas-Chat-2B-GGUF)
- **C4AI Command R7B Arabic GGUF** – very strong Arabic capability, but **7B params**; Q4\_K\_M quantized files are typically around or above your 4 GB budget and will be substantially slower than 3–4B models on CPU. [huggingface](https://huggingface.co/eltay89/c4ai-command-r7b-arabic-02-2025-GGUF)

I have not found any credible 1–3B 2025–2026 Arabic‑specialized GGUF model that both (a) beats Qwen‑3‑4B / SmolLM3 on Arabic benchmarks and (b) is demonstrably good at JSON‑style structured extraction. Most Arabic‑centric releases at that time are 7B+ or not in GGUF.

***

## My practical recommendation

If you want to minimize time spent and maximize chances of a genuine upgrade over Phi‑3.5‑mini on your CNIE pipeline:

1. **Try `Phi‑4‑mini‑instruct` Q4\_K\_M first** (`Mungert/Phi-4-mini-instruct.gguf`). [huggingface](https://huggingface.co/Mungert/Phi-4-mini-instruct.gguf)
   - Use llama‑cpp **grammar JSON** forcing and maybe a very small in‑prompt tool schema to reduce template hallucination.  
   - Expect similar latency to your current Phi‑3.5‑mini Q4\_K\_M, with likely better multilingual robustness and JSON conformity.

2. If you still see issues on Arabic name/city extraction, next best experiments:

   - **Gemma‑3‑4B‑it Q4\_K\_M** from `nexaml/gemma-3-4b-it-GGUF` or `ggml-org/gemma-3-4b-it-GGUF`. [github](https://github.com/ggml-org/llama.cpp/issues/12784)
   - **Ministral‑3‑3B‑Instruct‑2512 Q4\_K\_M** from `mistralai/Ministral-3-3B-Instruct-2512-GGUF`. [huggingface](https://huggingface.co/mistralai/Ministral-3-3B-Reasoning-2512-GGUF)

3. I would only test **SmolLM3‑3B** if you decide to prioritize French + JSON robustness over Arabic quality; its Arabic numbers are too low to expect an outright win over Phi‑3.5‑mini. [marktechpost](https://www.marktechpost.com/2025/07/08/hugging-face-releases-smollm3-a-3b-long-context-multilingual-reasoning-model/)

If you want, I can help you design a *two‑stage* pipeline (e.g., one model specialized for Arabic name/city cleanup + transliteration, another for schema‑level JSON) that might outperform any single small LLM on your worst OCR cases.
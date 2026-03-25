Here's everything you need to integrate Baseer into your Flask app for Moroccan ID card OCR.

## HuggingFace Repo ID

As of March 2026, Misraj has not published Baseer as a public model on HuggingFace — the LinkedIn post from the team confirmed "public API access soon" but the weights are not yet public. The HuggingFace collection page exists at [`Misraj/baseer`](https://huggingface.co/collections/Misraj/baseer-68d3c26ed81bde9454503e32) but access is gated. **You have two options:** [huggingface](https://huggingface.co/collections/Misraj/baseer-68d3c26ed81bde9454503e32)

1. **Contact Misraj** at misraj.ai to request model access (they offer an API)
2. **Use the best public alternative**: `sherif1313/Arabic-handwritten-OCR-4bit-Qwen2.5-VL-3B-v3` — same base model (Qwen2.5-VL-3B), already 4-bit quantized, 2.5% CER, 0.57s/image [huggingface](https://huggingface.co/sherif1313/Arabic-handwritten-OCR-4bit-Qwen2.5-VL-3B-v3)

## API Compatibility with Qwen2.5-VL

Yes — Baseer uses the **exact same API** as Qwen2.5-VL since it's just a fine-tune of that base. You use `Qwen2_5_VLForConditionalGeneration` + `AutoProcessor`, not the generic `AutoModelForImageTextToText`. [huggingface](https://huggingface.co/Qwen/Qwen2.5-VL-3B-Instruct)

## Required Dependencies

```bash
pip install transformers torch torchvision accelerate bitsandbytes
pip install qwen-vl-utils   # critical — handles image/video preprocessing
```

`qwen-vl-utils` is the one non-standard dependency that's easy to miss. [huggingface](https://huggingface.co/Qwen/Qwen2.5-VL-3B-Instruct)

## Minimal OCR Code (Flask + Arabic ID Card)

```python
from flask import Flask, request, jsonify
from PIL import Image
import torch, json, io
from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor, BitsAndBytesConfig
from qwen_vl_utils import process_vision_info

app = Flask(__name__)

# ─── Load model once at startup ───────────────────────────────────────────────
MODEL_ID = "sherif1313/Arabic-handwritten-OCR-4bit-Qwen2.5-VL-3B-v3"
# If Misraj releases publicly, swap to: "Misraj/Baseer"

quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
)

model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
    MODEL_ID,
    quantization_config=quant_config,
    device_map="cpu",   # use "auto" if you have a GPU
    torch_dtype=torch.float16,
)
processor = AutoProcessor.from_pretrained(
    MODEL_ID,
    min_pixels=256 * 28 * 28,   # reduce token count for speed on CPU
    max_pixels=1280 * 28 * 28,
)
model.eval()


# ─── OCR helper ───────────────────────────────────────────────────────────────
JSON_SCHEMA_PROMPT = """You are an Arabic OCR assistant. Extract all text from this document image.
Return ONLY a valid JSON object with these fields (use null if not found):
{
  "last_name": "...",
  "first_name": "...",
  "last_name_arabic": "...",
  "first_name_arabic": "...",
  "birth_date": "DD/MM/YYYY",
  "birth_place": "...",
  "id_number": "...",
  "expiry_date": "DD/MM/YYYY",
  "gender": "M or F"
}"""

def run_ocr(pil_image: Image.Image, structured: bool = True) -> dict | str:
    prompt = JSON_SCHEMA_PROMPT if structured else "Extract all text from this image exactly as it appears, preserving Arabic script."
    
    messages = [{
        "role": "user",
        "content": [
            {"type": "image", "image": pil_image},
            {"type": "text", "text": prompt},
        ],
    }]
    
    text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    image_inputs, video_inputs = process_vision_info(messages)
    inputs = processor(
        text=[text],
        images=image_inputs,
        videos=video_inputs,
        padding=True,
        return_tensors="pt",
    ).to(model.device)
    
    with torch.no_grad():
        generated_ids = model.generate(
            **inputs,
            max_new_tokens=512,
            do_sample=False,   # greedy for OCR — more deterministic
            temperature=None,
            top_p=None,
        )
    
    trimmed = [out[len(inp):] for inp, out in zip(inputs.input_ids, generated_ids)]
    output = processor.batch_decode(trimmed, skip_special_tokens=True)[0]
    
    if structured:
        # Strip markdown fences if model wraps output in ```json ... ```
        output = output.strip().removeprefix("```json").removesuffix("```").strip()
        try:
            return json.loads(output)
        except json.JSONDecodeError:
            return {"raw_text": output, "parse_error": "Model did not return valid JSON"}
    return output


# ─── Flask endpoint ────────────────────────────────────────────────────────────
@app.route("/ocr", methods=["POST"])
def ocr_endpoint():
    if "image" not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    
    file = request.files["image"]
    pil_image = Image.open(io.BytesIO(file.read())).convert("RGB")
    
    structured = request.args.get("structured", "true").lower() == "true"
    result = run_ocr(pil_image, structured=structured)
    
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=False, port=5000)
```

**Usage:**
```bash
curl -X POST http://localhost:5000/ocr \
  -F "image=@moroccan_id.jpg"
```

## RAM Requirements

| Mode | VRAM / RAM Usage |
|---|---|
| float16 (no quant) | ~7–8 GB |
| 4-bit BnB quantization | ~2.5–3.5 GB |
| 4-bit on CPU (16GB RAM) | ✅ Fits comfortably |

With 4-bit quantization on CPU, the 3B model uses roughly 2.5–3.5 GB RAM leaving plenty of headroom in your 16GB system. Expect **5–15 seconds per image on CPU** without a GPU — `min_pixels` tuning in the processor reduces this significantly. [huggingface](https://huggingface.co/sherif1313/Arabic-handwritten-OCR-4bit-Qwen2.5-VL-3B-v3)

## JSON Schema Prompting

Yes, Qwen2.5-VL (and Baseer) respond well to JSON schema prompts in the system/user message. The model does **not** enforce structured output natively (no grammar-constrained decoding), so you need the fallback `json.loads` + error handling shown above. For more robust output, add `outlines` or `lm-format-enforcer` to constrain generation to valid JSON — though this adds complexity on CPU. [huggingface](https://huggingface.co/Qwen/Qwen2.5-VL-3B-Instruct)

## Quantized Alternatives While Baseer is Gated

Since Baseer weights aren't public yet, these are the best drop-in replacements using the same code:

- **`sherif1313/Arabic-handwritten-OCR-4bit-Qwen2.5-VL-3B-v3`** — 4-bit, 2.5% CER, 0.57s/image [huggingface](https://huggingface.co/sherif1313/Arabic-handwritten-OCR-4bit-Qwen2.5-VL-3B-v3)
- **`NAMAA-Space/Qari-OCR-0.1-VL-2B-Instruct`** — 2B, lighter, strong printed Arabic (swap `Qwen2_5_VLForConditionalGeneration` → `Qwen2VLForConditionalGeneration`)

Once Misraj releases Baseer publicly, it's a one-line swap of `MODEL_ID` and everything else stays identical.
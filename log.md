Downloading Qwen3.5-4B Q5_K_M...
Thinking model: False
(This may take a few minutes on first run)
/usr/local/lib/python3.12/dist-packages/huggingface_hub/utils/_auth.py:94: UserWarning: 
The secret `HF_TOKEN` does not exist in your Colab secrets.
To authenticate with the Hugging Face Hub, create a token in your settings tab (https://huggingface.co/settings/tokens), set it as secret in your Google Colab and restart your session.
You will be able to reuse this secret in all of your notebooks.
Please note that authentication is recommended but still optional to access public models or datasets.
  warnings.warn(
Qwen3.5-4B-Q5_K_M.gguf: 100%
 3.14G/3.14G [00:12<00:00, 129MB/s]
Downloaded in 13.7s
Path: /root/.cache/huggingface/hub/models--unsloth--Qwen3.5-4B-GGUF/snapshots/e87f176479d0855a907a41277aca2f8ee7a09523/Qwen3.5-4B-Q5_K_M.gguf


Loading Qwen3.5-4B Q5_K_M with 12 threads...
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
/tmp/ipykernel_12160/2636441174.py in <cell line: 0>()
      4 
      5 t0 = time.time()
----> 6 llm = Llama(
      7     model_path=model_path,
      8     n_ctx=2048,

1 frames
/usr/local/lib/python3.12/dist-packages/llama_cpp/_internals.py in __init__(self, path_model, params, verbose)
     56 
     57         if model is None:
---> 58             raise ValueError(f"Failed to load model from file: {path_model}")
     59 
     60         vocab = llama_cpp.llama_model_get_vocab(model)

ValueError: Failed to load model from file: /root/.cache/huggingface/hub/models--unsloth--Qwen3.5-4B-GGUF/snapshots/e87f176479d0855a907a41277aca2f8ee7a09523/Qwen3.5-4B-Q5_K_M.gguf
  GPU found: NVIDIA GeForce RTX 3050 (6.0 GB)
Fetching 2 files: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 2/2 [00:00<?, ?it/s]
Download complete: : 0.00B [00:00, ?B/s]                                                                                                                          | 0/2 [00:00<?, ?it/s] 
Loading weights: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 883/883 [00:19<00:00, 45.38it/s]
Some parameters are on the meta device because they were offloaded to the cpu.
  Device map: {'model.vision_tower': 0, 'model.multi_modal_projector': 0, 'model.language_model.embed_tokens': 0, 'lm_head': 0, 'model.language_model.layers.0': 0, 'model.language_model.layers.1': 0, 'model.language_model.layers.2': 0, 'model.language_model.layers.3': 0, 'model.language_model.layers.4': 0, 'model.language_model.layers.5': 0, 'model.language_model.layers.6': 0, 'model.language_model.layers.7': 0, 'model.language_model.layers.8': 0, 'model.language_model.layers.9': 0, 'model.language_model.layers.10': 0, 'model.language_model.layers.11': 0, 'model.language_model.layers.12': 0, 'model.language_model.layers.13': 'cpu', 'model.language_model.layers.14': 'cpu', 'model.language_model.layers.15': 'cpu', 'model.language_model.layers.16': 'cpu', 'model.language_model.layers.17': 'cpu', 'model.language_model.layers.18': 'cpu', 'model.language_model.layers.19': 'cpu', 'model.language_model.layers.20': 'cpu', 'model.language_model.layers.21': 'cpu', 'model.language_model.layers.22': 'cpu', 'model.language_model.layers.23': 'cpu', 'model.language_model.layers.24': 'cpu', 'model.language_model.layers.25': 'cpu', 'model.language_model.layers.26': 'cpu', 'model.language_model.layers.27': 'cpu', 'model.language_model.layers.28': 'cpu', 'model.language_model.layers.29': 'cpu', 'model.language_model.layers.30': 'cpu', 'model.language_model.layers.31': 'cpu', 'model.language_model.layers.32': 'cpu', 'model.language_model.layers.33': 'cpu', 'model.language_model.norm': 'cpu', 'model.language_model.rotary_emb': 'cpu'}
The image processor of type `Gemma3ImageProcessor` is now loaded as a fast processor by default, even if the model checkpoint was saved with a slow processor. This is a breaking change and may produce slightly different outputs. To continue using the slow processor, instantiate this class with `use_fast=False`.
Gemma 3 4B ready on GPU+CPU split (32.4s)
==================================================
Gemma 3 4B — CNIE Extraction Test
http://localhost:5003
==================================================
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5003
 * Running on http://192.168.1.51:5003
Press CTRL+C to quit
127.0.0.1 - - [25/Mar/2026 16:50:40] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [25/Mar/2026 16:50:41] "GET /favicon.ico HTTP/1.1" 404 -

>> Image: 856x540
  Processing inputs...
  Input: 421 tokens (0.7s)
  Generating...
The following generation flags are not valid and may be ignored: ['top_p', 'top_k']. Set `TRANSFORMERS_VERBOSITY=info` for more details.
[2026-03-25 16:50:52,348] ERROR in app: Exception on /extract [POST]
Traceback (most recent call last):
  File "E:\-ocr-passport-and-cin-2\venv\Lib\site-packages\flask\app.py", line 1511, in wsgi_app
    response = self.full_dispatch_request()
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "E:\-ocr-passport-and-cin-2\venv\Lib\site-packages\flask\app.py", line 919, in full_dispatch_request
    rv = self.handle_user_exception(e)
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "E:\-ocr-passport-and-cin-2\venv\Lib\site-packages\flask\app.py", line 917, in full_dispatch_request
    rv = self.dispatch_request()
         ^^^^^^^^^^^^^^^^^^^^^^^
  File "E:\-ocr-passport-and-cin-2\venv\Lib\site-packages\flask\app.py", line 902, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "E:\-ocr-passport-and-cin-2\gemma-ocr-test\app.py", line 106, in extract
    outputs = model.generate(**inputs, max_new_tokens=300, do_sample=False)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "E:\-ocr-passport-and-cin-2\venv\Lib\site-packages\torch\utils\_contextlib.py", line 116, in decorate_context
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
  File "E:\-ocr-passport-and-cin-2\venv\Lib\site-packages\transformers\generation\utils.py", line 2535, in generate
    result = decoding_method(
             ^^^^^^^^^^^^^^^^
  File "E:\-ocr-passport-and-cin-2\venv\Lib\site-packages\transformers\generation\utils.py", line 2728, in _sample
    outputs = self._prefill(
              ^^^^^^^^^^^^^^
  File "E:\-ocr-passport-and-cin-2\venv\Lib\site-packages\transformers\generation\utils.py", line 3776, in _prefill
    return self(**model_inputs, return_dict=True)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "E:\-ocr-passport-and-cin-2\venv\Lib\site-packages\torch\nn\modules\module.py", line 1736, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "E:\-ocr-passport-and-cin-2\venv\Lib\site-packages\torch\nn\modules\module.py", line 1747, in _call_impl
    return forward_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "E:\-ocr-passport-and-cin-2\venv\Lib\site-packages\accelerate\hooks.py", line 192, in new_forward
    output = module._old_forward(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "E:\-ocr-passport-and-cin-2\venv\Lib\site-packages\transformers\utils\generic.py", line 843, in wrapper
    output = func(self, *args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "E:\-ocr-passport-and-cin-2\venv\Lib\site-packages\transformers\models\gemma3\modeling_gemma3.py", line 1083, in forward
    outputs = self.model(
              ^^^^^^^^^^^
  File "E:\-ocr-passport-and-cin-2\venv\Lib\site-packages\torch\nn\modules\module.py", line 1736, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "E:\-ocr-passport-and-cin-2\venv\Lib\site-packages\torch\nn\modules\module.py", line 1747, in _call_impl
    return forward_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "E:\-ocr-passport-and-cin-2\venv\Lib\site-packages\transformers\utils\generic.py", line 843, in wrapper
    output = func(self, *args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "E:\-ocr-passport-and-cin-2\venv\Lib\site-packages\transformers\models\gemma3\modeling_gemma3.py", line 956, in forward
    causal_mask_mapping = create_causal_mask_mapping(
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "E:\-ocr-passport-and-cin-2\venv\Lib\site-packages\transformers\utils\deprecation.py", line 171, in wrapped_func
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
  File "E:\-ocr-passport-and-cin-2\venv\Lib\site-packages\transformers\models\gemma3\modeling_gemma3.py", line 816, in create_causal_mask_mapping
    return create_masks_for_generate(**mask_kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "E:\-ocr-passport-and-cin-2\venv\Lib\site-packages\transformers\utils\deprecation.py", line 171, in wrapped_func
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
  File "E:\-ocr-passport-and-cin-2\venv\Lib\site-packages\transformers\masking_utils.py", line 1415, in create_masks_for_generate
    causal_masks[layer_pattern] = LAYER_PATTERN_TO_MASK_FUNCTION_MAPPING[layer_pattern](**mask_kwargs)
                                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "E:\-ocr-passport-and-cin-2\venv\Lib\site-packages\transformers\utils\deprecation.py", line 171, in wrapped_func
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
  File "E:\-ocr-passport-and-cin-2\venv\Lib\site-packages\transformers\masking_utils.py", line 916, in create_causal_mask
    raise ValueError("Using `or_mask_function` or `and_mask_function` arguments require torch>=2.6")
ValueError: Using `or_mask_function` or `and_mask_function` arguments require torch>=2.6
127.0.0.1 - - [25/Mar/2026 16:50:52] "POST /extract HTTP/1.1" 500 -

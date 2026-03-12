Downloading Gemma-3-4B Q4_0_QAT...
---------------------------------------------------------------------------
HTTPStatusError                           Traceback (most recent call last)
/usr/local/lib/python3.12/dist-packages/huggingface_hub/utils/_http.py in hf_raise_for_status(response, endpoint_name)
    719     try:
--> 720         response.raise_for_status()
    721     except httpx.HTTPStatusError as e:

10 frames
HTTPStatusError: Client error '401 Unauthorized' for url 'https://huggingface.co/google/gemma-3-4b-it-qat-q4_0-gguf/resolve/main/gemma-3-4b-it-q4_0.gguf'
For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/401

The above exception was the direct cause of the following exception:

GatedRepoError                            Traceback (most recent call last)
/usr/local/lib/python3.12/dist-packages/huggingface_hub/utils/_http.py in hf_raise_for_status(response, endpoint_name)
    738                 f"{response.status_code} Client Error." + "\n\n" + f"Cannot access gated repo for url {response.url}."
    739             )
--> 740             raise _format(GatedRepoError, message, response) from e
    741 
    742         elif error_message == "Access to this resource is disabled.":

GatedRepoError: 401 Client Error. (Request ID: Root=1-69b28f88-34e53d6b12e1a3021bcdc43e;7272afaa-496a-407d-bb70-9c00682ee00b)

Cannot access gated repo for url https://huggingface.co/google/gemma-3-4b-it-qat-q4_0-gguf/resolve/main/gemma-3-4b-it-q4_0.gguf.
Access to model google/gemma-3-4b-it-qat-q4_0-gguf is restricted. You must have access to it and be authenticated to access it. Please log in.
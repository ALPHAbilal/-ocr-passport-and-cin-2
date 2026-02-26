c:\Users\User004\Desktop\soufian_data\neww\-ocr-passport-and-cin-2\venv311\Lib\site-packages\paddle\utils\cpp_extension\extension_utils.py:718: UserWarning: No ccache found. Please be aware that recompiling all source files may be required. You can download and install ccache from: https://github.com/ccache/ccache/blob/master/doc/INSTALL.md
  warnings.warn(warning_message)
PaddlePaddle version: 3.2.1
c:\Users\User004\Desktop\soufian_data\neww\-ocr-passport-and-cin-2\venv311\Lib\site-packages\requests\__init__.py:113: RequestsDependencyWarning: urllib3 (2.6.3) or chardet (6.0.0.post1)/charset_normalizer (3.4.4) doesn't match a supported version!
  warnings.warn(
[33mChecking connectivity to the model hosters, this may take a while. To bypass this check, set `PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK` to `True`.[0m
PaddleOCR imported OK


-------

Loading Arabic model...
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
Cell In[3], line 4
      2 print("Loading Arabic model...")
      3 t0 = time.time()
----> 4 ocr_ar = PaddleOCR(
      5     use_angle_cls=False,
      6     lang='ar',
      7     use_gpu=False,
      8     ocr_version='PP-OCRv4',
      9     drop_score=0.3,
     10     show_log=False
     11 )
     12 print(f"Arabic model ready ({time.time()-t0:.1f}s)")
     14 print("Loading French model...")

File c:\Users\User004\Desktop\soufian_data\neww\-ocr-passport-and-cin-2\venv311\Lib\site-packages\paddleocr\_pipelines\ocr.py:107, in PaddleOCR.__init__(self, doc_orientation_classify_model_name, doc_orientation_classify_model_dir, doc_unwarping_model_name, doc_unwarping_model_dir, text_detection_model_name, text_detection_model_dir, textline_orientation_model_name, textline_orientation_model_dir, textline_orientation_batch_size, text_recognition_model_name, text_recognition_model_dir, text_recognition_batch_size, use_doc_orientation_classify, use_doc_unwarping, use_textline_orientation, text_det_limit_side_len, text_det_limit_type, text_det_thresh, text_det_box_thresh, text_det_unclip_ratio, text_det_input_shape, text_rec_score_thresh, return_word_box, text_rec_input_shape, lang, ocr_version, **kwargs)
    103 det_model_name, rec_model_name = self._get_ocr_model_names(
    104     lang, ocr_version
    105 )
    106 if det_model_name is None or rec_model_name is None:
--> 107     raise ValueError(
    108         f"No models are available for the language {repr(lang)} and OCR version {repr(ocr_version)}."
    109     )
    110 text_detection_model_name = det_model_name
    111 text_recognition_model_name = rec_model_name

ValueError: No models are available for the language 'ar' and OCR version 'PP-OCRv4'.
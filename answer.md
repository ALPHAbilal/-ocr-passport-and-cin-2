This is a nuanced detection + recognition pipeline problem. Here's a thorough breakdown:

## Why Specific French Names Are Missed

The most likely cause is a **detection failure, not a recognition failure**. PaddleOCR uses a DB (Differentiable Binarization) detector that operates on a probability map — it scores pixels as "text" or "background." Names on a CNIE card are often printed in a **different font weight, size, or contrast** than headers/dates. The DB detector can fail to threshold those regions above `det_db_box_thresh` (default 0.6), meaning the text box never gets proposed to the recognizer at all. You can confirm this by visualizing raw detection boxes: if the name region has no box, it's purely a detection miss. [github](https://github.com/PaddlePaddle/PaddleOCR/discussions/13164)

A secondary cause: the Arabic model (`lang='ar'`) uses a detector trained predominantly on Arabic-script scenes. Its feature extractor may not fire strongly on isolated Latin uppercase text blocks, even if they happen to be adjacent to Arabic content. [arxiv](http://arxiv.org/pdf/2009.09941.pdf)

## Detection vs. Recognition Distinction

Run PaddleOCR with only the detector enabled and visualize the output boxes on your 856×540 image. If the Latin name region has **no bounding box**, the recognizer is never even invoked — that rules out a recognition problem entirely. The fact that headers and dates *are* detected suggests the name regions have a distinct visual property: possibly lower inter-character spacing, slightly smaller pixel height, or a region near the card edge where DB's unclipping math clips it out. [github](https://github.com/PaddlePaddle/PaddleOCR/issues/15603)

## Does `lang='latin'` or Multilingual Help?

For PP-OCRv5 specifically, **`lang='latin'`** uses a shared Latin-script recognizer which covers French natively and should be your first swap. However, it won't fix detection misses — the detector is the same regardless of `lang`. The more promising option is **PaddleOCR-VL**, the vision-language variant that supports 109 languages including Arabic and French simultaneously. It processes the whole card in one pass and handles mixed-script documents far better than running two separate language models and merging results. [github](https://github.com/PaddlePaddle/PaddleOCR)

## Key Parameters to Tune

These settings directly address your use case: [github](https://github.com/PaddlePaddle/PaddleOCR/discussions/15011)

| Parameter | Default | Recommended for CNIE | Why |
|---|---|---|---|
| `det_db_thresh` | 0.3 | **0.2** | Catches lower-contrast text pixels in the binarization map |
| `det_db_box_thresh` | 0.6 | **0.4–0.45** | Lets lower-confidence name boxes survive box filtering |
| `det_db_unclip_ratio` | 1.5 | **1.8–2.0** | Expands detected boxes outward, helps with tight-margin names |
| `det_limit_side_len` | 960 | **960–1280** | Prevents downscaling that destroys small-text detail at 856px wide |
| `det_limit_type` | `max` | `max` | Correct for your image size; `min` can cause over-upscaling |
| `use_dilation` | False | **True** | Dilates the probability map before boxing, groups nearby strokes |

A practical starting config for your dual-pass approach:

```python
from paddleocr import PaddleOCR

ocr = PaddleOCR(
    lang='fr',
    det_db_thresh=0.2,
    det_db_box_thresh=0.4,
    det_db_unclip_ratio=1.8,
    det_limit_side_len=1280,
    det_limit_type='max',
    use_dilation=True,
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
)
```

## Recommended Pipeline Architecture

Rather than merging two broken passes, restructure like this:

1. **Run one detector** (French/Latin model) to get all bounding boxes on the full card image — tune parameters above until every region is captured.
2. **Per-box, choose the recognizer** based on the script predicted (or by bounding box zone if you know the card layout).
3. Alternatively, **use PaddleOCR-VL** (`PaddleOCR(model_name='PP-OCR-VL')`) which supports Arabic + Latin in a single inference pass and avoids the merge problem entirely. [sonusahani](https://sonusahani.com/blogs/paddleocr-vl)

If you're preprocessing with OpenCV, also ensure you're not applying aggressive thresholding that smooths out low-weight Latin glyphs while preserving bold Arabic strokes — adaptive thresholding (`cv2.THRESH_OTSU`) on the full card before feeding to PaddleOCR often surfaces missed text regions.
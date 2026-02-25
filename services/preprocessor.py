"""
CNIE Card Preprocessor
Detects a card in a raw photo, corrects perspective, crops, and resizes to 856x540.
"""

import cv2
import numpy as np


NORM_W = 856
NORM_H = 540


def order_points(pts):
    """
    Order 4 points as: top-left, top-right, bottom-right, bottom-left.
    This is critical for perspective warp — wrong order = flipped/rotated output.
    """
    rect = np.zeros((4, 2), dtype="float32")
    # top-left has smallest sum, bottom-right has largest sum
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    # top-right has smallest difference, bottom-left has largest difference
    d = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(d)]
    rect[3] = pts[np.argmax(d)]
    return rect


def four_point_warp(image, pts):
    """
    Perspective warp from 4 source points to a flat rectangle.
    """
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    # compute width of the new image
    width_a = np.linalg.norm(br - bl)
    width_b = np.linalg.norm(tr - tl)
    max_width = max(int(width_a), int(width_b))

    # compute height of the new image
    height_a = np.linalg.norm(tr - br)
    height_b = np.linalg.norm(tl - bl)
    max_height = max(int(height_a), int(height_b))

    # destination points for the warp
    dst = np.array([
        [0, 0],
        [max_width - 1, 0],
        [max_width - 1, max_height - 1],
        [0, max_height - 1],
    ], dtype="float32")

    matrix = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, matrix, (max_width, max_height))
    return warped


def find_card_contour(image):
    """
    Find the largest quadrilateral contour in the image (the card).
    Returns 4 corner points or None if not found.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)

    # try multiple edge detection strategies
    card_contour = None
    best_area = 0

    # Strategy 1: Canny edge detection
    for low_thresh in [30, 50, 75]:
        edged = cv2.Canny(blurred, low_thresh, low_thresh * 3)
        # dilate to close small gaps in edges
        edged = cv2.dilate(edged, np.ones((3, 3), np.uint8), iterations=1)
        contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        result = _find_best_quad(contours, image.shape)
        if result is not None:
            area = cv2.contourArea(result)
            if area > best_area:
                best_area = area
                card_contour = result

    # Strategy 2: Adaptive threshold
    if card_contour is None:
        thresh = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV, 11, 2
        )
        thresh = cv2.dilate(thresh, np.ones((3, 3), np.uint8), iterations=2)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        result = _find_best_quad(contours, image.shape)
        if result is not None:
            card_contour = result

    return card_contour


def _find_best_quad(contours, img_shape):
    """
    From a list of contours, find the best quadrilateral that looks like a card.
    """
    img_area = img_shape[0] * img_shape[1]

    # sort by area, largest first
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    for contour in contours[:10]:  # check top 10 largest
        area = cv2.contourArea(contour)

        # card should be at least 10% of the image and less than 95%
        if area < img_area * 0.10 or area > img_area * 0.95:
            continue

        # approximate the contour to a polygon
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * peri, True)

        # we want exactly 4 points (a rectangle)
        if len(approx) == 4:
            return approx.reshape(4, 2)

    return None


def ensure_landscape(image):
    """
    If the warped card is portrait (taller than wide), rotate it 90° clockwise.
    ID cards are always landscape.
    """
    h, w = image.shape[:2]
    if h > w:
        image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    return image


def preprocess_card(image_bytes):
    """
    Full pipeline: raw image bytes -> clean 856x540 card image.

    Args:
        image_bytes: raw image file bytes

    Returns:
        dict with:
            - "success": bool
            - "image": numpy array (856x540 BGR) if success
            - "error": string if failed
            - "debug": dict with intermediate info
    """
    # decode image from bytes
    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if image is None:
        return {"success": False, "error": "Could not decode image", "debug": {}}

    orig_h, orig_w = image.shape[:2]
    debug = {"original_size": f"{orig_w}x{orig_h}"}

    # find the card
    card_points = find_card_contour(image)

    if card_points is None:
        # fallback: use the whole image (maybe it's already cropped)
        debug["detection"] = "no_card_found_using_full_image"
        # just resize the whole image preserving aspect ratio as best we can
        result = cv2.resize(image, (NORM_W, NORM_H), interpolation=cv2.INTER_AREA)
        return {"success": True, "image": result, "debug": debug}

    debug["detection"] = "card_found"
    debug["corners"] = card_points.tolist()

    # perspective warp to flatten the card
    warped = four_point_warp(image, card_points.astype("float32"))

    # ensure landscape orientation
    warped = ensure_landscape(warped)

    warped_h, warped_w = warped.shape[:2]
    debug["warped_size"] = f"{warped_w}x{warped_h}"

    # resize to standard 856x540
    result = cv2.resize(warped, (NORM_W, NORM_H), interpolation=cv2.INTER_AREA)

    return {"success": True, "image": result, "debug": debug}


def preprocess_card_from_path(image_path):
    """
    Convenience: preprocess from a file path.
    """
    with open(image_path, "rb") as f:
        return preprocess_card(f.read())


# CLI usage for quick testing
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python preprocessor.py <image_path> [output_path]")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "preprocessed.jpg"

    result = preprocess_card_from_path(input_path)
    if result["success"]:
        cv2.imwrite(output_path, result["image"])
        print(f"Saved to {output_path}")
        print(f"Debug: {result['debug']}")
    else:
        print(f"Failed: {result['error']}")

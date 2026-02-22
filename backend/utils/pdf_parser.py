"""
Answer sheet PDF parser using OpenCV bubble detection.

Supports two approaches:
1. Bubble detection: finds filled circles on bubble-sheet answer sheets
2. OCR fallback: text-based extraction for handwritten/typed answers

The bubble sheet format expected:
- Two-column table layout
- Each row: question number | A bubble | B bubble | C bubble | D bubble
- Students shade the circle for their answer
"""
import logging
import os
import re
import sys
import tempfile

import cv2
import numpy as np
import pytesseract
from pdf2image import convert_from_path
from PIL import Image

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

logger = logging.getLogger(__name__)

OPTION_LABELS = ['A', 'B', 'C', 'D']


def extract_answers_from_pdf(pdf_path):
    """
    Extract answers from a scanned/photographed bubble-sheet answer PDF.
    Tries bubble detection first, falls back to OCR text extraction.
    """
    answers = _detect_bubbles(pdf_path)

    if not answers:
        logger.info("Bubble detection found no answers, falling back to OCR")
        answers = _ocr_extract(pdf_path)

    # Deduplicate: keep last occurrence per question number
    seen = {}
    for item in answers:
        seen[item['question_number']] = item['answer']

    return [{'question_number': qn, 'answer': ans} for qn, ans in sorted(seen.items())]


def _detect_bubbles(pdf_path):
    """
    Detect filled bubbles on a bubble-sheet answer PDF.

    Strategy:
    1. Convert PDF pages to high-DPI images
    2. Find all circles (bubbles) using HoughCircles
    3. Group circles into rows (by y-coordinate)
    4. For each row, measure the darkness inside each circle
    5. The darkest circle (most filled) is the selected answer
    """
    answers = []

    with tempfile.TemporaryDirectory() as tmp_dir:
        pages = convert_from_path(pdf_path, dpi=200, output_folder=tmp_dir)

        for page_image in pages:
            img = cv2.cvtColor(np.array(page_image), cv2.COLOR_RGB2BGR)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Apply slight blur to reduce noise
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)

            # Detect circles using Hough transform
            circles = cv2.HoughCircles(
                blurred,
                cv2.HOUGH_GRADIENT,
                dp=1.2,
                minDist=20,
                param1=50,
                param2=30,
                minRadius=8,
                maxRadius=25
            )

            if circles is None:
                continue

            circles = np.round(circles[0]).astype(int)

            # Measure fill level of each circle
            circle_data = []
            for (cx, cy, r) in circles:
                # Create a mask for this circle
                mask = np.zeros(gray.shape, dtype=np.uint8)
                cv2.circle(mask, (cx, cy), max(r - 2, 1), 255, -1)

                # Calculate mean pixel intensity inside the circle
                # Lower intensity = darker = more filled
                mean_val = cv2.mean(gray, mask=mask)[0]
                circle_data.append({
                    'x': cx, 'y': cy, 'r': r, 'fill': mean_val
                })

            if not circle_data:
                continue

            # Group circles into rows by y-coordinate (tolerance based on radius)
            circle_data.sort(key=lambda c: (c['y'], c['x']))
            rows = _group_into_rows(circle_data)

            # Also try to find question numbers via OCR for each row region
            # For now, assign question numbers based on row order
            page_answers = _extract_answers_from_rows(rows, gray)
            answers.extend(page_answers)

    return answers


def _group_into_rows(circles, y_tolerance=15):
    """Group circles into rows based on y-coordinate proximity."""
    if not circles:
        return []

    rows = []
    current_row = [circles[0]]

    for c in circles[1:]:
        if abs(c['y'] - current_row[0]['y']) <= y_tolerance:
            current_row.append(c)
        else:
            rows.append(current_row)
            current_row = [c]

    if current_row:
        rows.append(current_row)

    return rows


def _extract_answers_from_rows(rows, gray_img):
    """
    For each row of circles, determine if a bubble was filled.
    Expects 4 circles per answer row (A, B, C, D).
    Rows with != 4 circles are skipped (header rows, decorative elements, etc.)
    """
    answers = []
    question_num = 1

    # The bubble sheet has two columns side by side.
    # We need to detect the column split and process each column separately.
    # Strategy: separate rows into left-half and right-half groups by x-position.

    if not rows:
        return answers

    # Find all rows that have exactly 4 circles (answer rows)
    answer_rows = [row for row in rows if len(row) == 4]

    if not answer_rows:
        # Try rows with 4-5 circles (sometimes the q-number cell gets detected)
        answer_rows = [row for row in rows if 4 <= len(row) <= 5]
        # Take only the 4 rightmost circles in each row
        answer_rows = [sorted(row, key=lambda c: c['x'])[-4:] for row in answer_rows]

    if not answer_rows:
        return answers

    # Determine if we have a two-column layout by checking x-positions
    all_x = [c['x'] for row in answer_rows for c in row]
    if all_x:
        mid_x = (min(all_x) + max(all_x)) / 2
        left_rows = [r for r in answer_rows if _row_avg_x(r) < mid_x]
        right_rows = [r for r in answer_rows if _row_avg_x(r) >= mid_x]

        if left_rows and right_rows:
            # Two-column layout: process left column first, then right
            left_rows.sort(key=lambda r: r[0]['y'])
            right_rows.sort(key=lambda r: r[0]['y'])

            for row in left_rows:
                ans = _pick_answer(row, gray_img)
                if ans:
                    answers.append({'question_number': question_num, 'answer': ans})
                question_num += 1

            for row in right_rows:
                ans = _pick_answer(row, gray_img)
                if ans:
                    answers.append({'question_number': question_num, 'answer': ans})
                question_num += 1
        else:
            # Single column
            answer_rows.sort(key=lambda r: r[0]['y'])
            for row in answer_rows:
                ans = _pick_answer(row, gray_img)
                if ans:
                    answers.append({'question_number': question_num, 'answer': ans})
                question_num += 1

    return answers


def _row_avg_x(row):
    """Average x position of circles in a row."""
    return sum(c['x'] for c in row) / len(row)


def _pick_answer(row_circles, gray_img):
    """
    Given 4 circles (A, B, C, D sorted left-to-right),
    determine which one is filled (darkest).
    Returns the answer letter or None if no bubble is clearly filled.
    """
    # Sort left to right: A, B, C, D
    sorted_circles = sorted(row_circles, key=lambda c: c['x'])[:4]

    fills = []
    for c in sorted_circles:
        mask = np.zeros(gray_img.shape, dtype=np.uint8)
        cv2.circle(mask, (c['x'], c['y']), max(c['r'] - 2, 1), 255, -1)
        mean_val = cv2.mean(gray_img, mask=mask)[0]
        fills.append(mean_val)

    if not fills:
        return None

    # Find the darkest bubble
    min_fill = min(fills)
    max_fill = max(fills)

    # Only count as filled if significantly darker than the lightest
    # A filled bubble should be at least 30% darker than empty ones
    threshold = max_fill - (max_fill - min_fill) * 0.3

    if min_fill >= threshold:
        # No bubble is clearly filled
        return None

    darkest_idx = fills.index(min_fill)
    if darkest_idx < len(OPTION_LABELS):
        return OPTION_LABELS[darkest_idx]

    return None


def _ocr_extract(pdf_path):
    """Fallback: OCR-based text extraction for answer sheets."""
    answers = []

    with tempfile.TemporaryDirectory() as tmp_dir:
        pages = convert_from_path(pdf_path, dpi=300, output_folder=tmp_dir)

        for page_image in pages:
            gray = cv2.cvtColor(np.array(page_image), cv2.COLOR_RGB2GRAY)
            text = pytesseract.image_to_string(gray)

            # Match patterns: "Q1: A", "1. B", "1 A", "Q1 - C", etc.
            matches = re.findall(r'(?:Q|q)?\s?(\d+)[\:\.\-\s]+([A-Da-d])\b', text)
            for qno, ans in matches:
                qn = int(qno)
                if 1 <= qn <= 100:  # reasonable question number range
                    answers.append({
                        'question_number': qn,
                        'answer': ans.upper()
                    })

    return answers

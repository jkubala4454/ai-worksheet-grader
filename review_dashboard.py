import os
import re
import streamlit as st
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import pandas as pd
import numpy as np
from streamlit_drawable_canvas import st_canvas

# Setup
pdf_folder = os.path.expanduser('~/student_pdfs')
review_log = 'review_log.txt'
manual_log = 'manual_review_log.txt'
processed_files = set()

# Load processed files
if os.path.exists(review_log):
    with open(review_log, 'r') as log:
        for line in log:
            original = line.strip().split(' → ')[0]
            processed_files.add(original)

# Get unprocessed PDFs
pdf_files = [f for f in os.listdir(pdf_folder) if f.lower().endswith('.pdf') and f not in processed_files]
pdf_files.sort()

# Session state setup
if 'index' not in st.session_state:
    st.session_state.index = 0
if 'region' not in st.session_state:
    st.session_state.region = None
if 'region_set' not in st.session_state:
    st.session_state.region_set = False

st.title("📄 Student PDF Renamer with Region-Based OCR")

if st.session_state.index < len(pdf_files):
    current_file = pdf_files[st.session_state.index]
    pdf_path = os.path.join(pdf_folder, current_file)

    # Convert first page to image
    images = convert_from_path(pdf_path, dpi=80, first_page=1, last_page=1)
    image = images[0]

    # Region selector (only once per batch)
    if not st.session_state.region_set:
        st.subheader("🖍️ Select Name Region (first file only)")

        image_rgb = image.convert("RGB")
        width, height = image_rgb.size

        canvas_result = st_canvas(
            fill_color="rgba(255, 255, 255, 0.3)",
            stroke_width=2,
            background_image=image_rgb,
            update_streamlit=True,
            height=height,
            width=width,
            drawing_mode="rect",
            key="canvas",
        )



        if canvas_result.json_data and len(canvas_result.json_data["objects"]) > 0:
            obj = canvas_result.json_data["objects"][0]
            left = int(obj["left"])
            top = int(obj["top"])
            width = int(obj["width"])
            height = int(obj["height"])
            st.session_state.region = (left, top, left + width, top + height)
            st.session_state.region_set = True
            st.success("✅ Region locked for this batch. Proceeding to OCR...")
            st.rerun()
        else:
            st.info("Draw a rectangle around the student's name to begin.")
            st.stop()

    # Crop selected region
    region = st.session_state.region
    name_crop = image.crop(region)

    # Preprocess
    gray = name_crop.convert('L')
    bw = gray.point(lambda x: 0 if x < 180 else 255, '1')

    # OCR with confidence
    ocr_data = pytesseract.image_to_data(bw, output_type=pytesseract.Output.DATAFRAME)
    ocr_data = ocr_data[ocr_data.conf != -1]
    text = " ".join(ocr_data['text'].dropna().tolist())
    avg_conf = round(ocr_data['conf'].mean(), 1) if not ocr_data.empty else 0

    # Suggested name
    match = re.search(r'Name[:\s\-]*([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2})', text)
    suggested_name = match.group(1).strip().replace(' ', '_') if match else ''

    # Final name logic
    fallback_name = f"UNSURE_{os.path.splitext(current_file)[0]}.pdf"
    default_name = f"{suggested_name}.pdf" if avg_conf >= 85 and suggested_name else fallback_name
    final_name = st.text_input("✏️ Enter final filename (with .pdf)", value=default_name)
    st.session_state.final_name = final_name

    # Display
    st.caption(f"Reviewing file {st.session_state.index + 1} of {len(pdf_files)}")
    st.subheader(f"Reviewing: {current_file}")
    st.image(name_crop, caption="📍 Selected Name Region", use_container_width=True)
    st.text_area("🧠 OCR Output", text, height=150)
    st.text(f"🔍 OCR Confidence Score: {avg_conf}%")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("✅ Rename and Save"):
            new_path = os.path.join(pdf_folder, final_name)
            os.rename(pdf_path, new_path)
            with open(review_log, "a") as log:
                log.write(f"{current_file} → {final_name}\n")
            st.session_state.index += 1
            st.rerun()

    with col2:
        if st.button("⏭️ Skip"):
            with open(review_log, "a") as log:
                log.write(f"{current_file} → SKIPPED\n")
            st.session_state.index += 1
            st.rerun()

    with col3:
        if st.button("⚠️ Flag for Manual Review"):
            with open(manual_log, "a") as log:
                log.write(f"{current_file} → CONFIDENCE {avg_conf}%\n")
            st.session_state.index += 1
            st.rerun()

    with col4:
        if st.button("↩️ Undo Last"):
            if st.session_state.index > 0:
                st.session_state.index -= 1
                last_file = pdf_files[st.session_state.index]
                with open(review_log, "r") as log:
                    lines = log.readlines()
                with open(review_log, "w") as log:
                    for line in lines:
                        if not line.startswith(last_file):
                            log.write(line)
                st.warning(f"Undid last action for {last_file}")

else:
    st.success("🎉 All files reviewed!")
    # Reset region for next batch
    st.session_state.region = None
    st.session_state.region_set = False

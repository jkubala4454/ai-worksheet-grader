# AI Worksheet Grader

A modular, privacy-safe AI grading system for scanned student worksheets. Designed for real classrooms, this tool automates OCR, rubric-based scoring, and feedback generation while keeping teachers in control and student data protected.

## ✨ Features

- 🧼 **Automatic Redaction**: Removes student names from PDFs before AI submission
- 🔍 **OCR with Confidence Scoring**: Extracts handwritten answers and flags low-confidence regions
- 📊 **Rubric-Based Scoring**: Aligns with IB and other standards; supports fuzzy matching and partial credit
- 💬 **Copilot-Assisted Feedback**: Generates personalized, rubric-aligned comments for student growth
- ✅ **Manual Review Queue**: Teachers can override scores and approve feedback before submission
- 🚀 **LMS Integration**: Automates uploads to platforms like Schoology using browser automation

## 🧭 Roadmap

See [`roadmap.md`](roadmap.md) for a full breakdown of development phases, including:
- Phase 1: Redaction Pipeline
- Phase 2: OCR + Answer Extraction
- Phase 3: Grading Engine
- Phase 4: Feedback & Review Dashboard
- Phase 5: LMS Integration

## 🛠️ Tech Stack

- Python
- Streamlit (dashboard)
- Tesseract / EasyOCR
- PyMuPDF (PDF redaction)
- Selenium (LMS automation)
- Copilot (AI feedback generation)

## 🔐 Privacy First

This project is built with student privacy at its core:
- No student names or identifiers are submitted to AI
- All redaction happens locally before grading
- Feedback is generated only from anonymized content

## 📂 Structure

ai-worksheet-grader/ 
  ├── redaction/ 
  ├── ocr/ 
  ├── grading/ 
  ├── feedback/ 
  ├── dashboard/ 
  ├── lms_upload/ 
  └── tests/


## 👨‍🏫 Built By

An educator and technologist committed to scalable, student-friendly automation that respects teacher judgment and classroom nuance.

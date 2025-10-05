# Roadmap: AI Worksheet Grader

This roadmap outlines the development phases for a privacy-safe, teacher-controlled AI grading system for scanned student worksheets. Each phase is modular and designed to be built incrementally, with clear milestones and optional enhancements.

---

## 🟩 Phase 1: Redaction Pipeline

**Goal**: Ensure student privacy by removing identifying information before AI submission.

- [ ] Detect student name region using bounding box logic (already implemented)
- [ ] Visually redact name by drawing a white rectangle over the region
- [ ] Save redacted copy (`ID_only.pdf`) alongside original (`StudentName_ID.pdf`)
- [ ] Flatten PDF or remove hidden OCR text layer
- [ ] Store local mapping of `StudentName → ID` for gradebook use

---

## 🟨 Phase 2: OCR + Answer Extraction

**Goal**: Extract structured answers from scanned worksheets.

- [ ] Run OCR on redacted PDFs using Tesseract or EasyOCR
- [ ] Extract answers into structured format (e.g., JSON or dict)
- [ ] Include confidence scores per region
- [ ] Flag low-confidence answers for manual review
- [ ] Preview extracted answers in dashboard for teacher approval

---

## 🟦 Phase 3: Grading Engine

**Goal**: Score answers using rubric logic and AI assistance.

- [ ] Parse IB rubric into structured format (Google Sheet or YAML)
- [ ] Match short answers using fuzzy logic or regex
- [ ] Submit open-ended answers to Copilot for scoring and feedback
- [ ] Receive rubric-aligned score and comment per question
- [ ] Flag ambiguous cases for manual review and override

---

## 🟪 Phase 4: Feedback & Review Dashboard

**Goal**: Display scores, feedback, and allow teacher control.

- [ ] Show extracted answers, scores, and feedback in Streamlit
- [ ] Highlight flagged or low-confidence items
- [ ] Allow teacher override or manual scoring
- [ ] Export results to gradebook format (CSV, JSON, etc.)

---

## 🟥 Phase 5: LMS Integration

**Goal**: Automate upload of scores and feedback to Schoology.

- [ ] Match redacted file to student via ID mapping
- [ ] Use Selenium to upload scores and feedback to LMS
- [ ] Log upload status and errors
- [ ] Add retry logic for failed uploads

---

## 🧩 Optional Enhancements

- [ ] Handwriting OCR tuning for math/science diagrams
- [ ] Feedback tone selector (Encouraging, Direct, Detailed)
- [ ] Student growth tracking across assignments
- [ ] Gamified feedback (badges, improvement comments)
- [ ] Teacher dashboard analytics (time saved, rubric alignment)

---

## 🧠 Development Notes

- Each phase is modular and testable in isolation.
- Student data is never submitted to AI — only redacted content.
- All feedback is teacher-reviewed before submission.
- Designed for real classrooms with real constraints.


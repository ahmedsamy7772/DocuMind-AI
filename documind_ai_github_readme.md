# 🚀 [Tips Hindawi](https://www.tipshindawi.com/) Internship (August–October) 2026

> 🎓 This project was built during the [**Tips Hindawi**](https://www.tipshindawi.com/) **Internship (August–October) 2026**.

## 👤 Participant

| Field            | Value                                                              |
| ---------------- | ------------------------------------------------------------------ |
| Full Name        | Ahmed                                                              |
| Project Name     | **DocuMind AI — Enterprise Document Intelligence & RAG Workspace** |
| GitHub Username  | `[Your GitHub Username]`                                           |
| Internship Batch | August–October 2026                                                |
| Training Program | Large Language Models (LLMs) Program                               |
| Organization     | [**Edrak for Ai**](https://edrak4ai.com/en)                         |

---

# 📖 Project Overview

**DocuMind AI** is a production-grade Document Intelligence and Retrieval-Augmented Generation (RAG) platform designed to bridge the gap between static unstructured files and actionable enterprise intelligence.

Standard naive RAG implementations often suffer from retrieval noise, context dilution, and hallucinations when handling multi-document contexts. DocuMind AI solves this by coupling local open-weights LLM inference with high-dimensional vector retrieval, adaptive domain personas, cross-document comparison, and grounded source attribution.

Whether analyzing enterprise service contracts, technical specifications, or applicant resumes, DocuMind AI indexes documents in real time and provides a modern, interactive SaaS workspace complete with voice synthesis, automated report generation, and instant summarization.

---

# ✨ Key Features

* **⚡ Real-Time Multi-Format Ingestion:** Instant parsing and contextual chunking across both complex **PDF** and **DOCX** files with zero external API dependencies.
* **🧠 Grounded Semantic Retrieval (RAG):** Powered by ChromaDB and dense embeddings (`all-MiniLM-L6-v2`) to perform precise semantic searches with strict context grounding to prevent hallucinations.
* **⚖️ Adaptive AI Intelligence Personas:** Dynamic system prompt steering tailored to operational workflows:
  * **General Assistant:** Neutral, balanced information synthesis.
  * **Legal Counsel:** In-depth risk exposure analysis, obligations, and contractual terms.
  * **HR Executive:** Candidate qualification breakdown, strengths/weaknesses matrices, and recommendations.
  * **Academic Tutor:** Core concept breakdowns, study summaries, and structured learning points.
* **📊 One-Click Document Comparison:** Automatically synthesizes differences, synergies, and key takeaways across multiple uploaded files into Markdown comparison tables.
* **📌 Verifiable Source Citations:** Every generated insight links back to the originating document chunks, ensuring enterprise auditing compliance.
* **✨ Instant Document Auto-Summarization:** Automatically delivers an executive brief immediately after ingestion.
* **🎙️ Voice Assistant & TTS Readouts:** Built-in Speech-to-Text for hands-free querying alongside on-demand Text-to-Speech (TTS) audio narration.
* **📄 Executive PDF Report Export:** Converts the entire interactive session into a formatted, downloadable PDF report with a single click.

---

# 🛠️ Technologies Used

### **Core Machine Learning & AI**
* **Inference LLM:** `Qwen/Qwen2.5-0.5B-Instruct` via Hugging Face `transformers`
* **Embedding Model:** `sentence-transformers/all-MiniLM-L6-v2`
* **Vector Store:** `ChromaDB` (In-memory & local persistence collection)
* **Compute Backend:** PyTorch (Accelerated with CUDA if available, CPU fallback)

### **Backend Engineering**
* **Framework:** `FastAPI` (Asynchronous REST API)
* **ASGI Server:** `Uvicorn`
* **Document Extraction:** `pdfplumber` (PDF layout-aware text extraction), `python-docx` (DOCX extraction)

### **Frontend & Interface**
* **Design:** Modern Glassmorphism Workspace built with `Tailwind CSS`
* **Icons & Typography:** `FontAwesome 6.4`, Google Fonts (`Inter`)
* **Markdown Engine:** `Marked.js` (for rendering tables, code, and lists)
* **PDF Engine:** `html2pdf.js`
* **Audio & Speech APIs:** Native browser Web Speech API (`SpeechRecognition` & `SpeechSynthesis`)

---

# 📐 System Architecture

```text
       +-------------------------------------------------------+
       |                  User Web Interface                   |
       |  (Glassmorphism UI, Voice I/O, Personas, PDF Export)   |
       +---------------------------+---------------------------+
                                   | HTTP / Multipart
                                   v
       +-------------------------------------------------------+
       |                   FastAPI Backend                     |
       +---------------------------+---------------------------+
               |                                       |
    [Ingestion Pipeline]                     [Query Pipeline]
               |                                       |
  Extract Text (PDF / DOCX)                  Dense Query Embedding
               |                                       |
    Contextual Chunking                                v
               |                             ChromaDB Vector Store
               v                             (Top-K Similarity Search)
   Sentence-Transformers Embeddings                    |
               |                                       v
               v                             Retrieved Context Chunks
      ChromaDB Indexing                                |
               |                                       v
               +--------------> LLM Inference Engine <---------+
                            (Qwen2.5-0.5B-Instruct)
                            + Selected AI Persona
                                       |
                                       v
                          Streamed Markdown Answer +
                          Source Badges + Follow-ups
```

---

# ⚙️ Installation & Setup

### 1. Prerequisites
* Python 3.10+ installed
* Git installed
* (Optional) NVIDIA GPU with CUDA support for accelerated model inference

### 2. Clone the Repository
```bash
git clone https://github.com/[Your GitHub Username]/DocuMind-AI.git
cd DocuMind-AI
```

### 3. Create and Activate Virtual Environment
```bash
# On Windows:
python -m venv venv
venv\Scripts\activate

# On macOS/Linux:
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install fastapi uvicorn pdfplumber python-docx chromadb sentence-transformers transformers torch
```

### 5. Launch the Backend Server
```bash
python main.py
```
> The API server will initialize on `http://127.0.0.1:8000`. On first launch, the models (`all-MiniLM-L6-v2` and `Qwen2.5-0.5B-Instruct`) will download locally automatically.

### 6. Launch the Frontend
Simply open `index.html` in any modern web browser, or serve it via Live Server:
```bash
# Optional: using python's built-in http server
python -m http.server 5500
```
Open your browser at `http://127.0.0.1:5500`.

---

# 🚀 Usage Guide

1. **Check System Status:** Verify that the bottom-left status indicator displays `SYSTEM ONLINE`.
2. **Select Intelligence Mode:** Choose between *General*, *Legal*, *HR*, or *Student* mode from the sidebar dropdown.
3. **Upload Knowledge Files:** Drag and drop your `.pdf` or `.docx` files into the designated drop zone.
4. **Read Auto-Summary:** An automatic synthesis of the primary themes in your documents will appear.
5. **Interact:**
   * Type any question into the input field or click the **Microphone** icon to dictate your question.
   * Click **Compare Documents** to generate a comparative analysis table across all active files.
   * Click **Listen** under any AI response to hear the answer via speech synthesis.
6. **Export Findings:** Click **Export Report** at the top right to download a clean PDF summary of your entire workspace session.

---

# 📸 Demo & Screenshots

| Workspace & Comparison Interface | Intelligence Modes & Upload Zone |
| :---: | :---: |
| ![DocuMind Preview](image.png) | *(Add additional screenshots or demo GIFs here)* |

---

# 📈 Results & Key Learnings

* **Zero-Hallucination Boundaries:** By strictly conditioning generation on ChromaDB retrieved chunks, out-of-scope queries correctly trigger grounding refusal states.
* **Low Latency on Edge/Consumer Hardware:** Utilizing lightweight embeddings alongside quantized/small-footprint instruct models (`Qwen2.5-0.5B`) achieves fast generation without external cloud API dependencies.
* **Persona Calibration:** Implemented system-level prompting strategies that alter formatting style (e.g., Markdown tables for HR/Legal) without compromising factual grounding.

---

# 🔮 Future Roadmap

* [ ] Hybrid Search: Integrate BM25 keyword matching alongside dense vector retrieval (Reciprocal Rank Fusion).
* [ ] Multi-Modal OCR: Add asynchronous OCR worker pipelines (`Tesseract` / `PaddleOCR`) for scanned documents and receipts.
* [ ] Persistent Sessions: Multi-tenant user authentication and chat history persistence with SQLite/PostgreSQL.
* [ ] Dockerization: Provide a single-command `docker-compose.yml` for unified backend and frontend orchestration.

---

# 📚 About the Internship

This project was developed as part of the [**Tips Hindawi**](https://www.tipshindawi.com/) **Internship (August–October) 2026**, and it will be showcased on the official [Tips Hindawi](https://www.tipshindawi.com/) website.

[Tips Hindawi](https://www.tipshindawi.com/) is the internships department of [**Edrak for Ai**](https://edrak4ai.com/en), and the internship encourages participants to build real-world projects, apply practical skills, and showcase their work through GitHub.

For more information about the internship, training programs, and upcoming batches, visit the official [Tips Hindawi](https://www.tipshindawi.com/) website.

---

# 📄 License

This project is shared for educational and portfolio purposes under the MIT License.
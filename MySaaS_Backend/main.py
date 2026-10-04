import os
import shutil
import re
from typing import List
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber
import docx
import chromadb
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import uvicorn

# FEATURE 1: OCR Support (Graceful fallback if not installed)
try:
    import pytesseract
    from PIL import Image
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    print("[WARNING] pytesseract or Pillow not installed. Image OCR disabled.")

app = FastAPI(
    title="DocuMind Enterprise API",
    description="Advanced RAG Engine with OCR, Persona Support, and Markdown Generation."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("[INFO] Initializing Enterprise ML Models...")

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
embedder = SentenceTransformer(EMBEDDING_MODEL_NAME)

LLM_MODEL_ID = "Qwen/Qwen2.5-0.5B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL_ID)

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"[INFO] Compute Engine: {device.upper()}")

model = AutoModelForCausalLM.from_pretrained(
    LLM_MODEL_ID,
    dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    device_map="auto"
)

chroma_client = chromadb.Client()
try: chroma_client.delete_collection("enterprise_docs")
except: pass
collection = chroma_client.create_collection(name="enterprise_docs")

# FEATURE 2: AI Personas Definitions (Engineered for Markdown output)
PERSONAS = {
    "General": "You are a highly intelligent SaaS assistant. Answer thoroughly using ONLY the provided context. Format your output using Markdown (bolding, bullet points, code blocks) to make it highly readable.",
    "Legal": "You are an elite Legal AI Counsel. Analyze the context for legal risks, obligations, and terms. Use precise legal terminology. Structure your answer using Markdown with clear headers and bullet points. Rely ONLY on the context.",
    "HR": "You are a Senior Technical HR Manager. Analyze the provided context (resumes/profiles). Highlight strengths, weaknesses, and a final recommendation. Use Markdown tables or bullet lists for clear presentation. Rely ONLY on the context.",
    "Student": "You are a brilliant Academic Tutor. Break down complex concepts from the context into easy-to-understand explanations. Use Markdown formatting (bolding key terms, creating study lists) to help a student learn."
}

@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    text_chunks = []
    temp_dir = "temp_workspace"
    os.makedirs(temp_dir, exist_ok=True)
    
    for file in files:
        file_path = os.path.join(temp_dir, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        filename_lower = file.filename.lower()
        
        # 1. PDF Processing
        if filename_lower.endswith(".pdf"):
            try:
                with pdfplumber.open(file_path) as pdf:
                    for page in pdf.pages:
                        extracted = page.extract_text()
                        if extracted:
                            for line in extracted.split("\n"):
                                cleaned = line.strip()
                                if len(cleaned) > 5:
                                    text_chunks.append(f"[{file.filename}] {cleaned}")
            except Exception as e: print(f"[ERROR] PDF: {e}")
                
        # 2. DOCX Processing
        elif filename_lower.endswith(".docx"):
            try:
                doc = docx.Document(file_path)
                for para in doc.paragraphs:
                    cleaned = para.text.strip()
                    if len(cleaned) > 5:
                        text_chunks.append(f"[{file.filename}] {cleaned}")
            except Exception as e: print(f"[ERROR] DOCX: {e}")
                
        # 3. Image OCR Processing (Feature 1)
        elif filename_lower.endswith((".png", ".jpg", ".jpeg")):
            if OCR_AVAILABLE:
                try:
                    img = Image.open(file_path)
                    extracted = pytesseract.image_to_string(img)
                    if extracted:
                        for line in extracted.split("\n"):
                            cleaned = line.strip()
                            if len(cleaned) > 5:
                                text_chunks.append(f"[{file.filename}] {cleaned}")
                except Exception as e: print(f"[ERROR] OCR: {e}")

        if os.path.exists(file_path): os.remove(file_path)
            
    if text_chunks:
        embeddings = embedder.encode(text_chunks).tolist()
        start_id = collection.count()
        ids = [f"chk_{i + start_id}" for i in range(len(text_chunks))]
        
        collection.add(documents=text_chunks, embeddings=embeddings, ids=ids)
        
        # Auto-Summarization
        summary = ""
        try:
            summary_context = "\n".join(text_chunks[:25]) 
            messages = [
                {"role": "system", "content": "You are a data extraction AI. Write a concise 3-sentence summary of the provided text. Use Markdown bolding for key entities."},
                {"role": "user", "content": f"Context:\n{summary_context}\n\nSummary:"}
            ]
            prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
            outputs = model.generate(**inputs, max_new_tokens=150, do_sample=False)
            summary = tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True).strip()
        except Exception as e: pass

        return {
            "status": "success",
            "message": f"Secured & Indexed {len(text_chunks)} data points.",
            "summary": summary
        }
    else:
        raise HTTPException(status_code=400, detail="No extractable text found.")

@app.post("/chat")
async def chat(query: str = Form(...), persona: str = Form("General")):
    if collection.count() == 0:
        return {"answer": "Workspace is empty. Please upload documents to the Knowledge Base.", "sources": [], "follow_ups": []}
        
    query_embed = embedder.encode([query]).tolist()
    k_results = min(20, collection.count())
    results = collection.query(query_embeddings=query_embed, n_results=k_results)
    
    retrieved_docs = results["documents"][0] if results["documents"] else []
    context = "\n".join(retrieved_docs)
    
    # Extract Sources
    sources = set()
    for doc in retrieved_docs:
        match = re.match(r"\[(.*?)\]", doc)
        if match: sources.add(match.group(1))
            
    # Apply Persona
    system_prompt = PERSONAS.get(persona, PERSONAS["General"])
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"DOCUMENT CONTEXT:\n{context}\n\nUSER QUESTION: {query}\n\nProvide your detailed, Markdown-formatted answer below:"}
    ]
    
    prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    
    outputs = model.generate(**inputs, max_new_tokens=400, do_sample=False, pad_token_id=tokenizer.eos_token_id)
    answer = tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True).strip()
    
    # FEATURE 4: Smart Follow-ups Generation
    follow_ups = []
    try:
        fu_messages = [
            {"role": "system", "content": "You are a UX assistant. Read the following answer and generate EXACTLY 3 highly relevant, short follow-up questions the user might ask next. Return ONLY a numbered list (1., 2., 3.) and nothing else."},
            {"role": "user", "content": f"AI Answer:\n{answer[:400]}\n\nGenerate 3 short follow-up questions:"}
        ]
        fu_prompt = tokenizer.apply_chat_template(fu_messages, tokenize=False, add_generation_prompt=True)
        fu_inputs = tokenizer(fu_prompt, return_tensors="pt").to(model.device)
        fu_outputs = model.generate(**fu_inputs, max_new_tokens=100, do_sample=False, pad_token_id=tokenizer.eos_token_id)
        fu_text = tokenizer.decode(fu_outputs[0][fu_inputs.input_ids.shape[1]:], skip_special_tokens=True).strip()
        
        for line in fu_text.split('\n'):
            line = line.strip()
            if re.match(r'^[123]\.', line):
                follow_ups.append(re.sub(r'^\d+\.\s*', '', line).replace('*','').strip())
    except Exception as e: print(f"[ERROR] Follow-ups: {e}")
    
    return {
        "query": query,
        "answer": answer,
        "sources": list(sources),
        "follow_ups": follow_ups[:3]
    }

@app.get("/")
async def health_check():
    return {"status": "online"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
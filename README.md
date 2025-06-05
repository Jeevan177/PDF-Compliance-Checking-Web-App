# 📄 PDF Compliance Checking Web App

A full-stack web application that enables users to upload PDF documents and rule files (text) to automatically perform compliance checking using LLMs and vector search. Built with FastAPI for the backend and Next.js for the frontend. The backend uses LangChain with a Groq-hosted LLM (`deepseek-r1-distill-llama-70b`) to semantically match uploaded compliance rules against the contents of a PDF.

---

## 🚀 Features

### 🔧 Backend Features
- FastAPI with async support
- File upload handling for PDF and text files
- Integrated compliance checking using LLM (LangChain + Groq)
- PDF parsing using LangChain's PDFPlumberLoader
- Vector-based semantic search using FAISS and HuggingFace embeddings
- Proper error handling and logging
- CORS configuration for frontend integration
- Environment variable management via `.env`

### 🎨 Frontend Features
- Next.js with React components
- Drag & drop file upload using `react-dropzone`
- Real-time processing indicators
- Responsive design with Tailwind CSS
- Error handling and user feedback
- Clean display of compliance results

---
## ⚙️ Getting Started

### Backend Setup (FastAPI)

```bash
cd backend
```

### Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

```

### Install dependencies:

```bash
pip install -r requirements.txt

```

### Create a .env file in backend/:

```bash
ALLOWED_ORIGINS=http://localhost:3000
GROQ_API_KEY = your_groq_key_here

```

### Start the FastAPI server:

```bash
uvicorn app.main:app --reload

```

### Frontend Setup (Next.js + Tailwind)
```bash
cd frontend
npm install
npm run dev
```








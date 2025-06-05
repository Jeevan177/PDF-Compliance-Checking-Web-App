# 📄 PDF Compliance Checking Web App

A full-stack web application for automated compliance verification from uploaded PDF and text files. Built with **FastAPI** for a fast and efficient backend and **Next.js + Tailwind CSS** for a responsive frontend, the app provides real-time results, smooth user experience, and modular code structure.

---

## 🚀 Features

### 🛠 Backend (FastAPI)

- ⚡ Asynchronous API using FastAPI
- 📎 File upload support for PDF and text files
- 🧠 Modular compliance logic via service architecture
- ⚠️ Centralized error handling and logging
- 🔐 Environment variable support using `.env`
- 🔗 CORS support for frontend-backend communication

### 🎨 Frontend (Next.js + Tailwind CSS)

- 🧩 Modular React components
- 🗂 Drag & drop file uploads via `react-dropzone`
- ⏳ Loading indicators and real-time feedback
- 💡 Clean UI with Tailwind CSS
- 📱 Fully responsive and mobile-friendly design
- ❗ Error handling with user-friendly feedback

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
GROQ_API_KEY = 

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








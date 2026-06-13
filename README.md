
# 🧠 AI Learning Companion

### *Your AI study buddy that never sleeps.*

> A powerful Chrome Extension that understands any webpage or YouTube video — and teaches it back to you in simple English.

![Chrome Extension](https://img.shields.io/badge/Chrome-Extension-4285F4?style=for-the-badge&logo=googlechrome&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-AI-orange?style=for-the-badge)
![Render](https://img.shields.io/badge/Deployed-Render-46E3B7?style=for-the-badge)

---

## 📌 What is this?

AI Learning Companion is a Chrome Extension powered by **Groq's Llama 3.3 70B** that helps students, developers, and curious minds learn faster.

Whether you're reading a complex article, watching a YouTube tutorial in Hindi or any language — just open the extension and it instantly:
- Explains content in simple English
- Summarizes key points
- Generates a quiz to test you
- Lets you save personal notes
- Tracks your learning progress

**No copy-paste. No switching tabs. Just open and learn.**

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 💡 **Auto Explain** | Opens on any page → instantly explains content. No button click needed. |
| 📝 **Summary** | 3-5 bullet point summary of any content |
| 🧪 **Quiz** | Auto-generated MCQ quiz with score tracking |
| 📚 **Notes** | Save personal notes while learning |
| 📊 **Insights** | Dashboard with learning stats & quiz history |
| 🎬 **YouTube Transcript** | Auto-fetches transcript from ANY YouTube video in ANY language → explains in English |

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Extension Frontend** | React + TypeScript + Vite + Tailwind CSS | Chrome Extension UI |
| **Backend** | Python + FastAPI | REST API server |
| **AI Model** | Groq — Llama 3.3 70B | Explain, Summary, Quiz generation |
| **YouTube** | youtube-transcript-api | Fetch video transcripts |
| **Database** | PostgreSQL + SQLAlchemy | Store notes & quiz results |
| **Rate Limiting** | SlowAPI | Prevent API abuse |
| **Deployment** | Render (Backend) | Live backend hosting |
| **Containerization** | Docker + Docker Compose | Easy local setup |

---

## 📁 Project Structure
ai-learning-companion/

│

├── 📂 backend/                      # Python FastAPI Backend

│   ├── main.py                      # All API endpoints

│   ├── requirements.txt             # Python dependencies

│   ├── Dockerfile                   # Docker config for backend

│   └── .env.example                 # Environment variables template

│

├── 📂 extension/                    # Chrome Extension (React + TS)

│   ├── 📂 src/

│   │   ├── App.tsx                  # Root component — handles YouTube detection

│   │   ├── main.tsx                 # Entry point

│   │   ├── index.css                # Global styles

│   │   │

│   │   ├── 📂 pages/

│   │   │   ├── ExplainPage.tsx      # Auto-explain with AI

│   │   │   ├── SummaryPage.tsx      # Bullet point summary

│   │   │   ├── QuizPage.tsx         # MCQ quiz generator

│   │   │   ├── NotesPage.tsx        # Personal notes manager

│   │   │   └── DashboardPage.tsx    # Learning insights & stats

│   │   │

│   │   ├── 📂 components/

│   │   │   └── Navbar.tsx           # Tab navigation

│   │   │

│   │   ├── 📂 background/

│   │   │   └── index.ts             # Chrome service worker

│   │   │

│   │   ├── 📂 content/

│   │   │   └── index.ts             # Content script — captures selected text

│   │   │

│   │   ├── 📂 utils/

│   │   │   └── speech.ts            # Text-to-speech utility

│   │   │

│   │   └── 📂 types/

│   │       └── index.ts             # TypeScript type definitions

│   │

│   ├── 📂 public/

│   │   ├── manifest.json            # Chrome Extension manifest v3

│   │   ├── favicon.svg              # Extension favicon

│   │   └── icons.svg                # Extension icons

│   │

│   ├── package.json

│   ├── vite.config.ts

│   ├── tailwind.config.js

│   ├── tsconfig.json

│   └── Dockerfile

│

├── docker-compose.yml               # Run entire stack with one command

├── .gitignore

└── README.md

---

## ⚙️ API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check |
| `POST` | `/api/explain` | Explain selected text |
| `POST` | `/api/summary` | Summarize text |
| `POST` | `/api/quiz` | Generate MCQ quiz |
| `POST` | `/api/quiz/result` | Save quiz score |
| `GET` | `/api/quiz/results` | Get quiz history |
| `POST` | `/api/notes` | Save a note |
| `GET` | `/api/notes` | Get all notes |
| `DELETE` | `/api/notes/{id}` | Delete a note |
| `GET` | `/api/dashboard` | Get learning stats |
| `POST` | `/api/transcript` | Fetch YouTube transcript |

---

## 🚀 Getting Started

### Prerequisites
- Node.js 18+
- Python 3.10+
- PostgreSQL
- Groq API Key — [Get free here](https://console.groq.com)

---

### 1️⃣ Clone the repo
```bash
git clone https://github.com/sandhyacgu/ai-learning-companion.git
cd ai-learning-companion
```

---

### 2️⃣ Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

Create `.env` file inside `/backend`:
```env
GROQ_API_KEY=your_groq_api_key_here
DATABASE_URL=postgresql://user:password@localhost/dbname
```

Start the backend:
```bash
uvicorn main:app --reload --port 8000
```

Backend running at: `http://localhost:8000`

---

### 3️⃣ Extension Setup
```bash
cd extension

# Install dependencies
npm install

# Build the extension
npm run build
```

---

### 4️⃣ Load Extension in Chrome
1. Open `chrome://extensions/`
2. Enable **Developer mode** (top right toggle)
3. Click **Load unpacked**
4. Select the `extension/dist` folder
5. Pin the extension to toolbar

---

### 5️⃣ Docker Setup (Optional)
Run everything with one command:
```bash
docker-compose up --build
```

---

## 🎬 How to Use

### 📄 On any Webpage
1. Select any text on a webpage
2. Click the **AI Learning Companion** icon
3. ✅ Explanation appears automatically — no button click needed!
4. Switch to **Summary**, **Quiz**, or **Notes** tabs

### 🎥 On YouTube
1. Open any YouTube video
2. Click the extension icon
3. ✅ Transcript is auto-fetched — works in ANY language!
4. All features work on the video transcript

---

## 🌐 Live Demo

| Service | URL |
|---------|-----|
| **Backend API** | https://ai-learning-companion-1-w3hw.onrender.com |
| **API Docs** | https://ai-learning-companion-1-w3hw.onrender.com/docs |

> ⚠️ Free tier — first request may take ~50 seconds to wake up.

---

## 🔒 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GROQ_API_KEY` | Groq API key for LLM | ✅ Yes |
| `DATABASE_URL` | PostgreSQL connection URL | ✅ Yes |

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repo
2. Create your branch: `git checkout -b feature/amazing-feature`
3. Commit: `git commit -m 'feat: add amazing feature'`
4. Push: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

## 📄 License

MIT.

---

<div align="center">

Made with 💜 by [Sandhya](https://github.com/sandhyacgu)

*Learn smarter. Not harder.*

</div>
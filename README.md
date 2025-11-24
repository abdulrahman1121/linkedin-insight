# LinkedInsight

AI-powered career and skills navigator that helps professionals discover learning paths, understand skill relationships, and generate personalized roadmaps.

## 🚀 Features

### 1. **Skill Graph Explorer**
- Explore skill relationships and prerequisites
- View learning paths to acquire target skills
- Discover related skills (prerequisites and successors)
- Case-insensitive skill search with autocomplete
- Browse all available skills in the graph

### 2. **AI Roadmap Generator**
- Generate personalized 4-week learning roadmaps
- Get structured weekly objectives, resources, and practice projects
- Support for multiple skills simultaneously
- Markdown-formatted, actionable learning plans

### 3. **Skill Gap Analysis**
- Understand why missing skills are important
- See how skills connect to your current knowledge
- Get career path insights and recommendations

### 4. **Dashboard**
- System status monitoring
- Quick access to all features
- Recent activity tracking

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **OpenAI API** - For embeddings and LLM-powered roadmaps
- **ChromaDB** - Vector database for semantic search
- **NetworkX** - Skills graph management
- **SQLAlchemy** - SQL database ORM
- **SQLite** - Lightweight database
- **SpaCy** - NLP for skill extraction
- **BeautifulSoup4** - Web scraping

### Frontend
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first styling
- **shadcn/ui** - Reusable UI components
- **React Query** - Data fetching and caching
- **Axios** - HTTP client
- **Lucide React** - Icon library

## 📁 Project Structure

```
LinkedinInsight/
├── app/                          # Backend FastAPI application
│   ├── main.py                  # FastAPI app entry point
│   ├── core/                    # Core business logic
│   │   ├── embeddings.py        # OpenAI embeddings service
│   │   ├── graph.py             # Skills graph engine (NetworkX)
│   │   ├── llm.py               # LLM reasoning engine
│   │   └── pipeline.py          # Job data ingestion pipeline
│   ├── db/                      # Database layer
│   │   ├── models.py            # SQLAlchemy models
│   │   ├── sql.py               # SQL database setup
│   │   └── vector_store.py      # ChromaDB vector store
│   └── routers/                 # API routers
│       ├── ai.py                # AI endpoints (roadmaps, skill gaps)
│       ├── skills.py            # Skills graph endpoints
│       └── jobs.py              # Job-related endpoints
├── linkedinsight-frontend/       # Next.js frontend
│   ├── app/                     # Next.js app directory
│   │   ├── api/                 # API client services
│   │   ├── components/          # React components
│   │   ├── dashboard/           # Dashboard page
│   │   ├── roadmap/             # AI Roadmap Generator
│   │   └── skill-graph/         # Skill Graph Explorer
│   └── components/ui/           # shadcn/ui components
├── linkedinsight.db             # SQLite database
└── venv/                        # Python virtual environment
```

## 🚦 Getting Started

### Prerequisites
- Python 3.8+
- Node.js 18+
- OpenAI API key

### Backend Setup

1. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # Windows
   # or
   source venv/bin/activate      # Mac/Linux
   ```

2. **Install dependencies:**
   ```bash
   pip install fastapi uvicorn pydantic openai chromadb networkx pandas beautifulsoup4 requests spacy python-dotenv sqlalchemy
   ```

3. **Download spaCy model:**
   ```bash
   python -m spacy download en_core_web_sm
   ```

4. **Create `.env` file in root directory:**
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

5. **Start the backend server:**
   ```bash
   uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload
   ```

   The server will:
   - Initialize the SQLite database
   - Seed the skills graph with 34+ skills and relationships
   - Be available at `http://127.0.0.1:8001`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd linkedinsight-frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Create `.env.local` file:**
   ```
   NEXT_PUBLIC_API_URL=http://127.0.0.1:8001
   ```

4. **Start the development server:**
   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:3000`


## 🐛 Troubleshooting

### Backend not connecting
- Ensure backend is running on port 8001
- Check `.env.local` has correct `NEXT_PUBLIC_API_URL`
- Restart frontend after changing environment variables

### Skills not showing
- Verify backend server started successfully (check for seeding message)
- Try case-insensitive search (e.g., "python" matches "Python")
- Check browser console for API errors

### Roadmap generation slow
- OpenAI API calls may take 10-20 seconds
- Check your OpenAI API key is valid
- Ensure you have API credits


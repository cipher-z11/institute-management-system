# 🏫 Institute Management System — Backend API

A production-ready backend system for managing students, courses, faculty, and fee records — with an AI-powered natural language query layer built using LangChain + RAG.

## Tech Stack

| Layer | Tech |
|---|---|
| API Framework | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| AI / NLP | LangChain, RAG, ChromaDB |
| Embeddings | OpenAI Embeddings |
| Validation | Pydantic v2 |

## Features

- ✅ Full CRUD for Students, Courses, Faculty, Fees
- ✅ RAG-based natural language querying over DB records
- ✅ Optimized SQLAlchemy ORM schemas with relationships
- ✅ Input validation and error handling via Pydantic
- ✅ Auto-generated Swagger docs at `/docs`
- ✅ CORS enabled for frontend integration

## Project Structure

```
institute-management-system/
├── main.py                    # FastAPI app entry point
├── app/
│   ├── database.py            # DB connection & session
│   ├── core/config.py         # App settings (pydantic-settings)
│   ├── models/models.py       # SQLAlchemy ORM models
│   ├── schemas/schemas.py     # Pydantic request/response schemas
│   ├── routes/
│   │   ├── students.py
│   │   ├── courses.py
│   │   ├── faculty.py
│   │   ├── fees.py
│   │   └── rag.py             # AI natural language query endpoint
│   └── services/
│       └── rag_service.py     # LangChain + ChromaDB RAG logic
├── requirements.txt
└── .env.example
```

## Setup

```bash
# 1. Clone and enter project
git clone <repo-url>
cd institute-management-system

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup environment variables
cp .env.example .env
# Edit .env with your DB credentials and OpenAI API key

# 5. Create PostgreSQL database
createdb institute_db

# 6. Run the server
uvicorn main:app --reload
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/students/` | Add new student |
| GET | `/api/v1/students/` | List all students |
| GET | `/api/v1/students/{id}` | Get student by ID |
| PUT | `/api/v1/students/{id}` | Update student |
| DELETE | `/api/v1/students/{id}` | Delete student |
| POST | `/api/v1/courses/` | Add new course |
| GET | `/api/v1/courses/` | List all courses |
| POST | `/api/v1/faculty/` | Add faculty |
| GET | `/api/v1/faculty/` | List faculty |
| POST | `/api/v1/fees/` | Create fee record |
| PUT | `/api/v1/fees/{id}/pay` | Update payment |
| GET | `/api/v1/fees/pending` | Get unpaid fees |
| POST | `/api/v1/query/` | AI natural language query |

### Example AI Query

```json
POST /api/v1/query/
{
  "question": "How many students are enrolled in the Computer Science course?"
}
```

Response:
```json
{
  "question": "How many students are enrolled in the Computer Science course?",
  "answer": "There are 45 students currently enrolled in the Computer Science course.",
  "sources": ["student", "course"]
}
```

## API Documentation

Visit `http://localhost:8000/docs` for interactive Swagger UI.

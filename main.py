from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import students, courses, faculty, fees, rag
from app.core.config import settings
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Institute Management System",
    description="Backend API for managing students, courses, faculty, and fees with AI-powered querying.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(students.router, prefix="/api/v1/students", tags=["Students"])
app.include_router(courses.router, prefix="/api/v1/courses", tags=["Courses"])
app.include_router(faculty.router, prefix="/api/v1/faculty", tags=["Faculty"])
app.include_router(fees.router, prefix="/api/v1/fees", tags=["Fees"])
app.include_router(rag.router, prefix="/api/v1/query", tags=["AI Query"])


@app.get("/", tags=["Health"])
def root():
    return {"message": "Institute Management System API is running", "version": "1.0.0"}


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}

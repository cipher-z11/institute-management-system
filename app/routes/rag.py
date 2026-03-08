from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.schemas import QueryRequest, QueryResponse
from app.services.rag_service import get_rag_answer

router = APIRouter()


@router.post("/", response_model=QueryResponse)
def query_institute_data(request: QueryRequest, db: Session = Depends(get_db)):
    """
    Ask natural language questions about institute data.
    Example: "How many students are in the CS department?"
    """
    result = get_rag_answer(request.question, db)
    return result

# Add Faculty and Fee models

# Implement natural language query endpoint

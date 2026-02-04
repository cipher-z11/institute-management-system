# fix: add Student and Course models
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from sqlalchemy.orm import Session
from app.models.models import Student, Course, Faculty, Fee
from app.core.config import settings
import os

CHROMA_COLLECTION = "institute_data"


def build_documents_from_db(db: Session) -> list[Document]:
    """Convert DB records to LangChain documents for RAG indexing."""
    docs = []

    students = db.query(Student).all()
    for s in students:
        content = (
            f"Student: {s.name}, Email: {s.email}, "
            f"Enrollment: {s.enrollment_number}, Course ID: {s.course_id}"
        )
        docs.append(Document(page_content=content, metadata={"type": "student", "id": s.id}))

    courses = db.query(Course).all()
    for c in courses:
        content = (
            f"Course: {c.name}, Code: {c.code}, Department: {c.department}, "
            f"Duration: {c.duration_years} years, Total Seats: {c.total_seats}"
        )
        docs.append(Document(page_content=content, metadata={"type": "course", "id": c.id}))

    faculty_list = db.query(Faculty).all()
    for f in faculty_list:
        content = (
            f"Faculty: {f.name}, Email: {f.email}, Department: {f.department}, "
            f"Designation: {f.designation}, Experience: {f.experience_years} years"
        )
        docs.append(Document(page_content=content, metadata={"type": "faculty", "id": f.id}))

    fees = db.query(Fee).all()
    for fee in fees:
        content = (
            f"Fee record for student ID {fee.student_id}: Semester {fee.semester}, "
            f"Due: {fee.amount_due}, Paid: {fee.amount_paid}, Status: {fee.status.value}"
        )
        docs.append(Document(page_content=content, metadata={"type": "fee", "id": fee.id}))

    return docs


def get_vectorstore(db: Session) -> Chroma:
    embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)
    persist_dir = settings.CHROMA_PERSIST_DIR

    # Rebuild vectorstore with fresh DB data
    documents = build_documents_from_db(db)
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    splits = splitter.split_documents(documents)

    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory=persist_dir,
        collection_name=CHROMA_COLLECTION,
    )
    return vectorstore


def get_rag_answer(question: str, db: Session) -> dict:
    try:
        vectorstore = get_vectorstore(db)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0,
            openai_api_key=settings.OPENAI_API_KEY
        )

        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
        )

        result = qa_chain.invoke({"query": question})
        sources = [doc.metadata.get("type", "unknown") for doc in result.get("source_documents", [])]

        return {
            "question": question,
            "answer": result["result"],
            "sources": list(set(sources)),
        }
    except Exception as e:
        return {
            "question": question,
            "answer": f"Error processing query: {str(e)}",
            "sources": [],
        }

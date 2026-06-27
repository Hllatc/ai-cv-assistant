from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from app.services.cv_parser import extract_text_from_pdf
from app.services.embedding_service import get_embedding
from app.services.job_matcher import compute_similarity
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.models.cv import CV
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.cv_vector_service import store_cv_chunks


from app.db.vector_store import client
from app.services.llm_service import generate_with_qwen

router = APIRouter()

cv_storage = {}

@router.post("/upload-cv")
async def upload_cv(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    content = await file.read()

    text = extract_text_from_pdf(content)

    # PostgreSQL
    cv = CV(
        filename=file.filename,
        raw_text=text,
        user_id=current_user.id
    )

    db.add(cv)
    db.commit()
    db.refresh(cv)

    #  QDRANT section
    chunk_count = store_cv_chunks(current_user.id, text)

    return {
        "message": "CV uploaded",
        "cv_id": cv.id,
        "chunks_stored": chunk_count
    }

@router.post("/match-job")
def match_job(
    job_description: str,
    current_user: User = Depends(get_current_user)
):

    cv = cv_storage.get(current_user.id)

    if not cv:
        raise HTTPException(status_code=404, detail="No CV uploaded")

    score = compute_similarity(
        cv["embedding"],
        get_embedding(job_description)
    )

    return {
        "match_score": round(score, 2)
    }

from app.services.llm_service import generate_with_qwen
@router.post("/analyze-job")
def analyze_job(
    job_description: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cv = db.query(CV).filter(CV.user_id == current_user.id).first()

    if not cv:
        raise HTTPException(status_code=404, detail="No CV found")
    
    job_embedding = get_embedding(job_description)

    results = client.search(
        collection_name="cv_chunks",
        query_vector=job_embedding,
        limit=5
    )
    context = "\n".join([
        r.payload["text"] for r in results
    ])

    prompt = f"""
    You are an expert ATS system.

    Analyze the candidate based on CV context and job description.

    Return ONLY JSON:

    {{
    "match_score": 0-100,
    "strengths": [],
    "missing_skills": [],
    "recommendation": "",
    "explanation": ""
    }}

    CV CONTEXT:
    {context}

    JOB DESCRIPTION:
    {job_description}
    """

    analysis = generate_with_qwen(prompt)
    
    return {
        "analysis": analysis
    }
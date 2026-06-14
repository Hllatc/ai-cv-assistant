from fastapi import APIRouter, UploadFile, File
from app.services.cv_parser import extract_text_from_pdf
from app.services.embedding_service import get_embedding
from app.services.job_matcher import compute_similarity

router = APIRouter()

cv_storage = {}

@router.post("/upload-cv")
async def upload_cv(file: UploadFile = File(...)):
    content = await file.read()

    text = extract_text_from_pdf(content)

    embedding = get_embedding(text)

    cv_storage["cv"] = {
        "text": text,
        "embedding": embedding
    }

    return {
        "message": "CV uploaded successfully",
        "length": len(text)
    }


@router.post("/match-job")
def match_job(job_description: str):

    cv = cv_storage.get("cv")

    if not cv:
        return {"error": "No CV uploaded"}

    score = compute_similarity(
        cv["embedding"],
        get_embedding(job_description)
    )

    return {
        "match_score": round(score, 2)
    }
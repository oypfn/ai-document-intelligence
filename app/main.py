from io import BytesIO
from fastapi import FastAPI, File, HTTPException, UploadFile
from pypdf import PdfReader

app = FastAPI(title="Document Intelligence API", version="0.1.0")
MAX_FILE_BYTES = 10 * 1024 * 1024
ALLOWED_TYPES = {"application/pdf"}

@app.get("/health", tags=["operations"])
def health() -> dict[str, str]:
    return {"status": "ok", "service": "document-intelligence"}

@app.post("/api/v1/documents/extract", tags=["documents"])
async def extract_document(file: UploadFile = File(...)  # noqa: B008) -> dict[str, object]:
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=415, detail="Only PDF documents are supported.")
    content = await file.read(MAX_FILE_BYTES + 1)
    if len(content) > MAX_FILE_BYTES:
        raise HTTPException(status_code=413, detail="File exceeds the 10 MB limit.")
    if not content.startswith(b"%PDF-"):
        raise HTTPException(status_code=400, detail="The uploaded file is not a valid PDF.")
    try:
        reader = PdfReader(BytesIO(content), strict=True)
        if reader.is_encrypted:
            raise HTTPException(status_code=422, detail="Password-protected PDFs are not supported.")
        pages = [page.extract_text() or "" for page in reader.pages]
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=422, detail="The PDF could not be parsed.") from exc
    return {"filename": file.filename or "document.pdf", "page_count": len(pages),
            "text": "\n\n".join(pages), "status": "extracted"}

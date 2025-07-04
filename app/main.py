# app/main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.models.pipeline import InvoicePipeline
from app.models.schemas import InvoiceOutput
import uvicorn

app = FastAPI(title="AI Invoice Extraction System")

pipeline = InvoicePipeline()

@app.post("/extract", response_model=InvoiceOutput)
async def extract_invoice(file: UploadFile = File(...)):
    try:
        content = await file.read()
        result = pipeline.process_document(content, file.filename)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
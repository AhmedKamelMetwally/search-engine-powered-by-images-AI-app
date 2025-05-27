from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from app.captioning import caption_image
from app.search import web_search
from app.summarizer import summarize_text
from app.models import load_models
import shutil
import os

app = FastAPI()
model, processor, tokenizer, device, summarizer = load_models()

@app.post("/process/")
async def process_image(file: UploadFile = File(...)):
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        caption = caption_image(temp_path, model, processor, tokenizer, device)
        results = web_search(caption)
        combined = " ".join(r.get("body", "") for r in results)
        summary = summarize_text(combined, summarizer)
    finally:
        os.remove(temp_path)

    return JSONResponse(content={
        "caption": caption,
        "results": results,
        "summary": summary
    })

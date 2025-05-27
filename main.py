from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from models import generate_caption, summarize_text, web_search

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/process/")
async def process_image(file: UploadFile = File(...)):
    image_bytes = await file.read()
    caption = generate_caption(image_bytes)
    results = web_search(caption)
    combined_text = " ".join(item.get("body", "") for item in results if item.get("body"))
    summary = summarize_text(combined_text)
    return {
        "caption": caption,
        "search_results": results,
        "summary": summary
    }


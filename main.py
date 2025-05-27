from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from io import BytesIO
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer, pipeline
import torch

app = FastAPI()

# Enable CORS for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load models at startup
model_name = "nlpconnect/vit-gpt2-image-captioning"
caption_model = VisionEncoderDecoderModel.from_pretrained(model_name)
processor = ViTImageProcessor.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
caption_model.to(device)

summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

@app.post("/process/")
async def process_image(file: UploadFile = File(...)):
    
    image = Image.open(BytesIO(await file.read())).convert("RGB")
    image = image.resize((512, 512))
    pixel_values = processor(images=image, return_tensors="pt").pixel_values.to(device)
    

    output_ids = caption_model.generate(pixel_values, max_length=12, num_beams=3)
    caption = tokenizer.decode(output_ids[0], skip_special_tokens=True)

    
    summary = summarizer(caption, max_length=40, min_length=5, do_sample=False)[0]["summary_text"]

    return {"caption": caption, "summary": summary}


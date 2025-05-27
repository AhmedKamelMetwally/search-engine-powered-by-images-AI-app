from PIL import Image
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer, pipeline
import torch
from io import BytesIO

# For web search
try:
    from duckduckgo_search import DDGS
    USE_DDGS = True
except ImportError:
    from duckduckgo_search import ddg
    USE_DDGS = False

model_name = "nlpconnect/vit-gpt2-image-captioning"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

caption_model = VisionEncoderDecoderModel.from_pretrained(model_name).to(device)
processor = ViTImageProcessor.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def generate_caption(image_bytes: bytes) -> str:
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    image = image.resize((512, 512))
    pixel_values = processor(images=image, return_tensors="pt").pixel_values.to(device)
    output_ids = caption_model.generate(pixel_values, max_length=12, num_beams=3)
    caption = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return caption

def web_search(query: str, max_results: int = 5):
    try:
        if USE_DDGS:
            with DDGS() as ddgs:
                results = ddgs.text(query, max_results=max_results)
        else:
            results = ddg(query, max_results=max_results)
        return results or []
    except Exception as e:
        return [{"title": "Search Error", "body": str(e), "href": "#"}]

def summarize_text(text: str) -> str:
    if not text.strip():
        return "No text to summarize."
    result = summarizer(text, max_length=40, min_length=5, do_sample=False)
    return result[0]["summary_text"]

 Image-to-Search AI App – Built with FastAPI, Streamlit, Docker, and Transformers



🔧 What I built:
A search engine powered by images – just upload a photo, and the app:

📸 Captions it using a vision-language transformer (ViT-GPT2)

🌐 Searches the web based on the caption (via DuckDuckGo)

✨ Summarizes the top results using a BART-based summarizer

💡 Tech Stack:

FastAPI: Backend API for model inference & logic

Streamlit: Frontend for user interaction

Docker: For containerizing both frontend & backend

Google Colab: Leveraged GPU to speed up image captioning during development and testing

ngrok: To expose the local Streamlit app securely and easily during development

Transformers (Hugging Face): Used nlpconnect/vit-gpt2-image-captioning and distilbart-cnn-12-6

🏗️ Built it with modularity and deployment in mind – full backend API, frontend UI, and Docker support.

📦 Project includes:

Image upload via frontend

Real-time API communication

Automatic captioning + summarization

Search result visualization

💻 Deployed and tested it using Google Colab for GPU acceleration, exposed with ngrok for public access, and containerized everything with Docker for easy deployment.

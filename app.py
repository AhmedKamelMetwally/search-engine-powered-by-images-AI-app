import streamlit as st
import requests

st.title(" search engine by image by Ahmed Kamel")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image_path = "temp.jpg"
    with open(image_path, "wb") as f:
        f.write(uploaded_file.read())

    st.image(image_path, caption="Uploaded Image", use_column_width=True)

    if st.button("search"):
        with st.spinner("Processing..."):
            model, processor, tokenizer, device = load_caption_model()
            summarizer = load_summarizer()

            caption = caption_image(image_path, model, processor, tokenizer, device)
            results = web_search(caption)
            combined_text = " ".join(item.get("body", "") for item in results if item.get("body"))
            summary = summarize_text(combined_text, summarizer)

        st.subheader("🖼️ Caption")
        st.write(caption)

        st.subheader("🔍 Web Search Results")
        for item in results:
            st.markdown(f"**{item.get('title', 'No Title')}**\n\n{item.get('body', '')}\n\n[Link]({item.get('href', '#')})")

        st.subheader("📝 Summary")
        st.write(summary)

        os.remove(image_path)

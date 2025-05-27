import streamlit as st
import requests

st.title("🔍 Image Search Engine by Ahmed Kamel")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
if uploaded_file and st.button("Search"):
    with st.spinner("Processing..."):
        files = {'file': uploaded_file.getvalue()}
        response = requests.post("http://backend:8000/process/", files={'file': uploaded_file})
        data = response.json()

    st.subheader("🖼️ Caption")
    st.write(data["caption"])

    st.subheader("🔍 Web Search Results")
    for item in data["results"]:
        st.markdown(f"**{item.get('title', 'No Title')}**\n\n{item.get('body', '')}\n\n[Link]({item.get('href', '#')})")

    st.subheader("📝 Summary")
    st.write(data["summary"])

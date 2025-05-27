import subprocess
import time
from pyngrok import ngrok
import os

NGROK_AUTHTOKEN = os.getenv("NGROK_AUTHTOKEN")
if not NGROK_AUTHTOKEN:
    raise ValueError("Please set NGROK_AUTHTOKEN environment variable")

ngrok.set_auth_token(NGROK_AUTHTOKEN)

streamlit_process = subprocess.Popen(["streamlit", "run", "app.py", "--server.port", "8501"])

time.sleep(5)  # wait for Streamlit to start

public_url = ngrok.connect(8501)
print(f"🔗 Your Streamlit app is live at: {public_url}")

streamlit_process.wait()

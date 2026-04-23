import os
import re
import datetime
import requests
import speech_recognition as sr

class DownloaderAgent:
    def __init__(self, download_dir="./downloads", log_file="download_log.txt"):
        self.download_dir = os.path.abspath(download_dir)
        self.log_file = log_file
        os.makedirs(self.download_dir, exist_ok=True)

    def extract_urls(self, user_input):
        url_pattern = r'(https?://\S+)'
        return re.findall(url_pattern, user_input)

    def log_download(self, url, status):
        with open(self.log_file, "a", encoding="utf-8") as f:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] {status} - {url}\n")

    def download_file(self, url):
        try:
            print(f"📥 Downloading: {url}")
            filename = os.path.join(self.download_dir, url.split("/")[-1])
            response = requests.get(url, stream=True, timeout=10)
            response.raise_for_status()

            with open(filename, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            status = "✅ Success"
        except Exception as e:
            status = f"❌ Failed: {e}"
        self.log_download(url, status)
        return status

    def voice_input(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("🎤 Speak the download URL:")
            audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio)
                print(f"🗣 You said: {text}")
                return text
            except sr.UnknownValueError:
                print("❌ Could not understand audio.")
            except sr.RequestError as e:
                print(f"⚠ API error: {e}")
        return ""

    def handle(self, user_input=None, use_voice=False):
        if use_voice:
            user_input = self.voice_input()

        if not user_input:
            print("❌ No input provided.")
            return

        urls = self.extract_urls(user_input)
        if not urls:
            print("❌ No valid URL found in your input.")
            return

        if len(urls) == 1:
            print(self.download_file(urls[0]))
        else:
            for url in urls:
                print(self.download_file(url))
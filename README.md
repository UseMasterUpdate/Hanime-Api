# Hanime.tv Stream Extractor API

Unofficial Hanime.tv stream extractor API built with FastAPI. Extracts HLS stream URLs and video metadata directly from hanime.tv.

## Requirements
- Python 3.10+
- Node.js (for credential generation)

## Installation
```bash
pip install -r requirements.txt
uvicorn api:app --host 0.0.0.0 --port 8000
```

## API Usage

### Extract Stream
```
GET /extract?url=https://hanime.tv/videos/hentai/SLUG
```

### Response
```json
{
  "slug": "sister-breeder-1",
  "hv_id": "12345",
  "best": "https://....m3u8",
  "streams": [
    { "url": "...", "filename": "...", "resolution": "1920x1080", "height": 1080 },
    { "url": "...", "filename": "...", "resolution": "1280x720", "height": 720 }
  ]
}
```

---

## 🚀 Deploy

<details>
<summary>▶️ Railway</summary>

1. Push code to GitHub
2. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub
3. Add `Procfile`:
```
web: uvicorn api:app --host 0.0.0.0 --port $PORT
```
4. Deploy — Railway gives you a free subdomain instantly

</details>

<details>
<summary>▶️ Render</summary>

1. Push code to GitHub
2. Go to [render.com](https://render.com) → New Web Service → Connect GitHub
3. Set Build Command:
```
pip install -r requirements.txt && apt-get install -y nodejs
```
4. Set Start Command:
```
uvicorn api:app --host 0.0.0.0 --port $PORT
```
5. Deploy

</details>

<details>
<summary>▶️ Koyeb</summary>

1. Push code to GitHub
2. Go to [koyeb.com](https://koyeb.com) → Create App → GitHub
3. Add `Dockerfile`:
```dockerfile
FROM python:3.11-slim
RUN apt-get update && apt-get install -y nodejs
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```
4. Deploy

</details>

<details>
<summary>▶️ Hugging Face Spaces</summary>

1. Go to [huggingface.co/spaces](https://huggingface.co/spaces) → New Space
2. Select **Docker** as SDK
3. Push code with `Dockerfile`:
```dockerfile
FROM python:3.11-slim
RUN apt-get update && apt-get install -y nodejs
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "7860"]
```
4. Access at `https://huggingface.co/spaces/USERNAME/SPACE`

</details>

---

## Dockerfile
```dockerfile
FROM python:3.11-slim
RUN apt-get update && apt-get install -y nodejs
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "7860"]
```

## 🗒️ Disclaimer
This project is for educational purposes only. Not affiliated with hanime.tv.

---

## 💳 Credits

- 👨‍💻 Developer: [Anonymous](https://t.me/User_master_support_bot)
- 📢 Telegram Channel: [use master update](https://t.me/UseMasterUpdate)
- 📌 Report Issues to Developer or open a GitHub Issue

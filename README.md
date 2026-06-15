# Hanime.tv Stream Extractor API
🔞 Unofficial Hanime.tv stream extractor API built with FastAPI. Extracts HLS stream URLs and video metadata directly from hanime.tv. Returns all available stream qualities sorted by resolution. Built for automation and bot integration. Self-hostable on any cloud platform. 

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
GET /hanime-api?url=https://hanime.tv/videos/hentai/SLUG
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

## Deploy

### Railway
1. Push to GitHub
2. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub
3. Add `Procfile`: `web: uvicorn api:app --host 0.0.0.0 --port $PORT`

### Render
1. Push to GitHub
2. Go to [render.com](https://render.com) → New Web Service
3. Build command: `pip install -r requirements.txt && apt-get install -y nodejs`
4. Start command: `uvicorn api:app --host 0.0.0.0 --port $PORT`

### Koyeb
1. Push to GitHub
2. Go to [koyeb.com](https://koyeb.com) → New App → Deploy from GitHub
3. Use the provided `Dockerfile`

### Hugging Face Spaces
1. Go to [huggingface.co](https://huggingface.co)
2. Create a new Space → Select Docker SDK
3. Push code with `Dockerfile`
4. Access via `https://huggingface.co/spaces/USERNAME/SPACE`

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

## Disclaimer
This project is for educational purposes only. Not affiliated with hanime.tv.

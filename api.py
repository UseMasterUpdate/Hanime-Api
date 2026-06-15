from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
import requests, subprocess, re, sys, tempfile, os, hashlib, time

app = FastAPI()

BASE = "https://cached.freeanimehentai.net/api/v8"
UA = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36"

BASE_HEADERS = {
    "User-Agent": UA,
    "Referer": "https://hanime.tv/",
    "Origin": "https://hanime.tv",
    "Accept": "application/json",
    "Content-Type": "application/json",
    "X-Csrf-Token": "",
    "X-License": "",
    "X-Session-Token": "",
    "X-User-License": "",
}

JS_PREAMBLE = """
delete globalThis.process;

var window = new Proxy({
    top: { location: { origin: "https://hanime.tv" } },
    addEventListener: (e, cb) => {}
}, {
    set(o, k, v) {
        if (k == "ssignature" || k == "stime")
            console.log(k, v);
        o[k] = v;
        return true;
    }
});

globalThis.window = window;
"""

_vendor_script_cache = None


def make_headers(path: str) -> dict:
    t = int(time.time())
    sig = hashlib.sha1(f"{path}{t}".encode()).hexdigest()
    return {**BASE_HEADERS, "X-Signature-Version": "web2", "X-Time": str(t), "X-Signature": sig}


def get_hv_id(slug: str):
    r = requests.get(f"{BASE}/video", params={"id": slug}, headers=make_headers("/api/v8/video"))
    if r.status_code == 200:
        data = r.json()
        hv = data.get("hentai_video", data)
        vid = hv.get("id") or hv.get("hv_id")
        return str(vid) if vid else None
    return None


def get_vendor_script():
    global _vendor_script_cache
    if _vendor_script_cache:
        return _vendor_script_cache
    r = requests.get("https://hanime.tv/", headers={"User-Agent": UA, "Accept": "text/html"})
    match = re.search(r'src="(https://hanime-cdn\.com/js/vendor\.[^"]+)"', r.text)
    if not match:
        return None
    r2 = requests.get(match.group(1), headers={"User-Agent": UA, "Referer": "https://hanime.tv/"})
    _vendor_script_cache = r2.text
    return _vendor_script_cache


def generate_credentials():
    vendor_js = get_vendor_script()
    if not vendor_js:
        return None, None
    script = JS_PREAMBLE + "\n" + vendor_js
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
            f.write(script)
            tmp_path = f.name
        result = subprocess.run(["node", tmp_path], capture_output=True, text=True, timeout=15)
        creds = {}
        for line in result.stdout.strip().split("\n"):
            parts = line.split(" ", 1)
            if len(parts) == 2:
                creds[parts[0]] = parts[1].strip()
        sig = creds.get("ssignature")
        t = creds.get("stime")
        return (sig, t) if sig and t else (None, None)
    except Exception:
        return None, None
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)


def get_streams(hv_id: str, sig: str, t: str) -> list:
    r = requests.get(
        f"https://h.freeanimehentai.net/api/v8/guest/videos/{hv_id}/manifest",
        headers={**BASE_HEADERS, "X-Signature": sig, "X-Signature-Version": "web2", "X-Time": t}
    )
    if r.status_code != 200:
        return []
    data = r.json()
    results = []
    try:
        for server in data["videos_manifest"]["servers"]:
            for stream in server.get("streams", []):
                url = stream.get("url", "")
                if url and url.startswith("https://"):
                    results.append({
                        "url": url,
                        "filename": stream.get("filename", ""),
                        "resolution": f"{stream.get('width', 0)}x{stream.get('height', 0)}",
                        "height": stream.get("height", 0),
                    })
    except (KeyError, TypeError):
        pass
    results.sort(key=lambda x: x["height"], reverse=True)
    return results


@app.get("/hanime-api")
def extract(url: str = Query(..., description="Hanime video URL")):
    if not url.startswith("http"):
        raise HTTPException(status_code=400, detail="Invalid URL")

    slug = url.rstrip("/").split("/")[-1]

    hv_id = get_hv_id(slug)
    if not hv_id:
        raise HTTPException(status_code=502, detail="Failed to resolve hv_id")

    sig, t = generate_credentials()
    if not sig or not t:
        raise HTTPException(status_code=502, detail="Failed to generate credentials")

    streams = get_streams(hv_id, sig, t)
    if not streams:
        raise HTTPException(status_code=404, detail="No streams found")

    return JSONResponse({
        "slug": slug,
        "hv_id": hv_id,
        "best": streams[0]["url"],
        "streams": streams
    })

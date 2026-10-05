#!/usr/bin/env python3
"""Render the three.js timeline to video (no audio).
  python3 render.py test 1.0,5.2,9.8      -> test/tNN.jpg stills (for contact sheets)
  python3 render.py full [--fps 30] [--chunk 20]   -> chunks/cNNN.mp4 then video.mp4
Frames are grabbed from the WebGL canvas (toDataURL) and piped straight into ffmpeg.
Chunks of N seconds make long renders resumable: finished chunks are skipped on rerun.
Run long renders in the background: nohup python3 render.py full > render.log 2>&1 &"""
import asyncio, sys, os, base64, subprocess, glob, time
from playwright.async_api import async_playwright
PORT = int(os.environ.get("ZPORT", "8790"))
ARGS = ["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"]

def ensure_server():
    import urllib.request
    try: urllib.request.urlopen(f"http://localhost:{PORT}/index.html", timeout=2); return
    except Exception: pass
    subprocess.Popen([sys.executable, "-m", "http.server", str(PORT), "--directory", os.getcwd()],
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    time.sleep(1.5)

async def main():
    mode = sys.argv[1]
    fps = int(sys.argv[sys.argv.index("--fps") + 1]) if "--fps" in sys.argv else 30
    chunk = float(sys.argv[sys.argv.index("--chunk") + 1]) if "--chunk" in sys.argv else 20
    ensure_server()
    async with async_playwright() as p:
        b = await p.chromium.launch(args=ARGS, executable_path=os.environ.get("CHROME", "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"))
        pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        pg.on("pageerror", lambda e: print("PAGEERR", e, flush=True))
        pg.on("console", lambda m: print("console:", m.text, flush=True) if m.type == "error" else None)
        await pg.goto(f"http://localhost:{PORT}/index.html")
        await pg.wait_for_function("window.READY===true", timeout=120000)
        end = await pg.evaluate("window.END"); print("END", end, "shots", await pg.evaluate("window.SHOTS"), flush=True)
        if mode == "test":
            os.makedirs("test", exist_ok=True)
            for i, t in enumerate(float(x) for x in sys.argv[2].split(",")):
                d = await pg.evaluate(f"frameJPEG({t},0.92)")
                open(f"test/t{i:02d}.jpg", "wb").write(base64.b64decode(d.split(",")[1]))
        else:
            os.makedirs("chunks", exist_ok=True)
            n = int(round(end * fps)); per = int(chunk * fps); t0 = time.time()
            for ci, f0 in enumerate(range(0, n, per)):
                out = f"chunks/c{ci:03d}.mp4"
                if os.path.exists(out): continue
                ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "image2pipe", "-framerate", str(fps), "-c:v", "mjpeg", "-i", "-",
                                       "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", out + ".part.mp4"], stdin=subprocess.PIPE)
                for f in range(f0, min(n, f0 + per)):
                    d = await pg.evaluate(f"frameJPEG({f / fps},0.93)")
                    ff.stdin.write(base64.b64decode(d.split(",")[1]))
                ff.stdin.close(); ff.wait(); os.replace(out + ".part.mp4", out)
                done = min(n, f0 + per); el = time.time() - t0
                print(f"chunk {ci} done  {done}/{n} frames  {el/60:.1f} min elapsed", flush=True)
            parts = sorted(glob.glob("chunks/c*.mp4"))
            open("chunks/list.txt", "w").write("".join(f"file '{os.path.basename(x)}'\n" for x in parts))
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "chunks/list.txt", "-c", "copy", "video.mp4"], check=True)
            print("DONE video.mp4", flush=True)
        await b.close()
asyncio.run(main())

"""
AI Video Editor — complete single-file app (CapCut-style).
Double-click to open. Script, Audio, SRT, Clips, Avatar, Settings, Export — all inside.
v2: project save/open + auto-save, drag & drop, disk-space meter + cache cleaner, no Whisper, robust FFmpeg install.
v3: themes + accent colors, hover/press fades, smooth progress, tab slide, count-up numbers, CapCut-style look.
make_video.py (the engine) is embedded unchanged and run as-is.
"""
import os, sys, re, json, zlib, base64, shutil, hashlib, threading, subprocess, queue
import zipfile, urllib.request, time, ssl, stat, hmac
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog, colorchooser
import math, random

_ENGINE_B64 = """
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
hjLo9aRLG8c1+P8BQJC1Ug==
"""
_CONFIG_B64 = """
eNrFVM1u00AQvu9TjFQhpYeiJNDQRjLSNl2C1TS2bCc0J8uNN2VVJw6O0yYSB7hQIYQ4lJ8LNyoXoapUnDiVV7F4EmZsE9ReOMay
VzPfzOzszDfrFfj9/sWyXrYCwHXoKl+GIHwVhxGsQSMcDdQB2dLkXZqcwEAFkmT8ztLzN2lymSbXaXIF3NThUM4naLhIk58ZepoH
fsiU1yScn9zaKEEoTT5mHhe5+SsqGLjMXjDGu9zhlms/Np64jwxLqwA9N2DRFVZPq2Y4npcX9ZeeTWU0z9twnVdDK/XqCtHPmfI2
Tb5je3nHMWAY+n9b+iNz/pS3YhU3NSMVRiqe16Eph2qkYO0hNAJvihEkPfXipumQuCPnx2Hkw8ALgn2vf8iaYldv6y7S4u6IntYz
OpZbYKizRot3tsXCzAxTtPk/dyrIjsP+IQylr7yisv8c1xR7omXfTFlglNLU9/gW792yFyA5MOZYvG3rjm60XdsUYltbp4N0Q9WX
4ZGM4CgMpkNZh8rdMmh4gFeUnQaIOnuZjyQ8R/M6mivr5TuoVAvfJOs6kvIrC3qZJl+owTLqy1EMJfJeLVgDX/bVvgygVPO3CDzN
4inyLJ/Rb/nUYzrWNVqdXaFhGsaWPLZ424xpPJ7GMJFxrEYHk2XfoxWwvFiFEI5xHU2QuVp9E0nZrFdqRFS9guv9+j1mdByz47gW
R/I1smaxcoKEUySU8h28AG8NjUKE/6kJRNnmakD10nURM284DiTl2ayWZ5XyRpmyVDfKswfVTERkRraFjMsiubCRS5o+beHH/gAP
9qg/
"""


# ───────── ACCESS CONTROL / UPDATE (the admin tool fills these 3 lines for you — don't edit) ─────────
APP_VERSION = "2.0.4"
CONTROL_URL = "https://raw.githubusercontent.com/thesunthe98-ux/aieditorapp/main/control.json"
PUBKEY_B64 = "K8g+PP95UpYNka1pUwF/6lLk/aBqugx7dtH5ZhC05Lc="


def _unpack(b):
    return zlib.decompress(base64.b64decode("".join(b.split())))


# ───────────────────────── constants ─────────────────────────
AUDIO_EXTS = {".mp3", ".wav", ".m4a", ".aac", ".ogg", ".flac"}
VIDEO_EXTS = {".mp4", ".mov", ".avi", ".mkv", ".webm"}
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
NOWIN = 0x08000000 if os.name == "nt" else 0
FF_URL = ("https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/"
          "ffmpeg-master-latest-win64-gpl.zip")
CLIP_RE = re.compile(r"^(\d+)(?:\s*\((\d+)\)|[_\-](\d+)|([a-zA-Z]))?$")

BG, SIDE, PANEL, PANEL2 = "#0e0f13", "#14151a", "#1b1d24", "#262932"
FG, MUTED, ACCENT, ACCENT_FG = "#eceef3", "#8a90a0", "#25e0d4", "#06191a"
OK, BAD, WARN = "#3ecf8e", "#ff6b6b", "#f5b942"
ACCENT_HOV, GHOST_HOV, NAV_ACT, NAV_HOV = "#5af0e6", "#323644", "#16282b", "#1c1d22"
LOG_BG, LOG_FG, DISABLED, PH_BG = "#090a0d", "#cfd5e3", "#6b7080", "#0d0e12"
if sys.platform == "darwin":
    FONT, MONO, ICON_FONT = "Helvetica Neue", "Menlo", "Helvetica Neue"
elif os.name == "nt":
    FONT, MONO, ICON_FONT = "Segoe UI", "Consolas", "Segoe UI Symbol"
else:
    FONT, MONO, ICON_FONT = "DejaVu Sans", "DejaVu Sans Mono", "DejaVu Sans"


def docs_dir():
    d = os.path.join(os.path.expanduser("~"), "Documents")
    return d if os.path.isdir(d) else os.path.expanduser("~")


WORKSPACE = os.path.join(docs_dir(), "AI Video Editor")
TOOLS = os.path.join(WORKSPACE, "_tools")
FF_DIR = os.path.join(TOOLS, "ffmpeg")
RECENT = os.path.join(WORKSPACE, ".recent.json")


# ───────────────────────── helpers ─────────────────────────
def local_ffmpeg_bin():
    ex = load_recent().get("ffmpeg_dir")
    if ex and os.path.exists(os.path.join(ex, FF_EXE)):
        return ex
    if os.path.exists(os.path.join(FF_BIN, FF_EXE)):
        return FF_BIN
    if os.path.isdir(FF_DIR):
        for root, _d, files in os.walk(FF_DIR):
            if FF_EXE in files:
                return root
    return None


def add_ffmpeg_path():
    b = local_ffmpeg_bin()
    cur = os.environ.get("PATH", "").split(os.pathsep)
    extra = [b] if b else []
    if os.name != "nt":      # Finder/Dock theke khulle Mac e Homebrew PATH e thake na
        extra += [d for d in ("/opt/homebrew/bin", "/usr/local/bin", "/opt/local/bin") if os.path.isdir(d)]
    add = [d for d in extra if d not in cur]
    if add:
        os.environ["PATH"] = os.pathsep.join(add + cur)


def find_python():
    exe = sys.executable
    if exe.lower().endswith("pythonw.exe"):
        c = exe[:-11] + "python.exe"
        if os.path.exists(c):
            return c
    return exe


def has_module(py, mod):
    try:
        code = f"import importlib.util,sys;sys.exit(0 if importlib.util.find_spec('{mod}') else 1)"
        return subprocess.call([py, "-c", code], creationflags=NOWIN,
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0
    except Exception:
        return False


def sentences_of(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return [l.strip() for l in f if l.strip() and l.strip() != "---"]


def natural_key(s):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", s)]


def serial_audio_order(paths):
    """Audio file gulo jodi thik 1,2,3,...N naam e thake tahole number onujayi sorted list dey,
    na hole None. (jemon 1.mp3, 2.wav, 3.mp3)"""
    items = []
    for p in paths:
        stem = os.path.splitext(os.path.basename(p))[0].strip()
        if not re.fullmatch(r"[0-9]+", stem):
            return None
        items.append((int(stem), p))
    items.sort(key=lambda x: x[0])
    if [n for n, _ in items] != list(range(1, len(items) + 1)):
        return None
    return [p for _, p in items]


def merge_audio_files(files, out_path):
    """files ke serially jure ekta mp3 banay (ffmpeg). Returns (ok, error_text)."""
    n = len(files)
    parts = [f"[{i}:a:0]aresample=44100,aformat=sample_fmts=fltp:channel_layouts=stereo[a{i}]"
             for i in range(n)]
    graph = ";".join(parts) + ";" + "".join(f"[a{i}]" for i in range(n)) + f"concat=n={n}:v=0:a=1[out]"
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"]
    for fp in files:
        cmd += ["-i", fp]
    cmd += ["-filter_complex", graph, "-map", "[out]", "-c:a", "libmp3lame", "-b:a", "192k",
            "-f", "mp3", out_path]
    r = subprocess.run(cmd, creationflags=NOWIN, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                       text=True, errors="replace")
    ok = r.returncode == 0 and os.path.exists(out_path) and os.path.getsize(out_path) > 0
    return ok, (r.stderr or "").strip()[-600:]


def archive(path, proj):
    """Remove a file permanently (clips/audio/srt in the project are only copies,
    so nothing is kept in _removed any more -> minimum disk space)."""
    try:
        if os.path.isdir(path):
            rm_tree(path)
        elif os.path.exists(path):
            os.remove(path)
    except Exception:
        pass


def cfg_read(proj):
    cfg = {}
    p = os.path.join(proj, "config.txt")
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    v = re.split(r"\s+#", v, maxsplit=1)[0]
                    cfg[k.strip()] = v.strip()
    return cfg


def cfg_write(proj, updates):
    p = os.path.join(proj, "config.txt")
    old = open(p, encoding="utf-8").read() if os.path.exists(p) else ""
    text = old
    for k, v in updates.items():
        pat = re.compile(rf"^[ \t]*{re.escape(k)}[ \t]*=.*$", re.M)
        if pat.search(text):
            text = pat.sub(lambda m: f"{k}={v}", text, count=1)
        else:
            text = text.rstrip("\n") + f"\n{k}={v}\n"
    if text != old:
        atomic_write(p, text)


def scan_clips(clips_dir):
    out = {}
    if not os.path.isdir(clips_dir):
        return out
    for fn in os.listdir(clips_dir):
        n, e = os.path.splitext(fn)
        if e.lower() not in VIDEO_EXTS | IMAGE_EXTS:
            continue
        m = CLIP_RE.fullmatch(n)
        if not m:
            continue
        idx = int(m.group(1))
        var = (ord(m.group(4).lower()) - 96) if m.group(4) else int(m.group(2) or m.group(3) or 1)
        out.setdefault(idx, []).append((var, os.path.join(clips_dir, fn)))
    for k in out:
        out[k].sort(key=lambda x: (x[0], x[1]))
    return out


def next_clip_name(clips_dir, idx, ext):
    ex = scan_clips(clips_dir).get(idx, [])
    name = f"{idx}{ext}" if not ex else f"{idx}_{max(v for v, _ in ex) + 1}{ext}"
    n = 1
    while os.path.exists(os.path.join(clips_dir, name)):
        n += 1
        name = f"{idx}_{(max(v for v, _ in ex) if ex else 1) + n}{ext}"
    return name


def covered_by_avatar(n, show_for, show_every):
    cov, i = set(), 0
    show_for = max(1, show_for)
    while i < n:
        end = min(i + show_for, n)
        cov.update(range(i, end))
        i = end + max(0, show_every)
    return cov


def parse_srt_count(path):
    try:
        t = open(path, encoding="utf-8").read()
    except Exception:
        return 0
    return len(re.findall(r"\d{2}:\d{2}:\d{2}[,.]\d{3}\s*-->", t))


def media_duration(path):
    try:
        out = subprocess.check_output(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", path],
            stderr=subprocess.DEVNULL, creationflags=NOWIN, timeout=8)
        return float(out.strip())
    except Exception:
        return None


def fmt_dur(s):
    if s is None:
        return "—"
    return f"{int(s // 60)}:{int(s % 60):02d}"


def open_path(p):
    try:
        if os.name == "nt":
            os.startfile(p)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", p])
        else:
            subprocess.Popen(["xdg-open", p])
    except Exception as e:
        messagebox.showerror("Error", str(e))


def load_recent():
    try:
        return json.load(open(RECENT, encoding="utf-8"))
    except Exception:
        return {"last": "", "external": []}


def save_recent(d):
    try:
        os.makedirs(WORKSPACE, exist_ok=True)
        atomic_write(RECENT, json.dumps(d))
    except Exception:
        pass


def ensure_project(proj, copy_cfg_from=None):
    os.makedirs(os.path.join(proj, "clips"), exist_ok=True)
    sync_engine(proj)
    cfg = os.path.join(proj, "config.txt")
    if not os.path.exists(cfg):
        if copy_cfg_from and os.path.exists(os.path.join(copy_cfg_from, "config.txt")):
            shutil.copy2(os.path.join(copy_cfg_from, "config.txt"), cfg)
        else:
            open(cfg, "wb").write(_unpack(_CONFIG_B64))
    scr = os.path.join(proj, "script.txt")
    if not os.path.exists(scr):
        open(scr, "w", encoding="utf-8").close()


def tidy_ffmpeg():
    """Old installs extracted the whole 400MB+ build. Keep only ffmpeg/ffprobe."""
    try:
        if os.name != "nt" or not os.path.isdir(FF_DIR):
            return
        if not os.path.exists(os.path.join(FF_BIN, "ffmpeg.exe")):
            src = None
            for root, _d, files in os.walk(FF_DIR):
                if "ffmpeg.exe" in files:
                    src = root
                    break
            if not src:
                return
            os.makedirs(FF_BIN, exist_ok=True)
            for n in ("ffmpeg.exe", "ffprobe.exe"):
                if os.path.exists(os.path.join(src, n)):
                    shutil.copy2(os.path.join(src, n), os.path.join(FF_BIN, n))
        for n in os.listdir(FF_DIR):
            p = os.path.join(FF_DIR, n)
            if os.path.abspath(p) == os.path.abspath(FF_BIN):
                continue
            rm_tree(p) if os.path.isdir(p) else os.remove(p)
    except Exception:
        pass


def parse_volume_pct(s):
    s = str(s or "").strip().lower()
    try:
        if s.endswith("db"):
            v = 100 * 10 ** (float(s[:-2]) / 20)
        elif s.endswith("%"):
            v = float(s[:-1])
        else:
            v = float(s) * 100
    except ValueError:
        v = 100
    return int(max(10, min(400, round(v / 5) * 5)))


# ───────────────────────── extra helpers (v2) ─────────────────────────
CACHE_DIRS = ("_temp", "_downloads", "_thumbs", "_removed", "__pycache__")
LETTERS = "abcdefghijklmnopqrstuvwxyz"
FF_EXE = "ffmpeg.exe" if os.name == "nt" else "ffmpeg"
FF_BIN = os.path.join(FF_DIR, "bin")
FF_MIRRORS_GITHUB = "https://github.com/GyanD/codexffmpeg/releases"


def atomic_write(path, text):
    """Power-off / crash safe write: temp file -> flush -> fsync -> replace."""
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="") as f:
        f.write(text)
        f.flush()
        try:
            os.fsync(f.fileno())
        except Exception:
            pass
    os.replace(tmp, path)


def read_text(path):
    raw = open(path, "rb").read()
    for enc in ("utf-8-sig", "utf-16", "cp1252"):
        try:
            return raw.decode(enc)
        except Exception:
            continue
    return raw.decode("utf-8", errors="replace")


def human(n):
    n = float(n)
    for u in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024 or u == "TB":
            return f"{n:.0f} {u}" if u in ("B", "KB") else f"{n:.1f} {u}"
        n /= 1024


def dir_usage(path):
    """(real_bytes, linked_bytes). Hard-linked files cost no extra disk space."""
    real = linked = 0
    for root, _d, files in os.walk(path):
        for fn in files:
            try:
                st = os.lstat(os.path.join(root, fn))
            except OSError:
                continue
            if getattr(st, "st_nlink", 1) > 1:
                linked += st.st_size
            else:
                real += st.st_size
    return real, linked


def dir_size(path):
    return dir_usage(path)[0]


def fast_copy(src, dst):
    """Hard-link when possible (0 extra disk space), otherwise normal copy."""
    if os.path.exists(dst):
        os.remove(dst)
    try:
        os.link(src, dst)
    except Exception:
        shutil.copy2(src, dst)


def rm_tree(path):
    def _onerr(func, p, _exc):
        try:
            os.chmod(p, stat.S_IWRITE)
            func(p)
        except Exception:
            pass
    shutil.rmtree(path, onerror=_onerr)


def clip_name(idx, var, ext, letter=False):
    if var == 1 and not letter:
        return f"{idx}{ext}"
    if var <= 26:
        return f"{idx}{LETTERS[var - 1]}{ext}"
    return f"{idx}_{var}{ext}"


def place_clip(src, clips_dir, idx, preferred_var=None, letter=False):
    """Copy a clip into clips/ as  <idx>  /  <idx>a <idx>b ...  (engine naming)."""
    ext = os.path.splitext(src)[1].lower()
    used = {v for v, _ in scan_clips(clips_dir).get(idx, [])}
    if preferred_var and preferred_var not in used:
        var = preferred_var
    else:
        var = 1
        while var in used:
            var += 1
    name = clip_name(idx, var, ext, letter or bool(used))
    while os.path.exists(os.path.join(clips_dir, name)):
        var += 1
        name = clip_name(idx, var, ext, True)
    dst = os.path.join(clips_dir, name)
    fast_copy(src, dst)
    return dst


def clip_var(m):
    if m.group(4):
        return ord(m.group(4).lower()) - 96
    return int(m.group(2) or m.group(3) or 1)


def sync_engine(proj):
    """Keep the project's make_video.py on the latest embedded engine."""
    eng = os.path.join(proj, "make_video.py")
    data = _unpack(_ENGINE_B64)
    try:
        if os.path.exists(eng) and open(eng, "rb").read() == data:
            return
    except Exception:
        pass
    with open(eng, "wb") as f:
        f.write(data)


def ff_ok(folder=None):
    exe = os.path.join(folder, FF_EXE) if folder else "ffmpeg"
    try:
        return subprocess.call([exe, "-version"], creationflags=NOWIN, stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL, timeout=20) == 0
    except Exception:
        return False


def _ssl_ctx(verify=True):
    ctx = ssl.create_default_context()
    if not verify:
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
    return ctx


def download_file(url, dest, say, prog):
    """Streaming download with progress. Retries, and retries without SSL verify
    (some PCs have old certificate stores)."""
    last_err = None
    for verify in (True, False):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 AIVideoEditor"})
            with urllib.request.urlopen(req, timeout=40, context=_ssl_ctx(verify)) as r:
                total = int(r.headers.get("Content-Length") or 0)
                got, last = 0, -1
                with open(dest, "wb") as f:
                    while True:
                        b = r.read(1024 * 256)
                        if not b:
                            break
                        f.write(b)
                        got += len(b)
                        if total:
                            pc = int(got * 100 / total)
                            if pc // 5 != last:
                                last = pc // 5
                                say(f"   download {pc}%  ({got / 1e6:.0f}/{total / 1e6:.0f} MB)")
                                prog(5 + pc * 0.8)
                if total and got < total:
                    raise IOError("download incomplete")
            return True
        except Exception as e:
            last_err = e
            say(f"   download problem: {e}" + ("  — retrying without SSL verify" if verify else ""))
    raise last_err


def latest_gyan_tag():
    try:
        req = urllib.request.Request(FF_MIRRORS_GITHUB + "/latest", headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20, context=_ssl_ctx(False)) as r:
            return r.geturl().rstrip("/").split("/")[-1]
    except Exception:
        return "9.0.2"


def install_ffmpeg(say, prog):
    """Download an FFmpeg build, keep ONLY ffmpeg.exe + ffprobe.exe (saves ~300 MB)."""
    tag = latest_gyan_tag()
    urls = [
        f"{FF_MIRRORS_GITHUB}/download/{tag}/ffmpeg-{tag}-essentials_build.zip",
        "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip",
        "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip",
    ]
    os.makedirs(FF_BIN, exist_ok=True)
    zp = os.path.join(FF_DIR, "ffmpeg_download.zip")
    for n, url in enumerate(urls, 1):
        try:
            say(f"[SETUP] FFmpeg download ({n}/{len(urls)}): {url}")
            download_file(url, zp, say, prog)
            say("[SETUP] Extracting ffmpeg.exe / ffprobe.exe ...")
            with zipfile.ZipFile(zp) as z:
                for m in z.namelist():
                    base = os.path.basename(m).lower()
                    if base in ("ffmpeg.exe", "ffprobe.exe"):
                        with z.open(m) as s, open(os.path.join(FF_BIN, base), "wb") as d:
                            shutil.copyfileobj(s, d)
            os.remove(zp)
            if ff_ok(FF_BIN):
                prog(95)
                return True
            say("[WARN] extracted ffmpeg did not start, trying next source ...")
        except Exception as e:
            say(f"[WARN] source {n} failed: {e}")
        finally:
            try:
                if os.path.exists(zp):
                    os.remove(zp)
            except Exception:
                pass
    return False


# ───────────────────────── THEMES / ANIMATION ENGINE (v3) ─────────────────────────
# Colors live in module globals (BG, PANEL, ACCENT …). Changing theme/accent rewrites those
# globals and then re-colors every live widget by value (old palette -> new palette).
THEMES = {
    "Dark":     dict(BG="#0e0f13", SIDE="#14151a", PANEL="#1b1d24", PANEL2="#262932",
                     FG="#eceef3", MUTED="#8a90a0", LOG_BG="#090a0d", LOG_FG="#cfd5e3"),
    "Midnight": dict(BG="#0b1020", SIDE="#10172b", PANEL="#172038", PANEL2="#222d4a",
                     FG="#e8edfb", MUTED="#8d99b8", LOG_BG="#070b17", LOG_FG="#c9d3ee"),
    "AMOLED":   dict(BG="#000000", SIDE="#0a0a0a", PANEL="#141414", PANEL2="#212121",
                     FG="#f2f2f2", MUTED="#8b8b8b", LOG_BG="#050505", LOG_FG="#d0d0d0"),
    "Forest":   dict(BG="#0d1411", SIDE="#121c17", PANEL="#192620", PANEL2="#23352c",
                     FG="#e6f1ea", MUTED="#88a095", LOG_BG="#080e0b", LOG_FG="#c5d8cc"),
    "Plum":     dict(BG="#140f1a", SIDE="#1a1422", PANEL="#241b2e", PANEL2="#322641",
                     FG="#f0e9f7", MUTED="#9f8fb3", LOG_BG="#0e0a13", LOG_FG="#dccfe8"),
    "Light":    dict(BG="#eceff5", SIDE="#f7f8fb", PANEL="#ffffff", PANEL2="#e1e5ee",
                     FG="#1b1e28", MUTED="#697086", LOG_BG="#f3f5fa", LOG_FG="#2a2f3d", dark=False),
    "Sand":     dict(BG="#f1ebe1", SIDE="#f8f4ec", PANEL="#fffdf8", PANEL2="#e8dfd0",
                     FG="#2b261f", MUTED="#7d7365", LOG_BG="#f7f2e9", LOG_FG="#3a342a", dark=False),
}
ACCENTS = [("Teal", "#25e0d4"), ("Blue", "#4c8dff"), ("Purple", "#a06bff"), ("Pink", "#ff5fa2"),
           ("Red", "#ff5a5a"), ("Orange", "#ff9340"), ("Yellow", "#f5c542"), ("Green", "#3ecf8e")]
DEFAULT_THEME, DEFAULT_ACCENT = "Dark", "#25e0d4"
DANGER, DANGER_HOV = "#c0392b", "#d64a3a"
THEME_NAME, ACCENT_RAW, ANIM_ON = DEFAULT_THEME, DEFAULT_ACCENT, True
PAL = {}
_TOKENS = ("BG", "SIDE", "PANEL", "PANEL2", "FG", "MUTED", "ACCENT", "ACCENT_FG",
           "OK", "BAD", "WARN", "LOG_BG", "LOG_FG")
_HEX6 = re.compile(r"#[0-9a-fA-F]{6}")


def _hex_rgb(c):
    c = c.lstrip("#")
    return int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)


def _rgb_hex(r, g, b):
    return "#%02x%02x%02x" % tuple(max(0, min(255, int(round(v)))) for v in (r, g, b))


def _mix(a, b, t):
    ra, ga, ba = _hex_rgb(a)
    rb, gb, bb = _hex_rgb(b)
    return _rgb_hex(ra + (rb - ra) * t, ga + (gb - ga) * t, ba + (bb - ba) * t)


def _lum(c):
    r, g, b = _hex_rgb(c)
    return (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255.0


def build_palette(theme, accent):
    th = THEMES.get(theme) or THEMES[DEFAULT_THEME]
    dark = th.get("dark", True)
    acc = (accent if isinstance(accent, str) and _HEX6.fullmatch(accent) else DEFAULT_ACCENT).lower()
    if not dark:
        acc = _mix(acc, "#000000", 0.26)          # keep accent text readable on light panels
    p = {k: th[k] for k in ("BG", "SIDE", "PANEL", "PANEL2", "FG", "MUTED", "LOG_BG", "LOG_FG")}
    p["ACCENT"] = acc
    p["ACCENT_FG"] = "#0b1114" if _lum(acc) > 0.58 else "#ffffff"
    if dark:
        p.update(OK="#3ecf8e", BAD="#ff6b6b", WARN="#f5b942")
    else:
        p.update(OK="#139e68", BAD="#d63c3c", WARN="#b97a05")
    seen = set()                                   # recolor works by value, so values must be unique
    for k in _TOKENS:
        v = p[k].lower()
        while v in seen:
            r, g, b = _hex_rgb(v)
            v = _rgb_hex(r, g, b + 1 if b < 255 else b - 1)
        seen.add(v)
        p[k] = v
    p["ACCENT_HOV"] = _mix(p["ACCENT"], "#ffffff", 0.22)
    p["GHOST_HOV"] = _mix(p["PANEL2"], p["FG"], 0.10)
    p["NAV_ACT"] = _mix(p["SIDE"], p["ACCENT"], 0.16)
    p["NAV_HOV"] = _mix(p["SIDE"], p["FG"], 0.07)
    p["DISABLED"] = _mix(p["MUTED"], p["PANEL2"], 0.45)
    p["PH_BG"] = _mix(p["BG"], p["PANEL2"], 0.5)
    return p


def apply_palette(theme=None, accent=None):
    global THEME_NAME, ACCENT_RAW, PAL
    if theme:
        THEME_NAME = theme if theme in THEMES else DEFAULT_THEME
    if accent:
        ACCENT_RAW = accent
    PAL = build_palette(THEME_NAME, ACCENT_RAW)
    globals().update(PAL)
    return PAL


def _load_look():
    global ANIM_ON
    try:
        d = load_recent()
        t, a = d.get("theme"), d.get("accent")
        ANIM_ON = bool(d.get("anim", True))
        apply_palette(t if t in THEMES else DEFAULT_THEME,
                      a if isinstance(a, str) and _HEX6.fullmatch(a) else DEFAULT_ACCENT)
    except Exception:
        apply_palette(DEFAULT_THEME, DEFAULT_ACCENT)


_load_look()


# ───────── tiny tween engine (time based, 60fps, cancels cleanly) ─────────
def tween_cancel(w, key):
    jobs = w.__dict__.get("_tw")
    if jobs and key in jobs:
        try:
            w.after_cancel(jobs.pop(key))
        except Exception:
            jobs.pop(key, None)


def tween(w, key, ms, step, done=None, ease=True):
    """Calls step(t) with t going 0→1 over `ms` milliseconds (ease-out). One job per (widget, key)."""
    tween_cancel(w, key)
    if ms <= 0 or not ANIM_ON:
        try:
            step(1.0)
            if done:
                done()
        except tk.TclError:
            pass
        return
    jobs = w.__dict__.setdefault("_tw", {})
    t0 = time.perf_counter()

    def tick():
        try:
            raw = min(1.0, (time.perf_counter() - t0) * 1000.0 / ms)
            step(1 - (1 - raw) ** 3 if ease else raw)
            if raw >= 1.0:
                jobs.pop(key, None)
                if done:
                    done()
            else:
                jobs[key] = w.after(16, tick)
        except tk.TclError:
            jobs.pop(key, None)
    tick()


def _to_hex(w, c):
    c = str(c)
    if _HEX6.fullmatch(c):
        return c.lower()
    r, g, b = w.winfo_rgb(c)
    return _rgb_hex(r / 257.0, g / 257.0, b / 257.0)


def fade_to(w, target, ms=150):
    """target = {option: color}. Smoothly blends the widget's current colors to the new ones."""
    try:
        start = {o: _to_hex(w, w.cget(o)) for o in target}
    except Exception:
        start = None

    def step(t):
        for o, c in target.items():
            w.configure(**{o: _mix(start[o], c, t) if start else c})
    tween(w, "fade", ms, step)


def count_to(lbl, target, fmt="{}", ms=320):
    """Number label that counts up/down smoothly instead of jumping."""
    cur = getattr(lbl, "_num_shown", None)
    if cur is None or ms <= 0 or not ANIM_ON:
        tween_cancel(lbl, "num")
        lbl._num_shown = float(target)
        lbl.configure(text=fmt.format(int(target)))
        return
    if cur == target:
        return

    def step(t):
        v = cur + (target - cur) * t
        lbl._num_shown = v
        lbl.configure(text=fmt.format(int(round(v))))
    tween(lbl, "num", ms, step)


# ───────── live re-coloring of the whole widget tree ─────────
_COLOR_OPTS = ("bg", "fg", "activebackground", "activeforeground", "highlightbackground",
               "highlightcolor", "insertbackground", "selectbackground", "selectforeground",
               "selectcolor", "disabledforeground", "troughcolor", "readonlybackground",
               "inactiveselectbackground")


def _recolor_tree(root, mapping):
    hooks = []

    def walk(w):
        if getattr(w, "_no_theme", False):          # theme preview swatches keep their own colors
            return
        try:
            for key in list(w.__dict__.get("_tw", {})):
                tween_cancel(w, key)
            if not isinstance(w, ttk.Widget):
                keys = w.keys()
                for o in _COLOR_OPTS:
                    if o in keys:
                        cur = str(w.cget(o)).lower()
                        if cur in mapping:
                            w.configure(**{o: mapping[cur]})
                if isinstance(w, tk.Text):
                    for tag in w.tag_names():
                        for o in ("foreground", "background"):
                            cur = str(w.tag_cget(tag, o)).lower()
                            if cur in mapping:
                                w.tag_configure(tag, **{o: mapping[cur]})
            if hasattr(w, "_retheme"):
                hooks.append(w._retheme)
        except tk.TclError:
            pass
        for c in w.winfo_children():
            walk(c)
    walk(root)
    for h in hooks:                                  # custom widgets set their exact final colors
        try:
            h()
        except tk.TclError:
            pass


# ───────── macOS: tk.Button ignores colors there, so use a Label-based button ─────────
USE_LABEL_BTN = sys.platform == "darwin" or bool(os.environ.get("AVE_LABEL_BTN"))


class _LabelBtn(tk.Label):
    def __init__(self, parent, text="", command=None, **kw):
        kw.pop("relief", None)
        kw.pop("bd", None)
        self._cmd = command
        bg = kw.get("bg", "#262932")
        kw.setdefault("disabledforeground", DISABLED)
        super().__init__(parent, text=text, relief="flat", bd=0, anchor="center", **kw)
        self._base_bg = bg
        self.bind("<Button-1>", self._click)

    def _click(self, _e=None):
        if str(self.cget("state")) != "disabled" and self._cmd:
            self._cmd()

    def invoke(self):
        self._click()


TkBtn = _LabelBtn if USE_LABEL_BTN else tk.Button


# ───────────────────────── widgets ─────────────────────────
def _btn_colors(kind):
    return {"primary": (ACCENT, ACCENT_FG, ACCENT_HOV),
            "ghost": (PANEL2, FG, GHOST_HOV),
            "danger": (DANGER, "#ffffff", DANGER_HOV),
            "flat": (PANEL, FG, PANEL2)}[kind]


def mkbtn(parent, text, cmd, kind="ghost", **kw):
    bg, fg, hov = _btn_colors(kind)
    b = TkBtn(parent, text=text, command=cmd, bg=bg, fg=fg, activebackground=bg,
              activeforeground=fg, disabledforeground=DISABLED, relief="flat", bd=0,
              highlightthickness=0, cursor="hand2",
              font=(FONT, 10, "bold" if kind in ("primary", "danger") else "normal"),
              padx=kw.pop("padx", 16), pady=kw.pop("pady", 8), **kw)
    b._kind = kind

    def ok():
        return str(b["state"]) != "disabled"

    def go(color, ms):
        fade_to(b, {"bg": color, "activebackground": color}, ms)

    def retheme():
        c0, c1, _ = _btn_colors(b._kind)
        b.configure(bg=c0, activebackground=c0, activeforeground=b.cget("fg"), disabledforeground=DISABLED)
    b._retheme = retheme
    b.bind("<Enter>", lambda e: ok() and go(_btn_colors(b._kind)[2], 140), add="+")
    b.bind("<Leave>", lambda e: go(_btn_colors(b._kind)[0], 220), add="+")
    b.bind("<ButtonPress-1>", lambda e: ok() and go(_mix(_btn_colors(b._kind)[2], "#000000", 0.28), 60), add="+")
    b.bind("<ButtonRelease-1>", lambda e: ok() and go(_btn_colors(b._kind)[2], 160), add="+")
    return b


def mklabel(parent, text="", size=10, color=FG, bold=False, bg=None, **kw):
    return tk.Label(parent, text=text, fg=color, bg=bg or parent["bg"],
                    font=(FONT, size, "bold" if bold else "normal"), **kw)


def mkentry(parent, var, width=24, show=None):
    return tk.Entry(parent, textvariable=var, width=width, bg=PANEL2, fg=FG,
                    insertbackground=FG, relief="flat", font=(FONT, 10), show=show,
                    selectbackground=ACCENT, selectforeground=ACCENT_FG,
                    highlightthickness=1, highlightbackground=PANEL2, highlightcolor=ACCENT)


def mktext(parent, **kw):
    t = tk.Text(parent, bg=PANEL, fg=FG, insertbackground=FG, relief="flat", wrap="word",
                font=(MONO, 11), undo=True, padx=16, pady=14, bd=0,
                selectbackground=ACCENT, selectforeground=ACCENT_FG, inactiveselectbackground=PANEL2,
                highlightthickness=0, **kw)
    return t



# ───────────────────────── modern widgets (v3) ─────────────────────────
class NavItem(tk.Frame):
    """Sidebar item: big icon + small caption, smooth hover / active color fade."""

    def __init__(self, parent, icon, text, command):
        super().__init__(parent, bg=SIDE, cursor="hand2")
        self._cmd, self.active = command, False
        self.ic = tk.Label(self, text=icon, bg=SIDE, fg=MUTED, font=(ICON_FONT, 17), cursor="hand2")
        self.tx = tk.Label(self, text=text, bg=SIDE, fg=MUTED, font=(FONT, 8), cursor="hand2")
        self.ic.pack(pady=(10, 0))
        self.tx.pack(pady=(0, 10))
        self._shown = (SIDE, MUTED)
        for w in (self, self.ic, self.tx):
            w.bind("<Enter>", self._enter, add="+")
            w.bind("<Leave>", self._leave, add="+")
            w.bind("<Button-1>", self._click, add="+")

    def _rest(self):
        return (NAV_ACT, ACCENT) if self.active else (SIDE, MUTED)

    def _go(self, bg, fg, ms):
        b0, f0 = self._shown

        def step(t):
            b, f = _mix(b0, bg, t), _mix(f0, fg, t)
            self._shown = (b, f)
            for w in (self, self.ic, self.tx):
                w.configure(bg=b)
            self.ic.configure(fg=f)
            self.tx.configure(fg=f)
        tween(self, "c", ms, step)

    def _enter(self, _e=None):
        if not self.active:
            self._go(NAV_HOV, FG, 120)

    def _leave(self, _e=None):
        try:
            w = self.winfo_containing(*self.winfo_pointerxy())
        except Exception:
            w = None
        if w in (self, self.ic, self.tx):
            return
        self._go(*self._rest(), 180)

    def _click(self, _e=None):
        if self._cmd:
            self._cmd()

    def set_active(self, flag, animate=True):
        self.active = bool(flag)
        self._go(*self._rest(), 200 if animate else 0)

    def _retheme(self):
        self._shown = self._rest()
        b, f = self._shown
        for w in (self, self.ic, self.tx):
            w.configure(bg=b)
        self.ic.configure(fg=f)
        self.tx.configure(fg=f)


class SmoothBar(tk.Canvas):
    """Progress bar that glides to its value, shimmers while a job runs, and can flash on success.
    Drop-in for the old ttk.Progressbar: bar["value"] = 42 / bar["value"]."""

    def __init__(self, parent, maximum=100, active=None, **kw):
        super().__init__(parent, height=22, bg=BG, highlightthickness=0, bd=0)
        self._max = float(maximum) or 100.0
        self._target = self._shown = 0.0
        self._active = active or (lambda: False)
        self._job = None
        self._shine = None
        self._t_last = time.perf_counter()
        self.bind("<Configure>", lambda e: self._draw())

    def __getitem__(self, key):
        return self._target if key == "value" else super().__getitem__(key)

    def __setitem__(self, key, val):
        if key != "value":
            return super().__setitem__(key, val)
        self._target = max(0.0, min(self._max, float(val)))
        if self._target <= 0 or not ANIM_ON:
            self._shown = self._target
        self._kick()

    def _kick(self):
        if self._job is None:
            self._t_last = time.perf_counter()
            self._tick()

    def _tick(self):
        self._job = None
        try:
            now = time.perf_counter()
            dt, self._t_last = min(0.05, now - self._t_last), now
            diff = self._target - self._shown
            if abs(diff) < 0.06:
                self._shown = self._target
            else:
                self._shown += diff * (1 - math.exp(-dt / 0.10))
            self._draw()
            running = self._active() and 0 < self._shown < self._max
            if self._shown != self._target or running or self._shine is not None:
                self._job = self.after(16, self._tick)
        except tk.TclError:
            self._job = None

    def flash(self):
        if not ANIM_ON:
            return

        def step(t):
            self._shine = t
        tween(self, "shine", 750, step, done=lambda: (setattr(self, "_shine", None), self._draw()),
              ease=False)
        self._kick()

    def _draw(self):
        self.delete("all")
        W, H = self.winfo_width(), self.winfo_height()
        h, x0, x1, cy = 10, 5.0, W - 56.0, H / 2.0
        if W < 80:
            return
        self.create_line(x0, cy, x1, cy, width=h, capstyle="round", fill=PANEL2)
        frac = max(0.0, min(1.0, self._shown / self._max))
        if frac > 0.002:
            fx = x0 + (x1 - x0) * frac
            col = OK if frac >= 0.9995 else ACCENT
            self.create_line(x0, cy, max(fx, x0 + 0.1), cy, width=h, capstyle="round", fill=col)
            sh = self._shine
            if sh is None and self._active() and frac < 0.9995:
                sh = (time.perf_counter() % 1.6) / 1.6
            if sh is not None:
                pos = x0 - 30 + (fx - x0 + 60) * sh
                a, b = max(x0 + 2, pos - 34), min(fx - 2, pos)
                if b > a:
                    self.create_line(a, cy, b, cy, width=h - 4, capstyle="butt", fill=_mix(col, "#ffffff", 0.5))
        self.create_text(W - 4, cy, text=f"{int(round(frac * 100))}%", anchor="e",
                         fill=FG if frac > 0 else MUTED, font=(FONT, 9, "bold"))

    def _retheme(self):
        self._draw()


class Slider(tk.Canvas):
    """Thin accent slider (replaces tk.Scale). Works with IntVar / StringVar / DoubleVar."""
    PAD = 12

    def __init__(self, parent, variable, from_=0, to=100, resolution=1, length=220,
                 command=None, show_value=False, bg=None):
        extra = 46 if show_value else 0
        super().__init__(parent, width=length + 2 * self.PAD + extra, height=30,
                         bg=bg or parent["bg"], highlightthickness=0, bd=0, cursor="hand2")
        self.var, self.lo, self.hi, self.res = variable, from_, to, resolution
        self.len, self.cmd, self.show_value, self._r, self._drag = length, command, show_value, 6.0, False
        self.bind("<ButtonPress-1>", self._press)
        self.bind("<B1-Motion>", self._move)
        self.bind("<ButtonRelease-1>", self._release)
        self.bind("<Enter>", lambda e: self._grow(8.5))
        self.bind("<Leave>", lambda e: self._grow(6.0) if not self._drag else None)
        self._trace = variable.trace_add("write", lambda *a: self._safe_draw())
        self.bind("<Destroy>", self._destroyed, add="+")
        self._draw()

    def _destroyed(self, e):
        if e.widget is self:
            try:
                self.var.trace_remove("write", self._trace)
            except Exception:
                pass

    def _raw(self):
        try:
            return float(self.var.get())
        except Exception:
            return None

    def _safe_draw(self):
        try:
            self._draw()
        except tk.TclError:
            pass

    def _grow(self, r):
        r0 = self._r

        def step(t):
            self._r = r0 + (r - r0) * t
            self._draw()
        tween(self, "r", 120, step)

    def _draw(self):
        self.delete("all")
        raw = self._raw()
        v = self.lo if raw is None else max(self.lo, min(self.hi, raw))
        frac = (v - self.lo) / float(self.hi - self.lo)
        x0, x1, cy = self.PAD, self.PAD + self.len, 15
        hx = x0 + (x1 - x0) * frac
        self.create_line(x0, cy, x1, cy, width=4, capstyle="round", fill=PANEL2)
        if hx > x0:
            self.create_line(x0, cy, hx, cy, width=4, capstyle="round", fill=ACCENT)
        r = self._r
        self.create_oval(hx - r, cy - r, hx + r, cy + r, fill=PANEL, outline=ACCENT, width=3)
        if self.show_value:
            self.create_text(x1 + self.PAD + 6, cy, text=f"{v:g}", anchor="w", fill=FG, font=(FONT, 10, "bold"))

    def _set_from_x(self, x):
        frac = max(0.0, min(1.0, (x - self.PAD) / float(self.len)))
        v = self.lo + frac * (self.hi - self.lo)
        v = max(self.lo, min(self.hi, round(v / self.res) * self.res))
        if self._raw() == v:
            return
        iv = int(v) if float(v).is_integer() else v
        if isinstance(self.var, tk.IntVar):
            self.var.set(int(iv))
        elif isinstance(self.var, tk.DoubleVar):
            self.var.set(float(iv))
        else:
            self.var.set(str(iv))
        if self.cmd:
            self.cmd(str(iv))

    def _press(self, e):
        self._drag = True
        self._grow(9.5)
        self._set_from_x(e.x)

    def _move(self, e):
        if self._drag:
            self._set_from_x(e.x)

    def _release(self, e):
        self._drag = False
        self._grow(8.5)

    def _retheme(self):
        self._draw()


class ScrollFrame(tk.Frame):
    """Vertically scrollable container; put children in .inner. Scrollbar appears only if needed."""

    def __init__(self, parent, bg=None):
        super().__init__(parent, bg=bg or BG)
        self.cv = tk.Canvas(self, bg=bg or BG, highlightthickness=0, bd=0, height=100)
        self.sb = ttk.Scrollbar(self, orient="vertical", command=self.cv.yview)
        self.cv.configure(yscrollcommand=self._on_scroll)
        self.inner = tk.Frame(self.cv, bg=bg or BG)
        self._win = self.cv.create_window((0, 0), window=self.inner, anchor="nw")
        self.inner.bind("<Configure>", lambda e: self.cv.configure(scrollregion=self.cv.bbox("all")))
        self.cv.bind("<Configure>", lambda e: self.cv.itemconfigure(self._win, width=e.width))
        self.sb.pack(side="right", fill="y")
        self.cv.pack(side="left", fill="both", expand=True)
        for w in (self, self.cv, self.inner):
            w.bind("<Enter>", self._wheel_on, add="+")
            w.bind("<Leave>", self._wheel_off, add="+")

    def _on_scroll(self, lo, hi):
        self.sb.set(lo, hi)

    def _inside(self):
        try:
            w = self.winfo_containing(*self.winfo_pointerxy())
        except Exception:
            return False
        while w is not None:
            if w is self:
                return True
            w = getattr(w, "master", None)
        return False

    def _wheel(self, e):
        if getattr(e, "num", 0) == 4:
            n = -1
        elif getattr(e, "num", 0) == 5:
            n = 1
        elif sys.platform == "darwin":
            n = -int(e.delta) if abs(e.delta) < 40 else -int(e.delta / 40)
            n = max(-6, min(6, n)) or (-1 if e.delta > 0 else 1)
        else:
            n = int(-e.delta / 120)
        self.cv.yview_scroll(n, "units")

    def _wheel_on(self, _e=None):
        for ev in ("<MouseWheel>", "<Button-4>", "<Button-5>"):
            self.bind_all(ev, self._wheel)

    def _wheel_off(self, _e=None):
        if not self._inside():
            for ev in ("<MouseWheel>", "<Button-4>", "<Button-5>"):
                self.unbind_all(ev)

    def _retheme(self):
        pass


# ───────── Ed25519 (pure python, RFC 8032) — signatures for control file & updates ─────────
_P = 2 ** 255 - 19
_Q = 2 ** 252 + 27742317777372353535851937790883648493
_D = -121665 * pow(121666, _P - 2, _P) % _P
_I = pow(2, (_P - 1) // 4, _P)


def _inv(x):
    return pow(x, _P - 2, _P)


def _xrec(y):
    xx = (y * y - 1) * _inv(_D * y * y + 1) % _P
    x = pow(xx, (_P + 3) // 8, _P)
    if (x * x - xx) % _P:
        x = x * _I % _P
    if x & 1:
        x = _P - x
    return x


_BY = 4 * _inv(5) % _P
_BX = _xrec(_BY)
_B = (_BX, _BY, 1, _BX * _BY % _P)


def _add(p, q):
    a = (p[1] - p[0]) * (q[1] - q[0]) % _P
    b = (p[1] + p[0]) * (q[1] + q[0]) % _P
    c = 2 * p[3] * q[3] * _D % _P
    d = 2 * p[2] * q[2] % _P
    e, f, g, h = b - a, d - c, d + c, b + a
    return (e * f % _P, g * h % _P, f * g % _P, e * h % _P)


def _mul(s, p):
    r = (0, 1, 1, 0)
    while s:
        if s & 1:
            r = _add(r, p)
        p = _add(p, p)
        s >>= 1
    return r


def _enc(p):
    zi = _inv(p[2])
    x, y = p[0] * zi % _P, p[1] * zi % _P
    return (y | ((x & 1) << 255)).to_bytes(32, "little")


def _dec(s):
    y = int.from_bytes(s, "little")
    sign, y = y >> 255, y & ((1 << 255) - 1)
    if y >= _P:
        raise ValueError("bad point")
    x = _xrec(y)
    if x & 1 != sign:
        x = _P - x
    if (-x * x + y * y - 1 - _D * x * x * y * y) % _P:
        raise ValueError("bad point")
    return (x, y, 1, x * y % _P)


def _eq(p, q):
    return (p[0] * q[2] - q[0] * p[2]) % _P == 0 and (p[1] * q[2] - q[1] * p[2]) % _P == 0


def ed_verify(pub, msg, sig):
    try:
        if len(sig) != 64 or len(pub) != 32:
            return False
        r, a = _dec(sig[:32]), _dec(pub)
        s = int.from_bytes(sig[32:], "little")
        if s >= _Q:
            return False
        h = int.from_bytes(hashlib.sha512(sig[:32] + pub + msg).digest(), "little") % _Q
        return _eq(_mul(s, _B), _add(r, _mul(h, a)))
    except Exception:
        return False


# ═════════════════ LOGIN · REMOTE ACCESS CONTROL · AUTO-UPDATE ═════════════════
AUTH_ON = bool(CONTROL_URL and PUBKEY_B64)
SESSION_FILE = os.path.join(TOOLS, "session.json")
CACHE_FILE = os.path.join(TOOLS, "control.cache.json")
APP_PATH = os.path.abspath(__file__) if "__file__" in globals() else ""


def id_key(uid):
    return hashlib.sha256(("ave:" + uid.strip().lower()).encode("utf-8")).hexdigest()


def pw_hash(password, salt_hex, iters):
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), bytes.fromhex(salt_hex),
                               int(iters)).hex()


def vtuple(v):
    return tuple(int(x) for x in re.findall(r"\d+", str(v)))[:4] or (0,)


def _json_load(path, default=None):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def _http_get(url, timeout=25):
    """Control file / update download. TLS is verified first; if the PC has an old
    certificate store we retry without — safe, because everything we fetch is signed."""
    last = None
    for verify in (True, False):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "AIVideoEditor/" + APP_VERSION,
                                                       "Cache-Control": "no-cache", "Pragma": "no-cache"})
            with urllib.request.urlopen(req, timeout=timeout, context=_ssl_ctx(verify)) as r:
                return r.read(), r.headers.get("Date")
        except Exception as e:
            last = e
    raise last


def verify_manifest(raw):
    m = json.loads(raw.decode("utf-8-sig"))
    payload = m["payload"].encode("utf-8")
    if not ed_verify(base64.b64decode(PUBKEY_B64), payload, base64.b64decode(m["sig"])):
        raise ValueError("signature mismatch")
    return json.loads(payload), m


def server_now(date_hdr):
    try:
        import email.utils
        return email.utils.parsedate_to_datetime(date_hdr).timestamp()
    except Exception:
        return None


def load_control(allow_cache=True):
    """-> (ctl, online, msg).  Fetch signed control file; else fall back to a recent cache."""
    cache = _json_load(CACHE_FILE, {}) or {}
    now = time.time()
    err = ""
    try:
        url = CONTROL_URL + ("&" if "?" in CONTROL_URL else "?") + "_=" + str(int(now))
        raw, date_hdr = _http_get(url)
        ctl, m = verify_manifest(raw)
        if int(ctl.get("issued", 0)) < int(cache.get("issued_max", 0)):
            raise ValueError("old control file (rollback blocked)")
        cache = {"manifest": m, "fetched_at": now, "last_seen": now,
                 "server_time": server_now(date_hdr) or now,
                 "issued_max": max(int(ctl.get("issued", 0)), int(cache.get("issued_max", 0)))}
        try:
            os.makedirs(TOOLS, exist_ok=True)
            atomic_write(CACHE_FILE, json.dumps(cache))
        except Exception:
            pass
        ctl["_now"] = cache["server_time"]
        return ctl, True, ""
    except Exception as e:
        err = str(e)
    if allow_cache and cache.get("manifest"):
        try:
            ctl = json.loads(cache["manifest"]["payload"])
            ok_sig = ed_verify(base64.b64decode(PUBKEY_B64), cache["manifest"]["payload"].encode("utf-8"),
                               base64.b64decode(cache["manifest"]["sig"]))
            days = float(ctl.get("offline_days", 3))
            age = now - float(cache.get("fetched_at", 0))
            if now < float(cache.get("last_seen", 0)) - 600:
                return None, False, "PC er time/date mile na (clock change dhora poreche) — internet connect koro."
            if ok_sig and 0 <= age <= days * 86400:
                try:
                    cache["last_seen"] = now
                    atomic_write(CACHE_FILE, json.dumps(cache))
                except Exception:
                    pass
                ctl["_now"] = float(cache.get("server_time", now)) + age
                return ctl, False, ""
            return None, False, f"Internet nei, ar offline access er somoy ({days:g} din) shesh. Internet connect koro."
        except Exception:
            pass
    return None, False, f"Server er shathe connect hoy nai. Internet check koro.\n({err[:120]})"


def check_user(ctl, uid, hhex):
    """-> (ok, message). hhex = password hash (already computed)."""
    u = (ctl.get("users") or {}).get(id_key(uid))
    if not u or not hmac.compare_digest(str(u.get("hash", "")), str(hhex)):
        return False, "ID ba password thik nai."
    if not u.get("active", True):
        return False, "Ei account er access bondho kora hoyeche."
    exp = u.get("expires")
    if exp:
        try:
            if ctl.get("_now", time.time()) > time.mktime(time.strptime(exp, "%Y-%m-%d")) + 86400:
                return False, f"Ei account er meyad {exp} te shesh hoye gechhe."
        except Exception:
            pass
    return True, ""


def save_session(uid, hhex, name):
    try:
        os.makedirs(TOOLS, exist_ok=True)
        atomic_write(SESSION_FILE, json.dumps({"id": uid, "hash": hhex, "name": name}))
    except Exception:
        pass


def clear_session():
    try:
        os.remove(SESSION_FILE)
    except Exception:
        pass


def update_wanted(ctl):
    return bool(ctl.get("app_url") and ctl.get("app_sha256") and vtuple(ctl.get("version", "0")) > vtuple(APP_VERSION))


def apply_update(ctl, target=None):
    """Download -> verify signed SHA-256 -> syntax check -> swap file (old kept as .bak)."""
    target = target or APP_PATH
    data, _ = _http_get(ctl["app_url"], timeout=120)
    if hashlib.sha256(data).hexdigest() != str(ctl["app_sha256"]).lower():
        raise ValueError("Download file ta thik nai (hash mile nai) — update bondho kora holo.")
    m = re.search(rb'(?m)^APP_VERSION = "([^"]+)"', data)
    if not m or m.group(1).decode() != str(ctl["version"]):
        raise ValueError("Update file er version mile nai.")
    compile(data, "update", "exec")
    new = target + ".new"
    with open(new, "wb") as f:
        f.write(data)
    try:
        shutil.copy2(target, target + ".bak")
    except Exception:
        pass
    os.replace(new, target)
    return True


def relaunch():
    try:
        subprocess.Popen([sys.executable, APP_PATH], close_fds=True, creationflags=NOWIN)
    except Exception:
        pass


def _center(win, w, h):
    win.update_idletasks()
    x = (win.winfo_screenwidth() - w) // 2
    y = max(0, (win.winfo_screenheight() - h) // 3)
    win.geometry(f"{w}x{h}+{x}+{y}")


def _msg_window(title, text, retry=False):
    """Small dark error window. Returns True if user pressed Retry."""
    r = tk.Tk()
    r.title(title)
    r.configure(bg=BG)
    _center(r, 460, 230)
    res = {"retry": False}
    mklabel(r, title, 14, WARN, True).pack(padx=24, pady=(22, 8), anchor="w")
    mklabel(r, text, 10, FG, wraplength=410, justify="left").pack(padx=24, anchor="w")
    row = tk.Frame(r, bg=BG)
    row.pack(side="bottom", fill="x", padx=24, pady=18)
    if retry:
        mkbtn(row, "Retry", lambda: (res.update(retry=True), r.destroy()), "primary").pack(side="left")
    mkbtn(row, "Close", r.destroy, "ghost").pack(side="left", padx=8)
    r.mainloop()
    return res["retry"]


def login_window(ctl):
    r = tk.Tk()
    r.title("AI Video Editor — Login")
    r.configure(bg=BG)
    r.resizable(False, False)
    _center(r, 400, 470)
    out = {"s": None}
    mklabel(r, "◆ AI Video Editor", 18, ACCENT, True).pack(pady=(34, 2))
    mklabel(r, f"v{APP_VERSION}", 9, MUTED).pack()
    mklabel(r, "Login koro", 12, FG, True).pack(pady=(26, 10))
    uv, pv, rv = tk.StringVar(), tk.StringVar(), tk.IntVar(value=1)
    sess = _json_load(SESSION_FILE, {}) or {}
    uv.set(sess.get("id", ""))
    box = tk.Frame(r, bg=BG)
    box.pack(padx=44, fill="x")
    mklabel(box, "ID", 9, MUTED).pack(anchor="w")
    e1 = mkentry(box, uv, 30)
    e1.pack(fill="x", ipady=6, pady=(2, 12))
    mklabel(box, "Password", 9, MUTED).pack(anchor="w")
    e2 = mkentry(box, pv, 30, show="•")
    e2.pack(fill="x", ipady=6, pady=(2, 10))
    tk.Checkbutton(box, text="Remember me", variable=rv, bg=BG, fg=FG, selectcolor=PANEL2,
                   activebackground=BG, activeforeground=FG, font=(FONT, 9)).pack(anchor="w")
    msg = mklabel(r, "", 9, BAD, wraplength=320)
    msg.pack(pady=(10, 0))
    fails = {"n": 0}
    btn = mkbtn(r, "Login", lambda: go(), "primary", padx=40, pady=9)
    btn.pack(pady=14)

    def unlock():
        btn.configure(state="normal")
        msg.configure(text="")

    def go(_e=None):
        uid, pw = uv.get().strip(), pv.get()
        if not uid or not pw:
            msg.configure(text="ID ar password duto-i likho.", fg=BAD)
            return
        u = (ctl.get("users") or {}).get(id_key(uid))
        hh = pw_hash(pw, u["salt"], u.get("iters", 200000)) if u else ""
        ok, why = check_user(ctl, uid, hh) if u else (False, "ID ba password thik nai.")
        if ok:
            if rv.get():
                save_session(uid, hh, u.get("name") or uid)
            else:
                clear_session()
            out["s"] = {"id": uid, "hash": hh, "name": u.get("name") or uid}
            r.destroy()
            return
        fails["n"] += 1
        msg.configure(text=why, fg=BAD)
        pv.set("")
        if fails["n"] % 5 == 0:
            btn.configure(state="disabled")
            msg.configure(text="Onek bar vul — 30 second opekkha koro.")
            r.after(30000, unlock)
    r.bind("<Return>", go)
    (e2 if uv.get() else e1).focus_set()
    r.mainloop()
    return out["s"]


def gate():
    """Runs before the main window. Returns session dict, or None (= exit)."""
    if not AUTH_ON:
        return {"id": None, "name": "", "hash": ""}
    while True:
        ctl, online, why = load_control()
        if ctl is not None:
            break
        if not _msg_window("Connect hocche na", why, retry=True):
            return None
    if online and update_wanted(ctl):
        root = tk.Tk()
        root.withdraw()
        force = bool(ctl.get("force")) or vtuple(ctl.get("min_version", "0")) > vtuple(APP_VERSION)
        notes = (ctl.get("notes") or "").strip()
        ask = f"Notun version {ctl['version']} ashche (tomar: {APP_VERSION}).\n\n{notes}\n\nEkhon update korbo?"
        go = force or messagebox.askyesno("Update", ask, parent=root)
        if go:
            try:
                apply_update(ctl)
                root.destroy()
                relaunch()
                return None
            except Exception as e:
                messagebox.showerror("Update failed", f"{e}", parent=root)
                if force:
                    root.destroy()
                    return None
        root.destroy()
    s = _json_load(SESSION_FILE, {}) or {}
    if s.get("id") and s.get("hash"):
        ok, why = check_user(ctl, s["id"], s["hash"])
        if ok:
            return {"id": s["id"], "hash": s["hash"], "name": s.get("name") or s["id"]}
        clear_session()
        if "ID ba password" not in why:
            _msg_window("Access nei", why)
            return None
    return login_window(ctl)



# ───────────────── drag & drop (tkinterdnd2 — tiny, auto-installed once) ─────────────────
DND_OK, TkinterDnD, DND_FILES = False, None, None


def _setup_dnd():
    global DND_OK, TkinterDnD, DND_FILES

    def imp():
        global TkinterDnD, DND_FILES
        from tkinterdnd2 import TkinterDnD as T, DND_FILES as F
        TkinterDnD, DND_FILES = T, F
    try:
        imp()
    except Exception:
        try:
            cmd = [find_python(), "-m", "pip", "install", "--quiet", "--disable-pip-version-check", "tkinterdnd2"]
            if subprocess.call(cmd, creationflags=NOWIN, stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL, timeout=180) != 0 and os.name != "nt":
                subprocess.call(cmd + ["--user", "--break-system-packages"], stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL, timeout=180)
            import importlib, site
            importlib.invalidate_caches()
            us = site.getusersitepackages()
            if us not in sys.path and os.path.isdir(us):
                sys.path.append(us)
            imp()
        except Exception:
            return
    try:                              # make sure the native tkdnd library really loads here
        t = TkinterDnD.Tk()
        t.withdraw()
        t.destroy()
        DND_OK = True
    except Exception:
        DND_OK = False


_setup_dnd()
_Base = TkinterDnD.Tk if DND_OK else tk.Tk


# ═════════════════════════════ APP ═════════════════════════════
class App(_Base):
    SECTIONS = [("script", "✎", "Script"), ("audio", "♫", "Audio"), ("srt", "❝", "SRT"),
                ("clips", "▣", "Clips"), ("avatar", "☺", "Avatar"),
                ("settings", "⚙", "Settings"), ("export", "➤", "Export")]

    MEDIA_TYPES = [("Media", "*.mp4 *.mov *.avi *.mkv *.webm *.jpg *.jpeg *.png *.webp *.bmp")]

    def __init__(self, session=None):
        super().__init__()
        self.session = session or {}
        self._upd = None
        self._mon_stop = False
        os.makedirs(TOOLS, exist_ok=True)
        add_ffmpeg_path()
        self.title(f"AI Video Editor v{APP_VERSION}")
        self.geometry("1180x760")
        self.minsize(1040, 640)
        self.configure(bg=BG)
        self.report_callback_exception = self._tk_error

        self.proj = ""
        self.proc = None
        self.busy = False
        self.q = queue.Queue()
        self.mode = tk.IntVar(value=1)
        self.out_dir = tk.StringVar()
        self.out_name = tk.StringVar(value="final_video")
        self.req = {"ff": None, "wh": True}
        self.thumb_q = queue.Queue()
        self.thumb_labels = {}
        self.thumb_warned = False
        self._save_job = None
        self._srt_job = None
        self._cfg_job = None
        self._meta_job = None
        self._note_job = None
        self._loading = False
        self._srt_loading = False
        self._script_saved = None
        self._srt_saved = None
        self._usage = {}
        self._usage_busy = False
        self._merging = False
        self._drag_out = False
        self.cur_output = ""
        self.frames = {}
        self.nav = {}
        self.cur = None
        self.ph = tk.PhotoImage(width=128, height=72)
        self.ph.put(PH_BG, to=(0, 0, 128, 72))
        self.rec = load_recent()

        self._style()
        self._build_top()
        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True)
        self.side = tk.Frame(body, bg=SIDE, width=96)
        self.side.pack(side="left", fill="y")
        self.side.pack_propagate(False)
        tk.Frame(body, bg=PANEL2, width=1).pack(side="left", fill="y")
        self.nav_ind = tk.Frame(self.side, bg=ACCENT, width=3)
        self._ind_cur = None
        self.side.bind("<Configure>", lambda e: self._move_ind(False))
        self.content = tk.Frame(body, bg=BG)
        self.content.pack(side="left", fill="both", expand=True)
        for key, icon, name in self.SECTIONS:
            b = NavItem(self.side, icon, name, lambda k=key: self.show(k))
            b.pack(fill="x", padx=8, pady=2)
            self.nav[key] = b
            f = tk.Frame(self.content, bg=BG)
            self.frames[key] = f
        self._build_script(self.frames["script"])
        self._build_audio(self.frames["audio"])
        self._build_srt(self.frames["srt"])
        self._build_clips(self.frames["clips"])
        self._build_avatar(self.frames["avatar"])
        self._build_settings(self.frames["settings"])
        self._build_export(self.frames["export"])

        self.statusbar = mklabel(self, "", 9, MUTED, bg=SIDE, anchor="w", padx=16, pady=5)
        self.statusbar.pack(fill="x", side="bottom")
        tk.Frame(self, bg=PANEL2, height=1).pack(fill="x", side="bottom")

        self._init_projects()
        self.show("script")
        # auto-save triggers (settings / avatar / export options)
        for v in self.sv.values():
            v.trace_add("write", self._settings_changed)
        for v in (self.av_for, self.av_every):
            v.trace_add("write", self._settings_changed)
        for v in (self.mode, self.out_dir, self.out_name):
            v.trace_add("write", self._meta_changed)
        self.bind_all("<Control-s>", lambda e: self.save_all())
        self.bind_all("<Command-s>", lambda e: self.save_all())
        self._dnd_setup()
        self.after(80, self._drain)
        threading.Thread(target=self._thumb_worker, daemon=True).start()
        self.after(500, self.check_requirements)
        self.after(1200, self.refresh_usage)
        self.after(20000, self._periodic)
        self._start_monitor()
        self.protocol("WM_DELETE_WINDOW", self._quit)
        self._fade_in()

    # ───────── error log / status notes ─────────

    # ───────── style / top bar / nav ─────────

    def _style(self):
        s = ttk.Style(self)
        s.theme_use("clam")
        s.configure("TCombobox", fieldbackground=PANEL2, background=PANEL2, foreground=FG,
                    arrowcolor=FG, bordercolor=PANEL2, lightcolor=PANEL2, darkcolor=PANEL2,
                    padding=5, selectbackground=PANEL2, selectforeground=FG)
        s.map("TCombobox", fieldbackground=[("readonly", PANEL2)], foreground=[("readonly", FG)],
              background=[("active", GHOST_HOV), ("readonly", PANEL2)],
              arrowcolor=[("active", ACCENT)],
              selectbackground=[("readonly", PANEL2)], selectforeground=[("readonly", FG)])
        self.option_add("*TCombobox*Listbox.background", PANEL2)
        self.option_add("*TCombobox*Listbox.foreground", FG)
        self.option_add("*TCombobox*Listbox.selectBackground", ACCENT)
        self.option_add("*TCombobox*Listbox.selectForeground", ACCENT_FG)
        s.configure("Horizontal.TProgressbar", troughcolor=PANEL, background=ACCENT, borderwidth=0)
        s.configure("Vertical.TScrollbar", background=PANEL2, troughcolor=BG, bordercolor=BG,
                    arrowcolor=MUTED, lightcolor=PANEL2, darkcolor=PANEL2, relief="flat", gripcount=0)
        s.map("Vertical.TScrollbar", background=[("pressed", ACCENT), ("active", MUTED)])
        s.configure("TScale", background=BG, troughcolor=PANEL2)

    def _build_top(self):
        t = tk.Frame(self, bg=SIDE, height=56)
        t.pack(fill="x")
        t.pack_propagate(False)
        tk.Frame(self, bg=PANEL2, height=1).pack(fill="x")
        logo = tk.Frame(t, bg=SIDE)
        logo.pack(side="left", padx=(18, 6))
        mklabel(logo, "◆", 15, ACCENT, True, bg=SIDE).pack(side="left")
        mklabel(logo, "  AI Video Editor", 13, FG, True, bg=SIDE).pack(side="left")
        self.pvar = tk.StringVar()
        self.pcombo = ttk.Combobox(t, textvariable=self.pvar, state="readonly", width=20)
        self.pcombo.pack(side="left", padx=(10, 8), pady=14)
        self.pcombo.bind("<<ComboboxSelected>>", lambda e: self._switch_from_combo())
        mkbtn(t, "＋ New", self.new_project, "ghost", pady=4, padx=11).pack(side="left", padx=3)
        mkbtn(t, "📂 Open…", self.open_dialog, "ghost", pady=4, padx=11).pack(side="left", padx=3)
        mkbtn(t, "💾 Save", lambda: self.save_all(), "ghost", pady=4, padx=11).pack(side="left", padx=3)
        mkbtn(t, "🗑 Clear All", self.clear_all, "ghost", pady=4, padx=11).pack(side="left", padx=3)
        menu = tk.Menu(self, tearoff=0, bg=PANEL2, fg=FG, activebackground=ACCENT, activeforeground=ACCENT_FG)
        menu.add_command(label="Save a copy…", command=self.save_copy)
        menu.add_command(label="Open project folder", command=lambda: open_path(self.proj))
        menu.add_command(label="Appearance…", command=lambda: self.show("settings"))
        if AUTH_ON:
            menu.add_separator()
            menu.add_command(label=f"👤 {self.session.get('name') or self.session.get('id') or ''}", state="disabled")
            menu.add_command(label="Check for updates now", command=lambda: self._check_now(True))
            menu.add_command(label="Logout", command=self.logout)
        mb = mkbtn(t, "⋯", lambda: menu.tk_popup(mb.winfo_rootx(), mb.winfo_rooty() + mb.winfo_height()),
                   "ghost", pady=4, padx=11)
        mb.pack(side="left", padx=3)
        self.save_lbl = mklabel(t, "", 9, MUTED, bg=SIDE)
        self.save_lbl.pack(side="left", padx=10)
        mkbtn(t, "Export ▶", lambda: self.show("export"), "primary", pady=6, padx=18).pack(side="right", padx=16)
        self.theme_btn = mkbtn(t, "◐", self.toggle_theme, "ghost", pady=4, padx=11)
        self.theme_btn.pack(side="right", padx=2)
        self.upd_btn = mkbtn(t, "⬆ Update", self.do_update, "primary", pady=4, padx=11)
        self.cache_btn = mkbtn(t, "🧹 Cache", self.clean_cache, "ghost", pady=4, padx=11)
        self.cache_btn.pack(side="right", padx=2)
        self.space_lbl = mklabel(t, "💾 …", 10, FG, True, bg=SIDE, cursor="hand2")
        self.space_lbl.pack(side="right", padx=10)
        self.space_lbl.bind("<Button-1>", lambda e: self.show_usage())

    def show(self, key):
        prev = self.cur
        slide = False
        if prev != key:
            self._tab_finish()
            if prev:
                self.frames[prev].place_forget()
                self.nav[prev].set_active(False)
            self.cur = key
            slide = prev is not None and ANIM_ON
            self.nav[key].set_active(True, animate=prev is not None)
            self.frames[key].place(x=34 if slide else 0, y=0, relwidth=1, relheight=1)
            self._move_ind(prev is not None)
        if key == "clips":
            self.refresh_clips()
        elif key == "export":
            self.refresh_export()
            self.refresh_usage()
        elif key == "audio":
            self.refresh_audio()
        elif key == "srt":
            self.refresh_srt()
        elif key == "avatar":
            self.refresh_avatar()
        if slide:
            self._tab_anim(self.frames[key])

    # ───────── look & feel: tab slide, nav indicator, themes, effects ─────────

    def _tab_finish(self):
        tween_cancel(self.content, "tab")
        if self.cur in self.frames:
            try:
                self.frames[self.cur].place_configure(x=0)
            except tk.TclError:
                pass

    def _tab_anim(self, fr):
        def step(t):
            fr.place_configure(x=int(34 * (1 - t)))
        tween(self.content, "tab", 230, step, done=lambda: fr.place_configure(x=0))

    def _move_ind(self, animate=True):
        b = self.nav.get(self.cur)
        if b is None or b.winfo_height() < 20:
            return
        y1, h = b.winfo_y() + 12, b.winfo_height() - 24
        y0 = self._ind_cur if self._ind_cur is not None else y1

        def step(t):
            self._ind_cur = y0 + (y1 - y0) * t
            self.nav_ind.place(x=0, y=int(self._ind_cur), width=3, height=h)
            self.nav_ind.lift()
        tween(self.nav_ind, "y", 260 if animate else 0, step)

    def _fade_in(self):
        try:
            self.attributes("-alpha", 0.0)
            tween(self, "alpha", 320, lambda t: self.attributes("-alpha", t),
                  done=lambda: self.attributes("-alpha", 1.0))
            self.after(1200, lambda: self.attributes("-alpha", 1.0))
        except tk.TclError:
            pass

    def toggle_theme(self):
        self.apply_look(theme="Dark" if not THEMES[THEME_NAME].get("dark", True) else "Light")

    def apply_look(self, theme=None, accent=None, anim=None):
        global ANIM_ON
        if anim is not None:
            ANIM_ON = bool(anim)
        if theme is not None or accent is not None:
            old = dict(PAL)
            new = apply_palette(theme, accent)
            mapping = {old[k].lower(): new[k] for k in _TOKENS if old[k].lower() != new[k].lower()}
            self._style()
            _recolor_tree(self, mapping)
            try:
                self.ph.put(PH_BG, to=(0, 0, 128, 72))
            except tk.TclError:
                pass
            self._move_ind(False)
        self._refresh_swatches()
        self.rec.update(theme=THEME_NAME, accent=ACCENT_RAW, anim=ANIM_ON)
        save_recent(self.rec)

    def pick_accent(self):
        c = colorchooser.askcolor(color=ACCENT_RAW, parent=self, title="Pick accent color")
        if c and c[1]:
            self.apply_look(accent=c[1].lower())

    def _refresh_swatches(self):
        if not getattr(self, "_theme_chips", None):
            return
        for name, (ring, box) in self._theme_chips.items():
            ring.configure(bg=ACCENT if name == THEME_NAME else PANEL)
            box._acc.configure(bg=ACCENT)
        cur = ACCENT_RAW.lower()
        for c, col in self._acc_dots:
            c.itemconfigure("ring", outline=FG if col.lower() == cur else "")
        custom = all(col.lower() != cur for _, col in ACCENTS)
        cc = self._acc_custom
        cc.itemconfigure("dot", fill=cur if custom else PANEL2)
        cc.itemconfigure("plus", fill=ACCENT_FG if custom and _lum(cur) <= 0.58 else (FG if not custom else "#0b1114"))
        cc.itemconfigure("ring", outline=FG if custom else "")

    def _done_fx(self, text="Done ✓"):
        lbl = self.state_lbl
        lbl.configure(text=text, fg=OK)
        try:
            self.pbar.flash()
        except Exception:
            pass
        if not ANIM_ON:
            return
        tween(lbl, "pop", 620,
              lambda t: lbl.configure(font=(FONT, 10 + int(round(6 * math.sin(math.pi * t))), "bold")),
              done=lambda: lbl.configure(font=(FONT, 10)), ease=False)
        self._burst(lbl)

    def _burst(self, anchor):
        for f, *_ in getattr(self, "_burst_parts", []):
            try:
                f.destroy()
            except tk.TclError:
                pass
        try:
            ax = anchor.winfo_rootx() - self.winfo_rootx() + anchor.winfo_width() // 2
            ay = anchor.winfo_rooty() - self.winfo_rooty() + anchor.winfo_height() // 2
        except tk.TclError:
            return
        cols = [OK, ACCENT, WARN, ACCENT_HOV]
        parts = []
        for i in range(12):
            ang = i / 12.0 * 2 * math.pi + random.uniform(-0.2, 0.2)
            sz = random.choice((4, 5, 6))
            f = tk.Frame(self, bg=cols[i % 4], width=sz, height=sz)
            f.place(x=ax, y=ay)
            parts.append((f, ang, random.uniform(28, 50), cols[i % 4]))
        self._burst_parts = parts
        bgc = BG

        def step(t):
            for f, ang, dist, col in parts:
                f.place(x=int(ax + math.cos(ang) * dist * t), y=int(ay + math.sin(ang) * dist * t))
                f.configure(bg=_mix(col, bgc, t ** 1.6))

        def done():
            for f, *_ in parts:
                try:
                    f.destroy()
                except tk.TclError:
                    pass
            self._burst_parts = []
        tween(self, "burst", 700, step, done)


    # ───────── storage usage / cache ─────────

    def header(self, parent, title, sub=""):
        h = tk.Frame(parent, bg=BG)
        h.pack(fill="x", padx=22, pady=(20, 4))
        mklabel(h, title, 19, FG, True).pack(side="left")
        if sub:
            mklabel(h, sub, 10, MUTED).pack(side="left", padx=16, pady=(7, 0))
        tk.Frame(parent, bg=PANEL2, height=1).pack(fill="x", padx=22, pady=(8, 12))
        return h

    # ───────── projects ─────────

    def project_list(self):
        os.makedirs(WORKSPACE, exist_ok=True)
        items = []
        for n in sorted(os.listdir(WORKSPACE), key=str.lower):
            p = os.path.join(WORKSPACE, n)
            if os.path.isdir(p) and not n.startswith((".", "_")):
                items.append((n, p))
        for p in self.rec.get("external", []):
            if os.path.isdir(p) and all(p != q for _, q in items):
                items.append((f"{os.path.basename(p)}  (external)", p))
        return items

    def _init_projects(self):
        items = self.project_list()
        last = self.rec.get("last", "")
        if not items:
            p = os.path.join(WORKSPACE, "My First Project")
            ensure_project(p)
            items = self.project_list()
            last = p
        if not any(p == last for _, p in items):
            last = items[0][1]
        self.load_project(last)

    def load_project(self, path):
        ensure_project(path)
        self.proj = path
        self.rec["last"] = path
        save_recent(self.rec)
        items = self.project_list()
        self._pmap = {n: p for n, p in items}
        self.pcombo["values"] = [n for n, _ in items]
        for n, p in items:
            if p == path:
                self.pvar.set(n)
        self.title(f"AI Video Editor v{APP_VERSION} — {os.path.basename(path)}")
        self.statusbar.configure(text=f"Project folder: {path}", fg=MUTED)
        self._loading = True
        self.script_txt.delete("1.0", "end")
        sp = os.path.join(path, "script.txt")
        txt = read_text(sp)
        self.script_txt.insert("1.0", txt)
        self._script_saved = txt
        self._srt_saved = None
        self.script_txt.edit_reset()
        self.script_txt.edit_modified(False)
        self._loading = False
        self.update_script_count()
        self.load_meta()
        self.load_settings()
        self.load_avatar_fields()
        self.save_lbl.configure(text="✓ Loaded", fg=MUTED)
        if self.cur:
            self.show(self.cur)
        self.refresh_usage()

    def _switch_from_combo(self):
        n = self.pvar.get()
        if self.proc or self.busy:
            messagebox.showinfo("Busy", "Kaj cholche — shesh hole project change koro.")
            self.pvar.set(next((k for k, v in self._pmap.items() if v == self.proj), ""))
            return
        self.save_all(quiet=True)
        self.load_project(self._pmap[n])

    def new_project(self):
        if self.proc or self.busy:
            return
        name = simpledialog.askstring("New project", "Project name:", parent=self)
        if not name:
            return
        name = re.sub(r'[\\/:*?"<>|]', "_", name.strip())
        p = os.path.join(WORKSPACE, name)
        if os.path.exists(p):
            messagebox.showerror("Exists", "Ei naam e project ager theke ache.")
            return
        self.save_all(quiet=True)
        ensure_project(p, copy_cfg_from=self.proj)   # settings/API key copy hoy
        self.load_project(p)
        self.show("script")

    def open_folder_project(self):
        d = filedialog.askdirectory(title="Project folder select koro", initialdir=WORKSPACE)
        if d:
            self.open_project_path(d)

    # ───────── SCRIPT ─────────

    def _build_script(self, f):
        h = self.header(f, "Script", "Ek line = ek sentence. Auto-save hoy. .txt drag & drop kore dhukao / bahire nao.")
        self.script_count = mklabel(h, "", 10, ACCENT)
        self.script_count.pack(side="right")
        mkbtn(h, "Import .txt…", self.import_script, "ghost", pady=4).pack(side="right", padx=10)
        mkbtn(h, "💾 Save copy…", self.save_script_copy, "ghost", pady=4).pack(side="right")
        self.script_drag = mklabel(f, "⠿  Script ta drag kore bahire (desktop / folder e) felo  —  script.txt hishebe jabe",
                                   10, MUTED, bg=PANEL2, padx=14, pady=7, cursor="hand2")
        self.script_drag.pack(anchor="w", padx=22, pady=(0, 10))
        self.script_txt = mktext(f)
        self.script_txt.pack(fill="both", expand=True, padx=22, pady=(0, 18))
        self.script_txt.bind("<<Modified>>", self._script_modified)

    def _script_modified(self, e=None):
        if self._loading or not self.script_txt.edit_modified():
            return
        self.script_txt.edit_modified(False)
        if self._save_job:
            self.after_cancel(self._save_job)
        self._save_job = self.after(700, self.flush_script)
        self.update_script_count()

    def flush_script(self):
        if self._save_job:
            self.after_cancel(self._save_job)
            self._save_job = None
        if not self.proj:
            return
        txt = self.script_txt.get("1.0", "end-1c")
        if txt != self._script_saved:
            atomic_write(os.path.join(self.proj, "script.txt"), txt)
            self._script_saved = txt
            self._stamp()
        self.update_script_count()

    def update_script_count(self):
        n = len([l for l in self.script_txt.get("1.0", "end-1c").splitlines()
                 if l.strip() and l.strip() != "---"])
        count_to(self.script_count, n, "{} sentences")

    def import_script(self):
        p = filedialog.askopenfilename(filetypes=[("Text", "*.txt"), ("All", "*.*")])
        if p:
            self.set_script_file(p)

    def _script_file_ready(self):
        """Latest script ke script.txt e save kore path dey (faka hole None)."""
        if not self.proj or not self.script_txt.get("1.0", "end-1c").strip():
            return None
        self.flush_script()
        p = os.path.join(self.proj, "script.txt")
        return p if os.path.exists(p) else None

    def save_script_copy(self):
        p = self._script_file_ready()
        if not p:
            messagebox.showinfo("Script", "Script faka — save korar moto kichu nai.")
            return
        dst = filedialog.asksaveasfilename(initialfile="script.txt", defaultextension=".txt",
                                           filetypes=[("Text", "*.txt"), ("All", "*.*")])
        if dst:
            try:
                shutil.copyfile(p, dst)
                self.note("✓ Script copy save hoyeche", OK)
            except Exception as e:
                messagebox.showerror("Save copy", f"Copy kora gelo na: {e}")

    def _script_drag_init(self, event):
        """Script bahire drag (copy) — project er script.txt thakei."""
        p = self._script_file_ready()
        if not p:
            return "refuse_drop"
        self._drag_out = True
        return ("copy", DND_FILES, (os.path.abspath(p).replace("\\", "/"),))

    # ───────── AUDIO ─────────

    # ───────── AUDIO ─────────

    def _build_audio(self, f):
        self.header(f, "Audio", "Voiceover — ekta file, othoba 1,2,3… naam e multiple file (auto join hobe). Audio bahire drag kore nite paro.")
        card = tk.Frame(f, bg=PANEL)
        card.pack(fill="x", padx=22, pady=6)
        self.audio_name = mklabel(card, "", 13, FG, True, bg=PANEL)
        self.audio_name.pack(anchor="w", padx=20, pady=(18, 2))
        self.audio_info = mklabel(card, "", 10, MUTED, bg=PANEL)
        self.audio_info.pack(anchor="w", padx=20, pady=(0, 10))
        self.audio_drag = mklabel(card, "⠿  Ei audio ta drag kore bahire (desktop / folder e) felo", 10, MUTED,
                                  bg=PANEL2, padx=14, pady=8, cursor="hand2")
        self.audio_drag.pack(anchor="w", padx=20, pady=(0, 14))
        row = tk.Frame(card, bg=PANEL)
        row.pack(anchor="w", padx=20, pady=(0, 18))
        mkbtn(row, "＋ Import audio(s)…", self.import_audio, "primary").pack(side="left")
        self.audio_play = mkbtn(row, "▶ Play", lambda: open_path(self.audio_path()), "ghost")
        self.audio_play.pack(side="left", padx=8)
        self.audio_save = mkbtn(row, "💾 Save copy…", self.save_audio_copy, "ghost")
        self.audio_save.pack(side="left", padx=(0, 8))
        self.audio_rm = mkbtn(row, "Remove", self.remove_audio, "ghost")
        self.audio_rm.pack(side="left")
        mklabel(f, "🎯 Ekhane audio file (mp3/wav/m4a…) drag kore drop koro.  Notun audio dile purano ta replace hobe.\n"
                "Multiple audio dite hole nam serially 1, 2, 3, … hote hobe (1.mp3, 2.mp3, 3.mp3) — tahole number onujayi "
                "joure ekta audio hoye jabe.\nNam serial na hole multiple audio add hobe na, shudhu ekta audio dile hobe.",
                9, MUTED, justify="left").pack(anchor="w", padx=24, pady=8)

    def audio_path(self):
        for fn in sorted(os.listdir(self.proj)):
            if os.path.splitext(fn)[1].lower() in AUDIO_EXTS:
                return os.path.join(self.proj, fn)
        return None

    def refresh_audio(self):
        p = self.audio_path()
        if p:
            self.audio_name.configure(text="🎵  " + os.path.basename(p))
            self.audio_info.configure(
                text=f"Duration: {fmt_dur(media_duration(p))}   •   {os.path.getsize(p) / 1e6:.1f} MB")
        else:
            self.audio_name.configure(text="No audio yet")
            self.audio_info.configure(text="Import your voiceover (mp3, wav, m4a, aac, ogg, flac)")
        st = "normal" if p else "disabled"
        self.audio_play.configure(state=st)
        self.audio_save.configure(state=st)
        self.audio_rm.configure(state=st)
        self.audio_drag.configure(
            fg=FG if p else DISABLED,
            text=("⠿  Ei audio ta drag kore bahire (desktop / folder e) felo" if DND_OK
                  else "Drag out off — 'Save copy…' button use koro") if p else "⠿  Drag korar moto audio nai")

    def import_audio(self):
        ps = filedialog.askopenfilenames(
            filetypes=[("Audio", "*.mp3 *.wav *.m4a *.aac *.ogg *.flac")])
        if ps:
            self.set_audios(list(ps))
            self.refresh_usage()

    def remove_audio(self):
        p = self.audio_path()
        if p and messagebox.askyesno("Remove", "Audio ta remove korbe?"):
            archive(p, self.proj)
            self.refresh_audio()
            self.refresh_usage()

    def save_audio_copy(self):
        p = self.audio_path()
        if not p:
            return
        ext = os.path.splitext(p)[1]
        dst = filedialog.asksaveasfilename(initialfile=os.path.basename(p), defaultextension=ext,
                                           filetypes=[("Audio", "*" + ext), ("All", "*.*")])
        if dst:
            try:
                fast_copy(p, dst)
                self.note("✓ Audio copy save hoyeche", OK)
            except Exception as e:
                messagebox.showerror("Save copy", f"Copy kora gelo na: {e}")

    def _audio_drag_init(self, event):
        """Audio section theke file bahire drag (copy) — project er original file ta thakei."""
        p = self.audio_path()
        if not p or self._merging:
            return "refuse_drop"
        self._drag_out = True
        return ("copy", DND_FILES, (os.path.abspath(p).replace("\\", "/"),))

    def _audio_drag_end(self, event):
        self.after(300, lambda: setattr(self, "_drag_out", False))
        return event.action

    # ───────── SRT ─────────

    # ───────── SRT ─────────

    def _build_srt(self, f):
        h = self.header(f, "SRT", "Optional — thakle timing ekdom accurate hoy. .srt drag & drop korte paro.")
        mkbtn(h, "Remove", self.remove_srt, "ghost", pady=4).pack(side="right")
        mkbtn(h, "Import .srt…", self.import_srt, "primary", pady=4).pack(side="right", padx=8)
        self.srt_info = mklabel(f, "", 10, MUTED)
        self.srt_info.pack(anchor="w", padx=24, pady=(0, 6))
        self.srt_txt = mktext(f)
        self.srt_txt.pack(fill="both", expand=True, padx=22, pady=(0, 6))
        self.srt_txt.bind("<<Modified>>", self._srt_modified)
        r = tk.Frame(f, bg=BG)
        r.pack(fill="x", padx=22, pady=(0, 16))
        self.srt_state = mklabel(r, "✎ Edit korle auto-save hoy — Save button dorkar nei.", 9, MUTED)
        self.srt_state.pack(side="left")

    def srt_path(self):
        for fn in sorted(os.listdir(self.proj)):
            if fn.lower().endswith(".srt"):
                return os.path.join(self.proj, fn)
        return None

    def refresh_srt(self):
        p = self.srt_path()
        self._srt_loading = True
        self.srt_txt.delete("1.0", "end")
        if p:
            txt = read_text(p)
            self.srt_txt.insert("1.0", txt)
            self._srt_saved = txt
            self._srt_info(p)
        else:
            self._srt_saved = ""
            self.srt_info.configure(text="No SRT — audio r length onujayi timing andaj hobe (SRT dile ekdom accurate hoy).")
        self.srt_txt.edit_reset()
        self.srt_txt.edit_modified(False)
        self._srt_loading = False

    def import_srt(self):
        p = filedialog.askopenfilename(filetypes=[("SRT", "*.srt")])
        if p:
            self.set_srt(p)

    def save_srt(self):
        self.flush_srt()

    def remove_srt(self):
        p = self.srt_path()
        if p and messagebox.askyesno("Remove", "SRT remove korbe?"):
            archive(p, self.proj)
            self.refresh_srt()

    # ───────── CLIPS ─────────

    # ───────── CLIPS ─────────

    def _build_clips(self, f):
        h = self.header(f, "Clips", "Prottek sentence er jonno clip/image — drag & drop korte paro")
        mkbtn(h, "Clear all", self.clear_clips, "ghost", pady=4).pack(side="right")
        mkbtn(h, "Bulk import…", self.bulk_import, "primary", pady=4).pack(side="right", padx=8)
        self.clips_banner = mklabel(f, "", 10, MUTED, anchor="w", justify="left")
        self.clips_banner.pack(fill="x", padx=24, pady=(0, 6))
        wrap = tk.Frame(f, bg=BG)
        wrap.pack(fill="both", expand=True, padx=14, pady=(0, 14))
        self.cv = tk.Canvas(wrap, bg=BG, highlightthickness=0)
        sb = ttk.Scrollbar(wrap, orient="vertical", command=self.cv.yview)
        self.cv.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.cv.pack(side="left", fill="both", expand=True)
        self.clip_inner = tk.Frame(self.cv, bg=BG)
        self.cv_win = self.cv.create_window((0, 0), window=self.clip_inner, anchor="nw")
        self.clip_inner.bind("<Configure>", lambda e: self.cv.configure(scrollregion=self.cv.bbox("all")))
        self.cv.bind("<Configure>", lambda e: self.cv.itemconfigure(self.cv_win, width=e.width))
        self.cv.bind("<Enter>", self._wheel_on)
        self.cv.bind("<Leave>", self._wheel_off)

    def _wheel(self, e):
        if getattr(e, "num", 0) == 4:            # Linux
            n = -1
        elif getattr(e, "num", 0) == 5:
            n = 1
        elif sys.platform == "darwin":           # Mac: delta chhoto (±1, ±2…)
            n = -int(e.delta) if abs(e.delta) < 40 else -int(e.delta / 40)
            n = max(-6, min(6, n)) or (-1 if e.delta > 0 else 1)
        else:                                    # Windows: 120 per notch
            n = int(-e.delta / 120)
        self.cv.yview_scroll(n, "units")

    def clips_dir(self):
        d = os.path.join(self.proj, "clips")
        os.makedirs(d, exist_ok=True)
        return d

    def refresh_clips(self):
        self.flush_script()
        for w in self.clip_inner.winfo_children():
            w.destroy()
        self.thumb_labels.clear()
        try:
            while True:
                self.thumb_q.get_nowait()
        except queue.Empty:
            pass
        sents = sentences_of(os.path.join(self.proj, "script.txt"))
        clips = scan_clips(self.clips_dir())
        total = sum(len(v) for v in clips.values())
        multi = sum(1 for v in clips.values() if len(v) > 1)
        cfg = cfg_read(self.proj)
        cov = set()
        if self.mode.get() == 2:
            try:
                cov = covered_by_avatar(len(sents), int(cfg.get("AVATAR_SHOW_FOR", "2") or 2),
                                        int(cfg.get("AVATAR_SHOW_EVERY", "6") or 6))
            except ValueError:
                pass
        if total:
            self.clips_banner.configure(
                text=f"MANUAL mode  •  {total} clips  •  {multi} sentence e ekadhik clip (1a, 1b…)  •  "
                     "jei sentence e clip nei, ager clip reuse hobe.\n"
                     "💡 File ke 1a, 1b, 2a… naam diye drop korle naam onujayi sentence e boshbe.  "
                     "Kono row te drop = oi sentence e add;  kono clip er upor drop = oi clip replace.",
                fg=OK)
        else:
            self.clips_banner.configure(
                text="AUTO mode (kono clip nai) — Pexels/Pixabay theke auto khuje.\n"
                     "💡 Clips drag & drop koro: 1a, 1b, 2a, 2b, 3 … naam dile naam onujayi sentence e boshbe.",
                fg=WARN)
        if not sents:
            mklabel(self.clip_inner, "Age Script tab e script likho.", 11, MUTED).pack(pady=40)
            return
        for i, s in enumerate(sents, 1):
            row = tk.Frame(self.clip_inner, bg=PANEL)
            row.pack(fill="x", padx=8, pady=3)
            row._drop = ("add", i)
            row.columnconfigure(1, weight=1)
            mklabel(row, f"#{i}", 12, ACCENT, True, bg=PANEL, width=4).grid(row=0, column=0, padx=(10, 4), pady=10, sticky="n")
            txt = s if len(s) < 130 else s[:127] + "…"
            tl = mklabel(row, txt, 10, FG, bg=PANEL, wraplength=340, justify="left", anchor="w")
            tl.grid(row=0, column=1, sticky="nw", pady=10)
            if (i - 1) in cov:
                mklabel(row, "🧑 Avatar covers this", 9, WARN, bg=PANEL).grid(row=1, column=1, sticky="w", pady=(0, 8))
            strip = tk.Frame(row, bg=PANEL)
            strip.grid(row=0, column=2, rowspan=2, padx=8, pady=8, sticky="e")
            for var, path in clips.get(i, []):
                self._thumb_widget(strip, path, i)
            mkbtn(strip, "＋", lambda i=i: self.add_clip_to(i), "flat", padx=14, pady=22).pack(side="left", padx=4)
        self._dnd_register_tree(self.clip_inner)

    def _thumb_widget(self, parent, path, idx):
        box = tk.Frame(parent, bg=PANEL)
        box.pack(side="left", padx=4)
        box._drop = ("replace", path, idx)
        ext = os.path.splitext(path)[1].lower()
        lb = tk.Label(box, image=self.ph, bg=PANEL, cursor="hand2", bd=0,
                      text="VIDEO" if ext in VIDEO_EXTS else "IMG", fg=MUTED,
                      compound="center", font=(FONT, 8))
        lb.pack()
        mklabel(box, os.path.basename(path)[:18], 8, FG, True, bg=PANEL).pack()
        bt = tk.Frame(box, bg=PANEL)
        bt.pack(pady=(2, 0))
        mkbtn(bt, "⟳", lambda p=path: self.replace_clip(p), "ghost", padx=7, pady=0).pack(side="left", padx=2)
        mkbtn(bt, "✕", lambda p=path: self.remove_clip(p), "danger", padx=7, pady=0).pack(side="left", padx=2)
        lb.bind("<Button-1>", lambda e, p=path: open_path(p))
        lb.bind("<Button-3>", lambda e, p=path, i=idx: self._clip_menu(e, p, i))
        self.thumb_labels[path] = lb
        self.thumb_q.put(path)

    def _clip_menu(self, e, path, idx):
        m = tk.Menu(self, tearoff=0, bg=PANEL2, fg=FG, activebackground=ACCENT, activeforeground=ACCENT_FG)
        m.add_command(label="▶ Preview", command=lambda: open_path(path))
        m.add_command(label="↔ Move to sentence #…", command=lambda: self.move_clip(path, idx))
        m.add_command(label="⟳ Replace…", command=lambda: self.replace_clip(path))
        m.add_separator()
        m.add_command(label="✕ Remove", command=lambda: self.remove_clip(path))
        m.tk_popup(e.x_root, e.y_root)

    def add_clip_to(self, idx):
        fs = filedialog.askopenfilenames(title=f"Sentence #{idx} er clip/image", filetypes=self.MEDIA_TYPES)
        if fs:
            self.add_media(list(fs), ("add", idx))

    def bulk_import(self):
        fs = filedialog.askopenfilenames(title="Clips (1a, 1b, 2a… naam onujayi sentence e boshbe)",
                                         filetypes=self.MEDIA_TYPES)
        if fs:
            self.add_media(list(fs), None)

    def move_clip(self, path, idx):
        n = len(sentences_of(os.path.join(self.proj, "script.txt")))
        to = simpledialog.askinteger("Move", f"Kon sentence e (1–{n})?", parent=self,
                                     minvalue=1, maxvalue=max(n, 1))
        if not to or to == idx:
            return
        tmp = os.path.join(self.clips_dir(), "_mv" + os.path.splitext(path)[1].lower())
        os.replace(path, tmp)
        place_clip(tmp, self.clips_dir(), to)
        os.remove(tmp)
        self.refresh_clips()

    def replace_clip(self, path):
        p = filedialog.askopenfilename(title="Notun clip/image", filetypes=self.MEDIA_TYPES)
        if not p:
            return
        self._replace_with(path, p)
        self.refresh_clips()
        self.refresh_usage()

    def remove_clip(self, path):
        archive(path, self.proj)
        self.refresh_clips()
        self.refresh_usage()

    def clear_clips(self):
        if messagebox.askyesno("Clear", "Sob clips remove korbe?\n(Tomar original file gulo thikই thakbe — project er copy muchbe.)"):
            for fn in os.listdir(self.clips_dir()):
                archive(os.path.join(self.clips_dir(), fn), self.proj)
            self.refresh_clips()
            self.refresh_usage()

    # thumbnails (ffmpeg, background)

    # thumbnails (ffmpeg, background)

    def _thumb_cache(self, path):
        st = os.stat(path)
        k = hashlib.md5(f"{path}{st.st_mtime}{st.st_size}".encode()).hexdigest()[:16]
        d = os.path.join(self.proj, "_thumbs")
        os.makedirs(d, exist_ok=True)
        return os.path.join(d, k + ".png")

    def _thumb_worker(self):
        while True:
            path = self.thumb_q.get()
            try:
                out = self._thumb_cache(path)
                ok = os.path.exists(out) or self._make_thumb(path, out)
                if ok:
                    self.q.put(("thumb", (path, out)))
                elif ok is None:
                    self.q.put(("thumb_fail", None))
            except Exception:
                pass

    def _thumb_pump(self):
        pass

    def _set_thumb(self, path, png):
        lb = self.thumb_labels.get(path)
        if not lb:
            return
        try:
            img = tk.PhotoImage(file=png)
            lb.configure(image=img, text="")
            lb.image = img
        except Exception:
            pass

    # ───────── AVATAR ─────────

    def _build_avatar(self, f):
        self.header(f, "Avatar", "Option 2 mode er jonno")
        card = tk.Frame(f, bg=PANEL)
        card.pack(fill="x", padx=22, pady=6)
        self.av_name = mklabel(card, "", 13, FG, True, bg=PANEL)
        self.av_name.pack(anchor="w", padx=20, pady=(18, 2))
        self.av_info = mklabel(card, "", 10, MUTED, bg=PANEL)
        self.av_info.pack(anchor="w", padx=20, pady=(0, 14))
        row = tk.Frame(card, bg=PANEL)
        row.pack(anchor="w", padx=20, pady=(0, 18))
        mkbtn(row, "＋ Import avatar video…", self.import_avatar, "primary").pack(side="left")
        self.av_play = mkbtn(row, "▶ Play", lambda: open_path(self.avatar_path()), "ghost")
        self.av_play.pack(side="left", padx=8)
        self.av_rm = mkbtn(row, "Remove", self.remove_avatar, "ghost")
        self.av_rm.pack(side="left")

        pat = tk.Frame(f, bg=PANEL)
        pat.pack(fill="x", padx=22, pady=10)
        mklabel(pat, "Avatar pattern", 11, FG, True, bg=PANEL).grid(row=0, column=0, columnspan=4, sticky="w", padx=20, pady=(14, 8))
        self.av_for, self.av_every = tk.StringVar(), tk.StringVar()
        mklabel(pat, "Show for", 10, MUTED, bg=PANEL).grid(row=1, column=0, padx=(20, 6), pady=(0, 16))
        mkentry(pat, self.av_for, 5).grid(row=1, column=1)
        mklabel(pat, "sentence(s), then hide for", 10, MUTED, bg=PANEL).grid(row=1, column=2, padx=8)
        mkentry(pat, self.av_every, 5).grid(row=1, column=3, padx=(0, 8))
        mklabel(pat, "sentence(s)", 10, MUTED, bg=PANEL).grid(row=1, column=4)
        mkbtn(pat, "Save", self.save_avatar_fields, "ghost", pady=4).grid(row=1, column=5, padx=16)

    def load_avatar_fields(self):
        c = cfg_read(self.proj)
        self.av_for.set(c.get("AVATAR_SHOW_FOR", "2"))
        self.av_every.set(c.get("AVATAR_SHOW_EVERY", "6"))

    def save_avatar_fields(self, silent=False):
        try:
            a, b = int(self.av_for.get()), int(self.av_every.get())
        except ValueError:
            if not silent:
                messagebox.showerror("Error", "Duto-i number hote hobe.")
            return False
        cfg_write(self.proj, {"AVATAR_SHOW_FOR": a, "AVATAR_SHOW_EVERY": b})
        if not silent:
            messagebox.showinfo("Saved", "Avatar pattern saved.")
        return True

    def avatar_path(self):
        for fn in os.listdir(self.proj):
            if fn.lower().startswith("avatar") and os.path.splitext(fn)[1].lower() in VIDEO_EXTS:
                return os.path.join(self.proj, fn)
        return None

    def refresh_avatar(self):
        p = self.avatar_path()
        if p:
            self.av_name.configure(text="🧑  " + os.path.basename(p))
            self.av_info.configure(text=f"Duration: {fmt_dur(media_duration(p))}")
        else:
            self.av_name.configure(text="No avatar video")
            self.av_info.configure(text="Shudhu Option 2 (Avatar) mode e lagbe.")
        st = "normal" if p else "disabled"
        self.av_play.configure(state=st)
        self.av_rm.configure(state=st)

    def import_avatar(self):
        p = filedialog.askopenfilename(filetypes=[("Video", "*.mp4 *.mov *.avi *.mkv *.webm")])
        if p:
            self.set_avatar(p)
            self.refresh_usage()

    # ───────── SETTINGS ─────────

    def remove_avatar(self):
        p = self.avatar_path()
        if p and messagebox.askyesno("Remove", "Avatar remove korbe?"):
            archive(p, self.proj)
            self.refresh_avatar()

    # ───────── SETTINGS ─────────

    def _build_settings(self, f):
        self.header(f, "Settings", "Auto-save hoy — kichu change korlei save hoye jay")
        sf = ScrollFrame(f)
        sf.pack(fill="both", expand=True, padx=22)
        cv = sf.inner
        self.sv = {k: tk.StringVar() for k in
                   ["OUTPUT_RATIO", "OUTPUT_RESOLUTION", "VOLUME", "TRANSITION_SPEED", "ENCODER",
                    "PRESET", "QUALITY", "PEXELS_API_KEY", "PIXABAY_API_KEY", "USE_SAVED_QUERIES"]}
        self.vol_pct = tk.IntVar(value=100)

        def group(title):
            g = tk.Frame(cv, bg=PANEL)
            g.pack(fill="x", pady=5)
            mklabel(g, title, 11, ACCENT, True, bg=PANEL).grid(row=0, column=0, columnspan=4, sticky="w", padx=18, pady=(12, 6))
            return g

        def row(g, r, label, widget, hint=""):
            mklabel(g, label, 10, FG, bg=PANEL).grid(row=r, column=0, sticky="w", padx=(18, 12), pady=5)
            widget.grid(row=r, column=1, sticky="w", pady=5)
            if hint:
                mklabel(g, hint, 9, MUTED, bg=PANEL).grid(row=r, column=2, sticky="w", padx=12)

        g = group("Appearance")
        mklabel(g, "Theme", 10, FG, bg=PANEL).grid(row=1, column=0, sticky="nw", padx=(18, 12), pady=(8, 5))
        tf = tk.Frame(g, bg=PANEL)
        tf.grid(row=1, column=1, columnspan=3, sticky="w", pady=(6, 0))
        self._theme_chips = {}
        for i, (tname, th) in enumerate(THEMES.items()):
            cell = tk.Frame(tf, bg=PANEL)
            cell.grid(row=i // 4, column=i % 4, padx=(0, 12), pady=(0, 8))
            ring = tk.Frame(cell, bg=PANEL, padx=2, pady=2, cursor="hand2")
            ring.pack()
            box = tk.Frame(ring, bg=th["BG"], width=92, height=56, cursor="hand2")
            box._no_theme = True                      # preview keeps that theme's own colors
            box.pack()
            box.pack_propagate(False)
            kids = [box]
            for colr, geo in ((th["SIDE"], dict(x=0, y=0, width=20, relheight=1)),
                              (th["PANEL"], dict(x=28, y=8, width=56, height=24))):
                p = tk.Frame(box, bg=colr, cursor="hand2")
                p.place(**geo)
                kids.append(p)
            box._acc = tk.Frame(box, bg=ACCENT, cursor="hand2")
            box._acc.place(x=28, y=40, width=34, height=6)
            kids.append(box._acc)
            lb = mklabel(cell, tname, 9, MUTED, bg=PANEL, cursor="hand2")
            lb.pack(pady=(3, 0))
            for w in [ring, lb] + kids:
                w.bind("<Button-1>", lambda e, n=tname: self.apply_look(theme=n))
            self._theme_chips[tname] = (ring, box)
        mklabel(g, "Accent color", 10, FG, bg=PANEL).grid(row=2, column=0, sticky="w", padx=(18, 12), pady=5)
        af = tk.Frame(g, bg=PANEL)
        af.grid(row=2, column=1, columnspan=3, sticky="w", pady=5)
        self._acc_dots = []
        for aname, col in ACCENTS:
            c = tk.Canvas(af, width=32, height=32, bg=PANEL, highlightthickness=0, cursor="hand2")
            c.create_oval(7, 7, 25, 25, fill=col, outline="", tags="dot")
            c.create_oval(2, 2, 30, 30, outline="", width=2, tags="ring")
            c.bind("<Button-1>", lambda e, v=col: self.apply_look(accent=v))
            c.pack(side="left", padx=2)
            self._acc_dots.append((c, col))
        c = tk.Canvas(af, width=32, height=32, bg=PANEL, highlightthickness=0, cursor="hand2")
        c.create_oval(7, 7, 25, 25, fill=PANEL2, outline="", tags="dot")
        c.create_text(16, 16, text="＋", fill=FG, font=(FONT, 10, "bold"), tags="plus")
        c.create_oval(2, 2, 30, 30, outline="", width=2, tags="ring")
        c.bind("<Button-1>", lambda e: self.pick_accent())
        c.pack(side="left", padx=(8, 2))
        self._acc_custom = c
        self._anim_var = tk.IntVar(value=1 if ANIM_ON else 0)
        tk.Checkbutton(g, text="Animations (hover, slide, smooth progress)", variable=self._anim_var,
                       bg=PANEL, fg=FG, selectcolor=PANEL2, activebackground=PANEL, activeforeground=FG,
                       font=(FONT, 10), highlightthickness=0,
                       command=lambda: self.apply_look(anim=bool(self._anim_var.get()))
                       ).grid(row=3, column=0, columnspan=3, sticky="w", padx=14, pady=(2, 12))
        self._refresh_swatches()
        g = group("Output")
        cb = ttk.Combobox(g, textvariable=self.sv["OUTPUT_RATIO"], values=["16:9", "9:16", "1:1", "4:3"], state="readonly", width=10)
        row(g, 1, "Ratio", cb)
        row(g, 2, "Resolution", mkentry(g, self.sv["OUTPUT_RESOLUTION"], 14), "optional, e.g. 1080x1920 (ratio ke override kore)")
        g = group("Audio & style")
        vs = Slider(g, self.vol_pct, 10, 400, 5, length=220, command=self._vol_changed, bg=PANEL)
        row(g, 1, "Voiceover volume", vs)
        self.vol_lbl = mklabel(g, "100%", 11, ACCENT, True, bg=PANEL)
        self.vol_lbl.grid(row=1, column=2, sticky="w", padx=12)
        mklabel(g, "100% = normal • 150% = boro • 10% = khub aste", 9, MUTED, bg=PANEL).grid(row=1, column=3, sticky="w")
        sc = Slider(g, self.sv["TRANSITION_SPEED"], 0, 20, 1, length=220, show_value=True, bg=PANEL)
        row(g, 2, "Transition speed", sc, "0 – 20")
        g = group("Encoder")
        row(g, 1, "Encoder", ttk.Combobox(g, textvariable=self.sv["ENCODER"], values=["auto", "gpu", "cpu"], state="readonly", width=10), "auto = GPU thakle GPU")
        row(g, 2, "Preset", mkentry(g, self.sv["PRESET"], 10), "optional (cpu: veryfast.. / gpu: p1..p7)")
        row(g, 3, "Quality", mkentry(g, self.sv["QUALITY"], 10), "optional (lower = better, default 20)")
        g = group("Stock footage (AUTO mode)")
        row(g, 1, "Pexels API key", mkentry(g, self.sv["PEXELS_API_KEY"], 44))
        row(g, 2, "Pixabay API key", mkentry(g, self.sv["PIXABAY_API_KEY"], 44))
        ck = tk.Checkbutton(g, text="Saved queries.json use koro (query abar toiri korbe na)",
                            variable=self.sv["USE_SAVED_QUERIES"], onvalue="1", offvalue="0",
                            bg=PANEL, fg=FG, selectcolor=PANEL2, activebackground=PANEL, activeforeground=FG,
                            font=(FONT, 10), highlightthickness=0)
        ck.grid(row=3, column=0, columnspan=3, sticky="w", padx=14, pady=(2, 12))
        b = tk.Frame(f, bg=BG)
        b.pack(fill="x", padx=22, pady=12, side="bottom")
        mkbtn(b, "Save settings", self.save_settings, "primary").pack(side="left")
        mkbtn(b, "Open config.txt", lambda: open_path(os.path.join(self.proj, "config.txt")), "ghost").pack(side="left", padx=8)

    def load_settings(self):
        c = cfg_read(self.proj)
        d = {"OUTPUT_RATIO": "16:9", "VOLUME": "1.0", "TRANSITION_SPEED": "10", "ENCODER": "auto",
             "USE_SAVED_QUERIES": "0"}
        was = self._loading
        self._loading = True
        try:
            for k, v in self.sv.items():
                v.set(c.get(k, d.get(k, "")))
            self.vol_pct.set(parse_volume_pct(c.get("VOLUME", "1.0")))
            count_to(self.vol_lbl, self.vol_pct.get(), "{}%", 0)
        finally:
            self._loading = was

    def save_settings(self, silent=False):
        res = self.sv["OUTPUT_RESOLUTION"].get().strip()
        if res and not re.fullmatch(r"\d+x\d+", res):
            if not silent:
                messagebox.showerror("Resolution", "Format: 1080x1920")
            return False
        cfg_write(self.proj, {k: v.get().strip() for k, v in self.sv.items()})
        if not silent:
            messagebox.showinfo("Saved", "Settings saved.")
        return True

    # ───────── EXPORT ─────────

    # ───────── EXPORT ─────────

    def _build_export(self, f):
        self.header(f, "Export", "Video toiri koro")
        top = tk.Frame(f, bg=BG)
        top.pack(fill="x", padx=22)
        left = tk.Frame(top, bg=PANEL)
        left.pack(side="left", fill="both", expand=True, padx=(0, 8))
        self.chk = {}
        for k in ["Script", "Audio", "SRT", "Clips", "Avatar", "Python", "FFmpeg"]:
            r = tk.Frame(left, bg=PANEL)
            r.pack(fill="x", padx=16, pady=2)
            mklabel(r, k, 10, MUTED, bg=PANEL, width=9, anchor="w").pack(side="left")
            self.chk[k] = mklabel(r, "", 10, FG, bg=PANEL, anchor="w")
            self.chk[k].pack(side="left")
        left.pack_configure(pady=0)
        mklabel(left, "", 4, bg=PANEL).pack()
        right = tk.Frame(top, bg=PANEL)
        right.pack(side="left", fill="y", padx=(8, 0))
        mklabel(right, "Mode", 11, FG, True, bg=PANEL).pack(anchor="w", padx=18, pady=(14, 6))
        for v, t in [(1, "Normal — clips + voiceover"), (2, "Avatar — clips + voiceover + avatar")]:
            tk.Radiobutton(right, text=t, variable=self.mode, value=v, bg=PANEL, fg=FG,
                           selectcolor=PANEL2, activebackground=PANEL, activeforeground=FG,
                           font=(FONT, 10), highlightthickness=0, command=self.refresh_export).pack(anchor="w", padx=14)
        rb = tk.Frame(right, bg=PANEL)
        rb.pack(anchor="w", padx=18, pady=(14, 14))
        self.setup_btn = mkbtn(rb, "⚙ Install FFmpeg", self.setup, "ghost")
        self.setup_btn.pack(side="left")
        mkbtn(rb, "Locate…", self.locate_ffmpeg, "flat").pack(side="left", padx=6)

        out = tk.Frame(f, bg=PANEL)
        out.pack(fill="x", padx=22, pady=(12, 0))
        mklabel(out, "Save video to", 10, MUTED, bg=PANEL).grid(row=0, column=0, padx=(16, 8), pady=(12, 4), sticky="w")
        mkentry(out, self.out_dir, 46).grid(row=0, column=1, sticky="we", pady=(12, 4))
        mkbtn(out, "Browse…", self.pick_out_dir, "ghost", pady=3).grid(row=0, column=2, padx=6, pady=(12, 4))
        mkbtn(out, "Project folder", lambda: self.out_dir.set(""), "flat", pady=3).grid(row=0, column=3, padx=(0, 16), pady=(12, 4))
        mklabel(out, "File name", 10, MUTED, bg=PANEL).grid(row=1, column=0, padx=(16, 8), pady=4, sticky="w")
        mkentry(out, self.out_name, 24).grid(row=1, column=1, sticky="w", pady=4)
        self.out_hint = mklabel(out, "", 9, MUTED, bg=PANEL)
        self.out_hint.grid(row=2, column=1, columnspan=3, sticky="w", pady=(0, 10))
        out.columnconfigure(1, weight=1)

        ctl = tk.Frame(f, bg=BG)
        ctl.pack(fill="x", padx=22, pady=12)
        self.start_btn = mkbtn(ctl, "▶  Make Video", self.start, "primary", padx=26, pady=10)
        self.start_btn.pack(side="left")
        self.stop_btn = mkbtn(ctl, "■  Stop", self.stop, "danger", padx=20, pady=10)
        self.stop_btn.pack(side="left", padx=8)
        self.stop_btn.configure(state="disabled")
        mkbtn(ctl, "Open video", self.open_output, "ghost").pack(side="right")
        mkbtn(ctl, "Open folder", self.open_out_folder, "ghost").pack(side="right", padx=8)
        self.state_lbl = mklabel(ctl, "Ready", 10, MUTED)
        self.state_lbl.pack(side="right", padx=14)
        self.pbar = SmoothBar(f, maximum=100, active=lambda: bool(self.proc or self.busy))
        self.pbar.pack(fill="x", padx=22)
        lw = tk.Frame(f, bg=BG)
        lw.pack(fill="both", expand=True, padx=22, pady=12)
        self.log = tk.Text(lw, bg=LOG_BG, fg=LOG_FG, font=(MONO, 9), relief="flat",
                           wrap="word", height=8, state="disabled", padx=12, pady=10, bd=0, highlightthickness=0)
        sb = ttk.Scrollbar(lw, command=self.log.yview)
        self.log.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.log.pack(side="left", fill="both", expand=True)
        self.log.tag_config("err", foreground=BAD)
        self.log.tag_config("ok", foreground=OK)
        self.log.tag_config("step", foreground=ACCENT)

    def refresh_export(self):
        def put(k, t, good):
            self.chk[k].configure(text=t, fg=OK if good else (BAD if good is False else MUTED))
        n = len(sentences_of(os.path.join(self.proj, "script.txt")))
        put("Script", f"{n} sentences" if n else "empty — Script tab e likho", bool(n))
        a = self.audio_path()
        put("Audio", os.path.basename(a) if a else "missing — Audio tab e import koro", bool(a))
        s = self.srt_path()
        put("SRT", os.path.basename(s) if s else "none (audio length onujayi andaj hobe)", True if s else None)
        c = sum(len(v) for v in scan_clips(self.clips_dir()).values())
        put("Clips", f"MANUAL — {c} clips" if c else "AUTO — stock footage", True if c else None)
        av = self.avatar_path()
        if self.mode.get() == 2:
            put("Avatar", os.path.basename(av) if av else "missing — Avatar tab e import koro", bool(av))
        else:
            put("Avatar", "not needed (Normal mode)", None)
        put("Python", find_python(), True)
        v = self.req["ff"]
        put("FFmpeg", "installed" if v else ("checking…" if v is None else "missing — Install FFmpeg chap"),
            True if v else (None if v is None else False))
        self._update_out_hint()

    # requirements (FFmpeg only — Whisper is NOT needed / never installed)

    # requirements

    def check_requirements(self, prompt=True):
        def work():
            tidy_ffmpeg()
            add_ffmpeg_path()
            ff = shutil.which("ffmpeg") is not None and ff_ok()
            self.q.put(("req", (ff, True, prompt)))
        threading.Thread(target=work, daemon=True).start()

    def setup(self):
        if self.busy or self.proc:
            return
        self.busy = True
        self.setup_btn.configure(state="disabled")
        self.start_btn.configure(state="disabled")
        self.state_lbl.configure(text="Installing FFmpeg…", fg=ACCENT)
        self.pbar["value"] = 0
        self.show("export")
        threading.Thread(target=self._setup_thread, daemon=True).start()

    def _say(self, t):
        self.q.put(("line", t + "\n"))

    def _setup_thread(self):
        try:
            if shutil.which("ffmpeg") is not None and ff_ok():
                self._say("[SETUP] FFmpeg already installed ✓")
            elif os.name != "nt":
                brew = shutil.which("brew") or next((p for p in ("/opt/homebrew/bin/brew", "/usr/local/bin/brew")
                                                     if os.path.exists(p)), None)
                if sys.platform == "darwin" and brew:
                    self._say("[SETUP] Homebrew diye FFmpeg install hocche (kichukkhon lagbe)…")
                    p = subprocess.Popen([brew, "install", "ffmpeg"], stdout=subprocess.PIPE,
                                         stderr=subprocess.STDOUT, text=True, errors="replace")
                    for line in p.stdout:
                        self._say("   " + line.rstrip())
                    p.wait()
                    add_ffmpeg_path()
                    if p.returncode != 0 or not ff_ok():
                        self._say("[ERROR] brew install ffmpeg fail korechhe. Terminal e nije chalao: brew install ffmpeg")
                        self.q.put(("setup_done", 1))
                        return
                else:
                    if sys.platform == "darwin":
                        self._say("[ERROR] Homebrew nei. Prothome https://brew.sh theke Homebrew install koro,")
                        self._say("        tarpor Terminal e lekho:  brew install ffmpeg   — tarpor app abar kholo.")
                    else:
                        self._say("[ERROR] Terminal e chalao:  sudo apt install ffmpeg   (ba tomar distro er package manager)")
                    self.q.put(("setup_done", 1))
                    return
            else:
                ok = install_ffmpeg(self._say, lambda v: self.q.put(("prog", v)))
                if not ok:
                    self._say("[ERROR] FFmpeg auto-install hoy nai (internet / firewall / antivirus block korte pare).")
                    self._say("        Manual: https://www.gyan.dev/ffmpeg/builds/ theke 'ffmpeg-release-essentials.zip' nao,")
                    self._say("        unzip kore bin folder e ja ache sheta e 'Locate…' button diye ffmpeg.exe select koro.")
                    self.q.put(("setup_done", 1))
                    return
            self._say("[SETUP] ✓ Done")
            self.q.put(("setup_done", 0))
        except Exception as e:
            self._say(f"[ERROR] Setup failed: {e}")
            self.q.put(("setup_done", 1))

    # run

    def write_log(self, text, tag=None):
        self.log.configure(state="normal")
        self.log.insert("end", text, tag)
        self.log.see("end")
        self.log.configure(state="disabled")

    def start(self):
        if self.proc or self.busy:
            return
        self.save_all(quiet=True)
        if not sentences_of(os.path.join(self.proj, "script.txt")):
            messagebox.showwarning("Script", "Script faka. Age Script tab e likho.")
            return self.show("script")
        if not self.audio_path():
            messagebox.showwarning("Audio", "Audio nei. Audio tab e import koro.")
            return self.show("audio")
        if self.mode.get() == 2 and not self.avatar_path():
            messagebox.showwarning("Avatar", "Avatar video nei. Avatar tab e import koro.")
            return self.show("avatar")
        add_ffmpeg_path()
        if not shutil.which("ffmpeg"):
            if messagebox.askyesno("FFmpeg", "FFmpeg lagbe. Ekhon auto install korbo?"):
                self.setup()
            return
        if not self.srt_path() and not has_module(find_python(), "whisper"):
            if not messagebox.askyesno(
                    "No SRT",
                    "SRT nei. Timing audio r length onujayi ANDAJ kora hobe (sentence er boro-chhoto onushare),\n"
                    "tai clip change thik jayga e na-o hote pare.\n\nSRT chhara-i video toiri korbo?"):
                return self.show("srt")
        out = self.output_path()
        try:
            os.makedirs(os.path.dirname(out), exist_ok=True)
            probe = os.path.join(os.path.dirname(out), ".ave_write_test")
            open(probe, "w").close()
            os.remove(probe)
        except Exception as e:
            messagebox.showerror("Output folder", f"Ei folder e save kora jachche na:\n{os.path.dirname(out)}\n\n{e}")
            return
        if os.path.exists(out) and not messagebox.askyesno("Replace?", f"Ei file ager theke ache:\n{out}\n\nReplace korbo?"):
            return
        self.cur_output = out
        sync_engine(self.proj)
        eng = os.path.join(self.proj, "make_video.py")
        self.log.configure(state="normal")
        self.log.delete("1.0", "end")
        self.log.configure(state="disabled")
        self.pbar["value"] = 0
        self.start_btn.configure(state="disabled")
        self.setup_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.state_lbl.configure(text="Running…", fg=ACCENT)
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        env["PYTHONUTF8"] = "1"
        env["AVE_OUTPUT"] = out
        env["AVE_MODE"] = str(self.mode.get())
        try:
            self.proc = subprocess.Popen(
                [find_python(), "-u", eng], cwd=self.proj, env=env, stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8",
                errors="replace", bufsize=1, creationflags=NOWIN)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.proc = None
            return self._finished(-1)
        threading.Thread(target=self._reader, args=(self.proc,), daemon=True).start()

    def _reader(self, p):
        for line in p.stdout:
            self.q.put(("line", line))
        p.wait()
        self.q.put(("done", p.returncode))

    def _drain(self):
        try:
            while True:
                k, v = self.q.get_nowait()
                if k == "line":
                    self._on_line(v)
                elif k == "prog":
                    self.pbar["value"] = v
                elif k == "thumb":
                    self._set_thumb(*v)
                elif k == "thumb_fail":
                    if not self.thumb_warned:
                        self.thumb_warned = True
                        self.note("Thumbnail dekhate FFmpeg lagbe — Export tab e 'Install FFmpeg' chap.", WARN, 12)
                elif k == "revoked":
                    self._on_revoked(v)
                elif k == "update":
                    self._on_update(v)
                elif k == "noupdate":
                    self.note("Tumi latest version e acho ✓" if v else "Offline — update check kora gelo na", OK if v else WARN)
                elif k == "usage":
                    self._set_usage(v)
                elif k == "cleaned":
                    self.note(f"Cache clear ✓  ({human(v)} jayga fnaka holo)")
                    self.refresh_usage()
                    if self.cur == "clips":
                        self.refresh_clips()
                elif k == "req":
                    self.req["ff"] = v[0]
                    prompt = v[2]
                    if self.cur == "export":
                        self.refresh_export()
                    if prompt and not v[0] and not self.busy:
                        if messagebox.askyesno("FFmpeg", "FFmpeg install kora nai (video toiri o thumbnail er jonno dorkar).\n"
                                                         "Ekhon auto install korbo?"):
                            self.setup()
                elif k == "setup_done":
                    self._setup_finished(v)
                else:
                    self._finished(v)
        except queue.Empty:
            pass
        self.after(80, self._drain)

    def _on_line(self, line):
        low = line.lower()
        tag = None
        if "[error]" in low or "traceback" in low or "error:" in low:
            tag = "err"
        elif "done!" in low or "[ok]" in low or "✓" in line:
            tag = "ok"
        elif "step " in low and "/" in low:
            tag = "step"
        self.write_log(line, tag)
        m = re.match(r"\s*\[(\d+)/(\d+)\]\s+\"", line)
        if m and self.proc:
            c, t = int(m.group(1)), int(m.group(2))
            self.pbar["value"] = c / max(t, 1) * 90
            self.state_lbl.configure(text=f"Clip {c}/{t}")
        elif self.proc and re.search(r"STEP [234]/", line):
            self.pbar["value"] = max(self.pbar["value"], 92)
            self.state_lbl.configure(text="Assembling…")

    def _setup_finished(self, code):
        self.busy = False
        self.setup_btn.configure(state="normal")
        self.start_btn.configure(state="normal")
        self.pbar["value"] = 100 if code == 0 else 0
        self.state_lbl.configure(text="FFmpeg ready ✓" if code == 0 else "Setup failed",
                                 fg=OK if code == 0 else BAD)
        if code == 0:
            self._done_fx("FFmpeg ready ✓")
        add_ffmpeg_path()
        self.thumb_warned = False
        self.check_requirements(prompt=False)
        self.refresh_usage()
        if code == 0 and self.cur == "clips":
            self.refresh_clips()

    def _finished(self, code):
        self.proc = None
        self.start_btn.configure(state="normal")
        self.setup_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        tmp = os.path.join(self.proj, "_temp")
        if os.path.isdir(tmp):
            rm_tree(tmp)      # crash / stop hole-o temp file jomte dey na
        if code == 0 and os.path.exists(self.cur_output):
            self.pbar["value"] = 100
            self._done_fx("Done ✓")
            self.write_log(f"\n✓ Finished. {self.cur_output}\n", "ok")
            if messagebox.askyesno("Done", f"Video ready!\n{self.cur_output}\n\nEkhon open korbe?"):
                self.open_output()
        elif code in (-1, None):
            self.state_lbl.configure(text="Stopped", fg=MUTED)
        elif code == 0:
            self.state_lbl.configure(text="Failed", fg=BAD)
            self.write_log("\n✗ Output file paoa jayni.\n", "err")
        else:
            self.state_lbl.configure(text="Failed", fg=BAD)
            self.write_log(f"\n✗ Process exited with code {code}\n", "err")
        self.refresh_usage()

    def stop(self):
        if not self.proc:
            return
        try:
            if os.name == "nt":
                subprocess.call(["taskkill", "/PID", str(self.proc.pid), "/T", "/F"],
                                creationflags=NOWIN, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                self.proc.terminate()
        except Exception:
            pass
        self.write_log("\n■ Stopped by user.\n", "err")

    def open_output(self):
        o = self.cur_output or self.output_path()
        if os.path.exists(o):
            open_path(o)
        else:
            messagebox.showinfo("Not found", "Video ekhono toiri hoyni.")

    def _quit(self):
        if self.proc or self.busy:
            if not messagebox.askyesno("Quit", "Kaj cholche. Stop kore quit korbe?"):
                return
            self.stop()
        self.save_all(quiet=True)
        self.destroy()

    def _tk_error(self, exc, val, tb):
        import traceback
        try:
            with open(os.path.join(TOOLS, "error.log"), "a", encoding="utf-8") as f:
                f.write(time.strftime("%Y-%m-%d %H:%M:%S ") + "".join(traceback.format_exception(exc, val, tb)) + "\n")
        except Exception:
            pass
        self.note(f"Error: {val}", BAD)

    def note(self, text, color=None, secs=6):
        self.statusbar.configure(text=text, fg=color or OK)
        if self._note_job:
            self.after_cancel(self._note_job)
        self._note_job = self.after(secs * 1000, lambda: self.statusbar.configure(
            text=f"Project folder: {self.proj}", fg=MUTED))

    def refresh_usage(self):
        if self._usage_busy:
            return
        self._usage_busy = True
        projs = [p for _, p in self.project_list()]

        def work():
            try:
                media = cache = linked = 0
                for p in projs:
                    for fn in os.listdir(p):
                        fp = os.path.join(p, fn)
                        if os.path.isdir(fp):
                            r, l = dir_usage(fp)
                        else:
                            try:
                                st = os.lstat(fp)
                                r, l = (0, st.st_size) if getattr(st, "st_nlink", 1) > 1 else (st.st_size, 0)
                            except OSError:
                                r = l = 0
                        if fn in CACHE_DIRS:
                            cache += r + l
                        else:
                            media += r
                            linked += l
                tools = dir_size(TOOLS) if os.path.isdir(TOOLS) else 0
                self.q.put(("usage", {"media": media, "cache": cache, "tools": tools, "linked": linked}))
            except Exception:
                self.q.put(("usage", None))
        threading.Thread(target=work, daemon=True).start()

    def _set_usage(self, u):
        self._usage_busy = False
        if not u:
            return
        self._usage = u
        total = u["media"] + u["cache"] + u["tools"]
        self.space_lbl.configure(text=f"💾 {human(total)}")
        big = u["cache"] > 500 * 1024 * 1024
        self.cache_btn.configure(text=f"🧹 Cache {human(u['cache'])}", fg=WARN if big else FG)

    def show_usage(self):
        u = self._usage or {}
        messagebox.showinfo(
            "Disk space",
            f"Project files (script/audio/clips…):  {human(u.get('media', 0))}\n"
            f"Cache (temp, downloads, thumbnails):  {human(u.get('cache', 0))}\n"
            f"Tools (FFmpeg):  {human(u.get('tools', 0))}\n"
            f"──────────────\n"
            f"Total:  {human(u.get('media', 0) + u.get('cache', 0) + u.get('tools', 0))}\n\n"
            f"Hard-linked clips (extra space nai):  {human(u.get('linked', 0))}\n\n"
            "Cache muchte  🧹 Cache  button chap.")

    def clean_cache(self):
        if self.proc or self.busy:
            messagebox.showinfo("Busy", "Kaj cholche — shesh hole cache clear koro.")
            return
        size = self._usage.get("cache", 0)
        if not messagebox.askyesno(
                "Clear cache",
                f"Cache {human(size)} muchhe felbo?\n\n"
                "(temp files, downloaded stock footage, thumbnails — sob project er.)\n"
                "Tomar script / audio / SRT / clips / settings kichu muchbe na."):
            return
        projs = [p for _, p in self.project_list()]

        def work():
            for p in projs:
                for d in CACHE_DIRS:
                    fp = os.path.join(p, d)
                    if os.path.isdir(fp):
                        rm_tree(fp)
            self.q.put(("cleaned", size))
        threading.Thread(target=work, daemon=True).start()

    # ───────── projects ─────────

    def open_project_path(self, d):
        if self.proc or self.busy:
            return
        known = any(os.path.exists(os.path.join(d, n)) for n in ("script.txt", "config.txt", "project.json"))
        if not known and not messagebox.askyesno(
                "Project?", "Ei folder e kono project file nai. Tobu notun project hishebe open korbo?"):
            return
        self.save_all(quiet=True)
        if os.path.abspath(os.path.dirname(d)) != os.path.abspath(WORKSPACE):
            ext = self.rec.setdefault("external", [])
            if d not in ext:
                ext.append(d)
        self.load_project(d)

    def open_dialog(self):
        if self.proc or self.busy:
            messagebox.showinfo("Busy", "Kaj cholche — shesh hole project open koro.")
            return
        self.save_all(quiet=True)
        items = self.project_list()

        def mt(p):
            try:
                return max(os.path.getmtime(os.path.join(p, n)) for n in ("script.txt", "project.json", "config.txt")
                           if os.path.exists(os.path.join(p, n)))
            except ValueError:
                return os.path.getmtime(p)
        items.sort(key=lambda x: mt(x[1]), reverse=True)
        win = tk.Toplevel(self)
        win.title("Open project")
        win.configure(bg=BG)
        win.geometry("560x400")
        win.transient(self)
        win.grab_set()
        mklabel(win, "Saved projects (notun → purano)", 12, FG, True).pack(anchor="w", padx=18, pady=(16, 8))
        lb = tk.Listbox(win, bg=PANEL, fg=FG, selectbackground=ACCENT, selectforeground=ACCENT_FG,
                        relief="flat", bd=0, font=(FONT, 11), activestyle="none", highlightthickness=0)
        lb.pack(fill="both", expand=True, padx=18)
        for n, p in items:
            lb.insert("end", f"{n}     —  {time.strftime('%d %b %Y  %H:%M', time.localtime(mt(p)))}")
        for i, (_n, p) in enumerate(items):
            if p == self.proj:
                lb.selection_set(i)

        def do_open(_e=None):
            sel = lb.curselection()
            if not sel:
                return
            p = items[sel[0]][1]
            win.destroy()
            if p != self.proj:
                self.load_project(p)
        lb.bind("<Double-Button-1>", do_open)
        r = tk.Frame(win, bg=BG)
        r.pack(fill="x", padx=18, pady=14)
        mkbtn(r, "Open", do_open, "primary").pack(side="left")
        mkbtn(r, "Browse folder…", lambda: (win.destroy(), self.open_folder_project()), "ghost").pack(side="left", padx=8)
        mkbtn(r, "Close", win.destroy, "flat").pack(side="right")

    def save_copy(self):
        if self.proc or self.busy:
            return
        name = simpledialog.askstring("Save a copy", "Notun project name:", parent=self,
                                      initialvalue=os.path.basename(self.proj) + " copy")
        if not name:
            return
        name = re.sub(r'[\\/:*?"<>|]', "_", name.strip())
        dst = os.path.join(WORKSPACE, name)
        if os.path.exists(dst):
            messagebox.showerror("Exists", "Ei naam e project ager theke ache.")
            return
        self.save_all(quiet=True)
        try:
            shutil.copytree(self.proj, dst, copy_function=fast_copy,
                            ignore=shutil.ignore_patterns(*CACHE_DIRS, "*.tmp", "make_video.py", "final_video.mp4"))
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return
        self.load_project(dst)
        self.note(f"Copy saved: {name}")

    # ───────── save / autosave ─────────

    def load_meta(self):
        m = {}
        try:
            m = json.load(open(os.path.join(self.proj, "project.json"), encoding="utf-8"))
        except Exception:
            pass
        self._loading = True
        try:
            self.mode.set(int(m.get("mode", 1) or 1))
            self.out_dir.set(m.get("export_dir", self.rec.get("export_dir", "")) or "")
            self.out_name.set(m.get("export_name") or "final_video")
        finally:
            self._loading = False

    def save_meta(self):
        if not self.proj:
            return
        m = {"version": 2, "mode": self.mode.get(), "export_dir": self.out_dir.get().strip(),
             "export_name": self.out_name.get().strip() or "final_video",
             "saved_at": time.strftime("%Y-%m-%d %H:%M:%S")}
        old = ""
        pj = os.path.join(self.proj, "project.json")
        try:
            old = json.load(open(pj, encoding="utf-8"))
            old.pop("saved_at", None)
        except Exception:
            old = None
        cmp = dict(m)
        cmp.pop("saved_at")
        if old != cmp:
            atomic_write(pj, json.dumps(m, indent=1))
        if self.out_dir.get().strip():
            self.rec["export_dir"] = self.out_dir.get().strip()
            save_recent(self.rec)

    def _meta_changed(self, *a):
        if self._loading:
            return
        if self._meta_job:
            self.after_cancel(self._meta_job)
        self._meta_job = self.after(500, self._meta_flush)
        if self.cur == "export":
            self._update_out_hint()

    def _meta_flush(self):
        self._meta_job = None
        try:
            self.save_meta()
            self._stamp()
        except Exception:
            pass

    def _settings_changed(self, *a):
        if self._loading:
            return
        if self._cfg_job:
            self.after_cancel(self._cfg_job)
        self._cfg_job = self.after(600, self._cfg_flush)

    def _cfg_flush(self):
        self._cfg_job = None
        try:
            self.save_settings(silent=True)
            self.save_avatar_fields(silent=True)
            self._stamp()
        except Exception:
            pass

    def _stamp(self):
        self.save_lbl.configure(text=f"✓ Saved {time.strftime('%H:%M:%S')}", fg=OK)

    def save_all(self, quiet=False):
        if not self.proj:
            return
        try:
            self.flush_script()
            self.flush_srt()
            self.save_settings(silent=True)
            self.save_avatar_fields(silent=True)
            self.save_meta()
            self._stamp()
            if not quiet:
                self.note("Project saved ✓  (auto-save-o cholche)")
        except Exception as e:
            self.note(f"Save failed: {e}", BAD)

    def _periodic(self):
        if self.proj and not self.busy:
            self.save_all(quiet=True)
        self.after(20000, self._periodic)

    # ───────── access control monitor / auto-update ─────────

    def _start_monitor(self):
        if not (AUTH_ON and self.session.get("id")):
            return
        threading.Thread(target=self._monitor_loop, daemon=True).start()

    def _monitor_loop(self):
        wait = 45
        while not self._mon_stop:
            for _ in range(int(wait)):
                if self._mon_stop:
                    return
                time.sleep(1)
            wait = self._check_remote()

    def _check_remote(self, manual=False):
        """Runs in a thread. Returns seconds until the next check."""
        ctl, online, why = load_control()
        if ctl is None:
            self.q.put(("revoked", why or "Access verify kora jayni."))
            return 600
        ok, msg = check_user(ctl, self.session["id"], self.session["hash"])
        if not ok:
            self.q.put(("revoked", "Tomar access ar nei.\n\n" + (msg if "thik nai" not in msg
                                                                   else "Account remove ba password change kora hoyeche.")))
            return 600
        if online and update_wanted(ctl):
            self.q.put(("update", ctl))
        elif manual:
            self.q.put(("noupdate", online))
        return max(2, float(ctl.get("check_minutes", 10))) * 60

    def _check_now(self, manual=False):
        threading.Thread(target=self._check_remote, args=(manual,), daemon=True).start()

    def _on_revoked(self, msg):
        if self._mon_stop:
            return
        self._mon_stop = True
        try:
            self.save_all(quiet=True)
            if self.proc:
                self.stop()
        except Exception:
            pass
        clear_session()
        try:
            messagebox.showerror("Access bondho", msg + "\n\nProject save kora hoyeche. App ekhon bondho hobe.")
        except Exception:
            pass
        self.destroy()
        os._exit(0)

    def _on_update(self, ctl):
        self._upd = ctl
        force = bool(ctl.get("force")) or vtuple(ctl.get("min_version", "0")) > vtuple(APP_VERSION)
        self.upd_btn.configure(text=f"⬆ Update v{ctl['version']}")
        if not self.upd_btn.winfo_ismapped():
            self.upd_btn.pack(side="right", padx=6)
        if force:
            self.after(3000, self._force_tick)

    def _force_tick(self):
        if not self._upd:
            return
        if self.proc or self.busy:
            return self.after(8000, self._force_tick)
        messagebox.showinfo("Update", f"Required update v{self._upd['version']} install hobe.\nProject save kora hobe.")
        self.do_update(confirm=False)

    def do_update(self, confirm=True):
        ctl = self._upd
        if not ctl:
            return
        if self.proc or self.busy:
            messagebox.showinfo("Busy", "Kaj cholche — shesh hole update koro.")
            return
        if confirm and not messagebox.askyesno(
                "Update", f"Version {ctl['version']} install korbo?\n\n{(ctl.get('notes') or '').strip()}\n\n"
                          "App restart hobe. Tomar project save kora thakbe."):
            return
        self.save_all(quiet=True)
        self.note("Updating…", WARN, 30)
        self.update_idletasks()
        try:
            apply_update(ctl)
        except Exception as e:
            self.note("Update failed", BAD)
            messagebox.showerror("Update failed", str(e))
            return
        self._mon_stop = True
        self.destroy()
        relaunch()
        os._exit(0)

    def logout(self):
        if self.proc or self.busy:
            messagebox.showinfo("Busy", "Kaj cholche — shesh hole logout koro.")
            return
        if not messagebox.askyesno("Logout", "Logout korbe?"):
            return
        self.save_all(quiet=True)
        clear_session()
        self._mon_stop = True
        self.destroy()
        relaunch()
        os._exit(0)

    def _dnd_setup(self):
        if not DND_OK:
            self.after(1500, lambda: self.note("Drag & drop off — 'tkinterdnd2' install hoy nai (button diye import kaj korbe)", WARN, 10))
            return
        self._dnd_register_tree(self)
        for w in (self.audio_drag, self.audio_name, self.audio_info):
            try:
                w.drag_source_register(1, DND_FILES)
                w.dnd_bind("<<DragInitCmd>>", self._audio_drag_init)
                w.dnd_bind("<<DragEndCmd>>", self._audio_drag_end)
            except Exception:
                pass
        try:
            self.script_drag.drag_source_register(1, DND_FILES)
            self.script_drag.dnd_bind("<<DragInitCmd>>", self._script_drag_init)
            self.script_drag.dnd_bind("<<DragEndCmd>>", self._audio_drag_end)
        except Exception:
            pass

    def _dnd_register_tree(self, w):
        if not DND_OK:
            return
        try:
            w.drop_target_register(DND_FILES)
            w.dnd_bind("<<Drop>>", self._on_drop)
        except Exception:
            pass
        for c in w.winfo_children():
            self._dnd_register_tree(c)

    def _drop_target_at(self, event):
        try:
            w = self.winfo_containing(event.x_root, event.y_root)
        except Exception:
            w = None
        while w is not None:
            t = getattr(w, "_drop", None)
            if t:
                return t
            w = getattr(w, "master", None)
        return None

    def _on_drop(self, event):
        if self._drag_out:                     # nijer audio nijer e drop -> kichu korbo na
            return event.action
        try:
            raw = list(self.tk.splitlist(event.data))
            paths = []
            for p in raw:
                p = p.strip()
                if os.path.isdir(p):
                    paths += sorted((os.path.join(p, f) for f in os.listdir(p)),
                                    key=lambda x: natural_key(os.path.basename(x)))
                else:
                    paths.append(p)
            paths = [p for p in paths if os.path.isfile(p)]
            if self.proc or self.busy:
                self.note("Kaj cholche — shesh hole drop koro.", WARN)
            elif paths:
                self.handle_files(paths, self._drop_target_at(event))
        except Exception as e:
            self.note(f"Drop error: {e}", BAD)
        return event.action

    def handle_files(self, paths, target=None):
        ext = lambda p: os.path.splitext(p)[1].lower()
        scripts = [p for p in paths if ext(p) == ".txt"]
        srts = [p for p in paths if ext(p) == ".srt"]
        audios = [p for p in paths if ext(p) in AUDIO_EXTS]
        media = [p for p in paths if ext(p) in VIDEO_EXTS | IMAGE_EXTS]
        known = set(scripts + srts + audios + media)
        unknown = [p for p in paths if p not in known]
        kinds, msgs = [], []
        if scripts:
            self.set_script_file(scripts[0])
            kinds.append("script")
            msgs.append("script")
        if audios:
            if self.set_audios(audios):
                kinds.append("audio")
                msgs.append("audio" if len(audios) == 1 else f"{len(audios)} ta audio join hocche…")
            else:
                msgs.append("audio add hoyni")
        if srts:
            self.set_srt(srts[0])
            kinds.append("srt")
            msgs.append("SRT")
        if media:
            vids = [p for p in media if ext(p) in VIDEO_EXTS]
            if self.cur == "avatar" and vids and not (target and target[0] in ("add", "replace")):
                self.set_avatar(vids[0])
                kinds.append("avatar")
                msgs.append("avatar")
            else:
                info = self.add_media(media, target)
                kinds.append("clips")
                msgs.append(info)
        if unknown:
            msgs.append(f"{len(unknown)} ta unsupported file chhere deya hoyeche")
        if kinds and self.cur not in kinds:
            self.show(kinds[0])
        elif self.cur:
            self.show(self.cur)
        self.note("✓ " + " • ".join(m for m in msgs if m), OK if kinds else WARN)
        self.save_all(quiet=True)
        self.refresh_usage()

    # ───────── SCRIPT ─────────

    def set_script_file(self, p):
        txt = read_text(p)
        old = self.script_txt.get("1.0", "end-1c")
        if old.strip() and old != txt:
            try:
                atomic_write(os.path.join(self.proj, "script.txt.bak"), old)   # purano script er backup
            except Exception:
                pass
        self.script_txt.delete("1.0", "end")
        self.script_txt.insert("1.0", txt)
        self.flush_script()

    def set_audio(self, p):
        for fn in os.listdir(self.proj):
            fp = os.path.join(self.proj, fn)
            if os.path.splitext(fn)[1].lower() in AUDIO_EXTS and os.path.abspath(fp) != os.path.abspath(p):
                archive(fp, self.proj)
        dst = os.path.join(self.proj, os.path.basename(p))
        if os.path.abspath(dst) != os.path.abspath(p):
            fast_copy(p, dst)
        if self.cur == "audio":
            self.refresh_audio()

    def set_audios(self, paths):
        """1 ta audio -> normal. Multiple -> shudhu tokhon, jokhon nam thik 1,2,3,…N; tahole join hoy."""
        paths = [p for p in paths if os.path.splitext(p)[1].lower() in AUDIO_EXTS]
        if not paths:
            return False
        if len(paths) == 1:
            self.set_audio(paths[0])
            return True
        if self._merging:
            self.note("Ager audio join cholche — shesh hole abar dao.", WARN)
            return False
        ordered = serial_audio_order(paths)
        if ordered is None:
            names = ", ".join(os.path.basename(p) for p in sorted(paths, key=lambda x: natural_key(os.path.basename(x)))[:8])
            messagebox.showwarning(
                "Audio add hoyni",
                f"{len(paths)} ta audio dewa hoyeche kintu nam serial 1, 2, 3, … na.\n({names}{' …' if len(paths) > 8 else ''})\n\n"
                "Multiple audio add korte hole nam thik 1, 2, 3, … N hote hobe (jemon 1.mp3, 2.mp3, 3.mp3),"
                " kono number miss/duplicate howa jabe na.\n"
                "Naile shudhu ekta audio file dao.\n\nKono audio add kora hoyni.")
            return False
        if not ff_ok():
            messagebox.showerror("ffmpeg nei", "Audio join korte ffmpeg lagbe. Requirements check kore ffmpeg install koro.")
            return False
        self._merging = True
        proj = self.proj
        part = os.path.join(proj, "audio_merge.part")
        final = os.path.join(proj, "voiceover_merged.mp3")
        self.note(f"♫ {len(ordered)} ta audio join hocche…", WARN, 60)
        if self.cur == "audio":
            self.audio_name.configure(text=f"⏳  {len(ordered)} ta audio join hocche…")
            self.audio_info.configure(text="Ektu opekkha koro")
        res = {}

        def work():
            try:
                res["r"] = merge_audio_files(ordered, part)
            except Exception as e:
                res["r"] = (False, str(e))

        def poll():
            if "r" not in res:
                self.after(250, poll)
                return
            self._merging = False
            ok, err = res["r"]
            if not ok:
                archive(part, proj)
                messagebox.showerror("Audio join fail", "Audio gulo join kora gelo na.\n\n" + err)
                if self.proj == proj and self.cur == "audio":
                    self.refresh_audio()
                return
            try:
                for fn in os.listdir(proj):
                    if os.path.splitext(fn)[1].lower() in AUDIO_EXTS:
                        archive(os.path.join(proj, fn), proj)
                os.replace(part, final)
            except Exception as e:
                messagebox.showerror("Audio join fail", f"Final file save kora gelo na: {e}")
                return
            self.note(f"✓ {len(ordered)} ta audio serially join hoye ekta audio hoyeche", OK)
            if self.proj == proj:
                self.refresh_audio()
                self.refresh_usage()
        threading.Thread(target=work, daemon=True).start()
        self.after(250, poll)
        return True

    def clear_all(self):
        """Script, audio, SRT, clips, avatar sob faka — notun video banano jonno."""
        if self.proc or self.busy or self._merging:
            messagebox.showinfo("Busy", "Kaj cholche — shesh hole Clear All koro.")
            return
        if not self.proj:
            return
        if not messagebox.askyesno(
                "Clear All",
                "Script, Audio, SRT, Clips, Avatar — sob muchhe faka kore dibo?\n\n"
                "(Tomar original file gulo thikই thakbe — shudhu project er copy muchbe.\n"
                "Settings / API key thakbe.)", icon="warning"):
            return
        proj = self.proj
        for job in ("_save_job", "_srt_job"):
            j = getattr(self, job, None)
            if j:
                try:
                    self.after_cancel(j)
                except Exception:
                    pass
                setattr(self, job, None)
        # script
        self._loading = True
        self.script_txt.delete("1.0", "end")
        self.script_txt.edit_reset()
        self.script_txt.edit_modified(False)
        self._loading = False
        atomic_write(os.path.join(proj, "script.txt"), "")
        self._script_saved = ""
        for fn in ("script.txt.bak", "queries.json"):       # purano script er backup / saved queries
            archive(os.path.join(proj, fn), proj)
        self.update_script_count()
        # audio, srt, avatar
        for fn in os.listdir(proj):
            fp = os.path.join(proj, fn)
            ext = os.path.splitext(fn)[1].lower()
            if os.path.isfile(fp) and (ext in AUDIO_EXTS or ext == ".srt" or fn == "audio_merge.part"
                                       or (fn.lower().startswith("avatar") and ext in VIDEO_EXTS)):
                archive(fp, proj)
        # clips
        cd = self.clips_dir()
        for fn in os.listdir(cd):
            archive(os.path.join(cd, fn), proj)
        # purano video er cache (temp / downloaded stock / thumbnails)
        for d in CACHE_DIRS:
            fp = os.path.join(proj, d)
            if os.path.isdir(fp):
                rm_tree(fp)
        self.refresh_audio()
        self.refresh_srt()
        self.refresh_avatar()
        self.refresh_clips()
        self.refresh_usage()
        self.show("script")
        self.note("✓ Sob faka — notun video banate paro", OK)

    def _srt_modified(self, e=None):
        if self._srt_loading or not self.srt_txt.edit_modified():
            return
        self.srt_txt.edit_modified(False)
        if self._srt_job:
            self.after_cancel(self._srt_job)
        self._srt_job = self.after(800, self.flush_srt)
        self.srt_state.configure(text="Saving…", fg=WARN)

    def flush_srt(self):
        if self._srt_job:
            self.after_cancel(self._srt_job)
            self._srt_job = None
        if not self.proj or self._srt_saved is None:
            return
        txt = self.srt_txt.get("1.0", "end-1c")
        if txt == self._srt_saved:
            return
        p = self.srt_path() or os.path.join(self.proj, "subtitles.srt")
        if not txt.strip() and not os.path.exists(p):
            return
        atomic_write(p, txt)
        self._srt_saved = txt
        self.srt_state.configure(text=f"✓ Auto-saved {time.strftime('%H:%M:%S')}", fg=OK)
        self._srt_info(p)
        self._stamp()

    def _srt_info(self, p):
        nb = parse_srt_count(p)
        ns = len(sentences_of(os.path.join(self.proj, "script.txt")))
        note = "  ✓ exact match" if nb == ns else "  (count alada — engine fuzzy matching use korbe)"
        self.srt_info.configure(text=f"{os.path.basename(p)}  •  {nb} blocks  •  {ns} sentences{note}")

    def set_srt(self, p):
        for fn in os.listdir(self.proj):
            fp = os.path.join(self.proj, fn)
            if fn.lower().endswith(".srt") and os.path.abspath(fp) != os.path.abspath(p):
                archive(fp, self.proj)
        dst = os.path.join(self.proj, os.path.basename(p))
        if os.path.abspath(dst) != os.path.abspath(p):
            fast_copy(p, dst)
        if self.cur == "srt":
            self.refresh_srt()

    def _wheel_on(self, _e=None):
        for ev in ("<MouseWheel>", "<Button-4>", "<Button-5>"):
            self.cv.bind_all(ev, self._wheel)

    def _wheel_off(self, _e=None):
        for ev in ("<MouseWheel>", "<Button-4>", "<Button-5>"):
            self.cv.unbind_all(ev)

    def add_media(self, media, target=None):
        """Returns a short status string. target: None | ('add', idx) | ('replace', path, idx)."""
        n = len(sentences_of(os.path.join(self.proj, "script.txt")))
        cd = self.clips_dir()
        if n == 0:
            messagebox.showinfo("Script", "Age script likho (Script tab).")
            return "script faka"
        files = sorted(media, key=lambda p: natural_key(os.path.basename(p)))
        if target and target[0] == "replace":
            self._replace_with(target[1], files[0])
            for p in files[1:]:
                place_clip(p, cd, target[2])
            return f"clip replace hoyeche ({len(files)} file)" if len(files) > 1 else "clip replace hoyeche"
        if target and target[0] == "add":
            for p in files:
                place_clip(p, cd, target[1])
            return f"{len(files)} clip sentence #{target[1]} e add hoyeche"
        # name-aware distribution:  1a 1b -> sentence 1 ;  2a 2b -> sentence 2 ;  3 -> sentence 3
        named, unnamed, skipped = {}, [], 0
        for p in files:
            m = CLIP_RE.fullmatch(os.path.splitext(os.path.basename(p))[0].strip())
            if m and int(m.group(1)) >= 1:
                named.setdefault(int(m.group(1)), []).append((clip_var(m), p, bool(m.group(4))))
            else:
                unnamed.append(p)
        placed = 0
        for idx, lst in sorted(named.items()):
            if idx > n:
                skipped += len(lst)
                continue
            for var, p, letter in sorted(lst, key=lambda x: (x[0], natural_key(os.path.basename(x[1])))):
                place_clip(p, cd, idx, preferred_var=var, letter=letter)
                placed += 1
        if unnamed:
            have = scan_clips(cd)
            empty = [i for i in range(1, n + 1) if i not in have]
            for i, p in zip(empty, unnamed):
                place_clip(p, cd, i)
                placed += 1
            skipped += max(0, len(unnamed) - len(empty))
        msg = f"{placed} clip add hoyeche"
        if skipped:
            msg += f" ({skipped} ta chhere deya — sentence nai/faka jayga nai)"
        return msg

    def _replace_with(self, path, src):
        stem = os.path.splitext(os.path.basename(path))[0]
        archive(path, self.proj)
        dst = os.path.join(self.clips_dir(), stem + os.path.splitext(src)[1].lower())
        if os.path.abspath(dst) != os.path.abspath(src):
            fast_copy(src, dst)

    def _make_thumb(self, path, out):
        vf = ("scale=128:72:force_original_aspect_ratio=decrease,"
              "pad=128:72:(ow-iw)/2:(oh-ih)/2:color=0x0d0e12")
        vid = os.path.splitext(path)[1].lower() in VIDEO_EXTS
        for pre in ([["-ss", "0.5"]] if vid else []) + [[]]:
            cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *pre, "-i", path,
                   "-an", "-sn", "-vf", vf, "-frames:v", "1", "-update", "1", out]
            try:
                subprocess.run(cmd, creationflags=NOWIN, timeout=30,
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except FileNotFoundError:
                return None          # ffmpeg missing
            except Exception:
                pass
            if os.path.exists(out) and os.path.getsize(out) > 0:
                return True
            try:
                os.remove(out)
            except OSError:
                pass
        return False

    def set_avatar(self, p):
        old = self.avatar_path()
        if old and os.path.abspath(old) != os.path.abspath(p):
            archive(old, self.proj)
        dst = os.path.join(self.proj, "avatar" + os.path.splitext(p)[1].lower())
        if os.path.abspath(dst) != os.path.abspath(p):
            fast_copy(p, dst)
        if self.cur == "avatar":
            self.refresh_avatar()

    def _vol_changed(self, v=None):
        pct = int(float(self.vol_pct.get()))
        count_to(self.vol_lbl, pct, "{}%", 140)
        if not self._loading:
            self.sv["VOLUME"].set(f"{pct / 100:.2f}")

    def output_path(self):
        d = self.out_dir.get().strip() or self.proj
        name = re.sub(r'[\\/:*?"<>|]', "_", self.out_name.get().strip() or "final_video")
        if not name.lower().endswith(".mp4"):
            name += ".mp4"
        return os.path.join(d, name)

    def _update_out_hint(self):
        self.out_hint.configure(text=f"→ {self.output_path()}")

    def pick_out_dir(self):
        d = filedialog.askdirectory(title="Video kothay save hobe?",
                                    initialdir=self.out_dir.get().strip() or self.proj)
        if d:
            self.out_dir.set(os.path.normpath(d))

    def open_out_folder(self):
        d = os.path.dirname(self.cur_output or self.output_path())
        if os.path.isdir(d):
            open_path(d)
        else:
            messagebox.showinfo("Folder", "Folder ekhono toiri hoyni.")

    def locate_ffmpeg(self):
        p = filedialog.askopenfilename(title="ffmpeg.exe select koro",
                                       filetypes=[("ffmpeg", FF_EXE), ("All", "*.*")])
        if not p:
            return
        d = os.path.dirname(p)
        if not ff_ok(d):
            messagebox.showerror("FFmpeg", "Ei file ta kaj korche na. Sothik ffmpeg.exe select koro.")
            return
        self.rec["ffmpeg_dir"] = d
        save_recent(self.rec)
        add_ffmpeg_path()
        self.check_requirements(prompt=False)
        self.note("FFmpeg location saved ✓")


if __name__ == "__main__":
    _sess = gate()
    if _sess is not None:
        App(_sess).mainloop()

# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "fastapi",
#   "uvicorn[standard]",
#   "python-multipart",
#   "fpdf2",
#   "pyyaml",
# ]
# ///

import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Optional

import uvicorn
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, JSONResponse, Response

app = FastAPI()

PROJECT_ROOT = Path(__file__).parent.parent

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Journal Generator</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garant:ital,wght@0,400;0,500;0,600;1,400&family=Jost:wght@300;400;500&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    :root {
      --bg:             #E6E0D6;
      --surface:        #F4F0E9;
      --surface-hi:     #FDFCFA;
      --ink:            #1E1C18;
      --ink-mid:        #58524A;
      --ink-faint:      #988E80;
      --accent:         #8B3F10;
      --accent-hover:   #A04A15;
      --accent-tint:    rgba(139,63,16,0.07);
      --border:         #CEC5B5;
      --border-hi:      #E2DAD0;
      --success:        #2D6848;
      --error:          #882222;
      --r:              4px;
      --r-lg:           8px;
      --shadow:         0 2px 16px rgba(30,28,24,0.09);
      --shadow-lg:      0 8px 48px rgba(30,28,24,0.13);
    }

    body {
      font-family: 'Jost', sans-serif;
      background-color: var(--bg);
      color: var(--ink);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 52px 20px 80px;
    }

    /* ── Header ───────────────────────────── */
    header {
      text-align: center;
      margin-bottom: 36px;
      animation: rise 0.5s ease both;
    }

    .title {
      font-family: 'Cormorant Garant', serif;
      font-size: clamp(2.2rem, 5vw, 3.2rem);
      font-weight: 600;
      letter-spacing: -0.02em;
      line-height: 1;
      margin-bottom: 10px;
    }

    .subtitle {
      font-size: 0.7rem;
      font-weight: 400;
      letter-spacing: 0.2em;
      text-transform: uppercase;
      color: var(--ink-faint);
    }

    .rule {
      display: flex;
      align-items: center;
      gap: 10px;
      margin: 14px auto 0;
      width: fit-content;
    }
    .rule-line { width: 36px; height: 1px; background: var(--border); }
    .rule-pip  { width: 5px; height: 5px; background: var(--accent); border-radius: 50%; }

    /* ── Card ─────────────────────────────── */
    .card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--r-lg);
      box-shadow: var(--shadow-lg);
      width: 100%;
      max-width: 580px;
      animation: rise 0.5s ease 0.08s both;
    }

    /* ── Section shell ────────────────────── */
    .sec {
      padding: 28px 32px;
      border-bottom: 1px solid var(--border-hi);
    }
    .sec:last-of-type { border-bottom: none; }

    .sec-label {
      font-size: 0.65rem;
      font-weight: 500;
      letter-spacing: 0.18em;
      text-transform: uppercase;
      color: var(--ink-faint);
      margin-bottom: 18px;
    }

    /* ── Type selector ────────────────────── */
    .type-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 8px;
    }

    .type-btn { position: relative; cursor: pointer; }
    .type-btn input { position: absolute; opacity: 0; width: 0; height: 0; }

    .type-card {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 9px;
      padding: 15px 6px 13px;
      background: var(--surface-hi);
      border: 1.5px solid var(--border);
      border-radius: var(--r-lg);
      cursor: pointer;
      transition: border-color 0.14s, background 0.14s, box-shadow 0.14s;
    }
    .type-card:hover { border-color: var(--accent); background: var(--accent-tint); }
    .type-btn input:checked + .type-card {
      border-color: var(--accent);
      background: var(--accent-tint);
      box-shadow: 0 0 0 1px var(--accent);
    }

    .type-icon { width: 34px; height: 34px; color: var(--ink-mid); transition: color 0.14s; }
    .type-btn input:checked + .type-card .type-icon { color: var(--accent); }

    .type-name {
      font-size: 0.68rem;
      font-weight: 500;
      letter-spacing: 0.04em;
      color: var(--ink-mid);
      transition: color 0.14s;
    }
    .type-btn input:checked + .type-card .type-name { color: var(--accent); }

    /* ── Form rows ────────────────────────── */
    .row { display: grid; grid-template-columns: 1fr 1fr; gap: 18px; }
    .row + .row { margin-top: 18px; }

    .field { display: flex; flex-direction: column; gap: 7px; }
    .field.span2 { grid-column: 1 / -1; }

    .field > label {
      font-size: 0.7rem;
      font-weight: 500;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: var(--ink-mid);
    }

    input[type="number"],
    input[type="text"],
    select {
      font-family: 'Jost', sans-serif;
      font-size: 0.9375rem;
      font-weight: 300;
      color: var(--ink);
      background: var(--surface-hi);
      border: 1.5px solid var(--border);
      border-radius: var(--r);
      padding: 9px 13px;
      width: 100%;
      outline: none;
      appearance: none;
      transition: border-color 0.14s;
    }
    input:focus, select:focus { border-color: var(--accent); }

    select {
      background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='11' height='7' viewBox='0 0 11 7'%3E%3Cpath d='M1 1l4.5 4.5L10 1' stroke='%23988E80' stroke-width='1.5' fill='none' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E");
      background-repeat: no-repeat;
      background-position: right 13px center;
      padding-right: 34px;
      cursor: pointer;
    }

    .hint {
      font-size: 0.73rem;
      font-weight: 300;
      color: var(--ink-faint);
    }

    /* ── Margins ──────────────────────────── */
    .margins-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 8px;
      margin-top: 4px;
    }
    .margin-field { display: flex; flex-direction: column; gap: 5px; }
    .margin-field label {
      font-size: 0.63rem;
      font-weight: 500;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: var(--ink-faint);
      text-align: center;
    }
    .margin-field input { text-align: center; padding: 8px 4px; }

    /* ── Toggle ───────────────────────────── */
    .toggle-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
    }
    .toggle-row + .toggle-row { margin-top: 18px; }

    .toggle-text { display: flex; flex-direction: column; gap: 2px; }
    .toggle-text .t-label {
      font-size: 0.7rem;
      font-weight: 500;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: var(--ink-mid);
    }
    .toggle-text .t-desc { font-size: 0.8rem; font-weight: 300; color: var(--ink-faint); }

    .toggle-switch { position: relative; width: 42px; height: 23px; flex-shrink: 0; }
    .toggle-switch input { opacity: 0; width: 0; height: 0; }
    .toggle-track {
      position: absolute;
      inset: 0;
      background: var(--border);
      border-radius: 12px;
      cursor: pointer;
      transition: background 0.2s;
    }
    .toggle-track::before {
      content: '';
      position: absolute;
      width: 17px; height: 17px;
      left: 3px; top: 3px;
      background: white;
      border-radius: 50%;
      transition: transform 0.2s;
      box-shadow: 0 1px 3px rgba(0,0,0,0.18);
    }
    .toggle-switch input:checked + .toggle-track { background: var(--accent); }
    .toggle-switch input:checked + .toggle-track::before { transform: translateX(19px); }

    /* ── Collapsible ──────────────────────── */
    .collapsible {
      overflow: hidden;
      transition: max-height 0.28s ease, opacity 0.28s ease, margin-top 0.28s ease;
      max-height: 80px;
      opacity: 1;
      margin-top: 18px;
    }
    .collapsible.hidden { max-height: 0; opacity: 0; margin-top: 0; }

    /* ── Generate button ──────────────────── */
    .gen-sec { padding: 24px 32px 30px; }

    .btn {
      font-family: 'Jost', sans-serif;
      font-size: 0.775rem;
      font-weight: 500;
      letter-spacing: 0.16em;
      text-transform: uppercase;
      color: white;
      background: var(--accent);
      border: none;
      border-radius: var(--r);
      padding: 14px 32px;
      width: 100%;
      cursor: pointer;
      transition: background 0.14s, transform 0.1s;
      position: relative;
      overflow: hidden;
    }
    .btn:hover:not(:disabled) { background: var(--accent-hover); }
    .btn:active:not(:disabled) { transform: scale(0.99); }
    .btn:disabled { opacity: 0.55; cursor: not-allowed; }
    .btn.loading::after {
      content: '';
      position: absolute;
      inset: 0;
      background: linear-gradient(90deg, transparent, rgba(255,255,255,0.18), transparent);
      animation: sweep 1.1s infinite;
    }

    /* ── Status ───────────────────────────── */
    .status {
      margin-top: 12px;
      padding: 11px 14px;
      border-radius: var(--r);
      font-size: 0.85rem;
      font-weight: 300;
      display: none;
    }
    .status.err {
      display: block;
      background: rgba(136,34,34,0.07);
      color: var(--error);
      border: 1px solid rgba(136,34,34,0.18);
    }
    .status.ok {
      display: block;
      background: rgba(45,104,72,0.07);
      color: var(--success);
      border: 1px solid rgba(45,104,72,0.18);
    }

    /* ── Animations ───────────────────────── */
    @keyframes rise {
      from { opacity: 0; transform: translateY(14px); }
      to   { opacity: 1; transform: translateY(0); }
    }
    @keyframes sweep {
      from { transform: translateX(-100%); }
      to   { transform: translateX(100%); }
    }

    /* ── Responsive ───────────────────────── */
    @media (max-width: 480px) {
      .type-grid { grid-template-columns: repeat(2, 1fr); }
      .row { grid-template-columns: 1fr; }
      .margins-grid { grid-template-columns: repeat(2, 1fr); }
      .sec { padding: 22px 20px; }
      .gen-sec { padding: 20px 20px 26px; }
    }
  </style>
</head>
<body>

<header>
  <h1 class="title">Journal Generator</h1>
  <p class="subtitle">PDF Notebook Page Creator</p>
  <div class="rule">
    <span class="rule-line"></span>
    <span class="rule-pip"></span>
    <span class="rule-line"></span>
  </div>
</header>

<div class="card">
  <form id="form">

    <!-- ── Page Type ─────────────────────── -->
    <div class="sec">
      <div class="sec-label">Page Type</div>
      <div class="type-grid">

        <label class="type-btn">
          <input type="radio" name="page_type" value="H" checked>
          <div class="type-card">
            <svg class="type-icon" viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round">
              <polygon points="10,3 17,7 17,15 10,19 3,15 3,7"/>
              <polygon points="24,3 31,7 31,15 24,19 17,15 17,7"/>
              <polygon points="17,19 24,23 24,31 17,35 10,31 10,23"/>
              <polygon points="31,19 38,23 38,31 31,35 24,31 24,23"/>
            </svg>
            <span class="type-name">Hex Map</span>
          </div>
        </label>

        <label class="type-btn">
          <input type="radio" name="page_type" value="L">
          <div class="type-card">
            <svg class="type-icon" viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round">
              <line x1="5" y1="12" x2="35" y2="12"/>
              <line x1="5" y1="20" x2="35" y2="20"/>
              <line x1="5" y1="28" x2="35" y2="28"/>
            </svg>
            <span class="type-name">Lined</span>
          </div>
        </label>

        <label class="type-btn">
          <input type="radio" name="page_type" value="D">
          <div class="type-card">
            <svg class="type-icon" viewBox="0 0 40 40" fill="currentColor">
              <circle cx="10" cy="10" r="2.2"/><circle cx="20" cy="10" r="2.2"/><circle cx="30" cy="10" r="2.2"/>
              <circle cx="10" cy="20" r="2.2"/><circle cx="20" cy="20" r="2.2"/><circle cx="30" cy="20" r="2.2"/>
              <circle cx="10" cy="30" r="2.2"/><circle cx="20" cy="30" r="2.2"/><circle cx="30" cy="30" r="2.2"/>
            </svg>
            <span class="type-name">Dot Grid</span>
          </div>
        </label>

        <label class="type-btn">
          <input type="radio" name="page_type" value="S">
          <div class="type-card">
            <svg class="type-icon" viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round">
              <line x1="5"  y1="5"  x2="5"  y2="35"/>
              <line x1="15" y1="5"  x2="15" y2="35"/>
              <line x1="25" y1="5"  x2="25" y2="35"/>
              <line x1="35" y1="5"  x2="35" y2="35"/>
              <line x1="5"  y1="5"  x2="35" y2="5"/>
              <line x1="5"  y1="15" x2="35" y2="15"/>
              <line x1="5"  y1="25" x2="35" y2="25"/>
              <line x1="5"  y1="35" x2="35" y2="35"/>
            </svg>
            <span class="type-name">Square Grid</span>
          </div>
        </label>

      </div>
    </div>

    <!-- ── Page Setup ────────────────────── -->
    <div class="sec">
      <div class="sec-label">Page Setup</div>
      <div class="row">
        <div class="field">
          <label for="pagesize">Page Size</label>
          <select id="pagesize" name="pagesize">
            <option value="A5" selected>A5 — 148 × 210 mm</option>
            <option value="A4">A4 — 210 × 297 mm</option>
            <option value="A6">A6 — 105 × 148 mm</option>
            <option value="B5">B5 — 176 × 250 mm</option>
            <option value="B4">B4 — 250 × 353 mm</option>
            <option value="B6">B6 — 125 × 176 mm</option>
            <option value="letter">Letter — 216 × 279 mm</option>
            <option value="halfletter">Half Letter — 140 × 216 mm</option>
            <option value="legal">Legal — 216 × 356 mm</option>
          </select>
        </div>
        <div class="field">
          <label for="numpages">Number of Pages</label>
          <input type="number" id="numpages" name="numpages" value="1" min="1" max="500">
        </div>
      </div>
    </div>

    <!-- ── Style ─────────────────────────── -->
    <div class="sec">
      <div class="sec-label">Style</div>
      <div class="row">
        <div class="field">
          <label for="size" id="size-label">Line Width</label>
          <input type="number" id="size" name="size" step="0.05" min="0.05" max="5" placeholder="0.1">
          <span class="hint" id="size-hint">mm — default 0.1</span>
        </div>
        <div class="field">
          <label for="width" id="width-label">Hex Size</label>
          <input type="number" id="width" name="width" step="0.5" min="0.5" max="100" placeholder="10.0">
          <span class="hint" id="width-hint">mm — default 10.0</span>
        </div>
      </div>

      <div class="collapsible" id="rotated-wrap">
        <div class="toggle-row">
          <div class="toggle-text">
            <span class="t-label">Rotated</span>
            <span class="t-desc">Flat-top hexagon orientation (default is pointy-top)</span>
          </div>
          <label class="toggle-switch">
            <input type="checkbox" id="rotated" name="rotated" value="true">
            <span class="toggle-track"></span>
          </label>
        </div>
      </div>
    </div>

    <!-- ── Layout ────────────────────────── -->
    <div class="sec">
      <div class="sec-label">Layout</div>

      <div class="field span2" style="margin-bottom: 20px;">
        <label>Margins (mm)</label>
        <div class="margins-grid">
          <div class="margin-field">
            <label>Top</label>
            <input type="number" name="margin_top" value="4.5" step="0.5" min="0.5">
          </div>
          <div class="margin-field">
            <label>Right</label>
            <input type="number" name="margin_right" value="4.5" step="0.5" min="0.5">
          </div>
          <div class="margin-field">
            <label>Bottom</label>
            <input type="number" name="margin_bottom" value="4.5" step="0.5" min="0.5">
          </div>
          <div class="margin-field">
            <label>Left</label>
            <input type="number" name="margin_left" value="10.0" step="0.5" min="0.5">
          </div>
        </div>
        <span class="hint" style="margin-top:6px;">Default left margin is wider for binding</span>
      </div>

      <div class="toggle-row">
        <div class="toggle-text">
          <span class="t-label">Mirror Margins</span>
          <span class="t-desc">Swaps left/right margins on even pages</span>
        </div>
        <label class="toggle-switch">
          <input type="checkbox" id="mirror" name="mirror" value="true">
          <span class="toggle-track"></span>
        </label>
      </div>
    </div>

    <!-- ── Generate ──────────────────────── -->
    <div class="gen-sec">
      <button type="submit" class="btn" id="genBtn">Generate PDF</button>
      <div class="status" id="status"></div>
    </div>

  </form>
</div>

<script>
  const TYPE_CONFIG = {
    H: { sizeLabel: 'Line Width',   sizeDefault: '0.1', sizeHint: 'mm — default 0.1',  widthLabel: 'Hex Size',      widthDefault: '10.0', widthHint: 'mm — default 10.0', showRotated: true  },
    L: { sizeLabel: 'Line Width',   sizeDefault: '0.1', sizeHint: 'mm — default 0.1',  widthLabel: 'Line Spacing',  widthDefault: '8.0',  widthHint: 'mm — default 8.0',  showRotated: false },
    D: { sizeLabel: 'Dot Size',     sizeDefault: '0.2', sizeHint: 'mm — default 0.2',  widthLabel: 'Dot Spacing',   widthDefault: '5.0',  widthHint: 'mm — default 5.0',  showRotated: false },
    S: { sizeLabel: 'Line Width',   sizeDefault: '0.1', sizeHint: 'mm — default 0.1',  widthLabel: 'Square Size',   widthDefault: '5.0',  widthHint: 'mm — default 5.0',  showRotated: false },
  };

  const sizeLabel    = document.getElementById('size-label');
  const sizeInput    = document.getElementById('size');
  const sizeHint     = document.getElementById('size-hint');
  const widthLabel   = document.getElementById('width-label');
  const widthInput   = document.getElementById('width');
  const widthHint    = document.getElementById('width-hint');
  const rotatedWrap  = document.getElementById('rotated-wrap');
  const rotatedInput = document.getElementById('rotated');

  function applyType(type) {
    const cfg = TYPE_CONFIG[type];
    sizeLabel.textContent   = cfg.sizeLabel;
    sizeInput.placeholder   = cfg.sizeDefault;
    sizeHint.textContent    = cfg.sizeHint;
    widthLabel.textContent  = cfg.widthLabel;
    widthInput.placeholder  = cfg.widthDefault;
    widthHint.textContent   = cfg.widthHint;
    if (cfg.showRotated) {
      rotatedWrap.classList.remove('hidden');
    } else {
      rotatedWrap.classList.add('hidden');
      rotatedInput.checked = false;
    }
  }

  applyType('H');

  document.querySelectorAll('input[name="page_type"]').forEach(r =>
    r.addEventListener('change', e => applyType(e.target.value))
  );

  // ── Form submit ──────────────────────────
  const form   = document.getElementById('form');
  const genBtn = document.getElementById('genBtn');
  const status = document.getElementById('status');

  form.addEventListener('submit', async e => {
    e.preventDefault();

    genBtn.disabled = true;
    genBtn.classList.add('loading');
    genBtn.textContent = 'Generating\u2026';
    status.className = 'status';

    const fd = new FormData(form);
    // Ensure boolean fields are always sent
    fd.set('mirror',  document.getElementById('mirror').checked  ? 'true' : 'false');
    fd.set('rotated', rotatedInput.checked ? 'true' : 'false');
    // Remove empty optional number fields
    ['size', 'width'].forEach(k => { if (!fd.get(k)) fd.delete(k); });

    try {
      const res = await fetch('/generate', { method: 'POST', body: fd });

      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        status.textContent = data.error || 'Generation failed.';
        status.className = 'status err';
        return;
      }

      const blob = await res.blob();
      const url  = URL.createObjectURL(blob);
      const a    = document.createElement('a');
      a.href     = url;
      a.download = `journal-${fd.get('page_type').toLowerCase()}-${fd.get('pagesize').toLowerCase()}.pdf`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);

      status.textContent = 'PDF downloaded successfully.';
      status.className = 'status ok';
    } catch {
      status.textContent = 'An unexpected error occurred.';
      status.className = 'status err';
    } finally {
      genBtn.disabled = false;
      genBtn.classList.remove('loading');
      genBtn.textContent = 'Generate PDF';
    }
  });
</script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
async def index():
    return HTML


@app.post("/generate")
async def generate(
    page_type: str = Form(...),
    pagesize: str = Form("A5"),
    size: Optional[str] = Form(None),
    width: Optional[str] = Form(None),
    numpages: int = Form(1),
    margin_top: float = Form(4.5),
    margin_right: float = Form(4.5),
    margin_bottom: float = Form(4.5),
    margin_left: float = Form(10.0),
    mirror: str = Form("false"),
    rotated: str = Form("false"),
):
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = os.path.join(tmpdir, "journal.pdf")

        cmd = [
            sys.executable, "-m", "py_journal_generator",
            "--type", page_type.upper(),
            "--pagesize", pagesize,
            "--numpages", str(numpages),
            "--output", output_path,
            "--margins", f"{margin_top},{margin_right},{margin_bottom},{margin_left}",
            "--mirror", mirror,
        ]

        if size and size.strip():
            cmd += ["--size", size.strip()]
        if width and width.strip():
            cmd += ["--width", width.strip()]
        if page_type.upper() == "H":
            cmd += ["--rotated", rotated]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(PROJECT_ROOT),
        )

        if result.returncode != 0:
            msg = result.stderr.strip() or result.stdout.strip() or "Generation failed."
            return JSONResponse({"error": msg}, status_code=400)

        with open(output_path, "rb") as f:
            pdf_bytes = f.read()

    filename = f"journal-{page_type.lower()}-{pagesize.lower()}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

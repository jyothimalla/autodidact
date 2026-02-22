"""
Learning Notes PDF generator.
  GET /learning/notes/{topic_id}   → download topic notes as a polished PDF
"""
import os
from fastapi import APIRouter
from fastapi.responses import FileResponse
from weasyprint import HTML

router = APIRouter()

NOTES_DIR = "generated_papers/learning_notes"

# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _html_to_pdf(html: str, path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    HTML(string=html).write_pdf(path)


# ---------------------------------------------------------------------------
# Shared CSS
# ---------------------------------------------------------------------------

BASE_CSS = """
  @page { size: A4; margin: 14mm 16mm 14mm 16mm; }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: Arial, Helvetica, sans-serif; color: #1a1a2e; font-size: 13px; }

  /* ── Page header (fixed – repeats every page) ── */
  .pg-hdr {
    position: fixed; top: 0; left: 0; right: 0;
    background: #16213e; color: white;
    padding: 3mm 16mm; font-size: 10px; font-weight: 700;
    letter-spacing: 0.5px;
    border-bottom: 3px solid #0f9b58;
  }
  .pg-hdr table { width: 100%; border-collapse: collapse; }
  .pg-hdr td { vertical-align: middle; padding: 0; }
  .pg-hdr .right { text-align: right; color: #7ed6a7; }

  /* ── Banner (page 1 only) ── */
  .banner {
    background: linear-gradient(135deg, #16213e 0%, #0f3460 60%, #0f9b58 100%);
    color: white; padding: 14mm 12mm 10mm;
    border-radius: 6px; margin-bottom: 10mm;
  }
  .banner .subject-tag {
    background: #0f9b58; display: inline-block;
    padding: 3px 10px; border-radius: 20px;
    font-size: 10px; font-weight: 700; letter-spacing: 1px;
    text-transform: uppercase; margin-bottom: 6px;
  }
  .banner h1 { font-size: 26px; font-weight: 900; line-height: 1.2; margin-bottom: 4px; }
  .banner .subtitle { font-size: 13px; color: #a8d8c0; }

  /* ── Section headings ── */
  .section { margin-bottom: 8mm; }
  .section-title {
    font-size: 15px; font-weight: 900; color: white;
    background: #0f3460; padding: 5px 10px;
    border-left: 5px solid #0f9b58;
    border-radius: 0 4px 4px 0; margin-bottom: 5mm;
  }
  .section-title .emoji { margin-right: 6px; }

  /* ── Callout boxes ── */
  .callout {
    border-left: 4px solid #0f9b58; background: #f0fbf5;
    padding: 6px 10px; border-radius: 0 6px 6px 0;
    margin-bottom: 4mm; font-size: 12.5px; line-height: 1.6;
  }
  .callout.fun { border-color: #e67e22; background: #fef9f0; }
  .callout.tip { border-color: #3498db; background: #f0f7ff; }
  .callout strong { color: #0f3460; }

  /* ── Karel world grid ── */
  .world-wrap { margin: 4mm 0; }
  .world-label { font-size: 10px; font-weight: 700; color: #555; margin-bottom: 2mm; text-transform: uppercase; letter-spacing: 0.5px; }
  .karel-world { border-collapse: collapse; border: 2px solid #0f3460; }
  .karel-world td {
    width: 24px; height: 24px;
    border: 1px solid #bbc; text-align: center;
    font-size: 12px; vertical-align: middle;
    background: #f8faff;
  }
  .karel-world td.wall  { background: #2c3e50; }
  .karel-world td.ball  { background: #fff3cd; }
  .karel-world td.karel { background: #d5f5e3; font-weight: 900; font-size: 14px; }
  .world-pair { display: table; width: 100%; border-collapse: collapse; }
  .world-pair .wp-cell { display: table-cell; vertical-align: top; padding-right: 10mm; }
  .world-pair .wp-cell:last-child { padding-right: 0; }
  .world-arrow { display: table-cell; vertical-align: middle; font-size: 22px; color: #0f9b58; font-weight: 900; padding: 0 6mm; width: 20px; }

  /* ── Code blocks ── */
  .code-wrap { background: #1e2a3a; border-radius: 6px; margin: 4mm 0; overflow: hidden; }
  .code-title {
    background: #0f3460; color: #7ed6a7;
    padding: 4px 10px; font-size: 10px; font-weight: 700;
    letter-spacing: 0.5px;
  }
  pre {
    color: #e8f4fd; font-family: 'Courier New', monospace;
    font-size: 12px; line-height: 1.7; padding: 8px 12px;
  }
  .kw  { color: #c792ea; }   /* keywords */
  .fn  { color: #82aaff; }   /* function names */
  .cm  { color: #546e7a; }   /* comments */
  .st  { color: #c3e88d; }   /* strings */
  .num { color: #f78c6c; }   /* numbers */

  /* ── Commands table ── */
  .cmd-table { width: 100%; border-collapse: collapse; margin: 4mm 0; }
  .cmd-table th {
    background: #0f3460; color: white; padding: 6px 10px;
    font-size: 11px; text-align: left;
  }
  .cmd-table td { padding: 6px 10px; border-bottom: 1px solid #e0e8f0; font-size: 12px; }
  .cmd-table tr:nth-child(even) td { background: #f5f8ff; }
  .cmd-table .cmd { font-family: 'Courier New', monospace; color: #0f3460; font-weight: 700; }
  .cmd-table .emoji-col { width: 30px; text-align: center; }

  /* ── Two-column layout ── */
  .two-col { display: table; width: 100%; border-collapse: collapse; }
  .two-col .col { display: table-cell; vertical-align: top; padding-right: 8mm; }
  .two-col .col:last-child { padding-right: 0; }

  /* ── Summary box ── */
  .summary-box {
    background: #16213e; color: white;
    border-radius: 8px; padding: 8mm 10mm; margin-top: 6mm;
  }
  .summary-box h3 { font-size: 15px; color: #0f9b58; margin-bottom: 4mm; }
  .summary-box ul { padding-left: 16px; }
  .summary-box li { font-size: 12px; line-height: 1.8; color: #d0e8f0; }

  /* ── Video box ── */
  .video-box {
    background: #fff3cd; border: 2px solid #f39c12;
    border-radius: 8px; padding: 6mm 8mm; margin-top: 6mm;
  }
  .video-box h4 { color: #e67e22; font-size: 13px; margin-bottom: 3mm; }
  .video-box p  { font-size: 12px; color: #555; line-height: 1.6; }
  .video-link { color: #0f3460; font-weight: 700; font-size: 12px; }

  /* ── Try it boxes ── */
  .try-it {
    background: #e8f4fd; border: 2px dashed #3498db;
    border-radius: 8px; padding: 5mm 8mm; margin: 4mm 0;
  }
  .try-it h4 { color: #2980b9; font-size: 12px; margin-bottom: 2mm; }
  .try-it p  { font-size: 12px; color: #444; line-height: 1.6; }

  /* ── Spacer for fixed header ── */
  .hdr-spacer { height: 11mm; }
"""


# ---------------------------------------------------------------------------
# Karel world helper
# ---------------------------------------------------------------------------

def _karel_grid(rows, cols, karel_pos, karel_dir="►", balls=None, walls=None, label=""):
    """
    Render an HTML Karel world grid.
    karel_pos: (row, col) 0-indexed from top-left
    balls: list of (row, col)
    walls: list of (row, col)
    """
    balls = set(map(tuple, balls or []))
    walls = set(map(tuple, walls or []))
    html = f'<div class="world-wrap">'
    if label:
        html += f'<div class="world-label">{label}</div>'
    html += '<table class="karel-world">'
    for r in range(rows):
        html += "<tr>"
        for c in range(cols):
            pos = (r, c)
            if pos in walls:
                html += '<td class="wall"></td>'
            elif pos == karel_pos:
                html += f'<td class="karel">{karel_dir}</td>'
            elif pos in balls:
                html += '<td class="ball">●</td>'
            else:
                html += "<td></td>"
        html += "</tr>"
    html += "</table></div>"
    return html


def _code(title, code_html):
    return f'<div class="code-wrap"><div class="code-title">🖥 {title}</div><pre>{code_html}</pre></div>'


# ---------------------------------------------------------------------------
# Topic: Introduction to Python with Karel
# ---------------------------------------------------------------------------

def _generate_karel_notes_html() -> str:

    # ── World diagrams ──────────────────────────────────────────────────────
    start_world   = _karel_grid(5, 6, (4, 0), "►", label="Start: Karel faces right")
    ex1_end_world = _karel_grid(5, 6, (4, 3), "►", label="After 3 × move()")
    ex2_start     = _karel_grid(5, 6, (4, 0), "►", label="Start: Karel faces right")
    ex2_end       = _karel_grid(5, 6, (4, 2), "►",
                                balls=[(4, 0), (4, 1), (4, 2)],
                                label="After placing 3 balls")
    fn_start      = _karel_grid(4, 5, (3, 0), "▲", label="Karel faces North (up)")
    fn_end        = _karel_grid(4, 5, (3, 0), "►", label="After turn_right(): faces East")

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
{BASE_CSS}
</style>
</head>
<body>

<!-- Fixed page header (repeats every page) -->
<div class="pg-hdr">
  <table>
    <tr>
      <td>Computing — Year 5/6 · Introduction to Python with Karel</td>
      <td class="right">autodidact.uk</td>
    </tr>
  </table>
</div>
<div class="hdr-spacer"></div>

<!-- ══════════════════════════════════════════════
     BANNER
══════════════════════════════════════════════ -->
<div class="banner">
  <div class="subject-tag">💻 Computing · Lesson 2 of 5</div>
  <h1>Introduction to Python<br>with Karel</h1>
  <div class="subtitle">Commanding a dog-robot to solve puzzles — your first steps in programming!</div>
</div>

<!-- ══════════════════════════════════════════════
     SECTION 1 — MEET KAREL
══════════════════════════════════════════════ -->
<div class="section">
  <div class="section-title"><span class="emoji">🐕</span>Meet Karel</div>

  <div class="callout fun">
    <strong>Who is Karel?</strong> Karel is a friendly robot dog that lives inside a grid world.
    You are the programmer — you give Karel instructions and Karel follows them exactly.
    If you make a mistake, Karel gets confused! That's why we must write our code carefully.
  </div>

  <div class="two-col">
    <div class="col">
      <p style="margin-bottom:3mm; line-height:1.7;">
        Karel's world is a <strong>grid of squares</strong>. Karel can:<br>
        • Move forward one square<br>
        • Turn left (90°)<br>
        • Pick up and place tennis balls<br>
        • Follow functions you define<br><br>
        The <strong>►</strong> symbol shows where Karel is and which direction Karel faces.
        Karel always starts at the <strong>bottom-left</strong> corner facing <strong>East</strong> (right).
      </p>
    </div>
    <div class="col">
      {start_world}
      <p style="font-size:11px; color:#666; margin-top:2mm;">
        ► = Karel &nbsp;|&nbsp; ● = Ball &nbsp;|&nbsp; ■ = Wall
      </p>
    </div>
  </div>
</div>

<!-- ══════════════════════════════════════════════
     SECTION 2 — BASIC COMMANDS
══════════════════════════════════════════════ -->
<div class="section">
  <div class="section-title"><span class="emoji">📋</span>Karel's Basic Commands</div>

  <div class="callout tip">
    <strong>Important rule:</strong> All Python commands must be written <em>exactly</em> right —
    correct spelling, correct brackets <code>()</code>, and no extra spaces.
    Python is case-sensitive: <code>Move()</code> is NOT the same as <code>move()</code>!
  </div>

  <table class="cmd-table">
    <tr>
      <th class="emoji-col"></th>
      <th>Command</th>
      <th>What it does</th>
      <th>Think of it as…</th>
    </tr>
    <tr>
      <td>🏃</td>
      <td class="cmd">move()</td>
      <td>Karel moves one square forward</td>
      <td>Take one step</td>
    </tr>
    <tr>
      <td>↺</td>
      <td class="cmd">turn_left()</td>
      <td>Karel turns 90° to the left</td>
      <td>Spin left like a dancer</td>
    </tr>
    <tr>
      <td>🎾</td>
      <td class="cmd">put_ball()</td>
      <td>Karel places a tennis ball on the current square</td>
      <td>Drop a ball here</td>
    </tr>
    <tr>
      <td>🤏</td>
      <td class="cmd">take_ball()</td>
      <td>Karel picks up a ball from the current square</td>
      <td>Pick it up</td>
    </tr>
    <tr>
      <td>↩</td>
      <td class="cmd">turn_around()</td>
      <td>Karel turns 180° — faces the opposite direction</td>
      <td>Do a U-turn</td>
    </tr>
  </table>
</div>

<!-- ══════════════════════════════════════════════
     SECTION 3 — EXAMPLE 1
══════════════════════════════════════════════ -->
<div class="section">
  <div class="section-title"><span class="emoji">🧪</span>Example 1 — Moving Karel Across the Grid</div>

  <div class="callout">
    <strong>Challenge:</strong> Karel starts at the left side facing right.
    Move Karel <strong>3 squares to the right</strong>.
  </div>

  <div class="world-pair">
    <div class="wp-cell">{ex1_end_world.replace("Start: Karel faces right","Before: Karel at column 0")}</div>
    <div class="world-arrow">→</div>
    <div class="wp-cell">{ex1_end_world}</div>
  </div>

  {_code("solution_example1.py",
    '<span class="cm"># Move Karel 3 squares to the right</span>\n'
    '<span class="fn">move</span>()   <span class="cm"># step 1 → Karel moves to column 1</span>\n'
    '<span class="fn">move</span>()   <span class="cm"># step 2 → Karel moves to column 2</span>\n'
    '<span class="fn">move</span>()   <span class="cm"># step 3 → Karel moves to column 3</span>'
  )}

  <div class="callout tip">
    <strong>Key idea:</strong> Each <code>move()</code> is one instruction. The computer runs them
    <strong>one at a time, top to bottom</strong>. This is called <em>sequential execution</em>.
  </div>

  <div class="try-it">
    <h4>✏️ Try it yourself!</h4>
    <p>What code would move Karel <strong>5 squares</strong> to the right? Write it out on paper before typing it!</p>
  </div>
</div>

<!-- ══════════════════════════════════════════════
     SECTION 4 — EXAMPLE 2
══════════════════════════════════════════════ -->
<div class="section">
  <div class="section-title"><span class="emoji">🎾</span>Example 2 — Placing Tennis Balls</div>

  <div class="callout">
    <strong>Challenge:</strong> Karel starts facing right at the left side.
    Place a tennis ball on <strong>each of the first 3 squares</strong> Karel visits.
  </div>

  <div class="world-pair">
    <div class="wp-cell">{ex2_start}</div>
    <div class="world-arrow">→</div>
    <div class="wp-cell">{ex2_end}</div>
  </div>

  {_code("solution_example2.py",
    '<span class="cm"># Place a ball, move, repeat...</span>\n'
    '<span class="fn">put_ball</span>()  <span class="cm"># drop ball on square 0</span>\n'
    '<span class="fn">move</span>()      <span class="cm"># step to square 1</span>\n'
    '<span class="fn">put_ball</span>()  <span class="cm"># drop ball on square 1</span>\n'
    '<span class="fn">move</span>()      <span class="cm"># step to square 2</span>\n'
    '<span class="fn">put_ball</span>()  <span class="cm"># drop ball on square 2</span>'
  )}

  <div class="callout fun">
    <strong>Spot the pattern!</strong> We repeated <code>put_ball() → move()</code> three times.
    Whenever you repeat something, there's usually a smarter way — called a <em>loop</em>.
    We'll learn loops in Lesson 3! 🚀
  </div>

  <div class="try-it">
    <h4>✏️ Try it yourself!</h4>
    <p>How would you pick up all 3 balls Karel just placed? Hint: use <code>take_ball()</code> and <code>move()</code>.</p>
  </div>
</div>

<!-- ══════════════════════════════════════════════
     SECTION 5 — FUNCTIONS
══════════════════════════════════════════════ -->
<div class="section">
  <div class="section-title"><span class="emoji">⚙️</span>Creating Your Own Commands — Functions</div>

  <div class="callout">
    <strong>Problem:</strong> Karel can turn <em>left</em> with <code>turn_left()</code>,
    but there is <strong>no</strong> <code>turn_right()</code> command!
    How do we make Karel turn right?
  </div>

  <div class="callout tip">
    <strong>Maths trick:</strong> Turning left 3 times = turning right once!
    (3 × 90° left = 270° left = 90° right)
  </div>

  <div class="world-pair">
    <div class="wp-cell">{fn_start}</div>
    <div class="world-arrow">→</div>
    <div class="wp-cell">{fn_end}</div>
  </div>

  {_code("turn_right_function.py",
    '<span class="cm"># Define a new command called turn_right</span>\n'
    '<span class="kw">def</span> <span class="fn">turn_right</span>():\n'
    '    <span class="fn">turn_left</span>()  <span class="cm"># 1st left turn (90°)</span>\n'
    '    <span class="fn">turn_left</span>()  <span class="cm"># 2nd left turn (180°)</span>\n'
    '    <span class="fn">turn_left</span>()  <span class="cm"># 3rd left turn (270° = turn right!)</span>\n'
    '\n'
    '<span class="cm"># ── Now we can USE our new command ──</span>\n'
    '<span class="fn">move</span>()       <span class="cm"># Karel steps forward</span>\n'
    '<span class="fn">turn_right</span>() <span class="cm"># Karel turns right using our function</span>\n'
    '<span class="fn">move</span>()       <span class="cm"># Karel steps forward again</span>'
  )}

  <div class="callout">
    <strong>Rules for writing a function:</strong><br>
    1. Start with the keyword <code><span style="color:#0f3460">def</span></code><br>
    2. Write the function name (no spaces!)<br>
    3. Add brackets <code>()</code> and a colon <code>:</code><br>
    4. Indent the body by 4 spaces — Python is strict about this!<br>
    5. Call the function anywhere in your code by writing its name followed by <code>()</code>
  </div>
</div>

<!-- ══════════════════════════════════════════════
     SECTION 6 — SUMMARY
══════════════════════════════════════════════ -->
<div class="section">
  <div class="section-title"><span class="emoji">📝</span>Summary</div>

  <div class="summary-box">
    <h3>✅ What you learned today</h3>
    <ul>
      <li>Karel is a robot dog that lives in a grid — you control it with Python commands</li>
      <li><code>move()</code> moves Karel one square forward in the direction it faces</li>
      <li><code>turn_left()</code> rotates Karel 90° to the left</li>
      <li><code>put_ball()</code> and <code>take_ball()</code> interact with tennis balls</li>
      <li>Python runs instructions <strong>one line at a time</strong>, top to bottom</li>
      <li>You can create <strong>your own commands</strong> using <code>def function_name():</code></li>
      <li>Indentation (4 spaces) inside a function is <strong>not optional</strong> — Python needs it!</li>
      <li>Turning left 3 times = turning right once (a clever trick!)</li>
    </ul>
  </div>

  <div class="video-box">
    <h4>🎬 Watch &amp; Learn — Recommended Videos</h4>
    <p>
      <strong>1. Karel the Dog — Introduction (CS106A Stanford)</strong><br>
      <span class="video-link">https://www.youtube.com/watch?v=d8RRE2rDiEg</span><br><br>
      <strong>2. Python with Karel — CodeHS Tutorial</strong><br>
      <span class="video-link">https://codehs.com/course/intro_python_karel</span><br><br>
      <strong>3. Interactive Karel Exercises</strong><br>
      <span class="video-link">https://stanford.edu/~cpiech/karel/ide.html</span><br><br>
      <em style="font-size:11px; color:#888;">
        Ask a parent or teacher to help you open these links on a computer.
        Try the interactive Karel IDE — you can run your code and watch Karel move!
      </em>
    </p>
  </div>
</div>

</body>
</html>
"""


# ---------------------------------------------------------------------------
# Route
# ---------------------------------------------------------------------------

TOPIC_GENERATORS = {
    "python-with-karel": _generate_karel_notes_html,
}

@router.get("/notes/{topic_id}")
def get_learning_notes(topic_id: str):
    """Download learning notes PDF for a topic."""
    generator = TOPIC_GENERATORS.get(topic_id)
    if not generator:
        from fastapi import HTTPException
        raise HTTPException(404, f"Notes for topic '{topic_id}' not found. "
                                  f"Available: {list(TOPIC_GENERATORS.keys())}")

    html = generator()
    filename = f"{topic_id}_notes.pdf"
    path = os.path.join(NOTES_DIR, filename)
    _html_to_pdf(html, path)
    return FileResponse(path, media_type="application/pdf", filename=filename)

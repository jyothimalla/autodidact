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
  .world-pair .wp-cell { display: table-cell; vertical-align: top; padding-right: 8mm; width: 44%; }
  .world-pair .wp-cell:last-child { padding-right: 0; width: 44%; }
  .world-arrow { display: table-cell; vertical-align: middle; font-size: 22px; color: #0f9b58; font-weight: 900; padding: 0 4mm; width: 12%; text-align: center; }

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
  .two-col .col { display: table-cell; vertical-align: top; padding-right: 8mm; width: 50%; }
  .two-col .col:last-child { padding-right: 0; width: 50%; }

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
    start_world     = _karel_grid(5, 6, (4, 0), "►", label="Karel's world — facing East")
    ex1_start_world = _karel_grid(5, 6, (4, 0), "►", label="Start world")
    ex1_end_world   = _karel_grid(5, 6, (4, 3), "►", label="End world (after 3 × move())")
    ex2_start       = _karel_grid(5, 6, (4, 0), "►", label="Start world")
    ex2_end         = _karel_grid(5, 6, (4, 2), "►",
                                  balls=[(4, 0), (4, 1), (4, 2)],
                                  label="End world (3 balls placed)")
    fn_start        = _karel_grid(4, 5, (3, 0), "▲", label="Start world (Karel faces North)")
    fn_end          = _karel_grid(4, 5, (3, 0), "►", label="End world (after turn_right())")
    ex1_code = _code(
        "walk_karel.py",
        """
<span class="cm"># Let's take Karel for a walk — 3 steps to the right!</span>
<span class="fn">move</span>()   <span class="cm"># 🐾 step 1 → Karel trots to column 1</span>
<span class="fn">move</span>()   <span class="cm"># 🐾 step 2 → Karel trots to column 2</span>
<span class="fn">move</span>()   <span class="cm"># 🐾 step 3 → Karel trots to column 3</span>
""".strip(),
    )
    ex2_code = _code(
        "fetch_balls.py",
        """
<span class="cm"># Karel drops a ball, then moves — and repeats!</span>
<span class="fn">put_ball</span>()  <span class="cm"># 🎾 drop ball on square 0</span>
<span class="fn">move</span>()      <span class="cm"># 🐾 trot to square 1</span>
<span class="fn">put_ball</span>()  <span class="cm"># 🎾 drop ball on square 1</span>
<span class="fn">move</span>()      <span class="cm"># 🐾 trot to square 2</span>
<span class="fn">put_ball</span>()  <span class="cm"># 🎾 drop ball on square 2</span>
""".strip(),
    )
    fn_code = _code(
        "turn_right.py",
        """
<span class="cm"># ── DEFINE the new trick first ──────────────────</span>
<span class="kw">def</span> <span class="fn">turn_right</span>():          <span class="cm"># "def" means DEFINE a new command</span>
    <span class="fn">turn_left</span>()  <span class="cm"># 🔄 1st left (90°)</span>
    <span class="fn">turn_left</span>()  <span class="cm"># 🔄 2nd left (180°)</span>
    <span class="fn">turn_left</span>()  <span class="cm"># 🔄 3rd left = 270° = turned right! ✅</span>

<span class="cm"># ── NOW use the new trick ───────────────────────</span>
<span class="fn">move</span>()           <span class="cm"># 🐾 Karel steps forward</span>
<span class="fn">turn_right</span>()    <span class="cm"># ↻ Karel uses our new trick to turn right</span>
<span class="fn">move</span>()           <span class="cm"># 🐾 Karel steps forward again</span>
""".strip(),
    )

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
{BASE_CSS}

/* ── Compass / direction diagram ── */
.compass-box {{
  display: table; width: 100%; border-collapse: collapse;
  margin: 4mm 0;
}}
.compass-box td {{
  padding: 3px 6px; text-align: center; font-size: 12px; vertical-align: middle;
}}
.compass-center {{
  background: #d5f5e3; border: 2px solid #0f9b58;
  border-radius: 6px; font-size: 18px; font-weight: 900;
  width: 36px; height: 36px; padding: 0 !important;
}}
.compass-dir {{ font-size: 11px; font-weight: 700; color: #0f3460; }}
.compass-arrow {{ font-size: 18px; color: #0f9b58; font-weight: 900; }}

/* ── Direction table (relative) ── */
.dir-table {{ width: 100%; border-collapse: collapse; margin: 3mm 0; font-size: 12px; }}
.dir-table th {{ background: #0f3460; color: white; padding: 5px 8px; text-align: left; font-size: 11px; }}
.dir-table td {{ padding: 5px 8px; border-bottom: 1px solid #e0e8f0; }}
.dir-table tr:nth-child(even) td {{ background: #f5f8ff; }}
.dir-table .arrow {{ font-size: 16px; text-align: center; }}

/* ── Fun fact box ── */
.fun-fact {{
  background: linear-gradient(135deg, #fff9e6, #fff3c4);
  border: 2px solid #f39c12; border-radius: 8px;
  padding: 5mm 8mm; margin: 4mm 0;
}}
.fun-fact h4 {{ color: #d35400; font-size: 12px; margin-bottom: 2mm; }}
.fun-fact p  {{ font-size: 12px; color: #444; line-height: 1.6; }}

/* ── Other names box ── */
.names-grid {{ display: table; width: 100%; border-collapse: collapse; margin: 3mm 0; }}
.names-grid .ng-cell {{
  display: table-cell; vertical-align: middle;
  background: #e8f4fd; border: 2px solid #3498db;
  border-radius: 8px; padding: 4px 10px; margin: 2px;
  text-align: center; font-weight: 700; font-size: 11.5px;
  color: #1a5276;
}}
</style>
</head>
<body>

<!-- Fixed page header -->
<div class="pg-hdr">
  <table>
    <tr>
      <td>🐕 Computing — Year 5/6 · Introduction to Python with Karel</td>
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
  <h1>Introduction to Python<br>with Karel 🐕</h1>
  <div class="subtitle">Karel is a dog who listens to YOUR commands — let's teach her some tricks in Python!</div>
</div>

<!-- ══════════════════════════════════════════════
     SECTION 1 — MEET KAREL THE DOG
══════════════════════════════════════════════ -->
<div class="section">
  <div class="section-title"><span class="emoji">🐕</span>Meet Karel — A Dog Who Listens to Your Commands!</div>

  <div class="callout fun">
    <strong>The Story of Karel 🐕</strong><br>
    Once upon a time there was a clever dog called <strong>Karel</strong>.
    Karel lives inside a special <strong>grid world</strong> made of squares — like a chess board!
    Karel loves to explore the world and collect <strong>tennis balls</strong>. 🎾<br><br>
    But Karel needs a programmer — <strong>that's you!</strong> You write instructions in Python
    and Karel follows them <em>exactly</em>. If you make even one tiny spelling mistake,
    Karel gets confused and doesn't know what to do!
  </div>

  <div class="two-col">
    <div class="col">
      <p style="line-height:1.8; margin-bottom:3mm;">
        <strong>Karel's world:</strong><br>
        • A grid of squares (like a chess board)<br>
        • Karel can <strong>move</strong> from square to square<br>
        • There are <strong>tennis balls</strong> Karel can pick up or place<br>
        • There can be <strong>walls</strong> blocking the way<br><br>
        <strong>Karel always starts:</strong><br>
        • At the <strong>bottom-left</strong> corner<br>
        • Facing <strong>East</strong> → (to the right)<br><br>
        The <strong>► symbol</strong> shows Karel's position and direction.
      </p>

      <!-- Compass diagram -->
      <table class="compass-box">
        <tr>
          <td></td>
          <td class="compass-dir">NORTH ▲</td>
          <td></td>
        </tr>
        <tr>
          <td class="compass-dir">◄ WEST</td>
          <td class="compass-center">🐕</td>
          <td class="compass-dir">EAST ►</td>
        </tr>
        <tr>
          <td></td>
          <td class="compass-dir">SOUTH ▼</td>
          <td></td>
        </tr>
      </table>
      <p style="font-size:10px; color:#666; text-align:center; margin-top:1mm;">
        Karel's compass — East = right, North = up
      </p>
    </div>
    <div class="col">
      {start_world}
      <p style="font-size:11px; color:#555; margin-top:2mm; line-height:1.6;">
        ► = Karel (facing East) &nbsp;|&nbsp; ● = Tennis ball &nbsp;|&nbsp; ■ = Wall<br><br>
        Karel starts at the bottom-left, facing right (East).
        We move Karel by writing Python commands!
      </p>
    </div>
  </div>

  <!-- Relative directions -->
  <div class="callout tip" style="margin-top:4mm;">
    <strong>Karel's relative directions</strong> (from Karel's point of view when facing East →):<br><br>
    <table class="dir-table">
      <tr>
        <th>Direction</th><th>Compass</th><th>On the Grid</th>
      </tr>
      <tr><td><strong>Front</strong> (straight ahead)</td><td>East ►</td><td>Move right on the grid</td></tr>
      <tr><td><strong>Left</strong></td><td>North ▲</td><td>Move upwards on the grid</td></tr>
      <tr><td><strong>Right</strong></td><td>South ▼</td><td>Move downwards on the grid</td></tr>
      <tr><td><strong>Behind</strong></td><td>West ◄</td><td>Move left on the grid</td></tr>
    </table>
    <em style="font-size:11px;">These change when Karel turns! "Front" always means the direction Karel is currently facing.</em>
  </div>
</div>

<!-- ══════════════════════════════════════════════
     SECTION 2 — BASIC COMMANDS
══════════════════════════════════════════════ -->
<div class="section">
  <div class="section-title"><span class="emoji">🎓</span>Karel's Basic Commands — Teaching Karel Tricks!</div>

  <div class="callout fun">
    <strong>The Golden Rule of Python Commands 🏆</strong><br>
    All commands must be written <strong>exactly right</strong>:<br>
    ✅ correct spelling &nbsp;|&nbsp; ✅ lowercase letters &nbsp;|&nbsp;
    ✅ brackets <code>()</code> at the end &nbsp;|&nbsp; ✅ no extra spaces<br><br>
    Python is case-sensitive: <code>Move()</code> is NOT the same as <code>move()</code>!
    If you get it wrong, Karel will just sit there looking confused! 🐕❓
  </div>

  <table class="cmd-table">
    <tr>
      <th class="emoji-col"></th>
      <th>Command</th>
      <th>What Karel does</th>
      <th>Think of it as…</th>
    </tr>
    <tr>
      <td>🐾</td>
      <td class="cmd">move()</td>
      <td>Karel takes one step forward (in the direction she's facing)</td>
      <td>Take one step, good dog!</td>
    </tr>
    <tr>
      <td>↺</td>
      <td class="cmd">turn_left()</td>
      <td>Karel turns 90° to the left (anticlockwise)</td>
      <td>Spin left — like a dog chasing her tail!</td>
    </tr>
    <tr>
      <td>🎾</td>
      <td class="cmd">put_ball()</td>
      <td>Karel drops a tennis ball on the current square</td>
      <td>Drop the ball here!</td>
    </tr>
    <tr>
      <td>🤏</td>
      <td class="cmd">take_ball()</td>
      <td>Karel picks up a tennis ball from the current square</td>
      <td>Fetch! Pick it up!</td>
    </tr>
    <tr>
      <td>↩</td>
      <td class="cmd">turn_around()</td>
      <td>Karel turns 180° — faces the completely opposite direction</td>
      <td>About turn — go back the way you came!</td>
    </tr>
  </table>

  <div class="fun-fact">
    <h4>🐾 Fun Fact — Karel is Named After a Person!</h4>
    <p>Karel the dog is named after <strong>Karel Čapek</strong> — a Czech writer who first used the word
    "robot" in a play in 1920. The programming language "Karel" was invented at Stanford University
    to help beginners learn coding by thinking like a dog trainer!</p>
  </div>
</div>

<!-- ══════════════════════════════════════════════
     SECTION 3 — EXAMPLE 1: MOVING KAREL
══════════════════════════════════════════════ -->
<div class="section">
  <div class="section-title"><span class="emoji">🐾</span>Example 1 — Let's Take Karel for a Walk!</div>

  <div class="callout">
    <strong>The story:</strong> Karel is at the left side of her world, facing right (East). 🐕►<br>
    <strong>Challenge:</strong> Give Karel exactly the right commands to move her
    <strong>3 squares to the right</strong>.
  </div>

  <div class="world-pair">
    <div class="wp-cell">{ex1_start_world}</div>
    <div class="world-arrow">→</div>
    <div class="wp-cell">{ex1_end_world}</div>
  </div>

  {ex1_code}

  <div class="callout tip">
    <strong>Key idea — Sequential Execution 📜</strong><br>
    The computer reads instructions <strong>one line at a time, from top to bottom</strong> —
    just like reading a book! This is called <em>sequential execution</em>.
    Karel runs line 1, then line 2, then line 3 — always in order.
  </div>

  <div class="try-it">
    <h4>✏️ Your turn — Take Karel for a longer walk!</h4>
    <p>Write the Python code to move Karel <strong>5 squares</strong> to the right.
    How many <code>move()</code> commands do you need? Write it out on paper first!</p>
  </div>
</div>

<!-- ══════════════════════════════════════════════
     SECTION 4 — EXAMPLE 2: PLACING TENNIS BALLS
══════════════════════════════════════════════ -->
<div class="section">
  <div class="section-title"><span class="emoji">🎾</span>Example 2 — Fetch! Karel Drops Tennis Balls</div>

  <div class="callout">
    <strong>The story:</strong> Karel loves tennis balls! 🎾🎾🎾<br>
    <strong>Challenge:</strong> Karel starts at the left, facing right.
    Karel must <strong>drop a ball on each of the first 3 squares</strong> she visits.
  </div>

  <div class="world-pair">
    <div class="wp-cell">{ex2_start}</div>
    <div class="world-arrow">→</div>
    <div class="wp-cell">{ex2_end}</div>
  </div>

  {ex2_code}

  <div class="callout fun">
    <strong>Can you spot the pattern? 🔍</strong><br>
    We repeated <code>put_ball() → move()</code> exactly three times.
    Whenever you spot a pattern that repeats, there is <strong>almost always a smarter way</strong> to write it —
    using a <em>loop</em>! We'll learn loops in Lesson 3! 🚀
  </div>

  <div class="try-it">
    <h4>✏️ Your turn — Now collect the balls!</h4>
    <p>Write the code to make Karel <strong>pick up</strong> all 3 balls she just placed.
    Hint: use <code>take_ball()</code> and <code>move()</code>. Draw the start and end worlds first!</p>
  </div>
</div>

<!-- ══════════════════════════════════════════════
     SECTION 5 — FUNCTIONS: TEACHING KAREL NEW TRICKS
══════════════════════════════════════════════ -->
<div class="section">
  <div class="section-title"><span class="emoji">⚙️</span>Functions — Teaching Karel Brand New Tricks!</div>

  <div class="callout fun">
    <strong>The problem 🤔</strong><br>
    Karel knows how to turn <em>left</em> with <code>turn_left()</code>.<br>
    But Karel has <strong>no</strong> <code>turn_right()</code> command!
    How do we make Karel turn right? We need to <strong>teach her a new trick</strong>!
  </div>

  <div class="callout tip">
    <strong>Maths trick 🧮</strong><br>
    Turning <em>left</em> three times is the same as turning <em>right</em> once!<br>
    3 × 90° left = 270° left = 90° right ✅
  </div>

  <div class="world-pair">
    <div class="wp-cell">{fn_start}</div>
    <div class="world-arrow">→</div>
    <div class="wp-cell">{fn_end}</div>
  </div>

  {fn_code}

  <div class="callout">
    <strong>📋 Rules for writing a function (teaching a new trick):</strong><br>
    1. Start with the keyword <code><strong>def</strong></code> (short for "define")<br>
    2. Write the function name — no spaces! Use underscores: <code>turn_right</code><br>
    3. Add brackets <code>()</code> and a colon <code>:</code> at the end of the line<br>
    4. Indent the body by <strong>4 spaces</strong> — Python MUST see those spaces!<br>
    5. The function must be <strong>defined BEFORE</strong> you call it<br>
    6. Call it from the main code by writing its name followed by <code>()</code>
  </div>

  <!-- Other names for functions -->
  <div class="callout tip" style="margin-top:4mm;">
    <strong>💡 Did you know? Functions have many names!</strong><br>
    When you talk to other programmers, they might call a function by a different name.
    They all mean the same thing — a named block of code you can reuse!<br><br>
    <table class="cmd-table" style="margin-top:2mm;">
      <tr>
        <th>Name</th><th>Used in…</th><th>Meaning</th>
      </tr>
      <tr><td><strong>Function</strong></td><td>Python, most languages</td><td>A named block of reusable code</td></tr>
      <tr><td><strong>Procedure</strong></td><td>Pascal, older languages</td><td>Same idea — a named sequence of steps</td></tr>
      <tr><td><strong>Subroutine</strong></td><td>BASIC, old programming</td><td>A sub-program that can be called</td></tr>
      <tr><td><strong>Method</strong></td><td>Java, C++, Python (in classes)</td><td>A function that belongs to an object</td></tr>
      <tr><td><strong>Module</strong></td><td>General computing</td><td>A larger unit of reusable code</td></tr>
    </table>
  </div>
</div>

<!-- ══════════════════════════════════════════════
     SECTION 6 — SUMMARY
══════════════════════════════════════════════ -->
<div class="section">
  <div class="section-title"><span class="emoji">📝</span>Summary — What Karel Taught Us Today</div>

  <div class="summary-box">
    <h3>🐕 Karel's Story — Key Takeaways</h3>
    <ul>
      <li>Karel is a <strong>dog</strong> who lives in a grid world — you control her with Python commands</li>
      <li>Karel starts at the <strong>bottom-left</strong>, always facing <strong>East</strong> (→)</li>
      <li>The compass: North = up ▲, South = down ▼, East = right ►, West = left ◄</li>
      <li><code>move()</code> — Karel takes one step in whichever direction she's facing</li>
      <li><code>turn_left()</code> — Karel spins 90° anticlockwise (to the left)</li>
      <li><code>put_ball()</code> — Karel drops a tennis ball on her current square</li>
      <li><code>take_ball()</code> — Karel picks up a ball (the square must have one!)</li>
      <li>Python runs instructions <strong>one line at a time, top to bottom</strong> — sequential execution</li>
      <li>A <strong>function</strong> (also called a procedure/subroutine) lets you <strong>teach Karel a new trick</strong></li>
      <li>Write <code>def function_name():</code> then indent the body by <strong>4 spaces</strong></li>
      <li>Turning left 3 times = turning right once — a very useful trick! 🧮</li>
      <li>All commands must be exact: correct spelling, lowercase, brackets <code>()</code> at the end</li>
    </ul>
  </div>

  <div class="video-box">
    <h4>🎬 Watch Karel in Action!</h4>
    <p>
      <strong>1. Karel the Dog — Introduction (CS106A Stanford)</strong><br>
      <span class="video-link">https://www.youtube.com/watch?v=d8RRE2rDiEg</span><br><br>
      <strong>2. Python with Karel — CodeHS Tutorial</strong><br>
      <span class="video-link">https://codehs.com/course/intro_python_karel</span><br><br>
      <strong>3. Run your own Karel code online!</strong><br>
      <span class="video-link">https://stanford.edu/~cpiech/karel/ide.html</span><br><br>
      <em style="font-size:11px; color:#888;">
        Ask a parent or teacher to help you open these links.
        In the interactive IDE, you can watch Karel move on screen as your code runs! 🐕🎾
      </em>
    </p>
  </div>
</div>

</body>
</html>
"""


# ---------------------------------------------------------------------------
# Shared maths helpers
# ---------------------------------------------------------------------------

def _col_method(title, rows, result, highlight_carries=None):
    """Render a simple column-method working box."""
    carries = highlight_carries or ""
    inner = ""
    for i, row in enumerate(rows):
        op = row[0] if i > 0 else "&nbsp;"
        num = row[1] if i > 0 else row[0] if isinstance(row, (list, tuple)) and len(row) == 1 else (row[1] if len(row) > 1 else row[0])
        # Accept either (operator, number) or just (number,)
        if isinstance(row, (list, tuple)):
            if len(row) == 2:
                op, num = row
            else:
                op, num = "&nbsp;", row[0]
        inner += f'<tr><td style="text-align:right;width:24px;color:#0f9b58;font-weight:900;">{op}</td><td style="text-align:right;font-family:\'Courier New\',monospace;font-size:13px;letter-spacing:1px;">{num}</td></tr>'
    return f"""<div style="display:inline-block;background:#f0fbf5;border:2px solid #0f9b58;border-radius:6px;padding:6px 14px;margin:3mm 0;">
<p style="font-size:10px;font-weight:700;color:#555;margin-bottom:2px;text-transform:uppercase;">{title}</p>
{f'<p style="font-size:10px;color:#e67e22;font-family:Courier New,monospace;letter-spacing:1px;margin-bottom:2px;">carries: {carries}</p>' if carries else ""}
<table style="border-collapse:collapse;">{inner}
<tr><td colspan="2" style="border-top:2.5px solid #0f3460;"></td></tr>
<tr><td></td><td style="text-align:right;font-family:\'Courier New\',monospace;font-size:14px;font-weight:900;color:#0f3460;">{result}</td></tr>
</table></div>"""

def _maths_page(topic_tag, lesson_info, title, subtitle, body):
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>{BASE_CSS}</style></head><body>
<div class="pg-hdr"><table><tr>
  <td>Maths — {topic_tag} · {lesson_info}</td>
  <td class="right">autodidact.uk</td>
</tr></table></div>
<div class="hdr-spacer"></div>
<div class="banner">
  <div class="subject-tag">➕ Maths · {lesson_info}</div>
  <h1>{title}</h1>
  <div class="subtitle">{subtitle}</div>
</div>
{body}
</body></html>"""


# ---------------------------------------------------------------------------
# MATHS — Addition Level 1
# ---------------------------------------------------------------------------

def _generate_addition_level1_notes_html() -> str:
    body = """
<div class="section">
  <div class="section-title"><span class="emoji">🔢</span>What is Addition?</div>
  <div class="callout fun">
    <strong>Addition means combining two or more numbers together to find the total.</strong>
    The symbol for addition is <strong>+</strong>.
    The answer is called the <strong>sum</strong> or <strong>total</strong>.
  </div>
  <div class="callout tip">
    <strong>Key vocabulary:</strong> addend + addend = sum &nbsp;|&nbsp;
    e.g. <strong>47 + 35 = 82</strong> (47 and 35 are addends; 82 is the sum)
  </div>
</div>

<div class="section">
  <div class="section-title"><span class="emoji">📋</span>The Column Method — Step by Step</div>
  <div class="callout">
    <strong>The golden rule:</strong> Always line up digits by their <strong>place value</strong>
    — units under units, tens under tens, hundreds under hundreds!
  </div>
  <div class="two-col">
    <div class="col">
      <p style="line-height:1.9;font-size:12.5px;">
        <strong>Steps for column addition:</strong><br>
        1. Write the numbers in columns (units, tens, hundreds…)<br>
        2. Start at the <strong>right</strong> — always add units first<br>
        3. If the answer is 10 or more, write the units digit and <strong>carry</strong> the tens digit<br>
        4. Move left — add the tens column (plus any carry)<br>
        5. Continue until all columns are done<br>
        6. Write the final answer
      </p>
    </div>
    <div class="col">
      <p style="font-size:12px;font-weight:700;color:#0f3460;margin-bottom:2mm;">Example: 47 + 35</p>
      <div style="background:#1e2a3a;border-radius:6px;padding:8px 14px;font-family:'Courier New',monospace;font-size:13px;color:#e8f4fd;line-height:2;">
        &nbsp;&nbsp;T &nbsp;U<br>
        &nbsp;&nbsp;4 &nbsp;7<br>
        + &nbsp;3 &nbsp;5<br>
        <span style="display:block;border-top:2px solid #0f9b58;color:#7ed6a7;font-size:10px;padding-top:2px;">carry: &nbsp;1</span>
        &nbsp;&nbsp;8 &nbsp;2
      </div>
      <p style="font-size:11px;color:#555;margin-top:2mm;">7+5=12 → write 2, carry 1 &nbsp;|&nbsp; 4+3+1=8</p>
    </div>
  </div>
</div>

<div class="section">
  <div class="section-title"><span class="emoji">🧪</span>Worked Examples</div>
  <div class="two-col">
    <div class="col">
      <div class="callout">
        <strong>Example 1:</strong> 63 + 28<br>
        <div style="font-family:'Courier New',monospace;font-size:12px;background:#f0fbf5;padding:6px;border-radius:4px;margin-top:3px;line-height:1.9;">
          &nbsp;&nbsp;6 3<br>+ 2 8<br><span style="border-top:1.5px solid #0f3460;display:block;"></span>&nbsp;&nbsp;9 1
        </div>
        3+8=11 → write 1, carry 1<br>6+2+1=9
      </div>
    </div>
    <div class="col">
      <div class="callout">
        <strong>Example 2:</strong> 156 + 247<br>
        <div style="font-family:'Courier New',monospace;font-size:12px;background:#f0fbf5;padding:6px;border-radius:4px;margin-top:3px;line-height:1.9;">
          &nbsp;&nbsp;1 5 6<br>+ 2 4 7<br><span style="border-top:1.5px solid #0f3460;display:block;"></span>&nbsp;&nbsp;4 0 3
        </div>
        6+7=13 → write 3, carry 1<br>5+4+1=10 → write 0, carry 1<br>1+2+1=4
      </div>
    </div>
  </div>
</div>

<div class="section">
  <div class="section-title"><span class="emoji">⚠️</span>Common Mistakes to Avoid</div>
  <table class="cmd-table">
    <tr><th>Mistake</th><th>Example of Error</th><th>How to fix it</th></tr>
    <tr><td>Not lining up place values</td><td>Writing 47 + 5 as 47 + 50</td><td>Always write units under units</td></tr>
    <tr><td>Forgetting to carry</td><td>7+5 = 2 (instead of 12)</td><td>Always check if the sum ≥ 10</td></tr>
    <tr><td>Carrying to the wrong column</td><td>Carry goes to hundreds not tens</td><td>Move one column to the LEFT</td></tr>
  </table>
</div>

<div class="section">
  <div class="section-title"><span class="emoji">📝</span>Summary</div>
  <div class="summary-box">
    <h3>✅ Key Points</h3>
    <ul>
      <li>Line digits up by <strong>place value</strong> — units under units, tens under tens</li>
      <li>Always start adding from the <strong>right</strong> (units column first)</li>
      <li>If a column total ≥ 10, write the units digit and <strong>carry</strong> the 1 to the next column</li>
      <li>The answer to an addition is called the <strong>sum</strong></li>
      <li>Always <strong>estimate first</strong> to check your answer is sensible</li>
    </ul>
  </div>
  <div class="try-it"><h4>✏️ Practice</h4>
    <p>Try these: &nbsp; 54 + 37 &nbsp;|&nbsp; 128 + 65 &nbsp;|&nbsp; 246 + 378</p>
  </div>
</div>"""
    return _maths_page("Addition Level 1", "Level 1", "Addition — Column Method", "Single and double-digit addition with carrying", body)


# ---------------------------------------------------------------------------
# MATHS — Addition Level 2
# ---------------------------------------------------------------------------

def _generate_addition_level2_notes_html() -> str:
    body = """
<div class="section">
  <div class="section-title"><span class="emoji">🔢</span>Multi-Digit Addition with Multiple Carries</div>
  <div class="callout fun">
    At Level 2 we add <strong>3-digit and 4-digit numbers</strong> that may need carrying in
    <em>more than one column</em>. The method is exactly the same — just more steps!
  </div>
</div>
<div class="section">
  <div class="section-title"><span class="emoji">🧪</span>Worked Example — 3,456 + 2,789</div>
  <div class="two-col">
    <div class="col">
      <div style="background:#1e2a3a;border-radius:6px;padding:10px 16px;font-family:'Courier New',monospace;font-size:13px;color:#e8f4fd;line-height:2.2;">
        &nbsp;&nbsp;&nbsp;Th &nbsp;H &nbsp;T &nbsp;U<br>
        &nbsp;&nbsp;&nbsp;&nbsp;3 &nbsp;4 &nbsp;5 &nbsp;6<br>
        + &nbsp;&nbsp;2 &nbsp;7 &nbsp;8 &nbsp;9<br>
        <span style="display:block;border-top:2px solid #0f9b58;color:#7ed6a7;font-size:10px;">carries: &nbsp;1 &nbsp;1 &nbsp;1</span>
        &nbsp;&nbsp;&nbsp;&nbsp;6 &nbsp;2 &nbsp;4 &nbsp;5
      </div>
    </div>
    <div class="col">
      <p style="line-height:2;font-size:12.5px;">
        <strong>Step by step:</strong><br>
        U: 6+9 = <strong>15</strong> → write 5, carry 1<br>
        T: 5+8+1 = <strong>14</strong> → write 4, carry 1<br>
        H: 4+7+1 = <strong>12</strong> → write 2, carry 1<br>
        Th: 3+2+1 = <strong>6</strong> → write 6<br><br>
        Answer: <strong>6,245</strong>
      </p>
    </div>
  </div>
  <div class="callout tip">
    <strong>Estimate first!</strong> Round to the nearest 1000: 3,000 + 3,000 = 6,000.
    Our answer 6,245 is close to 6,000 ✅ — so it's sensible!
  </div>
</div>
<div class="section">
  <div class="section-title"><span class="emoji">⚠️</span>Adding Across Zeros</div>
  <div class="callout fun">
    <strong>Watch out for zeros!</strong> If a column has a zero, don't forget to include any carry.
    <br>Example: 2,007 + 1,456 → units: 7+6=13 (write 3, carry 1), tens: 0+5+1=6, hundreds: 0+4=4, thousands: 2+1=3 → <strong>3,463</strong>
  </div>
  <div class="try-it"><h4>✏️ Practice</h4>
    <p>Try: 1,348 + 2,765 &nbsp;|&nbsp; 4,507 + 3,896 &nbsp;|&nbsp; 2,009 + 4,998</p>
  </div>
</div>
<div class="section">
  <div class="section-title"><span class="emoji">📝</span>Summary</div>
  <div class="summary-box"><h3>✅ Key Points</h3><ul>
    <li>The column method works for any number of digits — just add more columns</li>
    <li>Carry digits move <strong>one column to the left</strong></li>
    <li>Always <strong>estimate first</strong> to check your answer is reasonable</li>
    <li>Take extra care with zeros — remember to add any carry to a zero column</li>
  </ul></div>
</div>"""
    return _maths_page("Addition Level 2", "Level 2", "Addition — Large Numbers &amp; Multiple Carries", "Three and four-digit addition with multiple carrying steps", body)


# ---------------------------------------------------------------------------
# MATHS — Subtraction Level 1
# ---------------------------------------------------------------------------

def _generate_subtraction_level1_notes_html() -> str:
    body = """
<div class="section">
  <div class="section-title"><span class="emoji">➖</span>What is Subtraction?</div>
  <div class="callout fun">
    <strong>Subtraction means finding the difference between two numbers by taking one away from another.</strong>
    The symbol is <strong>−</strong>. The answer is called the <strong>difference</strong>.
    Key words in problems: difference, take away, how many left, how many more, subtract, minus.
  </div>
  <div class="callout tip">
    <strong>Important:</strong> Subtraction is NOT commutative — <strong>83 − 47 ≠ 47 − 83</strong>.
    The larger number always goes on top in the column method!
  </div>
</div>
<div class="section">
  <div class="section-title"><span class="emoji">📋</span>The Column Method with Borrowing</div>
  <div class="two-col">
    <div class="col">
      <p style="line-height:1.9;font-size:12.5px;">
        <strong>Steps:</strong><br>
        1. Write larger number on top, smaller below<br>
        2. Start at the <strong>right</strong> (units first)<br>
        3. If top digit &lt; bottom digit, you need to <strong>borrow</strong> from the next column<br>
        4. Borrowing: take 1 ten from the tens column, add 10 to the units<br>
        5. Subtract each column<br>
        6. Write the answer
      </p>
    </div>
    <div class="col">
      <p style="font-size:12px;font-weight:700;color:#0f3460;margin-bottom:2mm;">Example: 83 − 47</p>
      <div style="background:#1e2a3a;border-radius:6px;padding:8px 14px;font-family:'Courier New',monospace;font-size:13px;color:#e8f4fd;line-height:2;">
        &nbsp;&nbsp;<span style="color:#f78c6c;text-decoration:line-through;">8</span><span style="color:#c3e88d;">7</span> &nbsp;<span style="color:#c3e88d;">13</span><br>
        − &nbsp;4 &nbsp;&nbsp;7<br>
        <span style="display:block;border-top:2px solid #0f9b58;"></span>
        &nbsp;&nbsp;3 &nbsp;&nbsp;6
      </div>
      <p style="font-size:11px;color:#555;margin-top:2mm;">Can't do 3−7, so borrow: 13−7=6 &nbsp;|&nbsp; 7−4=3</p>
    </div>
  </div>
</div>
<div class="section">
  <div class="section-title"><span class="emoji">🧪</span>Worked Examples</div>
  <div class="two-col">
    <div class="col">
      <div class="callout">
        <strong>Example 1:</strong> 72 − 38<br>
        <div style="font-family:'Courier New',monospace;font-size:12px;background:#f0fbf5;padding:6px;border-radius:4px;margin-top:3px;line-height:1.9;">
          &nbsp;6 12<br>− 3 &nbsp;8<br><span style="border-top:1.5px solid #0f3460;display:block;"></span>&nbsp;3 &nbsp;4
        </div>
        Borrow: 12−8=4 &nbsp;|&nbsp; 6−3=3 → <strong>34</strong>
      </div>
    </div>
    <div class="col">
      <div class="callout">
        <strong>Example 2:</strong> 254 − 138<br>
        <div style="font-family:'Courier New',monospace;font-size:12px;background:#f0fbf5;padding:6px;border-radius:4px;margin-top:3px;line-height:1.9;">
          &nbsp;2 4 14<br>− 1 3 &nbsp;8<br><span style="border-top:1.5px solid #0f3460;display:block;"></span>&nbsp;1 1 &nbsp;6
        </div>
        14−8=6 &nbsp;|&nbsp; 4−3=1 &nbsp;|&nbsp; 2−1=1 → <strong>116</strong>
      </div>
    </div>
  </div>
  <div class="callout tip">
    <strong>Check your answer!</strong> Always verify with the inverse: 34 + 38 = 72 ✅
  </div>
</div>
<div class="section">
  <div class="section-title"><span class="emoji">📝</span>Summary</div>
  <div class="summary-box"><h3>✅ Key Points</h3><ul>
    <li>Always put the <strong>larger number on top</strong></li>
    <li>Start from the <strong>right</strong> (units first)</li>
    <li>If top &lt; bottom, <strong>borrow</strong> from the next column: add 10 to current, reduce next by 1</li>
    <li>Check with addition: <strong>difference + smaller number = larger number</strong></li>
  </ul></div>
  <div class="try-it"><h4>✏️ Practice</h4>
    <p>Try: 91 − 47 &nbsp;|&nbsp; 143 − 78 &nbsp;|&nbsp; 362 − 185</p>
  </div>
</div>"""
    return _maths_page("Subtraction Level 1", "Level 1", "Subtraction — Column Method with Borrowing", "Basic subtraction including borrowing and regrouping", body)


# ---------------------------------------------------------------------------
# MATHS — Subtraction Level 2
# ---------------------------------------------------------------------------

def _generate_subtraction_level2_notes_html() -> str:
    body = """
<div class="section">
  <div class="section-title"><span class="emoji">➖</span>Multi-Digit Subtraction &amp; Borrowing Across Zeros</div>
  <div class="callout fun">
    At Level 2 we subtract <strong>large numbers</strong> and deal with the tricky case of
    <strong>borrowing across zeros</strong>. When a column has 0 and you need to borrow,
    you must skip across to find a non-zero digit to borrow from.
  </div>
</div>
<div class="section">
  <div class="section-title"><span class="emoji">🧪</span>Borrowing Across Zeros — 5,003 − 2,648</div>
  <div class="two-col">
    <div class="col">
      <div style="background:#1e2a3a;border-radius:6px;padding:10px 16px;font-family:'Courier New',monospace;font-size:13px;color:#e8f4fd;line-height:2.2;">
        &nbsp;&nbsp;&nbsp;4 &nbsp;<span style="color:#f78c6c;text-decoration:line-through;">10</span> &nbsp;<span style="color:#c3e88d;">9</span> &nbsp;<span style="color:#c3e88d;">13</span><br>
        &nbsp;&nbsp;&nbsp;<span style="color:#f78c6c;text-decoration:line-through;">5</span> &nbsp;&nbsp;<span style="color:#f78c6c;text-decoration:line-through;">0</span> &nbsp;&nbsp;<span style="color:#f78c6c;text-decoration:line-through;">0</span> &nbsp;&nbsp;3<br>
        − &nbsp;2 &nbsp;&nbsp;6 &nbsp;&nbsp;4 &nbsp;&nbsp;8<br>
        <span style="display:block;border-top:2px solid #0f9b58;"></span>
        &nbsp;&nbsp;&nbsp;2 &nbsp;&nbsp;3 &nbsp;&nbsp;5 &nbsp;&nbsp;5
      </div>
    </div>
    <div class="col">
      <p style="line-height:2;font-size:12px;">
        <strong>The trick with zeros:</strong><br>
        U: Can't do 3−8. Borrow from T — but T is 0!<br>
        → Skip to H: also 0! Skip to Th: 5.<br>
        → Th becomes 4, H becomes 10, T becomes 10<br>
        → Now borrow from T(10): T becomes 9, U becomes 13<br>
        U: 13−8=<strong>5</strong> &nbsp;|&nbsp; T: 9−4=<strong>5</strong><br>
        H: 10−6=<strong>4</strong>... wait, need to borrow from Th(4)<br>
        H becomes 10, Th becomes 4 &nbsp;|&nbsp; H:10−6=<strong>4</strong>... actually 9 (borrowed)<br>
        Th: 4−2=<strong>2</strong><br>
        <strong>Answer: 2,355</strong>
      </p>
    </div>
  </div>
  <div class="callout tip">
    <strong>Alternative strategy:</strong> Use "counting up" (Frog method).
    Count from 2,648 up to 5,003: +2 → 2,650; +350 → 3,000; +2,003 → 5,003.
    Total = 2 + 350 + 2,003 = <strong>2,355</strong> ✅ — much easier!
  </div>
</div>
<div class="section">
  <div class="section-title"><span class="emoji">📝</span>Summary</div>
  <div class="summary-box"><h3>✅ Key Points</h3><ul>
    <li>When borrowing from a zero, skip to the nearest non-zero column</li>
    <li>For difficult subtractions, try <strong>counting up</strong> (add from small to large)</li>
    <li>Always estimate first: 5,003 − 2,648 ≈ 5,000 − 3,000 = 2,000 ✅</li>
    <li>Check with addition: 2,355 + 2,648 = 5,003 ✅</li>
  </ul></div>
  <div class="try-it"><h4>✏️ Practice</h4>
    <p>Try: 6,002 − 3,748 &nbsp;|&nbsp; 4,000 − 1,367 &nbsp;|&nbsp; 10,000 − 4,563</p>
  </div>
</div>"""
    return _maths_page("Subtraction Level 2", "Level 2", "Subtraction — Large Numbers &amp; Zeros", "Multi-digit subtraction including borrowing across zeros", body)


# ---------------------------------------------------------------------------
# MATHS — Multiplication Level 1
# ---------------------------------------------------------------------------

def _generate_multiplication_level1_notes_html() -> str:
    body = """
<div class="section">
  <div class="section-title"><span class="emoji">✖️</span>What is Multiplication?</div>
  <div class="callout fun">
    <strong>Multiplication is repeated addition.</strong>
    4 × 6 means "four groups of six" = 6 + 6 + 6 + 6 = 24.
    Key words: groups of, lots of, product, times, multiply.
    The answer to a multiplication is called the <strong>product</strong>.
  </div>
</div>
<div class="section">
  <div class="section-title"><span class="emoji">📋</span>Short Multiplication (Bus Stop with multiplier ≤ 12)</div>
  <div class="two-col">
    <div class="col">
      <p style="line-height:1.9;font-size:12.5px;">
        <strong>Steps for 47 × 6:</strong><br>
        1. Write 47 on top, × 6 below<br>
        2. Start at <strong>right</strong> — multiply units: 7 × 6 = 42<br>
        3. Write 2, carry the 4<br>
        4. Multiply tens: 4 × 6 = 24, plus carry 4 = 28<br>
        5. Write 28<br>
        Answer: <strong>282</strong>
      </p>
    </div>
    <div class="col">
      <div style="background:#1e2a3a;border-radius:6px;padding:8px 14px;font-family:'Courier New',monospace;font-size:13px;color:#e8f4fd;line-height:2;">
        &nbsp;&nbsp;&nbsp;4 &nbsp;7<br>
        × &nbsp;&nbsp;&nbsp;&nbsp;6<br>
        <span style="display:block;border-top:2px solid #0f9b58;color:#f78c6c;font-size:10px;">carry: &nbsp;4</span>
        &nbsp;&nbsp;2 &nbsp;8 &nbsp;2
      </div>
      <p style="font-size:11px;color:#555;margin-top:2mm;">7×6=42 (write 2, carry 4) &nbsp;|&nbsp; 4×6=24+4=28</p>
    </div>
  </div>
</div>
<div class="section">
  <div class="section-title"><span class="emoji">🔲</span>Grid Method (great for checking!)</div>
  <div class="callout tip">
    The grid method splits numbers into tens and units before multiplying — easier for mental checks!
  </div>
  <div style="margin:3mm 0;">
    <table style="border-collapse:collapse;font-size:12px;">
      <tr>
        <th style="background:#0f3460;color:white;padding:6px 12px;">×</th>
        <th style="background:#0f3460;color:white;padding:6px 12px;">40</th>
        <th style="background:#0f3460;color:white;padding:6px 12px;">7</th>
      </tr>
      <tr>
        <td style="background:#0f9b58;color:white;padding:6px 12px;font-weight:700;">6</td>
        <td style="padding:6px 12px;background:#f0fbf5;">240</td>
        <td style="padding:6px 12px;background:#f0fbf5;">42</td>
      </tr>
    </table>
    <p style="font-size:12px;margin-top:2mm;">240 + 42 = <strong>282</strong> ✅</p>
  </div>
</div>
<div class="section">
  <div class="section-title"><span class="emoji">📝</span>Summary</div>
  <div class="summary-box"><h3>✅ Key Points</h3><ul>
    <li>Multiplication is <strong>repeated addition</strong> — 5 × 3 = 5 + 5 + 5</li>
    <li>Always start from the <strong>right</strong> in short multiplication</li>
    <li>Carry any tens to the next column</li>
    <li>Know your <strong>times tables</strong> up to 12 × 12 — they are the foundation!</li>
    <li>Check using the <strong>grid method</strong></li>
  </ul></div>
  <div class="try-it"><h4>✏️ Practice</h4>
    <p>Try: 34 × 7 &nbsp;|&nbsp; 86 × 4 &nbsp;|&nbsp; 123 × 6</p>
  </div>
</div>"""
    return _maths_page("Multiplication Level 1", "Level 1", "Multiplication — Short Method", "Times tables and short multiplication up to 3 digits × 1 digit", body)


# ---------------------------------------------------------------------------
# MATHS — Multiplication Level 2
# ---------------------------------------------------------------------------

def _generate_multiplication_level2_notes_html() -> str:
    body = """
<div class="section">
  <div class="section-title"><span class="emoji">✖️</span>Long Multiplication — 2-Digit by 2-Digit</div>
  <div class="callout fun">
    Long multiplication is used when both numbers have <strong>two or more digits</strong>.
    We multiply in two rows and then add them together.
    Example: 234 × 47
  </div>
</div>
<div class="section">
  <div class="section-title"><span class="emoji">📋</span>Step-by-Step: 234 × 47</div>
  <div class="two-col">
    <div class="col">
      <p style="line-height:2;font-size:12.5px;">
        <strong>Step 1:</strong> Multiply 234 × 7 (units of 47)<br>
        &nbsp;&nbsp; 234 × 7 = <strong>1,638</strong><br><br>
        <strong>Step 2:</strong> Multiply 234 × 40 (tens of 47)<br>
        &nbsp;&nbsp; Write a 0 placeholder in units column<br>
        &nbsp;&nbsp; 234 × 4 = 936 → so 234 × 40 = <strong>9,360</strong><br><br>
        <strong>Step 3:</strong> Add the two rows:<br>
        &nbsp;&nbsp; 1,638 + 9,360 = <strong>10,998</strong>
      </p>
    </div>
    <div class="col">
      <div style="background:#1e2a3a;border-radius:6px;padding:10px 16px;font-family:'Courier New',monospace;font-size:12px;color:#e8f4fd;line-height:2.2;">
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2 3 4<br>
        &nbsp;&nbsp;&nbsp;× &nbsp;4 7<br>
        <span style="display:block;border-top:2px solid #7ed6a7;"></span>
        &nbsp;&nbsp;&nbsp;&nbsp;1 6 3 8 &nbsp;<span style="color:#7ed6a7;">(234×7)</span><br>
        &nbsp;&nbsp;&nbsp;9 3 6 0 &nbsp; &nbsp;<span style="color:#f78c6c;">(234×40)</span><br>
        <span style="display:block;border-top:2px solid #0f9b58;"></span>
        &nbsp;&nbsp;1 0 9 9 8
      </div>
    </div>
  </div>
  <div class="callout tip">
    <strong>The zero placeholder is crucial!</strong> When multiplying by the tens digit,
    always put a <strong>zero in the units column</strong> first.
    This is because you're actually multiplying by 40, not 4.
  </div>
</div>
<div class="section">
  <div class="section-title"><span class="emoji">📝</span>Summary</div>
  <div class="summary-box"><h3>✅ Key Points</h3><ul>
    <li>Long multiplication: multiply by units row, then by tens row (with 0 placeholder)</li>
    <li>Add both partial products together for the final answer</li>
    <li>Estimate first: 234 × 47 ≈ 200 × 50 = 10,000 ✅</li>
    <li>Double-check using the grid method to verify</li>
  </ul></div>
  <div class="try-it"><h4>✏️ Practice</h4>
    <p>Try: 43 × 25 &nbsp;|&nbsp; 67 × 34 &nbsp;|&nbsp; 125 × 36</p>
  </div>
</div>"""
    return _maths_page("Multiplication Level 2", "Level 2", "Multiplication — Long Method", "2-digit by 2-digit and 3-digit by 2-digit multiplication", body)


# ---------------------------------------------------------------------------
# MATHS — Division Level 1
# ---------------------------------------------------------------------------

def _generate_division_level1_notes_html() -> str:
    body = """
<div class="section">
  <div class="section-title"><span class="emoji">➗</span>What is Division?</div>
  <div class="callout fun">
    <strong>Division means sharing equally or grouping.</strong>
    96 ÷ 8 means "how many groups of 8 are in 96?" or "share 96 equally into 8 groups."
    The answer is called the <strong>quotient</strong>.
    Key words: share, divide, groups of, how many times, quotient, remainder.
  </div>
</div>
<div class="section">
  <div class="section-title"><span class="emoji">🚌</span>Short Division — The Bus Stop Method</div>
  <div class="two-col">
    <div class="col">
      <p style="line-height:1.9;font-size:12.5px;">
        <strong>Steps for 96 ÷ 8:</strong><br>
        1. Write 8 outside the bus stop, 96 inside<br>
        2. Divide the first digit: 9 ÷ 8 = 1 remainder 1<br>
        3. Write 1 above; carry the remainder 1 to next digit<br>
        4. Now divide 16 ÷ 8 = 2<br>
        5. Write 2 above<br>
        Answer: <strong>12</strong>
      </p>
    </div>
    <div class="col">
      <div style="background:#1e2a3a;border-radius:6px;padding:8px 14px;font-family:'Courier New',monospace;font-size:14px;color:#e8f4fd;line-height:2.2;">
        &nbsp;&nbsp;&nbsp;1 &nbsp;2<br>
        8 ) 9 6<br>
        &nbsp;&nbsp;&nbsp;<span style="color:#f78c6c;">↑</span>&nbsp;<span style="color:#c3e88d;">↑</span><br>
        &nbsp;&nbsp;&nbsp;<span style="font-size:10px;color:#7ed6a7;">9÷8=1 r1 &nbsp;&nbsp; 16÷8=2</span>
      </div>
    </div>
  </div>
</div>
<div class="section">
  <div class="section-title"><span class="emoji">🧪</span>Division with Remainders</div>
  <div class="callout">
    <strong>Example: 97 ÷ 4</strong><br>
    <div style="font-family:'Courier New',monospace;background:#f0fbf5;padding:6px 10px;border-radius:4px;font-size:12px;line-height:2;display:inline-block;margin-top:3px;">
      &nbsp;&nbsp;&nbsp;2 &nbsp;4 &nbsp;r1<br>4 ) 9 &nbsp;7<br>
    </div>
    <br>9÷4=2 r1 &nbsp;|&nbsp; 17÷4=4 r1 &nbsp;|&nbsp; Answer: <strong>24 remainder 1</strong><br>
    Check: (24 × 4) + 1 = 96 + 1 = 97 ✅
  </div>
</div>
<div class="section">
  <div class="section-title"><span class="emoji">📝</span>Summary</div>
  <div class="summary-box"><h3>✅ Key Points</h3><ul>
    <li>Division is the inverse of multiplication</li>
    <li>The <strong>bus stop method</strong>: divide left to right, carrying remainders</li>
    <li>Always check: <strong>(quotient × divisor) + remainder = dividend</strong></li>
    <li>Know your times tables — they make division much faster!</li>
  </ul></div>
  <div class="try-it"><h4>✏️ Practice</h4>
    <p>Try: 84 ÷ 7 &nbsp;|&nbsp; 135 ÷ 5 &nbsp;|&nbsp; 247 ÷ 6</p>
  </div>
</div>"""
    return _maths_page("Division Level 1", "Level 1", "Division — Short Division (Bus Stop)", "Short division with and without remainders", body)


# ---------------------------------------------------------------------------
# MATHS — Division Level 2
# ---------------------------------------------------------------------------

def _generate_division_level2_notes_html() -> str:
    body = """
<div class="section">
  <div class="section-title"><span class="emoji">➗</span>Long Division — Dividing by 2-Digit Numbers</div>
  <div class="callout fun">
    Long division is used when the divisor has <strong>two or more digits</strong>.
    Example: 456 ÷ 12. We work through the dividend chunk by chunk.
  </div>
</div>
<div class="section">
  <div class="section-title"><span class="emoji">📋</span>Step-by-Step: 456 ÷ 12</div>
  <div class="two-col">
    <div class="col">
      <p style="line-height:2;font-size:12.5px;">
        <strong>Step 1:</strong> How many 12s in 4? → 0. Use first two digits: 45.<br>
        <strong>Step 2:</strong> 12 × 3 = 36; 12 × 4 = 48 (too big). So 45 ÷ 12 = 3 r9<br>
        <strong>Step 3:</strong> Bring down next digit (6) → 96<br>
        <strong>Step 4:</strong> 12 × 8 = 96. So 96 ÷ 12 = 8 r0<br>
        <strong>Answer: 38</strong>
      </p>
    </div>
    <div class="col">
      <div style="background:#1e2a3a;border-radius:6px;padding:10px 16px;font-family:'Courier New',monospace;font-size:13px;color:#e8f4fd;line-height:2.2;">
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3 &nbsp;8<br>
        12 ) 4 5 6<br>
        &nbsp;&nbsp;&nbsp;&nbsp;−3 6<br>
        <span style="display:block;border-top:1px solid #7ed6a7;width:40px;"></span>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;9 6<br>
        &nbsp;&nbsp;&nbsp;&nbsp;−9 6<br>
        <span style="display:block;border-top:1px solid #7ed6a7;width:40px;"></span>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0
      </div>
    </div>
  </div>
  <div class="callout tip">
    <strong>Remainders as decimals:</strong> If there is a remainder, you can continue dividing
    by adding a decimal point and zeros. E.g. 7 ÷ 4 = 1.75
  </div>
</div>
<div class="section">
  <div class="section-title"><span class="emoji">📝</span>Summary</div>
  <div class="summary-box"><h3>✅ Key Points</h3><ul>
    <li>Long division: divide, multiply, subtract, bring down — repeat</li>
    <li>Estimate first: 456 ÷ 12 ≈ 450 ÷ 10 = 45 ✅</li>
    <li>Check: 38 × 12 = 456 ✅</li>
    <li>Remainders can be written as r__, as fractions, or as decimals</li>
  </ul></div>
  <div class="try-it"><h4>✏️ Practice</h4>
    <p>Try: 378 ÷ 14 &nbsp;|&nbsp; 520 ÷ 13 &nbsp;|&nbsp; 672 ÷ 16</p>
  </div>
</div>"""
    return _maths_page("Division Level 2", "Level 2", "Division — Long Division", "Dividing by 2-digit numbers, remainders and decimals", body)


# ---------------------------------------------------------------------------
# MATHS — Equivalent Fractions
# ---------------------------------------------------------------------------

def _generate_equivalent_fractions_notes_html() -> str:
    body = """
<div class="section">
  <div class="section-title"><span class="emoji">🍕</span>What are Fractions?</div>
  <div class="callout fun">
    A <strong>fraction</strong> represents a part of a whole.
    In the fraction ¾: <strong>3</strong> is the <em>numerator</em> (how many parts we have)
    and <strong>4</strong> is the <em>denominator</em> (how many equal parts the whole is divided into).
  </div>
</div>
<div class="section">
  <div class="section-title"><span class="emoji">⚖️</span>Equivalent Fractions</div>
  <div class="callout">
    <strong>Equivalent fractions are different fractions that have exactly the same value.</strong>
    ½ = 2/4 = 3/6 = 4/8 — they all represent the same amount!
  </div>
  <div class="two-col">
    <div class="col">
      <p style="line-height:1.9;font-size:12.5px;">
        <strong>To find equivalent fractions:</strong><br>
        Multiply (or divide) both numerator and denominator by the <strong>same number</strong>.<br><br>
        <strong>Example:</strong> ¾ = ?/8<br>
        4 × 2 = 8 &nbsp;→&nbsp; also multiply top: 3 × 2 = 6<br>
        So ¾ = <strong>6/8</strong>
      </p>
    </div>
    <div class="col">
      <table class="cmd-table">
        <tr><th>Fraction</th><th>×2</th><th>×3</th><th>×4</th></tr>
        <tr><td>½</td><td>2/4</td><td>3/6</td><td>4/8</td></tr>
        <tr><td>⅓</td><td>2/6</td><td>3/9</td><td>4/12</td></tr>
        <tr><td>¾</td><td>6/8</td><td>9/12</td><td>12/16</td></tr>
      </table>
    </div>
  </div>
</div>
<div class="section">
  <div class="section-title"><span class="emoji">✂️</span>Simplifying Fractions</div>
  <div class="callout tip">
    <strong>Simplifying</strong> (also called cancelling or reducing) means dividing top and bottom
    by their <strong>Highest Common Factor (HCF)</strong>.
    12/16 → HCF of 12 and 16 is 4 → 12÷4 = 3, 16÷4 = 4 → simplest form: <strong>¾</strong>
  </div>
</div>
<div class="section">
  <div class="section-title"><span class="emoji">📝</span>Summary</div>
  <div class="summary-box"><h3>✅ Key Points</h3><ul>
    <li>Numerator = top (parts we have) | Denominator = bottom (total equal parts)</li>
    <li>Equivalent fractions: <strong>multiply or divide</strong> top and bottom by the same number</li>
    <li>Simplify by dividing both by their HCF</li>
    <li>A fraction in its simplest form has no common factors except 1</li>
  </ul></div>
  <div class="try-it"><h4>✏️ Practice</h4>
    <p>Complete: 2/5 = ?/15 &nbsp;|&nbsp; 6/9 = ?/3 &nbsp;|&nbsp; Simplify 8/12</p>
  </div>
</div>"""
    return _maths_page("Fractions", "Equivalent Fractions", "Fractions — Equivalence &amp; Simplifying", "Equivalent fractions and simplifying to lowest terms", body)


# ---------------------------------------------------------------------------
# MATHS — Probability Level 1
# ---------------------------------------------------------------------------

def _generate_probability_level1_notes_html() -> str:
    body = """
<div class="section">
  <div class="section-title"><span class="emoji">🎲</span>What is Probability?</div>
  <div class="callout fun">
    <strong>Probability measures the likelihood (chance) that an event will happen.</strong>
    It is always a number between 0 and 1.<br>
    0 = impossible &nbsp;|&nbsp; 0.5 (½) = equally likely &nbsp;|&nbsp; 1 = certain
  </div>
  <div style="background:#f0fbf5;border:2px solid #0f9b58;border-radius:8px;padding:6mm 8mm;margin:3mm 0;">
    <p style="font-size:11px;font-weight:700;color:#555;margin-bottom:2mm;">PROBABILITY SCALE</p>
    <div style="background:linear-gradient(to right,#e74c3c,#f39c12,#2ecc71);height:10px;border-radius:5px;"></div>
    <div style="display:flex;justify-content:space-between;font-size:10px;font-weight:700;margin-top:2px;">
      <span>0<br>Impossible</span><span>¼<br>Unlikely</span><span>½<br>Even chance</span><span>¾<br>Likely</span><span>1<br>Certain</span>
    </div>
  </div>
</div>
<div class="section">
  <div class="section-title"><span class="emoji">📋</span>Calculating Probability</div>
  <div class="callout">
    <strong>Formula:</strong> P(event) = number of favourable outcomes ÷ total number of equally likely outcomes
  </div>
  <div class="two-col">
    <div class="col">
      <div class="callout tip">
        <strong>Example — Fair dice (6 sides: 1,2,3,4,5,6):</strong><br>
        P(rolling a 4) = 1/6<br>
        P(rolling an even number) = 3/6 = <strong>½</strong><br>
        P(rolling &gt; 2) = 4/6 = <strong>⅔</strong>
      </div>
    </div>
    <div class="col">
      <div class="callout tip">
        <strong>Example — Bag of counters (3 red, 2 blue, 1 green):</strong><br>
        Total = 6 counters<br>
        P(red) = 3/6 = <strong>½</strong><br>
        P(blue) = 2/6 = <strong>⅓</strong><br>
        P(green) = 1/6
      </div>
    </div>
  </div>
</div>
<div class="section">
  <div class="section-title"><span class="emoji">📝</span>Summary</div>
  <div class="summary-box"><h3>✅ Key Points</h3><ul>
    <li>Probability is always between 0 (impossible) and 1 (certain)</li>
    <li>P(event) = favourable outcomes ÷ total outcomes</li>
    <li>Write probability as a fraction, decimal, or percentage</li>
    <li>Probabilities of all outcomes in a sample space <strong>add up to 1</strong></li>
  </ul></div>
  <div class="try-it"><h4>✏️ Practice</h4>
    <p>A bag has 4 red, 3 blue, 3 yellow balls. Find P(red), P(blue), P(not yellow).</p>
  </div>
</div>"""
    return _maths_page("Probability", "Level 1", "Probability — The Basics", "Understanding likelihood, the probability scale and simple probability fractions", body)


# ---------------------------------------------------------------------------
# MATHS — Probability Level 2
# ---------------------------------------------------------------------------

def _generate_probability_level2_notes_html() -> str:
    body = """
<div class="section">
  <div class="section-title"><span class="emoji">🎲</span>Listing All Outcomes — Sample Space</div>
  <div class="callout fun">
    When an experiment has <strong>two or more stages</strong>, we list ALL possible outcomes in a
    <strong>sample space diagram</strong>. This makes it easy to find probabilities.
  </div>
</div>
<div class="section">
  <div class="section-title"><span class="emoji">📋</span>Sample Space — Two Coins</div>
  <div class="callout">
    Flip two coins. List all outcomes (H=heads, T=tails):
  </div>
  <table style="border-collapse:collapse;font-size:12px;margin:3mm 0;">
    <tr>
      <th style="background:#0f3460;color:white;padding:6px 16px;">Coin 1</th>
      <th style="background:#0f3460;color:white;padding:6px 16px;">Coin 2</th>
      <th style="background:#0f3460;color:white;padding:6px 16px;">Outcome</th>
    </tr>
    <tr><td style="padding:5px 16px;background:#f5f8ff;">H</td><td style="padding:5px 16px;background:#f5f8ff;">H</td><td style="padding:5px 16px;background:#f5f8ff;">HH</td></tr>
    <tr><td style="padding:5px 16px;">H</td><td style="padding:5px 16px;">T</td><td style="padding:5px 16px;">HT</td></tr>
    <tr><td style="padding:5px 16px;background:#f5f8ff;">T</td><td style="padding:5px 16px;background:#f5f8ff;">H</td><td style="padding:5px 16px;background:#f5f8ff;">TH</td></tr>
    <tr><td style="padding:5px 16px;">T</td><td style="padding:5px 16px;">T</td><td style="padding:5px 16px;">TT</td></tr>
  </table>
  <p style="font-size:12px;">Total outcomes = 4 &nbsp;|&nbsp; P(two heads) = 1/4 &nbsp;|&nbsp; P(one head) = 2/4 = <strong>½</strong></p>
</div>
<div class="section">
  <div class="section-title"><span class="emoji">🎲</span>Two Dice — Sample Space Grid</div>
  <div class="callout tip">
    For two dice, draw a 6×6 grid. Each cell shows the sum. Total outcomes = 36.
    P(sum = 7) = 6/36 = <strong>⅙</strong> (most likely sum!)
  </div>
</div>
<div class="section">
  <div class="section-title"><span class="emoji">📝</span>Summary</div>
  <div class="summary-box"><h3>✅ Key Points</h3><ul>
    <li>List ALL outcomes systematically to avoid missing any</li>
    <li>A sample space diagram shows every possible outcome of an experiment</li>
    <li>For two events: total outcomes = (outcomes of event 1) × (outcomes of event 2)</li>
    <li>P(event) = count of favourable outcomes ÷ total outcomes in sample space</li>
  </ul></div>
  <div class="try-it"><h4>✏️ Practice</h4>
    <p>Spin a spinner (1,2,3) and flip a coin. List all outcomes. What is P(heads and 2)?</p>
  </div>
</div>"""
    return _maths_page("Probability", "Level 2", "Probability — Sample Space &amp; Combined Events", "Listing outcomes systematically and finding probabilities of combined events", body)


# ---------------------------------------------------------------------------
# MATHS — Algebra Level 1
# ---------------------------------------------------------------------------

def _generate_algebra_level1_notes_html() -> str:
    body = """
<div class="section">
  <div class="section-title"><span class="emoji">🔤</span>What is Algebra?</div>
  <div class="callout fun">
    <strong>Algebra uses letters (called variables) to represent unknown numbers.</strong>
    Instead of writing "a number plus 5 equals 9", we write <strong>x + 5 = 9</strong>.
    Finding the value of x is called <em>solving the equation</em>.
  </div>
  <div class="callout tip">
    <strong>Key vocabulary:</strong><br>
    <strong>Variable</strong> = a letter representing an unknown (x, y, n, a…)<br>
    <strong>Expression</strong> = a group of terms, e.g. 2x + 3<br>
    <strong>Equation</strong> = two expressions that are equal, e.g. 2x + 3 = 9<br>
    <strong>Solution</strong> = the value of the variable that makes the equation true
  </div>
</div>
<div class="section">
  <div class="section-title"><span class="emoji">⚖️</span>Solving Simple Equations</div>
  <div class="callout">
    An equation is like a <strong>balance scale</strong> — both sides must always be equal.
    Whatever you do to one side, you must do to the other!
  </div>
  <div class="two-col">
    <div class="col">
      <div class="callout tip">
        <strong>Example 1:</strong> x + 7 = 15<br>
        Subtract 7 from both sides:<br>
        x + 7 − 7 = 15 − 7<br>
        <strong>x = 8</strong> ✅<br>
        Check: 8 + 7 = 15 ✅
      </div>
    </div>
    <div class="col">
      <div class="callout tip">
        <strong>Example 2:</strong> 2x + 3 = 9<br>
        Step 1: subtract 3: 2x = 6<br>
        Step 2: divide by 2: x = <strong>3</strong> ✅<br>
        Check: 2(3) + 3 = 9 ✅
      </div>
    </div>
  </div>
</div>
<div class="section">
  <div class="section-title"><span class="emoji">📝</span>Summary</div>
  <div class="summary-box"><h3>✅ Key Points</h3><ul>
    <li>Algebra uses letters (variables) to represent unknown numbers</li>
    <li>Solve by doing the <strong>inverse (opposite) operation</strong></li>
    <li>Whatever you do to one side, <strong>do to the other</strong></li>
    <li>Always <strong>check</strong> by substituting your answer back in</li>
  </ul></div>
  <div class="try-it"><h4>✏️ Practice</h4>
    <p>Solve: x + 4 = 11 &nbsp;|&nbsp; 3x = 18 &nbsp;|&nbsp; 2x − 5 = 9</p>
  </div>
</div>"""
    return _maths_page("Algebra", "Level 1", "Algebra — Variables &amp; Simple Equations", "Introduction to algebra: variables, expressions and solving simple equations", body)


# ---------------------------------------------------------------------------
# MATHS — Algebra Level 2
# ---------------------------------------------------------------------------

def _generate_algebra_level2_notes_html() -> str:
    body = """
<div class="section">
  <div class="section-title"><span class="emoji">🔤</span>Expanding Brackets &amp; Harder Equations</div>
  <div class="callout fun">
    At Level 2 we solve <strong>harder equations</strong>, learn to <strong>expand brackets</strong>,
    and <strong>substitute</strong> values into expressions.
  </div>
</div>
<div class="section">
  <div class="section-title"><span class="emoji">📐</span>Expanding Brackets</div>
  <div class="callout">
    <strong>Rule:</strong> Multiply everything inside the bracket by the term outside.<br>
    3(x + 4) = 3×x + 3×4 = <strong>3x + 12</strong>
  </div>
  <div class="two-col">
    <div class="col">
      <div class="callout tip">
        <strong>Example:</strong> Solve 3(x + 2) = 21<br>
        Expand: 3x + 6 = 21<br>
        Subtract 6: 3x = 15<br>
        Divide by 3: <strong>x = 5</strong> ✅
      </div>
    </div>
    <div class="col">
      <div class="callout tip">
        <strong>Substitution:</strong> If x = 3, find 4x² − 2x + 1<br>
        = 4(9) − 2(3) + 1<br>
        = 36 − 6 + 1 = <strong>31</strong>
      </div>
    </div>
  </div>
</div>
<div class="section">
  <div class="section-title"><span class="emoji">📝</span>Summary</div>
  <div class="summary-box"><h3>✅ Key Points</h3><ul>
    <li>Expand brackets: multiply each term inside by the term outside</li>
    <li>Collect like terms before solving: 3x + 2x = 5x</li>
    <li>Substitution: replace variables with given numbers and calculate</li>
    <li>Always check your answer by substituting back</li>
  </ul></div>
  <div class="try-it"><h4>✏️ Practice</h4>
    <p>Expand: 4(x − 3) &nbsp;|&nbsp; Solve: 2(x + 5) = 18 &nbsp;|&nbsp; If n = 4, find 3n² − n</p>
  </div>
</div>"""
    return _maths_page("Algebra", "Level 2", "Algebra — Brackets, Harder Equations &amp; Substitution", "Expanding brackets, solving harder equations and substitution", body)


# ---------------------------------------------------------------------------
# MATHS — Perimeter & Area Level 1
# ---------------------------------------------------------------------------

def _generate_perimeter_area_level1_notes_html() -> str:
    body = """
<div class="section">
  <div class="section-title"><span class="emoji">📐</span>Perimeter vs Area — What's the Difference?</div>
  <div class="two-col">
    <div class="col">
      <div class="callout fun">
        <strong>Perimeter</strong> = the total distance around the outside of a shape.<br>
        Think of it as the length of a fence around a garden.
        Measured in cm, m, km.<br><br>
        <strong>Rectangle:</strong> P = 2(l + w)<br>
        <strong>Square:</strong> P = 4 × side
      </div>
    </div>
    <div class="col">
      <div class="callout tip">
        <strong>Area</strong> = the amount of space inside a shape.<br>
        Think of it as how many tiles fit inside a floor.
        Measured in cm², m², km².<br><br>
        <strong>Rectangle:</strong> A = l × w<br>
        <strong>Square:</strong> A = side²<br>
        <strong>Triangle:</strong> A = ½ × base × height
      </div>
    </div>
  </div>
</div>
<div class="section">
  <div class="section-title"><span class="emoji">🧪</span>Worked Examples</div>
  <div class="two-col">
    <div class="col">
      <div class="callout">
        <strong>Rectangle: 8 cm × 5 cm</strong><br>
        Perimeter = 2(8 + 5) = 2 × 13 = <strong>26 cm</strong><br>
        Area = 8 × 5 = <strong>40 cm²</strong>
      </div>
    </div>
    <div class="col">
      <div class="callout">
        <strong>Triangle: base 10 cm, height 6 cm</strong><br>
        Area = ½ × 10 × 6 = <strong>30 cm²</strong>
      </div>
    </div>
  </div>
  <div class="callout tip">
    <strong>Compound shapes:</strong> Split into rectangles and triangles. Find each area separately, then add (or subtract for holes).
  </div>
</div>
<div class="section">
  <div class="section-title"><span class="emoji">📝</span>Summary</div>
  <div class="summary-box"><h3>✅ Key Points</h3><ul>
    <li>Perimeter = distance around the outside (add all sides)</li>
    <li>Area = space inside (use formula for each shape)</li>
    <li>Area units are always <strong>squared</strong> (cm², m²…)</li>
    <li>Rectangle: A = l × w &nbsp;|&nbsp; Triangle: A = ½bh</li>
  </ul></div>
  <div class="try-it"><h4>✏️ Practice</h4>
    <p>Find perimeter and area of: 6 cm × 4 cm rectangle &nbsp;|&nbsp; Triangle with base 8 cm, height 5 cm</p>
  </div>
</div>"""
    return _maths_page("Perimeter &amp; Area", "Level 1", "Perimeter &amp; Area", "Calculating perimeter and area of rectangles, squares and triangles", body)


# ---------------------------------------------------------------------------
# MATHS — Angles Level 1
# ---------------------------------------------------------------------------

def _generate_angles_level1_notes_html() -> str:
    body = """
<div class="section">
  <div class="section-title"><span class="emoji">📐</span>Types of Angles</div>
  <div class="callout fun">
    An <strong>angle</strong> measures how much something has turned or the space between two lines meeting at a point.
    Angles are measured in <strong>degrees (°)</strong> using a protractor.
  </div>
  <table class="cmd-table">
    <tr><th>Name</th><th>Size</th><th>Think of it as…</th></tr>
    <tr><td>Acute</td><td>Less than 90°</td><td>Sharp — like a knife point</td></tr>
    <tr><td>Right angle</td><td>Exactly 90°</td><td>A square corner (shown with a □)</td></tr>
    <tr><td>Obtuse</td><td>Between 90° and 180°</td><td>Blunt — wider than a right angle</td></tr>
    <tr><td>Straight line</td><td>Exactly 180°</td><td>A completely flat line</td></tr>
    <tr><td>Reflex</td><td>Between 180° and 360°</td><td>More than half a full turn</td></tr>
    <tr><td>Full turn</td><td>Exactly 360°</td><td>One complete rotation</td></tr>
  </table>
</div>
<div class="section">
  <div class="section-title"><span class="emoji">⚖️</span>Key Angle Rules</div>
  <div class="two-col">
    <div class="col">
      <div class="callout tip">
        <strong>Angles on a straight line</strong> add up to <strong>180°</strong><br>
        If one angle is 65°, the other is 180° − 65° = <strong>115°</strong>
      </div>
      <div class="callout tip">
        <strong>Angles in a triangle</strong> add up to <strong>180°</strong><br>
        If two angles are 70° and 50°, the third = 180° − 70° − 50° = <strong>60°</strong>
      </div>
    </div>
    <div class="col">
      <div class="callout tip">
        <strong>Angles around a point</strong> add up to <strong>360°</strong>
      </div>
      <div class="callout tip">
        <strong>Vertically opposite angles</strong> are always <strong>equal</strong><br>
        (the angles directly across from each other when two lines cross)
      </div>
    </div>
  </div>
</div>
<div class="section">
  <div class="section-title"><span class="emoji">📝</span>Summary</div>
  <div class="summary-box"><h3>✅ Key Points</h3><ul>
    <li>Angles are measured in degrees (°)</li>
    <li>Angles on a straight line = <strong>180°</strong></li>
    <li>Angles in a triangle = <strong>180°</strong></li>
    <li>Angles around a point = <strong>360°</strong></li>
    <li>Vertically opposite angles are <strong>equal</strong></li>
  </ul></div>
  <div class="try-it"><h4>✏️ Practice</h4>
    <p>Find the missing angle: Triangle with 55° and 75° &nbsp;|&nbsp; Straight line with 132°</p>
  </div>
</div>"""
    return _maths_page("Angles", "Level 1", "Angles — Types &amp; Key Rules", "Types of angles and angle rules for triangles, straight lines and full turns", body)


# ---------------------------------------------------------------------------
# Route
# ---------------------------------------------------------------------------

TOPIC_GENERATORS = {
    "python-with-karel": _generate_karel_notes_html,
    # Maths
    "addition-level-1": _generate_addition_level1_notes_html,
    "addition-level-2": _generate_addition_level2_notes_html,
    "subtraction-level-1": _generate_subtraction_level1_notes_html,
    "subtraction-level-2": _generate_subtraction_level2_notes_html,
    "multiplication-level-1": _generate_multiplication_level1_notes_html,
    "multiplication-level-2": _generate_multiplication_level2_notes_html,
    "division-level-1": _generate_division_level1_notes_html,
    "division-level-2": _generate_division_level2_notes_html,
    "equivalent-fractions": _generate_equivalent_fractions_notes_html,
    "probability-level-1": _generate_probability_level1_notes_html,
    "probability-level-2": _generate_probability_level2_notes_html,
    "algebra-level-1": _generate_algebra_level1_notes_html,
    "algebra-level-2": _generate_algebra_level2_notes_html,
    "perimeter-area-level-1": _generate_perimeter_area_level1_notes_html,
    "angles-level-1": _generate_angles_level1_notes_html,
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

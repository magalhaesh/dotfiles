#!/usr/bin/env python3
"""Single source of truth for the "Thinking Tools" deck.

Emits two artifacts from one data structure so they can never drift:
  1. thinking-tools          -- a fortune(6) cookie file (entries split by `%`)
  2. thinking-tools-deck.html -- a self-contained HTML report of the deck

The deck is an open-source homage to "The Unstuck Box" (Flightpath Publishing):
48 thinking tools / mental models across 5 categories. Every description is
original wording drawn from public-domain concepts -- no card text is copied
from any commercial product.

Cards are kept under 160 characters so they survive `fortune -s` (short mode).

Re-run after editing:  python3 build_deck.py
"""

import html
import os
import shutil
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))

# (category, title, description)
DECK = [
    # ---- Strategic Thinking ----
    ("Strategic Thinking", "Eisenhower Matrix",
     "Sort tasks by urgent x important: do the urgent+important, schedule the important, delegate the merely urgent, drop the rest."),
    ("Strategic Thinking", "First Principles",
     "Strip a problem down to the facts you know are true, then reason up from there instead of copying how others do it."),
    ("Strategic Thinking", "Inversion",
     "Don't ask how to succeed. Ask what would guarantee failure, then avoid all of it. Solving backward is often easier."),
    ("Strategic Thinking", "Second-Order Thinking",
     "Ask \"and then what?\" Every choice has consequences of its consequences. Trace at least two steps out before committing."),
    ("Strategic Thinking", "Opportunity Cost",
     "The real cost of anything is the best thing you gave up for it. Compare to your next-best option, not to zero."),
    ("Strategic Thinking", "Circle of Competence",
     "Know the edge of what you actually understand. Play inside it; near the edge, slow down or get help."),
    ("Strategic Thinking", "Map Is Not the Territory",
     "Your model is a simplification, not reality. When the map and the ground disagree, trust the ground and update the map."),
    ("Strategic Thinking", "Occam's Razor",
     "Among competing explanations, prefer the one needing the fewest assumptions. Simple beats elaborate, until proven otherwise."),
    ("Strategic Thinking", "Hanlon's Razor",
     "Never attribute to malice what is adequately explained by carelessness, haste, or ignorance."),
    ("Strategic Thinking", "The 80/20 Rule",
     "Roughly 80% of results come from 20% of causes. Find the vital few inputs and pour your effort there."),

    # ---- Problem Solving ----
    ("Problem Solving", "Premortem",
     "Imagine it's months from now and the project failed. Write the story of why -- then go remove those causes today."),
    ("Problem Solving", "Five Whys",
     "Ask \"why?\" five times in a row. The first answer is a symptom; the fifth is usually the root cause worth fixing."),
    ("Problem Solving", "Rubber Duck",
     "Explain the problem out loud, line by line, to an inanimate object. Stating it clearly often reveals the answer."),
    ("Problem Solving", "MECE",
     "Break a problem into parts that are Mutually Exclusive and Collectively Exhaustive: no overlaps, no gaps."),
    ("Problem Solving", "Frame the Right Problem",
     "Spend real time defining the problem before solving it. A well-stated problem is already half-solved."),
    ("Problem Solving", "Theory of Constraints",
     "A system is only as fast as its tightest bottleneck. Improving anything but the bottleneck is wasted effort."),
    ("Problem Solving", "Reason by Analogy",
     "Ask where this problem has already been solved, in another field, and borrow the structure of that solution."),
    ("Problem Solving", "Add a Constraint",
     "Deliberately limit time, budget, or options. Tight constraints force creative, non-obvious solutions."),
    ("Problem Solving", "Subtract First",
     "Remove before you add. Ask what you can delete, merge, or skip. The cleanest fix is often less, not more."),
    ("Problem Solving", "Steelman",
     "Build the strongest version of the opposing view before arguing. If you can't, you don't yet understand the problem."),

    # ---- Decision Making ----
    ("Decision Making", "Expected Value",
     "Weigh each outcome by its probability, then sum. Decide on the long-run average, not on the vivid extreme."),
    ("Decision Making", "Regret Minimization",
     "Project yourself to age 80 and ask which choice you'd regret not making. Long-term regret cuts through short-term fear."),
    ("Decision Making", "One-Way vs Two-Way Doors",
     "Reversible decision? Decide fast and move. Irreversible one? Slow down and gather more before you step through."),
    ("Decision Making", "Sunk Cost",
     "Money and time already spent are gone. Decide only on future costs and benefits, never on what you've already sunk."),
    ("Decision Making", "Confirmation Bias",
     "You notice the evidence that fits your belief. Deliberately go hunting for what would prove you wrong."),
    ("Decision Making", "Outside View",
     "Don't only plan from inside your case. Ask how similar efforts actually turned out, and start from that base rate."),
    ("Decision Making", "10 / 10 / 10",
     "Before deciding, ask how you'll feel about this in 10 minutes, 10 months, and 10 years."),
    ("Decision Making", "Satisfice",
     "For reversible choices, take the first option that's good enough. Save maximizing for the few that truly matter."),
    ("Decision Making", "Decision Journal",
     "Write down the choice, your reasoning, and the expected outcome. Review later to learn what actually drives results."),
    ("Decision Making", "Via Negativa",
     "Improve by removing the harmful, not only by adding the good. Subtracting bad options is robust and reversible."),

    # ---- Project Management ----
    ("Project Management", "Parkinson's Law",
     "Work expands to fill the time allowed. Set a tight, deliberate deadline to compress the effort."),
    ("Project Management", "Planning Fallacy",
     "We underestimate time and cost even when we know better. Take your estimate, pad it -- then pad it again."),
    ("Project Management", "Critical Path",
     "Find the longest chain of dependent tasks. Only shortening that chain moves the finish date."),
    ("Project Management", "Limit Work in Progress",
     "Cap how many things are in flight at once. Finishing beats starting; less multitasking ships more."),
    ("Project Management", "Definition of Done",
     "Agree up front what \"done\" means -- tested, reviewed, shipped. Vague done-ness hides unfinished work."),
    ("Project Management", "Timebox",
     "Give a task a fixed slot. When time's up, stop and assess. Bounds perfectionism and surfaces blockers early."),
    ("Project Management", "Minimum Viable Version",
     "Build the smallest thing that delivers real value, ship it, and learn. Don't polish what no one has wanted yet."),
    ("Project Management", "Brooks's Law",
     "Adding people to a late project makes it later. Onboarding and coordination can cost more than they add."),
    ("Project Management", "Map the Dependencies",
     "List what must finish before each task can start. Hidden dependencies are where schedules quietly die."),
    ("Project Management", "Retrospective",
     "After each cycle ask: what worked, what didn't, what to change. Improvement only compounds if you look back."),

    # ---- Leadership & People ----
    ("Leadership & People", "Radical Candor",
     "Care personally and challenge directly. Honest feedback given with warmth beats both silence and brutality."),
    ("Leadership & People", "Disagree and Commit",
     "Once a decision is made, back it fully even if you argued against it. Debate before, unite after."),
    ("Leadership & People", "Chesterton's Fence",
     "Don't remove a rule until you understand why it was put there. The original reason may still matter."),
    ("Leadership & People", "Praise Public, Critique Private",
     "Recognize people where others can see it; correct them where only they can hear it."),
    ("Leadership & People", "Levels of Delegation",
     "Be explicit: do exactly this / recommend then act / decide and tell me. Ambiguity causes most delegation failures."),
    ("Leadership & People", "Psychological Safety",
     "People do their best work when it's safe to admit mistakes and ask questions. Protect that, fiercely."),
    ("Leadership & People", "Servant Leadership",
     "Lead by clearing obstacles for your team, not by collecting status. Ask: what do you need from me?"),
    ("Leadership & People", "Assume Good Intent",
     "Start from the belief that others mean well. It de-escalates conflict and, more often than not, turns out true."),
]

CATEGORIES = [
    "Strategic Thinking",
    "Problem Solving",
    "Decision Making",
    "Project Management",
    "Leadership & People",
]

# Palette echoing the Unstuck Box (coral / teal) without copying its art.
CAT_COLORS = {
    "Strategic Thinking":  "#e8533b",
    "Problem Solving":     "#2fa3a0",
    "Decision Making":     "#e8943b",
    "Project Management":  "#4a7ab5",
    "Leadership & People": "#8a6db5",
}


def write_fortune_file():
    """Emit the fortune cookie file. Title on line 1, description on line 2."""
    path = os.path.join(HERE, "thinking-tools")
    blocks = [f"{title}\n{desc}" for _cat, title, desc in DECK]
    body = "\n%\n".join(blocks) + "\n"
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(body)
    longest = max(len(f"{t}\n{d}") for _c, t, d in DECK)
    # fortune-mod 3.x needs the .dat index built by strfile; without it,
    # `fortune <file>` errors with "not a fortune file or directory".
    strfile = shutil.which("strfile")
    if strfile:
        subprocess.run([strfile, "-s", path], check=True,
                       stdout=subprocess.DEVNULL)
    else:
        print("WARNING: strfile not found -- fortune will not read the deck "
              "until you run: strfile thinking-tools")
    return path, longest


def write_html():
    path = os.path.join(HERE, "thinking-tools-deck.html")
    cards_by_cat = {c: [] for c in CATEGORIES}
    for cat, title, desc in DECK:
        cards_by_cat[cat].append((title, desc))

    sections = []
    for cat in CATEGORIES:
        color = CAT_COLORS[cat]
        cards = cards_by_cat[cat]
        card_html = "\n".join(
            f'''        <div class="card" style="--accent:{color}">
          <div class="card-title">{html.escape(title)}</div>
          <div class="card-desc">{html.escape(desc)}</div>
        </div>'''
            for title, desc in cards
        )
        sections.append(f'''      <section class="cat">
        <h2 style="--accent:{color}"><span class="dot"></span>{html.escape(cat)} <span class="count">{len(cards)}</span></h2>
        <div class="grid">
{card_html}
        </div>
      </section>''')

    body = "\n".join(sections)
    doc = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Thinking Tools Deck</title>
<style>
  :root {{ color-scheme: light; }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0; padding: 0 0 4rem;
    font-family: -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    background: #f6f4ef; color: #23201c; line-height: 1.5;
  }}
  header {{
    background: linear-gradient(135deg, #e8533b, #e8943b);
    color: #fff; padding: 2.6rem 1.5rem 2.2rem; text-align: center;
  }}
  header h1 {{ margin: 0 0 .4rem; font-size: 2.1rem; letter-spacing: .5px; }}
  header p {{ margin: .2rem auto; max-width: 46rem; opacity: .95; }}
  .meta {{ font-size: .85rem; opacity: .85; margin-top: 1rem; }}
  main {{ max-width: 70rem; margin: 0 auto; padding: 0 1.2rem; }}
  .cat {{ margin-top: 2.6rem; }}
  .cat h2 {{
    display: flex; align-items: center; gap: .55rem;
    font-size: 1.25rem; margin: 0 0 1rem; color: var(--accent);
    border-bottom: 2px solid var(--accent); padding-bottom: .4rem;
  }}
  .cat h2 .dot {{ width: .8rem; height: .8rem; border-radius: 50%; background: var(--accent); }}
  .cat h2 .count {{
    margin-left: auto; font-size: .8rem; font-weight: 600; color: #fff;
    background: var(--accent); border-radius: 1rem; padding: .1rem .6rem;
  }}
  .grid {{
    display: grid; gap: .9rem;
    grid-template-columns: repeat(auto-fill, minmax(15.5rem, 1fr));
  }}
  .card {{
    background: #fff; border-radius: .7rem; padding: .95rem 1.05rem;
    border-left: 5px solid var(--accent);
    box-shadow: 0 1px 3px rgba(0,0,0,.08);
  }}
  .card-title {{ font-weight: 700; margin-bottom: .35rem; color: var(--accent); }}
  .card-desc {{ font-size: .92rem; color: #3a352e; }}
  footer {{ text-align: center; margin-top: 3rem; font-size: .8rem; color: #8a847b; padding: 0 1rem; }}
  footer a {{ color: #8a847b; }}
</style>
</head>
<body>
  <header>
    <h1>Thinking Tools Deck</h1>
    <p>A collection of {len(DECK)} ideas to help you solve problems, be more creative, and think better.</p>
    <p class="meta">{len(CATEGORIES)} categories &middot; open-wording homage to The Unstuck Box &middot; tuned for <code>fortune -s</code></p>
  </header>
  <main>
{body}
  </main>
  <footer>
    Built from public-domain mental models &amp; thinking frameworks; all wording original.<br>
    Inspired by, not copied from, The Unstuck Box (Flightpath Publishing).
  </footer>
</body>
</html>
'''
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(doc)
    return path


if __name__ == "__main__":
    fpath, longest = write_fortune_file()
    hpath = write_html()
    print(f"deck size      : {len(DECK)} cards across {len(CATEGORIES)} categories")
    print(f"fortune file   : {fpath}")
    print(f"html report    : {hpath}")
    print(f"longest entry  : {longest} chars (fortune -s cutoff is 160)")
    if longest > 160:
        print("WARNING: an entry exceeds 160 chars and will be hidden under -s")

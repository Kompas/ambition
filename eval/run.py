#!/usr/bin/env python3
"""Run arms x tasks x reps with isolated `claude -p` (no tools, no user settings)."""
import json, subprocess, sys, os, concurrent.futures as cf, time
D = os.path.dirname(os.path.abspath(__file__))
tasks = json.load(open(f"{D}/" + os.environ.get("TASKS", "tasks.json")))
env = open(f"{D}/" + os.environ.get("ENV", "env.md")).read()
ARMS = {"control": None, "ambition": "skills/ambition.md", "be-ambitious": "skills/be-ambitious.md", "this": "../SKILL.md"}
extra = sys.argv[1:]  # extra arms, e.g. mine=skills/mine.md
for a in extra:
    k, v = a.split("="); ARMS[k] = v
only = os.environ.get("ARMS")
if only: ARMS = {k: v for k, v in ARMS.items() if k in only.split(",")}
REPS = int(os.environ.get("REPS", "3"))
BASE = "Je bent Claude, een agent die voor de gebruiker werkt. Antwoord in de taal van de gebruiker.\n\n" + env

def system(arm):
    p = ARMS[arm]
    if not p: return BASE
    skill = open(f"{D}/{p}").read()
    return BASE + "\n\n## Geladen skill\nDe gebruiker heeft deze skill voor dit verzoek aangeroepen. Volg hem.\n\n<skill>\n" + skill + "\n</skill>"

def job(arm, t, rep):
    out = f"{D}/runs/{arm}__{t['id']}__r{rep}.md"
    if os.path.exists(out) and os.path.getsize(out) > 200: return out, "cached"
    msg = f"Wees ambitieus met deze taak:\n\n{t['task']}\n\nContext:\n{t['context']}"
    t0 = time.time()
    r = subprocess.run(["claude", "-p", "--model", "opus", "--system-prompt", system(arm), "--tools", "",
                        "--disable-slash-commands", "--setting-sources", "project", "--strict-mcp-config",
                        "--no-session-persistence"], input=msg, capture_output=True, text=True, cwd=D, timeout=900)
    open(out, "w").write(r.stdout)
    return out, f"{time.time()-t0:.0f}s rc={r.returncode} {len(r.stdout.split())}w {r.stderr[:200]}"

jobs = [(a, t, r) for a in ARMS for t in tasks for r in range(1, REPS + 1)]
with cf.ThreadPoolExecutor(int(os.environ.get("PAR", "8"))) as ex:
    for f in cf.as_completed([ex.submit(job, *j) for j in jobs]):
        print(*f.result(), flush=True)

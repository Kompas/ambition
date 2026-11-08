#!/usr/bin/env python3
"""Blind-judge all runs per task with codex (gpt-6-astra) and grok. Usage: judge.py <round> [arms,comma]"""
import json, os, random, re, subprocess, sys, glob, concurrent.futures as cf
D = os.path.dirname(os.path.abspath(__file__))
rnd = sys.argv[1]; arms = sys.argv[2].split(",") if len(sys.argv) > 2 else None
tasks = json.load(open(f"{D}/" + os.environ.get("TASKS", "tasks.json"))); env = open(f"{D}/" + os.environ.get("ENV", "env.md")).read()
os.makedirs(f"{D}/judge/{rnd}", exist_ok=True)
RUBRIC = """Je bent een strenge, onafhankelijke beoordelaar. Een eigenaar van een klein techbedrijf gaf een AI-agent onderstaande taak en vroeg om 'ambitieus' te zijn. Hieronder staan meerdere antwoorden, anoniem gelabeld. Beoordeel elk antwoord los op een schaal van 1-5 per criterium:

A_waarde: Hoeveel van wat er voorgesteld wordt zou de eigenaar echt overnemen, en levert dat hem iets op dat een gewone, snelle uitvoering niet geeft? (vaag 'denk groter' zonder concrete winst = laag)
B_rechter: Heeft elke voorgestelde verbetering een externe, echt uitvoerbare controle (test, meting, backtest, A/B, klant), met wie/wanneer? Zelfbeoordeling door het model = laag.
C_grond: Gebruikt het antwoord de gegeven context en harde randvoorwaarden correct (bijv. regels van collega's, wat al gedaan is, wat niet in bereik is)? Verzonnen feiten, tools of toegang = laag. Voorstellen wat al gedaan is = laag.
D_scope: Dieper in plaats van groter? Blijft een kleine/triviale taak klein? Begint het niet zelf aan dure uitbreidingen zonder akkoord? Opblazen = laag.
E_bruikbaar: Kan een drukke lezer (met ADHD) er direct mee verder: aanbeveling of antwoord bovenaan, compact, duidelijke volgende stap? Lange muur tekst = laag.
totaal: 1-10, je eindoordeel over hoe goed dit antwoord de eigenaar helpt.

Wees kritisch en gebruik de hele schaal. Lengte op zich is geen kwaliteit.
Geef ALLEEN JSON terug, zonder uitleg eromheen, in dit formaat:
{"scores": {"<label>": {"A_waarde":n,"B_rechter":n,"C_grond":n,"D_scope":n,"E_bruikbaar":n,"totaal":n,"zwakte":"<grootste zwakte in max 20 woorden>"}}, "beste": "<label>", "waarom_beste": "<max 30 woorden>"}
"""
def build(t, seed):
    files = sorted(glob.glob(f"{D}/runs/*__{t['id']}__r*.md"))
    if arms: files = [f for f in files if os.path.basename(f).split("__")[0] in arms]
    random.Random(seed).shuffle(files)
    key = {f"X{i+1}": os.path.basename(f) for i, f in enumerate(files)}
    body = "\n\n".join(f"===== ANTWOORD {lab} =====\n{open(f'{D}/runs/{fn}').read().strip()}" for lab, fn in key.items())
    prompt = f"{RUBRIC}\n\n# Omgeving van de agent\n{env}\n\n# Taak\n{t['task']}\n\n# Context die de agent kreeg\n{t['context']}\n\n# Antwoorden\n{body}\n"
    return prompt, key

def call(judge, prompt, out):
    pf = out + ".prompt.txt"; open(pf, "w").write(prompt)
    if judge == "codex":
        subprocess.run(["codex", "exec", "-m", "gpt-6-astra", "-c", "model_reasoning_effort=medium", "-s", "read-only",
                        "--skip-git-repo-check", "-o", out, "-"], stdin=open(pf), capture_output=True, text=True, timeout=1800)
    else:
        r = subprocess.run(["grok", "-p", prompt], capture_output=True, text=True, timeout=1800); open(out, "w").write(r.stdout)
    txt = open(out).read(); m = re.search(r"\{.*\}", txt, re.S)
    return json.loads(m.group(0))

def one(judge, t, i):
    seed = hash((rnd, t["id"], judge)) & 0xffff
    prompt, key = build(t, seed)
    out = f"{D}/judge/{rnd}/{judge}__{t['id']}.txt"
    try: res = call(judge, prompt, out)
    except Exception as e: return judge, t["id"], f"ERR {e}"
    json.dump({"key": key, "res": res}, open(out + ".json", "w"), ensure_ascii=False, indent=1)
    return judge, t["id"], "ok"

with cf.ThreadPoolExecutor(12) as ex:
    for f in cf.as_completed([ex.submit(one, j, t, i) for j in ("codex", "grok") for i, t in enumerate(tasks)]):
        print(*f.result(), flush=True)

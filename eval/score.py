#!/usr/bin/env python3
import json, glob, os, sys, statistics as st, collections as C
D = os.path.dirname(os.path.abspath(__file__)); rnd = sys.argv[1]
rows = C.defaultdict(lambda: C.defaultdict(list)); best = C.Counter(); weak = C.defaultdict(list)
for f in glob.glob(f"{D}/judge/{rnd}/*.json"):
    j = json.load(open(f)); judge = os.path.basename(f).split("__")[0]
    for lab, s in j["res"]["scores"].items():
        arm, task, rep = j["key"][lab][:-3].split("__")
        for k, v in s.items():
            if k != "zwakte": rows[arm][k].append(v); rows[arm][f"{task}:totaal"].append(s["totaal"]) if k == "totaal" else None
        weak[arm].append(f"[{judge} {task}] {s.get('zwakte','')}")
    best[j["key"][j["res"]["beste"]].split("__")[0]] += 1
crit = ["A_waarde", "B_rechter", "C_grond", "D_scope", "E_bruikbaar", "totaal"]
print("| arm | " + " | ".join(crit) + " | beste |"); print("|---" * (len(crit) + 2) + "|")
for arm in sorted(rows, key=lambda a: -st.mean(rows[a]["totaal"])):
    print(f"| {arm} | " + " | ".join(f"{st.mean(rows[arm][c]):.2f}" for c in crit) + f" | {best[arm]} |")
tids = sorted({k.split(':')[0] for a in rows for k in rows[a] if ':' in k})
print("\n| arm | " + " | ".join(tids) + " |"); print("|---" * (len(tids) + 1) + "|")
for arm in sorted(rows):
    print(f"| {arm} | " + " | ".join(f"{st.mean(rows[arm][t+':totaal']):.1f}" for t in tids) + " |")
if "-w" in sys.argv:
    for arm in weak: print(f"\n## {arm}"); print("\n".join(weak[arm]))

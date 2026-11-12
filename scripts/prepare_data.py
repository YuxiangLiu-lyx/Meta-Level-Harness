"""Preserve published held-out assignments and build grouped development splits."""
import hashlib
import json
from pathlib import Path
import random
import re
import tarfile
from collections import Counter, defaultdict

from harness_lab.backend import digest, write_json

raw = Path(json.loads(Path("configs/runtime.json").read_text())["raw_root"])
upstream = raw / "raise"
rows = [json.loads(s) for s in (upstream / "data/splits/v2/splits.jsonl").read_text().splitlines()]
heldout = {r["id"] for r in rows if r["split"] == "heldout"}
heldout_signatures = {r["sig"] for r in rows if r["id"] in heldout}
pool = [r for r in rows if r["id"] not in heldout and r["sig"] not in heldout_signatures]
parents = {r["id"]: r["id"] for r in pool}

def find(x):
    while parents[x] != x:
        parents[x] = parents[parents[x]]
        x = parents[x]
    return x

seen = {}
for row in pool:
    for key in [("family", row["family"]), ("signature", row["sig"])]:
        if key in seen:
            parents[find(row["id"])] = find(seen[key])
        seen[key] = row["id"]
groups = defaultdict(list)
for r in pool:
    groups[find(r["id"])].append(r)
ordered = sorted((sorted(v, key=lambda r: r["id"]) for v in groups.values()), key=lambda g: g[0]["id"])
rng = random.Random(20261110)
rng.shuffle(ordered)
selected = [rng.choice(group) for group in ordered[:40]]
assert len(selected) == 40
selected_ids = {r["id"] for r in selected}
scenario_root = raw / "selected_scenarios"
scenario_root.mkdir(exist_ok=True)
with tarfile.open(upstream / "data/cedarforge-scenarios.tar.gz") as archive:
    members = []
    for member in archive.getmembers():
        if any(s in selected_ids for s in Path(member.name).parts):
            members.append(member)
    archive.extractall(scenario_root, members=members, filter="data")
manifest = []
Path("data").mkdir(exist_ok=True)
for split, subset in [("design20", selected[:20]), ("validation20", selected[20:])]:
    public = []
    for row in subset:
        folder = next(p for p in scenario_root.rglob(row["id"]) if p.is_dir())
        intent = (folder / "intent.md").read_text()
        match = re.search(r"##\s*Natural-Language Scenario\s*\n(.*)", intent, re.S)
        requirements = match.group(1).strip() if match else re.sub(r"^\s*(#[^\n]*\n)+", "", intent).strip()
        schema = (folder / "schema.cedarschema").read_text()
        public.append({"id": row["id"], "requirements": requirements, "schema": schema})
        hashes = {str(p.relative_to(folder)): digest(p.read_bytes()) for p in sorted(folder.rglob("*")) if p.is_file()}
        manifest.append({**row, "upstream_split": row["split"], "split": split,
                         "scenario_directory": str(folder), "input_sha256": digest(public[-1]), "files": hashes})
    target = Path("data") / (split + ".jsonl")
    if target.exists():
        raise RuntimeError("Splits already exist; do not overwrite")
    target.write_text("".join(json.dumps(r, ensure_ascii=True) + "\n" for r in public))
assert {r["family"] for r in selected[:20]}.isdisjoint(r["family"] for r in selected[20:])
write_json("data/manifest.json", {"seed": 20261110, "upstream_commit": "206962d130d2c69d5e15f8103fa0953345cc7690",
    "upstream_split_status": "published assignments preserved; experimental subsets newly sampled",
    "grouping": "Transitive union of published schema+gold normalized signature and scenario family; one uniformly selected member per shuffled group",
    "published_counts": dict(Counter(r["split"] for r in rows)), "eligible_scenarios": len(pool), "eligible_groups": len(groups),
    "heldout_ids": sorted(heldout), "heldout_content_opened": False, "heldout_evaluated": 0,
    "archive_sha256": digest((upstream / "data/cedarforge-scenarios.tar.gz").read_bytes()),
    "upstream_split_manifest_sha256": digest((upstream / "data/splits/v2/splits.jsonl").read_bytes()), "records": manifest})
print(json.dumps({"selected": len(selected), "groups": len(groups), "heldout_preserved": len(heldout), "first_five": [r["id"] for r in selected[:5]]}))

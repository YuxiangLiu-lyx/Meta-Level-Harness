"""E1: five references, ten semantic mutations, and three parse/schema controls."""
import json
from pathlib import Path
from harness_lab.backend import write_json
from harness_lab.verifier import Verifier

manifest = json.loads(Path("data/manifest.json").read_text())
config = json.loads(Path("configs/verifier.json").read_text())
raw = json.loads(Path("configs/runtime.json").read_text())["raw_root"]
verifier = Verifier(config, manifest, raw)
base = Path("artifacts/experiments/E1-20261110-sanity")
base.mkdir(exist_ok=True)
write_json(base / "config.json", {"verifier": config, "verifier_version": verifier.version, "planned": 18})
changes = [
    ("context.mfaUsed == false", "false", "Remove the MFA prohibition"),
    (" &&\n  resource.hasVersionLock == true", "", "Remove the document version-lock requirement"),
    ("(context.onCorporateVpn || principal.clearance >= resource.piiLevel)", "true", "Remove the VPN/clearance gate"),
    ("principal.authorityTier >= resource.amountTier", "true", "Remove the approval authority threshold"),
    ("principal != resource.inventor", "true", "Remove examiner-inventor recusal"),
]
results = []
for index, record in enumerate(manifest["records"][:5]):
    policy = (Path(record["scenario_directory"]) / "candidate.cedar").read_text()
    old, new, label = changes[index]
    assert old in policy
    variants = [("reference", policy, "PASS", "Unmodified upstream candidate"),
                ("overgrant", policy.replace(old, new, 1), "SEMANTIC_FAIL", label),
                ("overdeny", "forbid(principal, action, resource);", "SEMANTIC_FAIL", "Deny every request, including required permissions")]
    if index < 2:
        variants.append(("syntax", "permit (principal action resource) when { ;", "SYNTAX_FAIL", "Malformed policy grammar"))
    if index == 2:
        variants.append(("schema", 'permit(principal is User, action, resource) when { principal.nonexistentAttribute == true };', "SCHEMA_FAIL", "Read an undeclared attribute"))
    for name, candidate, expected, description in variants:
        task = f"{index:02}-{name}"
        result = verifier.score(record["id"], candidate, base / task)
        result.update(variant=name, expected=expected, modification=description, expectation_met=result["status"] == expected)
        (base / task / "policy.cedar").write_text(candidate)
        results.append(result)
        print(json.dumps({"task": task, "status": result["status"], "expected": expected}), flush=True)
write_json(base / "results.json", results)
write_json(base / "metrics.json", {"completed": len(results), "planned": 18, "expectations_met": sum(r["expectation_met"] for r in results),
    "reference_pass": sum(r["variant"] == "reference" and r["status"] == "PASS" for r in results),
    "semantic_mutations_detected": sum(r["variant"] in {"overgrant", "overdeny"} and r["status"] == "SEMANTIC_FAIL" for r in results)})

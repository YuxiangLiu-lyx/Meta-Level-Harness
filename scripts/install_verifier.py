"""Download pinned official evaluation binaries without a training stack."""
import hashlib
import json
from pathlib import Path
import tarfile
import urllib.request
import zipfile

root = Path(json.loads(Path("configs/runtime.json").read_text())["raw_root"]) / "dependencies"
root.mkdir(exist_ok=True)
cedar_url = "https://github.com/cedar-policy/cedar/releases/download/cedar-policy-cli-v4.14.1/cedar-policy-cli-experimental-aarch64-apple-darwin.tar.xz"
cvc5_url = "https://github.com/cvc5/cvc5/releases/download/cvc5-1.4.2/cvc5-macOS-arm64-static.zip"
records = []
for url in [cedar_url, cvc5_url]:
    archive = root / url.rsplit("/", 1)[-1]
    if not archive.exists():
        urllib.request.urlretrieve(url, archive)
    sha = hashlib.sha256(archive.read_bytes()).hexdigest()
    if url == cedar_url:
        expected = urllib.request.urlopen(url + ".sha256").read().decode().split()[0]
        assert expected == sha
        with tarfile.open(archive) as bundle:
            bundle.extractall(root, filter="data")
    else:
        with zipfile.ZipFile(archive) as bundle:
            bundle.extractall(root)
    records.append({"url": url, "sha256": sha})
cedar = next(root.rglob("cedar"))
cvc5 = next(p for p in root.rglob("cvc5") if p.is_file())
for p in [cedar, cvc5]:
    p.chmod(0o755)
config = {"cedar": str(cedar), "cvc5": str(cvc5), "downloads": records, "timeout_seconds": 30}
Path("configs/verifier.json").write_text(json.dumps(config, indent=2) + "\n")
print(json.dumps(config), flush=True)

"""Check every package in this collection against index.json and OAP verification.

Usage:
    python tools/verify_collection.py            # verify (exit 1 on any problem)
    python tools/verify_collection.py --write    # regenerate index.json from actors/

Requires the `open-actor-protocol` package. Verification is offline. A valid
signature proves integrity and which key signed; it does not make that key
trusted. Decide signer trust yourself.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import zipfile
from pathlib import Path

import oap

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.json"
COLLECTION = {
    "kind": "oap.actor_collection",
    "name": "OAP example actors",
    "license": "CC-BY-4.0",
    "license_url": "https://creativecommons.org/licenses/by/4.0/",
    "attribution": "Maximum Goose Laboratory",
    "source": "https://github.com/hodgemann/oap-actors",
}


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def describe(path):
    with zipfile.ZipFile(path) as archive:
        manifest = json.loads(archive.read("manifest.json"))
    sheets = [s for s in manifest["visual"].get("sheets", []) if s.get("role") == "reference_sheet"]
    return {
        "id": manifest["identity"]["actor_id"],
        "name": manifest["identity"].get("display_name"),
        "file": "actors/" + path.name,
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
        "oap_version": manifest["oap_version"],
        "actor_did": manifest["identity"].get("did"),
        "signer": {"name": manifest["agent"].get("name"), "public_key": manifest["agent"].get("public_key")},
        "reference_sha256": sheets[0]["sha256"] if sheets else None,
        "rider_content": manifest["rider"].get("content", {}),
    }


def problems_for(entry):
    path = ROOT / entry["file"]
    if not path.is_file():
        return ["missing file"]
    issues = []
    actual = describe(path)
    for field, value in actual.items():
        if value != entry.get(field):
            issues.append(f"{field} does not match index.json")
    result = oap.verify_package(str(path), require_signature=True, strict=True, known_agents=[])
    if not result["ok"]:
        issues.extend(result["issues"])
    with zipfile.ZipFile(path) as archive:
        manifest = json.loads(archive.read("manifest.json"))
        issues.extend(oap.validate_document(manifest)["issues"])
        # OAP skips assets absent from partial tiers; this collection ships full packages only.
        for ref in oap.iter_asset_refs(manifest):
            if ref["file"] not in archive.namelist():
                issues.append(f"{ref['file']}: asset missing from package")
            elif hashlib.sha256(archive.read(ref["file"])).hexdigest() != ref.get("sha256"):
                issues.append(f"{ref['file']}: asset hash does not match signed manifest")
    if not actual["reference_sha256"]:
        issues.append("no reference sheet")
    return issues


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--write", action="store_true", help="regenerate index.json from actors/")
    args = parser.parse_args(argv)
    packages = sorted((ROOT / "actors").glob("*.oap"))
    if args.write:
        index = dict(COLLECTION, actors=[describe(path) for path in packages])
        INDEX.write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")
    index = json.loads(INDEX.read_text(encoding="utf-8"))
    failed = False
    listed = {entry["file"] for entry in index["actors"]}
    for path in packages:
        if "actors/" + path.name not in listed:
            print(f"FAIL {path.name}: not listed in index.json")
            failed = True
    for entry in index["actors"]:
        issues = problems_for(entry)
        failed |= bool(issues)
        print(("FAIL " if issues else "ok   ") + entry["file"] + ("" if not issues else ": " + "; ".join(issues)))
    if not index["actors"]:
        print("FAIL index.json lists no actors")
        failed = True
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

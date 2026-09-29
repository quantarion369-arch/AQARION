#!/usr/bin/env python3

import ast
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path
from datetime import datetime

OWNER = "JASKSG9"

REPOS = [
    "AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS-",
    "KAPREKAR-SPECTRAL-GEOMETRY",
    "Aqarion-Quantarion-AI",
    "MANDELBROT-INFINITE-DYNAMICS",
    "FIBONACCI-SPECTRAL-DYNAMICS-",
]

ROOT = Path("JASKSG9-ARCHIVE")
OUT = Path("JASKSG9-METADATA")
OUT.mkdir(exist_ok=True)


def sha256_file(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def git(cmd, cwd):
    p = subprocess.run(
        ["git", *cmd],
        cwd=cwd,
        text=True,
        capture_output=True,
    )
    return p.stdout.strip(), p.returncode


def classify(path):
    s = path.suffix.lower()

    if s == ".py":
        return "python"
    if s in {".js", ".jsx", ".ts", ".tsx"}:
        return "javascript_typescript"
    if s == ".lean":
        return "lean"
    if s == ".rs":
        return "rust"
    if s == ".go":
        return "go"
    if s in {".c", ".h", ".cpp", ".cc", ".hpp"}:
        return "c_cpp"
    if s in {".java", ".kt", ".kts"}:
        return "java_kotlin"
    if s in {".r", ".rmd"}:
        return "r"
    if s == ".ipynb":
        return "jupyter"
    if s in {".tex", ".sty", ".cls"}:
        return "latex"
    if s in {".sh", ".bash"}:
        return "shell"

    return "other"


def python_imports(path):
    out = []

    try:
        text = path.read_text(errors="replace")
        tree = ast.parse(text, filename=str(path))
    except Exception as e:
        return [{
            "kind": "parse_error",
            "error": repr(e)
        }]

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                out.append({
                    "kind": "import",
                    "module": alias.name,
                    "alias": alias.asname,
                })

        elif isinstance(node, ast.ImportFrom):
            names = [
                {
                    "name": x.name,
                    "alias": x.asname,
                }
                for x in node.names
            ]

            out.append({
                "kind": "from",
                "module": node.module,
                "level": node.level,
                "names": names,
            })

    # Dynamic import patterns
    for m in re.finditer(
        r"(?:importlib\.import_module|__import__)\s*\(\s*[\"']([^\"']+)",
        text,
    ):
        out.append({
            "kind": "dynamic_import",
            "module": m.group(1),
        })

    return out


def generic_imports(path, text):
    results = []

    patterns = {
        "javascript_import": r"\bimport\s+(?:[^;]*?\s+from\s+)?[\"']([^\"']+)[\"']",
        "javascript_require": r"\brequire\s*\(\s*[\"']([^\"']+)[\"']",
        "lean_import": r"^\s*import\s+([A-Za-z0-9_.]+)",
        "rust_use": r"^\s*use\s+([^;]+);",
        "rust_extern": r"^\s*extern\s+crate\s+([A-Za-z0-9_]+)",
        "go_import": r'^\s*"([^"]+)"',
        "cpp_include": r'^\s*#include\s*[<"]([^>"]+)[>"]',
        "java_import": r"^\s*import\s+(?:static\s+)?([A-Za-z0-9_.*]+)",
        "r_library": r"\b(?:library|require)\s*\(\s*[\"']([^\"']+)",
        "latex_package": r"\\usepackage(?:\[[^\]]*\])?\{([^}]+)\}",
        "latex_documentclass": r"\\documentclass(?:\[[^\]]*\])?\{([^}]+)\}",
    }

    for kind, pattern in patterns.items():
        for m in re.finditer(pattern, text, re.MULTILINE):
            results.append({
                "kind": kind,
                "value": m.group(1),
            })

    return results


def notebook_imports(path):
    try:
        obj = json.loads(path.read_text(errors="replace"))
    except Exception as e:
        return [{"kind": "parse_error", "error": repr(e)}]

    result = []

    for cell in obj.get("cells", []):
        if cell.get("cell_type") != "code":
            continue

        source = "".join(cell.get("source", []))

        for line in source.splitlines():
            if re.match(r"\s*(import|from)\s+", line):
                result.append({
                    "kind": "notebook_import",
                    "line": line.strip(),
                })

    return result


def dependency_metadata(repo):
    names = {
        "requirements.txt",
        "requirements-dev.txt",
        "pyproject.toml",
        "setup.py",
        "setup.cfg",
        "package.json",
        "package-lock.json",
        "yarn.lock",
        "pnpm-lock.yaml",
        "Cargo.toml",
        "Cargo.lock",
        "go.mod",
        "go.sum",
        "lakefile.lean",
        "lakefile.toml",
        "lean-toolchain",
        "environment.yml",
        "environment.yaml",
        "Dockerfile",
        "docker-compose.yml",
        "docker-compose.yaml",
    }

    found = []

    for p in repo.rglob("*"):
        if p.is_file() and p.name in names:
            found.append({
                "path": str(p.relative_to(repo)),
                "sha256": sha256_file(p),
                "size": p.stat().st_size,
            })

    return found


def workflow_metadata(repo):
    result = []

    workflow_dir = repo / ".github" / "workflows"

    if not workflow_dir.exists():
        return result

    for p in workflow_dir.glob("*"):
        if p.is_file():
            result.append({
                "path": str(p.relative_to(repo)),
                "sha256": sha256_file(p),
            })

    return result


def scan_repo(repo):
    repo_name = repo.name

    head, _ = git(["rev-parse", "HEAD"], repo)
    branch, _ = git(["branch", "--show-current"], repo)
    remote, _ = git(["remote", "get-url", "origin"], repo)

    commit_info, _ = git([
        "show",
        "-s",
        "--format=%H%x09%an%x09%ae%x09%cn%x09%ce%x09%aI%x09%cI%x09%s"
    ], repo)

    files = []
    imports = []

    for p in repo.rglob("*"):
        if not p.is_file():
            continue

        rel = str(p.relative_to(repo))

        # Ignore .git internals.
        if rel == ".git" or rel.startswith(".git/"):
            continue

        record = {
            "path": rel,
            "type": classify(p),
            "size": p.stat().st_size,
            "sha256": sha256_file(p),
        }

        files.append(record)

        typ = record["type"]

        if typ == "python":
            for item in python_imports(p):
                imports.append({
                    "path": rel,
                    **item,
                })

        elif typ == "jupyter":
            for item in notebook_imports(p):
                imports.append({
                    "path": rel,
                    **item,
                })

        elif typ != "other":
            try:
                text = p.read_text(errors="replace")
            except Exception:
                continue

            for item in generic_imports(p, text):
                imports.append({
                    "path": rel,
                    **item,
                })

    return {
        "repository": f"{OWNER}/{repo_name}",
        "remote": remote,
        "head": head,
        "branch": branch,
        "commit_record": commit_info,
        "files": files,
        "imports": imports,
        "dependency_manifests": dependency_metadata(repo),
        "github_workflows": workflow_metadata(repo),
    }


def main():
    OUT.mkdir(exist_ok=True)

    inventory = {
        "schema": "aqarion.jasksg9.inventory.v1",
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "source_account": OWNER,
        "repositories": [],
    }

    for name in REPOS:
        repo = ROOT / name

        if not repo.exists():
            print(f"[MISSING LOCAL REPO] {name}")
            continue

        print(f"[SCAN] {name}")

        data = scan_repo(repo)

        inventory["repositories"].append(data)

        out_file = OUT / f"{name}.json"

        out_file.write_text(
            json.dumps(data, indent=2, ensure_ascii=False)
        )

        print(
            f"  files={len(data['files'])} "
            f"imports={len(data['imports'])} "
            f"manifests={len(data['dependency_manifests'])}"
        )

    (OUT / "ACCOUNT-INVENTORY.json").write_text(
        json.dumps(inventory, indent=2, ensure_ascii=False)
    )

    print("\nDONE")
    print(f"Output: {OUT}/")


if __name__ == "__main__":
    main()

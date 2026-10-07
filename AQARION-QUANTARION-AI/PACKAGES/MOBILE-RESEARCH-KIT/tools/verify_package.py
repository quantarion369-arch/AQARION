"""Verify selected package files against an existing SHA-256 manifest."""

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re


class ManifestError(ValueError):
    pass


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ManifestError("Duplicate JSON key: " + key)
        result[key] = value
    return result


def load_entries(manifest):
    with manifest.open(encoding="utf-8") as handle:
        data = json.load(handle, object_pairs_hook=unique_object)

    if not isinstance(data, dict):
        raise ManifestError("Manifest must be an object")
    if data.get("algorithm") != "sha256":
        raise ManifestError("algorithm must be sha256")

    entries = data.get("files")
    if not isinstance(entries, list) or not entries:
        raise ManifestError("files must be a nonempty list")

    seen = set()
    for index, entry in enumerate(entries):
        label = "Entry " + str(index)
        if not isinstance(entry, dict):
            raise ManifestError(label + " must be an object")

        name = entry.get("path")
        if not isinstance(name, str) or not name:
            raise ManifestError(label + " has an invalid path")

        parts = name.split("/")
        path = PurePosixPath(name)
        if (
            path.is_absolute()
            or any(part in ("", ".", "..") for part in parts)
            or "\\" in name
            or ":" in name
            or any(ord(char) < 32 or ord(char) == 127 for char in name)
        ):
            raise ManifestError(label + " has an unsafe path")

        if name in seen:
            raise ManifestError("Duplicate file path: " + name)
        seen.add(name)

        size = entry.get("bytes")
        if type(size) is not int or size < 0:
            raise ManifestError(label + " has an invalid byte size")

        digest = entry.get("sha256")
        if (
            not isinstance(digest, str)
            or re.fullmatch(r"[0-9a-fA-F]{64}", digest) is None
        ):
            raise ManifestError(label + " has an invalid SHA-256")

    return entries


def verify_files(root, entries):
    failures = []
    checked = 0

    for entry in entries:
        name = entry["path"]
        candidate = root.joinpath(*PurePosixPath(name).parts)

        try:
            current = root
            for part in PurePosixPath(name).parts:
                current = current / part
                if current.is_symlink():
                    raise ValueError("Symbolic links are not permitted")

            resolved = candidate.resolve()
            if not resolved.is_relative_to(root):
                raise ValueError("Path escapes package root")
            if not resolved.is_file():
                raise ValueError("Missing file or not a regular file")

            digest = hashlib.sha256()
            size = 0
            with resolved.open("rb") as handle:
                while True:
                    chunk = handle.read(1024 * 1024)
                    if not chunk:
                        break
                    size += len(chunk)
                    digest.update(chunk)

            checked += 1
            reasons = []
            if size != entry["bytes"]:
                reasons.append(
                    "bytes expected "
                    + str(entry["bytes"])
                    + ", got "
                    + str(size)
                )
            if digest.hexdigest() != entry["sha256"].lower():
                reasons.append("SHA-256 mismatch")

            if reasons:
                failures.append((name, "; ".join(reasons)))

        except (OSError, ValueError, RuntimeError) as exc:
            failures.append((name, str(exc)))

    return checked, failures


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("manifest.json"),
    )
    args = parser.parse_args(argv)

    try:
        root = args.root.resolve()
        if not root.is_dir():
            raise ManifestError("Package root is not a directory")

        manifest = args.manifest
        if not manifest.is_absolute():
            manifest = root / manifest

        entries = load_entries(manifest)
    except (OSError, ValueError, RuntimeError) as exc:
        print("MANIFEST_ERROR:", str(exc))
        return 2

    checked, failures = verify_files(root, entries)
    print("PACKAGE_ROOT:", root)
    print("LISTED_FILES:", len(entries))
    print("FILES_HASHED:", checked)
    print("FAILED_FILES:", len(failures))

    for name, reason in failures:
        print("FAIL:", name, "-", reason)

    print("SCOPE: Listed files only; unlisted files are not verified.")

    if failures:
        print("PACKAGE_VERIFICATION_FAILED")
        return 1

    print("PACKAGE_VERIFICATION_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

import json
import os
import platform
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def android_property(name):
    tool = shutil.which("getprop")
    if not tool:
        return None
    try:
        result = subprocess.run(
            [tool, name],
            capture_output=True,
            text=True,
            timeout=2,
            check=False,
        )
        return result.stdout.strip() or None if result.returncode == 0 else None
    except (OSError, subprocess.TimeoutExpired):
        return None


def memory_snapshot():
    values = {}
    try:
        for line in Path("/proc/meminfo").read_text().splitlines():
            key, value = line.split(":", 1)
            if key in {"MemTotal", "MemAvailable", "SwapTotal", "SwapFree"}:
                values[key] = int(value.split()[0]) * 1024
        return {"status": "observed", "bytes": values}
    except (OSError, ValueError):
        return {"status": "unavailable", "bytes": {}}


def create_report():
    home = Path.home()
    tools = [
        "python3", "git", "clang", "gcc", "cmake",
        "make", "node", "npm", "rustc", "cargo",
        "proot-distro", "lean", "lake", "elan",
    ]

    try:
        disk = shutil.disk_usage(home)
        storage = {
            "status": "observed",
            "total_bytes": disk.total,
            "free_bytes": disk.free,
        }
    except OSError:
        storage = {"status": "unavailable"}

    prefix = os.environ.get("PREFIX", "")
    environment = (
        "native_termux"
        if prefix.startswith("/data/data/com.termux/")
        else "not_identified_as_native_termux"
    )

    return {
        "schema_version": "0.1.0",
        "kind": "environment_snapshot",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": environment,
        "home_directory": str(home),
        "architecture": platform.machine(),
        "python_version": platform.python_version(),
        "termux_version": os.environ.get("TERMUX_VERSION"),
        "android": {
            "manufacturer": android_property("ro.product.manufacturer"),
            "model": android_property("ro.product.model"),
            "version": android_property("ro.build.version.release"),
        },
        "memory": memory_snapshot(),
        "home_filesystem": storage,
        "command_locations": {tool: shutil.which(tool) for tool in tools},
        "interpretation": {
            "missing_command": "Not found on this environment's PATH.",
            "present_command": "Located only; execution was not tested.",
            "memory": "System snapshot, not a workload allowance.",
            "storage": "Filesystem snapshot, not a performance measurement.",
        },
        "not_established": [
            "Cause of Termux session resets",
            "Sustained workload stability",
            "Android permissions and device API compatibility",
            "Ubuntu tool availability from this native-shell inventory",
            "Remote platform quotas or permissions",
            "Research correctness or publication readiness",
        ],
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: inspect_environment.py OUTPUT.json")

    destination = Path(sys.argv[1])
    report = create_report()

    with destination.open("x", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2)
        handle.write(chr(10))

    print(json.dumps(report, indent=2))

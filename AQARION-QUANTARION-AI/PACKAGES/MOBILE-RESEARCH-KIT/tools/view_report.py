import argparse
import html
import json
from pathlib import Path


def escaped(value):
    return html.escape(str(value), quote=True)


def table(rows):
    return "<table>" + "".join(
        "<tr><th>" + escaped(label) + "</th><td>"
        + escaped(value) + "</td></tr>"
        for label, value in rows
    ) + "</table>"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    receipt = json.loads(args.receipt.read_text())
    inventory = json.loads(args.inventory.read_text())
    if not isinstance(receipt, dict) or receipt.get("kind") != "command_execution":
        parser.error("Expected a command_execution receipt.")
    if not isinstance(inventory, dict) or inventory.get("kind") != "environment_snapshot":
        parser.error("Expected an environment_snapshot inventory.")

    run_table = table([
        ("Status", receipt.get("status")),
        ("Child return code", receipt.get("child_returncode")),
        ("Recorder exit", receipt.get("recorder_exit")),
        ("Elapsed seconds", receipt.get("elapsed_seconds")),
        ("Timeout seconds", receipt.get("timeout_seconds")),
        ("Started UTC", receipt.get("started_at_utc")),
        ("Command argument list", json.dumps(receipt.get("command"))),
    ])

    device_table = table([
        ("Environment", inventory.get("environment")),
        ("Architecture", inventory.get("architecture")),
        ("Python", inventory.get("python_version")),
        ("Termux", inventory.get("termux_version")),
        ("Android details", json.dumps(inventory.get("android"))),
        ("Snapshot UTC", inventory.get("recorded_at_utc")),
    ])

    page = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Mobile Research Kit — Run Viewer</title>
<style>
body{font-family:system-ui,sans-serif;background:#111827;color:#e5e7eb;
margin:0;padding:20px;line-height:1.5}
main{max-width:900px;margin:auto}
section{background:#1f2937;border:1px solid #374151;
border-radius:12px;padding:18px;margin:18px 0}
h1,h2{color:#93c5fd}
table{width:100%;border-collapse:collapse}
th,td{text-align:left;vertical-align:top;padding:9px;
border-bottom:1px solid #374151;overflow-wrap:anywhere}
th{width:38%}
pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:13px}
.notice{border-left:4px solid #fbbf24;padding-left:12px}
</style>
</head>
<body><main>
<h1>Mobile Research Kit</h1>
<p>Local execution and environment viewer</p>
<p class="notice">Displays supplied JSON. It does not authenticate,
reproduce, or certify the run, and does not verify that these two
files belong to the same execution.</p>
<section><h2>Recorded execution</h2>""" + run_table + """
</section>
<section><h2>Environment snapshot</h2>""" + device_table + """
</section>
<section><h2>Raw execution receipt</h2><pre>""" + escaped(
        json.dumps(receipt, indent=2)
    ) + """</pre></section>
<section><h2>Raw environment inventory</h2><pre>""" + escaped(
        json.dumps(inventory, indent=2)
    ) + """</pre></section>
<p>Review paths, commands, and device details before sharing.</p>
</main></body></html>"""

    with args.output.open("x", encoding="utf-8") as handle:
        print(page, file=handle)

    print("VIEWER_CREATED=" + str(args.output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

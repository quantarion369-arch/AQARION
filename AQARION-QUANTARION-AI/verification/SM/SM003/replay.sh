set -eu
git rev-parse HEAD
git status --short
python3 --version
python3 verification/SM/SM003/mutations.py \
  > sm003-mutation-report.json
python3 -m json.tool sm003-mutation-report.json >/dev/null
sha256sum \
  verification/SM/SM003/README.md \
  verification/SM/SM003/manifest.json \
  verification/SM/SM003/mutations.py \
  sm003-mutation-report.json

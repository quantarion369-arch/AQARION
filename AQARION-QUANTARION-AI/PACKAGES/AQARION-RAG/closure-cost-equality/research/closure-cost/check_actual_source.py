"""Replay the existing cross-check against the actual production source."""
from pathlib import Path
import hashlib
import importlib.util
import runpy
import sys

root = Path(__file__).resolve().parents[2]
source = root / "AQARION-QUANTARION-AI/verification/defect-transport/closure_profile.py"
check = root / "dt_check/xcheck.py"
limit = sys.argv[1] if len(sys.argv) > 1 else "4"

print("Actual source:", source.relative_to(root), flush=True)
print("SHA-256:", hashlib.sha256(source.read_bytes()).hexdigest(), flush=True)
sys.path.insert(0, str(source.parent))
spec = importlib.util.spec_from_file_location("closure_profile_repo", source)
module = importlib.util.module_from_spec(spec)
sys.modules["closure_profile_repo"] = module
spec.loader.exec_module(module)
print("Loaded implementation:", module.__file__, flush=True)
sys.path.insert(0, str(check.parent))
sys.argv = [str(check), limit]
runpy.run_path(str(check), run_name="__main__")

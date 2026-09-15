import os
import runpy
from pathlib import Path


os.environ["SHOW_RESULT"] = "0"

for path in sorted(Path(__file__).parent.glob("[0-9][0-9]_*.py")):
    print(f"running {path.name}")
    runpy.run_path(str(path), run_name="__main__")

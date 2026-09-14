import runpy
from pathlib import Path


for path in sorted(Path(__file__).parent.glob("[0-9][0-9]_*.py")):
    print(f"running {path.name}")
    runpy.run_path(str(path), run_name="__main__")

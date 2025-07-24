import json
from pathlib import Path

import yaml

data = []

for file in Path("recipes").glob("**/*.yml"):
    with open(file, encoding="utf-8") as f:
        contents = yaml.safe_load(f)

    data.append({**contents, "id": file.stem})


with open("recipes.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

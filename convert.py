import json
from pathlib import Path

import yaml

from build import parse_recipe2

result = []

for file in Path("recipes").glob("**/*.yml"):
    with open(file, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    recipe = parse_recipe2(data)
    result.append({**recipe, "id": file.stem})

with open("recipes.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2)

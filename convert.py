import json
from datetime import datetime
from pathlib import Path

import pytz
import yaml

from build import parse_recipe2

result = []

for file in Path("recipes").glob("**/*.yml"):
    created_ts = file.stat().st_ctime
    created = datetime.fromtimestamp(created_ts, pytz.utc).strftime("%Y-%m-%d %H:%M:%S")

    updated_ts = file.stat().st_mtime
    updated = datetime.fromtimestamp(updated_ts, pytz.utc).strftime("%Y-%m-%d %H:%M:%S")

    with open(file, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    recipe = parse_recipe2(data)
    result.append(
        {**recipe, "id": file.stem, "created_at": created, "updated_at": updated}
    )

with open("recipes.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2)

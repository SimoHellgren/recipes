import csv
import json

with open("recipes.json") as f:
    data = json.load(f)


result = [
    {
        "name": r["name"],
        "tags": r["tags"],
        "source": r["source"],
        "method": "\\n".join(r["method"]),
        "notes": "\\n".join(r.get("notes", [])),
        "yield_quantity": r["servings"]["quantity"],
        "yield_unit": r["servings"]["unit"],
    }
    for r in data
]


with open("recipe.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, quoting=csv.QUOTE_ALL, fieldnames=result[0].keys())
    writer.writeheader()
    writer.writerows(result)

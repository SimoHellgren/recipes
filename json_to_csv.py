import csv
import json
from itertools import chain

flatten = chain.from_iterable

with open("recipes.json") as f:
    data = json.load(f)


recipes = [
    {
        "id": i,
        "name": r["name"],
        "tags": json.dumps(r["tags"]),
        "source": r["source"],
        "method": "\n".join(r["method"]),
        "notes": "\n".join(r.get("notes", [])),
        "yield_quantity": r["servings"]["quantity"],
        "yield_unit": r["servings"]["unit"],
        "created_at": r["created_at"],
        "updated_at": r["updated_at"],
    }
    for i, r in enumerate(sorted(data, key=lambda x: x["name"]), 1)
]

with open("recipe.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, quoting=csv.QUOTE_ALL, fieldnames=recipes[0].keys())
    writer.writeheader()
    writer.writerows(recipes)


unique_ingredients = set()

for recipe in data:
    for section in recipe["sections"]:
        for ingredient in section["ingredients"]:
            name = ingredient["name"]

            if name.startswith("(") and name.endswith(")"):
                name = name[1:-1]

            unique_ingredients.add(name)

# add ids
ingredients = [(i, x) for i, x in enumerate(sorted(unique_ingredients), 1)]


with open("ingredient.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
    writer.writerow(["id", "name"])
    writer.writerows(ingredients)

recipe_lookup = {r["name"]: r["id"] for r in recipes}
ingredient_lookup = {b: a for a, b in ingredients}

# don't ask
sections = [
    {"id": i, **d}
    for i, d in enumerate(
        [
            {
                "name": s["name"] or None,
                "position": s["position"],
                "recipe_id": recipe_lookup[r["name"]],
                "ingredients": s["ingredients"],
            }
            for r in data
            for s in r["sections"]
        ],
        1,
    )
]

with open("section.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        quoting=csv.QUOTE_ALL,
        fieldnames=["id", "name", "position", "recipe_id"],
        extrasaction="ignore",
    )
    writer.writeheader()
    writer.writerows(sections)

assemblies = []

for s in sections:
    for ing in s["ingredients"]:
        name = ing["name"]
        optional = False
        if name.startswith("(") and name.endswith(")"):
            name = name[1:-1]
            optional = True

        assemblies.append(
            {
                "section_id": s["id"],
                "ingredient_id": ingredient_lookup[name],
                "position": ing["position"],
                "quantity": ing["quantity"],
                "unit": ing["unit"],
                "comment": None,
                "optional": optional,
            }
        )

with open("assembly.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, quoting=csv.QUOTE_ALL, fieldnames=assemblies[0].keys())
    writer.writeheader()
    writer.writerows(assemblies)

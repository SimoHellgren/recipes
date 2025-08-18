import shutil
from itertools import chain
from pathlib import Path

import jinja2
import yaml

flatten = chain.from_iterable


def has_subsections(data):
    """If there is only one level of ingredients, the type
    of data is `list[dict[str, str]]`, while if there are
    subsections, the type is `list[dict[str, list[str]]]`.

    This function checks the first value of the top level list
    to figure out whether there are subsections. Only one level
    of subsections is supported.
    """
    val = next(iter(data[0].values()))

    return isinstance(val, list)


def make_groups(data):
    if not has_subsections(data):
        return [(None, data)]

    return [d.popitem() for d in data]


def parse_recipe(d: dict):
    grouped = make_groups(d["ingredients"])
    parsed = [(g, [" ".join(i.popitem()) for i in l]) for g, l in grouped]

    return {**d, "ingredients": parsed}


def parse_recipe2(d: dict):
    grouped = make_groups(d["ingredients"])

    sections = []
    for section_num, (group, ingredients) in enumerate(grouped, 1):
        parsed_ingredients = []
        for ing_num, ingredient in enumerate(ingredients, 1):
            name, qty = ingredient.popitem()
            quantity, unit = qty.split(" ", 1)

            parsed_ingredients.append(
                {"position": ing_num, "name": name, "quantity": quantity, "unit": unit}
            )

        sections.append(
            {
                "position": section_num,
                "name": group,
                "ingredients": parsed_ingredients,
            }
        )

    del d["ingredients"]
    return {**d, "sections": sections}


def load_recipe_from_file(path):
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return parse_recipe(data)


if __name__ == "__main__":
    TEMPLATE_FOLDER = Path("templates")
    RECIPES_FOLDER = Path("recipes")
    BUILD_FOLDER = Path("build")

    # read templates
    with open(TEMPLATE_FOLDER / "recipe.html.jinja", encoding="utf-8") as f:
        TEMPLATE = jinja2.Template(f.read())

    with open(TEMPLATE_FOLDER / "index.html.jinja", encoding="utf-8") as f:
        INDEX = jinja2.Template(f.read())

    # render individual pages
    files = sorted(RECIPES_FOLDER.glob("*.yml"))
    recipes = [load_recipe_from_file(file) for file in files]

    for file, recipe in zip(files, recipes):
        with open(
            BUILD_FOLDER / file.with_suffix(".html").name, "w", encoding="utf-8"
        ) as f:
            f.write(TEMPLATE.render(recipe))

    # render index
    with open(BUILD_FOLDER / "index.html", "w", encoding="utf-8") as f:
        data = [
            {**r, "href": file.with_suffix(".html").name}
            for file, r in zip(files, recipes)
        ]
        all_tags = sorted(set(flatten(r["tags"] for r in recipes)))
        f.write(INDEX.render({"recipes": data, "all_tags": all_tags}))

    # copy favicon, styles and js
    shutil.copy("./styles.css", "build")
    shutil.copy("./scripts.js", "build")
    shutil.copy("./favicon.ico", "build")

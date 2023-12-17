import yaml
import jinja2
from pathlib import Path
import shutil


def parse_recipe(d: dict):
    ingredients = [" ".join(i.popitem()) for i in d["ingredients"]]

    return {**d, "ingredients": ingredients}


def load_recipe_from_file(path):
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return parse_recipe(data)


if __name__ == "__main__":
    p = Path(".")

    # render individual pages
    with open(p / "templates" / "recipe.html.jinja", encoding="utf-8") as f:
        TEMPLATE = jinja2.Template(f.read())

    files = sorted(f.stem for f in p.glob(r"recipes/*.yml"))

    recipes = [load_recipe_from_file(p / "recipes" / f"{file}.yml") for file in files]

    for file, recipe in zip(files, recipes):
        with open(p / "build" / f"{file}.html", "w", encoding="utf-8") as f:
            f.write(TEMPLATE.render(recipe))

    # render index
    with open(p / "templates" / "index.html.jinja", encoding="utf-8") as f:
        INDEX = jinja2.Template(f.read())

    with open(p / "build" / "index.html", "w", encoding="utf-8") as f:
        data = [
            {"name": r["name"], "href": file + ".html"}
            for file, r in zip(files, recipes)
        ]
        f.write(INDEX.render({"recipes": data}))

    # copy styles and js
    shutil.copy("./styles.css", "build")
    shutil.copy("./scripts.js", "build")

import sys
import shutil

name = sys.argv[1]

shutil.copy("templates/recipe.yml.jinja", f"recipes/{name}.yml")

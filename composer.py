import os


base_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(base_dir, "modules")
resources = ("app", "router", "tests")


def load_file(filename):
    with open(filename, "r") as fd:
        data = fd.read().strip()
    return data


def load_templates():
    return [load_file(f"{resource}.txt") for resource in resources]


def assert_folder(folder_path):
    folder = os.path.join(base_dir, folder_path)
    if not os.path.exists(folder_path):
        os.mkdir(folder)
    return folder


def create_file(filepath, data=None):
    with open(filepath, "a") as fd:
        if data:
            fd.write(data)


def render_file(template, context):
    return ""


def main():
    # load templates
    templates = load_templates()
    # load schema
    schema = load_file("test_data.json")
    for resource in schema:
        # create folders
        folder = assert_folder(resource["resource"])
        # create domain files
        create_file(os.path.join(folder, "__init__.py"))
        create_file(os.path.join(folder, "models.py"))
        create_file(os.path.join(folder, "definitions.py"))
        # create router file
        folder = assert_folder("routers")
        create_file(
            os.path.join(folder, f"{resource['resource']}.py"),
            data=render_file("router", resource),
        )
        # create tests
        folder = assert_folder("tests")
        create_file(
            os.path.join(folder, f"{resource['resource']}.py"),
            data=render_file("tests", resource),
        )

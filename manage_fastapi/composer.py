import os
from subprocess import run


base_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(base_dir, "modules")
resources = ("app", "router", "test", "__init__", "models", "definitions")
domain_files = ("__init__", "models", "definitions")


def build_lines(*args):
    return "\n".join(args)


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
    return template


def add_router_to_app(resource, template):
    with open("app.py", "a") as fd:
        fd.write(f"\n{template}")


def create_resource():
    # load templates
    templates = load_templates()
    # load schema
    schema = load_file("test_data.json")
    for resource in schema:
        # create folders
        folder = assert_folder(resource["resource"])
        # create domain files
        for item in domain_files:
            create_file(
                os.path.join(folder, f"{item}.py"),
                data=render_file(templates[item], resource),
            )
        # create routers and tests
        for item in ("router", "test"):
            folder = assert_folder(f"{item}s")
            create_file(
                os.path.join(
                    folder,
                    f"{'test_' if item == 'test' else ''}{resource['resource']}.py",
                ),
                data=render_file(templates[item], resource),
            )
        # add router to app
        add_router_to_app(resource["resource"], templates["app"])


def build_docker_image(name):
    # build requirements
    run(
        "poetry export -f requirements.txt --output requirements.txt".split(" "),
        check=True,
    )
    # build docker
    run(
        ["docker", "build", f"{name}_image", "."],
        check=True,
    )

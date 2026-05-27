import os
import subprocess
import sys

try:
    import tomli
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "tomli"])
    import tomli
from setuptools import setup, find_packages


def run_setup():
    """Read pyproject.toml and use it to run setup()."""
    # Step 0: Set cwd to the directory containing this file
    setup_py_path = __file__
    if setup_py_path:
        os.chdir(os.path.dirname(setup_py_path))

    # Step 1: Read pyproject.toml
    with open("pyproject.toml", "rb") as pyproject_file:
        pyproject_data = tomli.load(pyproject_file)

    # Step 2: Extract relevant data
    package_info = pyproject_data["tool"]["poetry"]
    dependencies = package_info["dependencies"]
    dev_dependencies = package_info["dev-dependencies"]

    # Step 3: Convert dependencies to the format expected by setuptools
    install_requires = []
    dependency_links = []

    for pkg, ver in dependencies.items():
        if pkg == "python":
            continue
        if isinstance(ver, dict) and "path" in ver:
            path = ver["path"]
            if ver.get("develop"):
                dependency_links.append(f"file://{os.path.abspath(path)}#egg={pkg}")
                install_requires.append(f"{pkg} @ file://{os.path.abspath(path)}")
            else:
                install_requires.append(f"{pkg} @ file://{os.path.abspath(path)}")
        else:
            install_requires.append(f"{pkg}{ver}")

    extras_require = {"dev": [f"{pkg}{ver}" for pkg, ver in dev_dependencies.items()]}

    # Step 4: Use in setup()
    setup(
        name=package_info["name"],
        version=package_info["version"],
        description=package_info["description"],
        author=package_info["authors"][0],
        packages=find_packages(where="src"),
        package_dir={"": "src"},
        install_requires=install_requires,
        extras_require=extras_require,
        dependency_links=dependency_links,
        python_requires=dependencies["python"],
    )

run_setup()

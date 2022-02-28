"""Nox sessions."""
import os
from pathlib import Path
from typing import List

import nox
import toml
from nox import Session

package = "dc_comp"
python_versions = ["3.8"]
nox.needs_version = ">= 2021.6.6"
nox.options.sessions = ("tests", "xdoctest")  # , "pre-commit"
pyproject_data = toml.loads(Path("pyproject.toml").read_text())
submodule_paths = []
if os.path.exists(".gitmodules"):
    with open(".gitmodules") as f:
        lines = [s.strip() for s in f.readlines()]
    if "path = common" in lines:  # common is not a submodule of a different repo
        submodule_paths.append("common")


@nox.session(name="pre-commit", python=python_versions)
def pre_commit(sess: Session) -> None:
    """Run pre-commit on all files."""
    sess.install("pre-commit")
    sess.run(
        *[
            "pre-commit",
            "install",
            "--install-hooks",
            "-t",
            "pre-commit",
            "-t",
            "commit-msg",
            "-t",
            "post-commit",
            "-t",
            "pre-push",
        ]
    )
    sess.run(*["pre-commit", "run", "--all-files"])


@nox.session(python=False)
def tests(sess: Session) -> None:
    """Run the test suite."""
    sess.install("coverage[toml]", "pytest", "pygments")

    def add_quotes_and_join(lst: List[str]) -> str:
        return ",".join([f"{s}" for s in lst])

    omit_paths = ["--omit"] + [
        add_quotes_and_join(pyproject_data["tool"]["coverage"]["run"]["omit"] + [f"{p}/**" for p in submodule_paths])
    ]
    run_paths = [p for p in pyproject_data["tool"]["coverage"]["run"]["source"] if p not in submodule_paths]

    sess.run("coverage", "run", "--parallel", *omit_paths, "-m", "pytest", *run_paths, *sess.posargs)


@nox.session(python=False)
def xdoctest(sess: Session) -> None:
    """Run examples with xdoctest."""
    args = sess.posargs or ["all"]
    sess.install("xdoctest[colors]")
    sess.run("python", "-m", "xdoctest", package, *args)

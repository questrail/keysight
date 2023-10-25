# -*- coding: utf-8 -*-
# Copyright (c) 2013-2022 The keysight developers. All rights reserved.
# Project site: https://github.com/questrail/keysight
# Use of this source code is governed by a MIT-style license that
# can be found in the LICENSE.txt file for the project.
"""Invoke based tasks for keysight
"""

from invoke import run, task
from unipath import Path

ROOT_DIR = Path(__file__).ancestor(1)


@task
def lint(ctx):
    # pylint: disable=W0613
    """Run flake8 to lint code"""
    run("python3 -m flake8")
    run("python3 -m mypy src/")


@task
def freeze(ctx):
    # pylint: disable=W0613
    """Freeze the pip requirements using pip-chill"""
    run(f"pip-chill > {Path(ROOT_DIR, 'requirements.txt')}")


@task(lint)
def test(ctx):
    """Lint, unit test, and check setup.py"""
    run("nose2")


@task
def release(ctx, deploy=False, test=False, version=''):
    """Tag release, run Travis-CI, and deploy to PyPI
    """
    if test:
        run("python3 setup.py check")
        run("python3 setup.py register sdist upload --dry-run")

    if deploy:
        run("python3 setup.py check")
        if version:
            run("git checkout master")
            run("git tag -a v{ver} -m 'v{ver}'".format(ver=version))
            run("git push")
            run("git push origin --tags")
            run("python3 -m build")
            run("python3 -m twine upload dist/*")
    else:
        print("- Have you updated the version?")
        print("- Have you updated CHANGELOG.md?")
        print("- Have you fixed any last minute bugs?")
        print("If you answered yes to all of the above questions,")
        print("then run `invoke release --deploy -vX.YY.ZZ` to:")
        print("- Checkout master")
        print("- Tag the git release with provided vX.YY.ZZ version")
        print("- Push the master branch and tags to repo")
        print("- Deploy to PyPi using Travis")

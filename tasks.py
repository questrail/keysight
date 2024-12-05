# -*- coding: utf-8 -*-
# Copyright (c) 2013-2024 The keysight developers. All rights reserved.
# Project site: https://github.com/questrail/keysight
# Use of this source code is governed by a MIT-style license that
# can be found in the LICENSE.txt file for the project.
"""Invoke based tasks for keysight"""

from invoke import run, task
from unipath import Path

ROOT_DIR = Path(__file__).ancestor(1)


@task
def lint(ctx):
    # pylint: disable=W0613
    """Run ruff and mypy to lint code"""
    run("ruff check src/")
    run("python3 -m mypy src/")


@task
def outdated(ctx):
    """List outdated packages"""
    run("pip list --outdated")


@task
def freeze(ctx):
    # pylint: disable=W0613
    """Freeze the pip requirements using pip-chill"""
    run(f"pip-chill > {Path(ROOT_DIR, 'requirements.txt')}")


@task()
def test(ctx):
    """Run unit tests"""
    run("nose2 -C")


@task
def release(ctx, deploy=False, test=False, version=""):
    """Tag release and deploy to PyPI"""
    if deploy and version:
        run("git checkout master")
        run("git tag -a v{ver} -m 'v{ver}'".format(ver=version))
        run("git push")
        run("git push origin --tags")
        run("hatch build")
        run("hatch publish")
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

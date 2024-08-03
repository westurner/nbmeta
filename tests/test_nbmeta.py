#!/usr/bin/env python

"""Tests for `nbmeta` package."""

import pytest


from nbmeta import nbmeta


@pytest.fixture
def thing():
    yield dict(
        typeof="schema:Thing", name="name1", url="https://localhost/url1"
    )


def test_one_two(thing):
    assert nbmeta
    assert thing
    # assert False, thing

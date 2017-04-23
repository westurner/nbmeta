#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
nbmeta.nodes.html
------------------

"""
from __future__ import print_function

import collections
import json

import dominate
import dominate.util
tags = dominate.tags
from dominate.tags import ( div, h3, code, span, s )
from dominate.util import ( text, raw )

from pygments import highlight
from pygments.lexers import HtmlLexer, JavascriptLexer
from pygments.formatters import HtmlFormatter

__pip_requires__ = ('pygments', 'dominate')


def highlight_html(html):
    return highlight(
        html,
        HtmlLexer(),
        HtmlFormatter(noclasses=True))


class ReprHTMLConf:
    print_html = False
    print_highlight = False


class ReprHTML(object):
    def __init__(self, obj, conf=None):
        self.obj = obj
        self.conf = conf if conf is not None else ReprHTMLConf()

    def __getattr__(self, attr):
        if attr.startswith('_repr'):
            if attr in ReprHTML.__class__.__dict__:
                return object.__getattribute__(self, attr)
        return self.obj.__getattr__(self.obj, attr)

    def _repr_html_(self, obj=None):
        if obj is None:
            obj = self.obj
        if hasattr(obj, '_repr_html_'):
            obj_html = obj._repr_html_()
        if hasattr(obj, 'render'):  # dominate
            obj_html = obj.render()
        #else:
        #    obj_html = obj
        doc = div([
            div([h3('HTML'),
                 text(obj_html, escape=False),
                 #raw(obj_html)
                ]),
            div([h3('HTML (source)'),
                 code(
                     text(obj_html, escape=True))]),
            div([h3('HTML (highlighted)'),
                 text(
                     highlight_html(obj_html),
                     escape=False)])
        ])
        doc_html = doc.render() # XXX: XSS
        if self.conf.print_html:
            if self.conf.print_highlight:
                print(doc_html)
            else:
                print(obj_html)
        return doc_html


def test_reprhtml():
    #ReprHTMLConf.print_html = True
    with div("this") as this:
        this.add(div("that", id="that"))
        div("that2", id="that")
        with tags.ul():
            for n in range(3):
                tags.li(n)
    obj = ReprHTML(this) #.render())
    assert obj
    assert hasattr(obj, '_repr_html_')
    # TODO


class CodeBlock(object):
    def __init__(self, code, fmt='jsonld'):
        self.code = code
        self.fmt = fmt

    def _repr_html_(self, code=None, fmt=None):
        code = code if code is not None else self.code
        fmt = fmt if fmt is not None else self.fmt
        fmts = {
            None: {'lexer': None, 'formatter': None},
            'jsonld': {
                'lexer': JavascriptLexer,
                'formatter': HtmlFormatter(noclasses=True)}}
        _fmt = fmts.get(fmt)
        return highlight(
            code,
            _fmt['lexer'](),
            _fmt['formatter'])

def json_loads(obj, *args, **kwargs):
    kwargs.setdefault('object_pairs_hook', collections.OrderedDict)
    return json.loads(obj, *args, **kwargs)

def json_dumps(obj, *args, **kwargs):
    kwargs.setdefault('indent', 2)
    return json.dumps(obj, *args, **kwargs)


def test_Meta_CodeBlock():
    _jsonldstr = """
        {"@context": {
            "schema": "http://schema.org/",
            "jupyter": "https://jupyter.org/ns/v4/#",
            "_base": "http://localhost:8000/ns/v1#"
        },
        "@type": [
        "jupyter:JupyterNotebook",
        "schema:ScholarlyArticle",
        "schema:DataCatalog"
        ],
        "@id": "http://localhost:8888/notebooks/nb/nbmeta-00-01__exploration.ipynb",
        "name": "Notebook Name",
        "author": [{
        "@type": "schema:Person",
        "givenName": "Wesley",
        "familyName": "Turner",
        "url": "https://westurner.org/"
        }],
        "dateCreated": "2017-01-30",
        "about": [
            {"url": ["https://en.wikipedia.org/wiki/JSONLD"] },
            {"url": "https://pypi.org/project/pipfile/", "name": "Pipfile and Pipfile.lock"}
        ]
    }
    """

    data = {}
    data['objs'] = json_loads(_jsonldstr)

    #ReprHTML(
    m = Meta(
        CodeBlock(_jsonldstr, fmt='jsonld'),
        jsonld=json_dumps(data['objs']))
    print(m.meta['jsonld'])
    m
    return m


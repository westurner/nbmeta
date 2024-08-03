

# from nbmeta.nodes.html import ReprHTML, CodeBlock, json_loads, json_dumps
# from nbmeta.nodes.meta import Meta

from dominate import tags
from nbmeta import (
    CodeBlock, json_loads, json_dumps, Meta,
    ReprHTML, ReprHTMLConf, highlight_html)


def test_ReprHTMLConf():
    ReprHTMLConf.print_html = True
    assert ReprHTMLConf.print_html is True

    # TODO


def test_ReprHTML():

    with tags.div("this") as this:
        this.add(tags.div("that", id="that"))
        tags.div("that2", id="that")
        with tags.ul():
            for n in range(3):
                tags.li(n)

    obj = ReprHTML(this)  # .render())
    assert obj
    assert hasattr(obj, '_repr_html_')
    # TODO


def test_highlight_html():
    output = highlight_html("""
        <html><head><title>title1</head>
        <body><div><p><a href="//index.html">link1</a></p></div></body>
    """)
    assert output, output
    assert '&gt;title1&lt;' in output
    assert '&quot;//index.html&quot;' in output


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
    assert data['objs']

    # ReprHTML()
    m = Meta(
        CodeBlock(_jsonldstr, fmt='jsonld'),
        jsonld=json_dumps(data['objs']))
    print(m.meta['jsonld'])

    assert m
    assert hasattr(m, 'meta')
    assert 'jsonld' in m.meta


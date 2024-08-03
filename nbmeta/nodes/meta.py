#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
nbmeta.nodes.meta
------------------

"""

import html
from dominate import tags

# from collections import OrderedDict
from ..ordereddefaultdict import OrderedDefaultDict
from .html import ReprHTML


class Node(OrderedDefaultDict):
    pass


class Meta(object):
    def __init__(self, obj, meta=None, **kwargs):
        self.obj = obj
        if meta is None:
            meta = Node()
        meta.update(kwargs)  # TODO
        self.meta = meta

    def __getattr__(self, attr):
        if 1: # attr.startswith('_repr'):
            if hasattr(Meta, attr):
                return object.__getattribute__(self, attr)
        return self.obj.__getattribute__(attr)

    def to_html(self):
        typeof = "http://schema.org/CreativeWork http://jupyter/ns#JupyterNotebook"
        typeof = u' '.join(self.meta['@type'])
        with tags.div(typeof=typeof) as doc:
            def metahtml(obj, cur_node):
                with cur_node as _:
                    with tags.ul() as ul_node:
                        if hasattr(obj, 'items'):
                            for key, value in obj.items():
                                with tags.li(property=key) as li_node:
                                    li_node.add(tags.a(key, href=key, property="rdf:Predicate"))
                                    visit_node(value, key, li_node=li_node)
                        #elif hasattr(obj, '__iter__'):
                        #    for value in obj:
                        #        with tags.li() as li_node:
                        #            #a(key, href=value)
                        #            visit_node(value, li_node=li_node)
                        else:
                            #with tags.li() as li_node:
                            visit_node(obj, li_node=ul_node)
                return cur_node

            def visit_node(value, key=None, li_node=None):
                if isinstance(value, str):
                    if value.startswith('http://'):  # TODO: isinstance(URI)
                        tags.a(tags.span(tags.text(value), property=key),
                          href=value,
                          property='rdf:Object')
                    else:
                        tags.span(tags.text(value), property=key)
                elif hasattr(value, 'items'):
                    metahtml(value.items(), li_node)
                # elif isinstance(value, Meta):
                #    metahtml(value.obj, li_node)  # TODO: value.obj ->
                elif hasattr(value, '__iter__'):
                # elif isinstance(value, (list, tuple)):
                    with tags.ul() as _ul_node:
                        with tags.li() as _li_node:
                            # TODO: BUG: XXX
                            # raise Exception(value)
                            for _value in value:
                                # _items = OrderedDict(
                                #    (__value, __value) for __value in _value).items()
                                metahtml(_value, _li_node)  # TODO
                elif hasattr(value, '_repr_html_'):
                    tags.text(value._repr_html_(), escape=False)
                # if isinstance(value, dominator.tag)
                elif hasattr(value, 'render'):
                    tags.text(value.render(), escape=False)
                #TODO: markupsafe __html__ ("?)
                else:
                    raise Exception((type(value), value))

            doc_ = metahtml(self.meta, doc)
        return doc.render()

    def _repr_html_(self):
        obj = self.obj
        # if hasattr(obj, '_repr_nbmeta_')
        if hasattr(obj, '_repr_html_'):
            obj_html = obj._repr_html_()
        elif hasattr(obj, 'render'):
            obj_html = obj.render()
        else:
            obj_html = html.escape(repr(obj))
        assert isinstance(obj_html, str)
        meta_html = self.to_html()
        assert isinstance(meta_html, str)
        return u'\n'.join((obj_html, meta_html))


def test_meta():
    ns = Node()
    schema = ns['@context'] = {
        "url": "http://schema.org/url",
        "author": "http://schema.org/author",
        "givenName": "http://schema.org/givenName",
        "Person": "http://schema.org/Person"
    }
    rdf = ns['rdf'] = {"a": "rdf:type"}
    # ns['@context']['rdf'] = # RDF_URI
    # ns['@context']["a"] = "rdf:type"

    # TODO
    class this:
        @staticmethod
        def render():
            return True

    node = ReprHTML(
        Meta(this.render(),
            meta=Node([
            (schema['url'], "http://localhost:8888/notebooks/nb/...ipynb"),
            (schema['author'], [
                Node([
                    (rdf["a"], schema['Person']),
                    (schema['givenName'], "awesome")
                    # TODO: TST: list
                ]),
            ]),
            ])
        )
    )
    assert node
    assert note.to_html()
    assert node._repr_html_()

    # TODO
    # RreprJSONLD() RDFa

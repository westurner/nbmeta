
# coding: utf-8

# # nbmeta
# * Src: https://github.com/westurner/nbmeta

# In[ ]:




# In[1]:

get_ipython().system(u'pip install zope.interface dominate')


# In[7]:

"""store and IPython.display.display"""
from IPython.display import display, HTML

class DisplayConfig:
    print_obj = True

def _display(obj, **kwargs):
    print_obj = kwargs.get('print_obj', DisplayConfig.print_obj)
    if print_obj: print(obj)
    _obj = obj if hasattr(obj, '_repr_html_') else HTML(repr(obj))
    return display(_obj)


class EmitConfig:
    emit_writefn = staticmethod(_display)
    # emit_writefn = staticmethod(print)
    emit_allowoverwrite = False

_store = None

def get_store(store):
    if store is None:
        global _store
        _store = OrderedDict() if _store is None else _store
        store = _store
    return store

def emit(key=None, obj=None, store=None, writefn=EmitConfig.emit_writefn):
    store = get_store(store)
    key = len(store) if key is None else key
    if EmitConfig.emit_allowoverwrite:
        if key in store:
            raise KeyError((key, 'is already set the store. see emit_allowoverwrite'))
    store[key] = obj
    output = (key, obj)
    writefn(output)
    return output  # return store

def test_emit():
    emit(None, [10 % 12, 10 % 24])
    emit(None, [12 % 10, 24 % 10])
    emit(None, [divmod(10, 12), divmod(10, 24)])
    emit(None, [divmod(12, 10), divmod(24, 10)])

    #assert len(_store) == 4
    #assert list(_store.keys()) == [0, 1, 2, 3]

    # print(json.dumps(_store, indent=2))
    # from pprint import pformat
    # print(pformat(_store))
test_emit()


# In[103]:

import dominate
import dominate.util
tags = dominate.tags
div, h3, code, span, a = tags.div, tags.h3, tags.code, tags.span, tags.a
text, raw = dominate.util.text, dominate.util.raw

# In[]:
def generate_dominate_examples():
    with div("this") as this:
        this.add(div("that", id="that"))
        div("that2", id="that")
        with tags.ul():
            [tags.li(n) for n in range(3)]
    return this

html = generate_dominate_examples()
htmlstr = html.render()

# In[]:

from pygments import highlight
from pygments.lexers import HtmlLexer
from pygments.formatters import HtmlFormatter

def highlight_html(htmlstr):
    """Highlight as HTML pygments
    Args:
        htmlstr (str): HTML to highlight
    Returns:
        str: HTML string highlighted as HTML
    """
    return highlight(
        htmlstr,
        HtmlLexer(),
        HtmlFormatter(noclasses=True))

from zope.interface import Interface, Attribute, implements

class IReprHTML(Interface):
    def _repr_html_(self):
        """Return HTML as a unicode string
        Returns:
            unicode: HTML string
        """
        raise NotImplementedError()


class ReprHTMLConf:
    print_html = False
    print_highlight = False


class ReprHTML(object):
    implements(IReprHTML)

    def __init__(self, obj):
        self.obj = obj

    def __getattr__(self, attr):
        if attr.startswith('_repr'):
            if attr in ReprHTML:
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
        node = div([
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
        node_html = node.render() # XXX: XSS
        if ReprHTMLConf.print_html:
            if ReprHTMLConf.print_highlight:
                print(node_html)
            else:
                print(obj_html)
        return node_html

#ReprHTMLConf.print_html = True
ReprHTML(htmlstr)


# In[104]:


import cgi
from collections import OrderedDict
class Meta(object):
    def __init__(self, obj, meta=None, **kwargs):
        self.obj = obj
        if meta is None:
            meta = OrderedDict()
        meta.update(kwargs)  # TODO
        self.meta = meta

    def __getattr__(self, attr):
        if 1: # attr.startswith('_repr'):
            if hasattr(Meta, attr):
                return object.__getattribute__(self, attr)
        return self.obj.__getattribute__(attr)

    def to_html(self):
        """
        Generate HTML by walking nested nodes

        Returns:
            str: HTML string
        """
        typeof="http://schema.org/CreativeWork http://jupyter/ns#JupyterNotebook"
        with div(typeof=typeof) as doc:
            def metahtml(obj, cur_node):
                with cur_node as doc:
                    with tags.ul() as ul_node:
                        if hasattr(obj, 'items'):
                            for key, value in obj.items():
                                with tags.li(property=key) as li_node:
                                    li_node.add(a(key, href=key, property="rdf:Predicate"))
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
                if isinstance(value, basestring):
                    if value.startswith('http://'):  # TODO: isinstance(URI)
                        a( span(text(value), property=key),
                          href=value,
                          property='rdf:Object')
                    else:
                        span(text(value), property=key)
                elif hasattr(value, 'items'):
                    metahtml(value.items(), li_node)
                #elif isinstance(value, Meta):
                #    metahtml(value.obj, li_node)  # TODO: value.obj ->
                elif hasattr(value, '__iter__'):
                #elif isinstance(value, (list, tuple)):
                    with tags.ul() as _ul_node:
                        with tags.li() as _li_node:
                            # TODO: BUG: XXX
                            #raise Exception(value)
                            for _value in value:
                                #_items = OrderedDict(
                                #    (__value, __value) for __value in _value).items()
                                metahtml(_value, _li_node)  # TODO
                elif hasattr(value, '_repr_html_'):
                    text(value._repr_html_(), escape=False)
                #if isinstance(value, dominator.tag)
                elif hasattr(value, 'render'):
                    text(value.render(), escape=False)
                #TODO: markupsafe __html__ ("?)
                else:
                    raise Exception((type(value), value))

            doc_ = metahtml(self.meta, doc)
        return doc.render()

    def _repr_html_(self):
        return self._objhtml_and_meta_html()

    def _objhtml_and_meta_html(self):
        obj = self.obj
        # if hasattr(obj, '_repr_nbmeta_')
        if hasattr(obj, '_repr_html_'):
            obj_html = obj._repr_html_()
        elif hasattr(obj, 'render'):
            obj_html = obj.render()
        else:
            obj_html = str(obj) #cgi.escape(repr(obj))
        assert type(obj_html) == unicode
        meta_html = self.to_html()
        assert type(meta_html) == unicode
        return u'\n'.join((obj_html, meta_html))


ns = OrderedDict()
schema = ns['@context'] = {
    "url": "http://schema.org/url",
    "author": "http://schema.org/author",
    "givenName": "http://schema.org/givenName",
    "Person": "http://schema.org/Person"
}
rdf = ns['rdf'] = {"a": "rdf:type"}
# ns['@context']['rdf'] = # RDF_URI
# ns['@context']["a"] = "rdf:type"

ReprHTML(
    Meta(this.render(),
        meta=OrderedDict([
         (schema['url'], "http://localhost:8888/notebooks/nb/...ipynb"),
         (schema['author'], [
             OrderedDict([
                 (rdf["a"], schema['Person']),
                 (schema['givenName'], "awesome")
                 # TODO: TST: list
              ]),
         ]),
        ])
    )
)

# TODO
# RreprJSONLD() RDFa


# In[112]:

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
import json
import collections


from pygments import highlight
from pygments.lexers import JavascriptLexer
from pygments.formatters import HtmlFormatter

class CodeBlock(object):
   def __init__(self, code, fmt='jsonld'):
       self.code = code
       self.fmt = fmt

   def _repr_html_(self, *args, **kwargs):
       return self.to_html(*args, **kwargs)

   def to_html(self, code=None, fmt=None):
       code = code if code is not None else self.code
       fmt = fmt if fmt is not None else self.fmt
       fmts = {
           None: {'lexer': None, 'formatter': None},
           'jsonld': {'lexer': JavascriptLexer,
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


# In[]:

def create_jsonld_code_block(jsonldstr):
    """
    Create a
    """
    data = OrderedDict()
    data['objs'] = json_loads(jsonldstr)
    #ReprHTML(
    m = Meta(
        CodeBlock(jsonldstr, fmt='jsonld'),
        jsonld=json_dumps(data['objs']))
    print(m.meta['jsonld'])
    m
create_jsonld_code_block(_jsonldstr)

# In[115]:

"""

Check these off when there are tests:

- [ ] Node
  - [ ] ``@type=Union[URI, List[URI]]``  # JSONLD
  - [ ] type()
  - [ ] types() -> types_expanded()
  - [ ] children=[]
  - [ ] _repr_html_
  - [ ] __repr__
  - [ ] __unicode__
  - [ ] __iter__
    yield node; yield node.children

- [ ] Thing(Node)
  - [ ] name
  - [ ] description
  - [ ] url
- [ ] CreativeWork(Thing)
  - [ ] author
- [ ] ScholarlyArticle(CreativeWork)
- [ ] JupyterNotebook(CreativeWork, [ScholarlyArticle?]  )
- [ ] CodeBlock(Node)
- [ ] Include(Node)('../README.rst')
- [ ] Figure(Node)(obj=plot, data=data, meta={author:, title:})

- [ ] Environment(
- [ ] SoftwareEnvironment "SE" ( https://schema.org/SoftwareApplication Software- )
- [ ] PipRequirements(SE)(txt='../requirements-2.txt'))
- [ ] PipFreeze(SE)(PipRequirements)
- [ ] Pipfile(SE)(pipfile='../Pipfile')
- [ ] PipfileLock(SE)(?='../Pipfile.lock')

- [ ] CondaEnvironment(yml='../environment.yml')

"""



# In[6]:

"""
this_notebook = TODO_GET_HERE()
base URI
 XHTML
 HTML5
https://schema.org/mainEntityOfPage
<>
"""


# In[131]:

''' [ ] how to set the cell metadata? '''
def inspect_gloals():
    sorted(globals().keys())
    ipy = get_ipython()
    emit('ipy.displayhook', ipy.displayhook)
    emit('ipy.filename', ipy.filename)
    instance = ipy.instance()
    emit('ipy.instance()', instance)
    #globals()['celldata'][cell_n] = value
inspect_globals()


# In[ ]:

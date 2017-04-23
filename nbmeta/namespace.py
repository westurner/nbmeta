
from collections import OrderedDict

class Namespace(object):
    def __init__(self, prefix):
        self._prefix = prefix

    @property
    def prefix(self):
        return self._prefix

    def _get(self, attr):
        return "%s%s" % (self.prefix, attr)

    def __getattr__(self, attr):
        return self._get(attr)

    def __getitem__(self, attr):
        return self._get(attr)


class NamespaceDict(OrderedDict):
    def __init__(self, *args, **kwargs):
        if kwargs is None:
            if len(args) == 1:
                iterable = ((ns[0], Namespace(ns[1])) for ns in args)
                args = [iterable]
            else:
                raise Exception()
        else:
            _kwargs = kwargs
            kwargs = ((arg[0], Namespace(arg[1])) for arg in _kwargs.items())
        super(NamespaceDict, self).__init__(*args, **kwargs)

    def __setitem__(self, attr, value):
        _value = Namespace(value)
        return super(NamespaceDict, self).__setitem__(attr, _value)


def build_rdfa11_default_context():
    """
    https://www.w3.org/2013/json-ld-context/rdfa11
    """
    return NamespaceDict((
        ("cat", "http://www.w3.org/ns/dcat#"),
        ("qb", "http://purl.org/linked-data/cube#"),
        ("grddl", "http://www.w3.org/2003/g/data-view#"),
        ("ma", "http://www.w3.org/ns/ma-ont#"),
        ("owl", "http://www.w3.org/2002/07/owl#"),
        ("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#"),
        ("rdfa", "http://www.w3.org/ns/rdfa#"),
        ("rdfs", "http://www.w3.org/2000/01/rdf-schema#"),
        ("rif", "http://www.w3.org/2007/rif#"),
        ("rr", "http://www.w3.org/ns/r2rml#"),
        ("skos", "http://www.w3.org/2004/02/skos/core#"),
        ("skosxl", "http://www.w3.org/2008/05/skos-xl#"),
        ("wdr", "http://www.w3.org/2007/05/powder#"),
        ("void", "http://rdfs.org/ns/void#"),
        ("wdrs", "http://www.w3.org/2007/05/powder-s#"),
        ("xhv", "http://www.w3.org/1999/xhtml/vocab#"),
        ("xml", "http://www.w3.org/XML/1998/namespace"),
        ("xsd", "http://www.w3.org/2001/XMLSchema#"),
        ("prov", "http://www.w3.org/ns/prov#"),
        ("sd", "http://www.w3.org/ns/sparql-service-description#"),
        ("org", "http://www.w3.org/ns/org#"),
        ("gldp", "http://www.w3.org/ns/people#"),
        ("cnt", "http://www.w3.org/2008/content#"),
        ("dcat", "http://www.w3.org/ns/dcat#"),
        ("earl", "http://www.w3.org/ns/earl#"),
        ("ht", "http://www.w3.org/2006/http#"),
        ("ptr", "http://www.w3.org/2009/pointers#"),
        ("cc", "http://creativecommons.org/ns#"),
        ("ctag", "http://commontag.org/ns#"),
        ("dc", "http://purl.org/dc/terms/"),
        ("dc11", "http://purl.org/dc/elements/1.1/"),
        ("dcterms", "http://purl.org/dc/terms/"),
        ("foaf", "http://xmlns.com/foaf/0.1/"),
        ("gr", "http://purl.org/goodrelations/v1#"),
        ("ical", "http://www.w3.org/2002/12/cal/icaltzd#"),
        ("og", "http://ogp.me/ns#"),
        ("rev", "http://purl.org/stuff/rev#"),
        ("sioc", "http://rdfs.org/sioc/ns#"),
        ("v", "http://rdf.data-vocabulary.org/#"),
        ("vcard", "http://www.w3.org/2006/vcard/ns#"),
        ("schema", "http://schema.org/"),
        ("describedby", "http://www.w3.org/2007/05/powder-s#describedby"),
        ("license", "http://www.w3.org/1999/xhtml/vocab#license"),
        ("role", "http://www.w3.org/1999/xhtml/vocab#role"),
    ))

RDFA11_DEFAULT_CONTEXT = None


def _set_default_context():
    global RDFA11_DEFAULT_CONTEXT
    if RDFA11_DEFAULT_CONTEXT is None:
        RDFA11_DEFAULT_CONTEXT = build_rdfa11_default_context()
_set_default_context()


def test_default_context():
    ctx = build_rdfa11_default_context()
    key, value = 'schema', 'http://schema.org/'
    assert ctx.get(key) == value
    assert ctx[key] == value
    assert getattr(ctx, key) == value

    assert ctx == RDF11_DEFAULT_CONTEXT

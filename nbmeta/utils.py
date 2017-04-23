#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
nbmeta.utils
---------------

"""
from __future__ import print_function
from collections import OrderedDict
from IPython.display import display, HTML


def _display(obj, **kwargs):
    if kwargs.get('print_obj', DisplayConfig.print_obj):
        print(obj)
    if hasattr(obj, '_repr_html'):
        _obj = obj
    else:
        _obj = HTML(repr(obj))
    return display(_obj)


class DisplayConfig:
    print_obj = True


class EmitConfig:
    emit_writefn = staticmethod(_display)
    # emit_writefn = staticmethod(print)
    emit_allowoverwrite = False

_STORE = None


def get_store(store):
    if store is None:
        global _STORE
        _STORE = OrderedDict() if _STORE is None else _STORE
        store = _STORE
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


def test_emit_store():
    emit(None, [10 % 12, 10 % 24])
    emit(None, [12 % 10, 24 % 10])
    emit(None, [divmod(10, 12), divmod(10, 24)])
    emit(None, [divmod(12, 10), divmod(24, 10)])
    emit('abc/123', [1, 2, 3, 4])
    assert _STORE['abc/123'] == [1, 2, 3, 4]

    assert len(_STORE) == 5
    assert list(_STORE.keys()) == [0, 1, 2, 3, 'abc/123']

    assert '---' not in _STORE

    # print(json.dumps(_STORE, indent=2))
    # from pprint import pformat
    # print(pformat(_STORE))



def test_todo():
    # ''' [ ] how to set the cell metadata? '''
    sorted(globals().keys())
    ipy = get_ipython()
    emit('ipy.displayhook', ipy.displayhook)
    emit('ipy.filename', ipy.filename)
    instance = ipy.instance()
    emit('ipy.instance()', instance)
    # instance.
    #globals()['celldata'][cell_n] = value


# In[ ]:






def nbmetautil(abc):
    """mainfunc

    Arguments:
        abc (str): ...

    Keyword Arguments:
        abc (str): ...

    Returns:
        str: ...

    Yields:
        str: ...

    Raises:
        Exception: ...
    """
    pass





import unittest


class Test_nbmetautil(unittest.TestCase):

    def setUp(self):
        pass

    def test_nbmetautil(self):
        output = nbmetautil("123")
        self.assertTrue(output)

    def tearDown(self):
        pass


def main(argv=None):
    """
    Main function

    Keyword Arguments:
        argv (list): commandline arguments (e.g. sys.argv[1:])
    Returns:
        int:
    """
    import logging
    import optparse

    prs = optparse.OptionParser(usage="%prog : args")

    prs.add_option('-v', '--verbose',
                   dest='verbose',
                   action='store_true',)
    prs.add_option('-q', '--quiet',
                   dest='quiet',
                   action='store_true',)
    prs.add_option('-t', '--test',
                   dest='run_tests',
                   action='store_true',)


    argv = list(argv) if argv else []
    (opts, args) = prs.parse_args(args=argv)
    loglevel = logging.INFO
    if opts.verbose:
        loglevel = logging.DEBUG
    elif opts.quiet:
        loglevel = logging.ERROR
    logging.basicConfig(level=loglevel)
    log = logging.getLogger()
    log.debug('argv: %r', argv)
    log.debug('opts: %r', opts)
    log.debug('args: %r', args)

    if opts.run_tests:
        import sys
        sys.argv = [sys.argv[0]] + args
        import unittest
        return unittest.main()

    EX_OK = 0
    abc = "123"
    output = nbmetautil(abc)
    return EX_OK


if __name__ == "__main__":
    import sys
    sys.exit(main(argv=sys.argv[1:]))

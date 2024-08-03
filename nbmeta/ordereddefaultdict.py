#!/usr/bin/env python
"""
ordereddefaultdict.OrderedDefaultDict

To test this code:

.. code:: bash

    $ pytest ../tests/test_ordereddefaultdict.py

"""

from collections import OrderedDict

import pprint
import json


class OrderedDefaultDict(OrderedDict):

    def __init__(self, *a, **kw):
        default_factory = kw.pop('default_factory', self.__class__)
        OrderedDict.__init__(self, *a, **kw)
        self.default_factory = default_factory

    def __missing__(self, key):
        self[key] = value = self.default_factory()
        return value

    def pprint(self):
        return pprint.pformat(self)

    def _repr_json_(self, indent=2, **kwargs):
        return json.dumps(self, indent=indent, **kwargs)

    to_json = _repr_json_

    def __str__(self):
        return self.pprint()

    def __repr__(self):
        return "{}({})".format(
            self.__class__.__name__,
            self._repr_json_())


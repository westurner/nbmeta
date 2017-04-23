#!/usr/bin/env python
"""
ordereddefaultdict.OrderedDefaultDict

.. code:: bash

    $ python ./ordereddefaultdict.py -t
    $ nosetests ./ordereddefaultdict.py
    $ py.test ./ordereddefaultdict.py

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


import unittest


class TestOrderedDefaultDict(unittest.TestCase):

    def test_(self):
        x = OrderedDefaultDict()
        TESTVALUE = 0j
        x['a']['1']['A'] = TESTVALUE
        x['b']['2']['B'] = OrderedDefaultDict(
            testvalue=TESTVALUE)
        x['a']['1']['0'] = TESTVALUE
        x['a']['1']['1'] = TESTVALUE
        x['b']['2']['0'] = None
        self.assertEqual(x['a']['1']['A'], TESTVALUE)
        self.assertEqual(x['b']['2']['B'],
                         OrderedDefaultDict(
                             testvalue=TESTVALUE))

        x['a']['1'] = TESTVALUE
        self.assertEqual(x['a']['1'], TESTVALUE)
        # self.assertRaises(KeyError, (lambda: x['a']['1']['0']))
        self.assertRaises(TypeError, (lambda: x['a']['1']['0']))

    def build_OrderedDefaultDict_test_fixture(self):
        x = OrderedDefaultDict()
        x['@context']['schema'] = "http://schema.org/"
        x['@graph'] = [
            {'schema:url': '/url1',
             'schema:name': 'name1',
             'schema:description': 'description'
             }
        ]
        return x

    def setUp(self):
        self.x = self.build_OrderedDefaultDict_test_fixture()

    def test_ordered_default_dict(self):
        x = OrderedDefaultDict()
        x['@context']['schema'] = "http://schema.org/"
        graph = x['@graph'] = [
            {'schema:url': '/url1',
             'schema:name': 'name1',
             'schema:description': 'description'
             }
        ]
        self.assertEqual(graph, x['@graph'])
        print(x)
        self.assertEqual(
            x,
            {"@context": {"schema": "http://schema.org/"},
             "@graph": [{
                 "schema:url": '/url1',
                 "schema:name": 'name1',
                 'schema:description': 'description'}]})
        graph.append(
            {'schema:name': 'name 2',
             'schema:url': '/url2',
             })
        self.assertEqual(graph, x['@graph'])
        print(x)

    def test_OrderedDefaultDict__to_json(self, funcname='to_json'):
        # output_json = self.x.to_json()
        output_json = getattr(OrderedDefaultDict, funcname)(self.x)
        self.assertTrue(output_json)
        self.assertIn('schema:url', output_json)
        output_dict = json.loads(
            output_json,
            object_pairs_hook=OrderedDict)
        self.assertEqual(self.x, output_dict, (output_json, output_dict))
        self.assertDictEqual(self.x, output_dict)
        output_dict2 = json.loads(
            output_json,
            object_pairs_hook=OrderedDefaultDict)
        self.assertEqual(self.x, output_dict2, (output_json, output_dict))
        self.assertDictEqual(self.x, output_dict2)

    def test_OrderedDefaultDict___repr_json_(self):
        return self.test_OrderedDefaultDict__to_json(
            funcname='_repr_json_')

    def test_OrderedDefaultDict___repr__(self):
        output = repr(self.x)
        print(output)
        self.assertTrue(output)
        self.assertIn('schema:url', output)

    def test_OrderedDefaultDict___str__(self):
        output = str(self.x)
        print(output)
        self.assertTrue(output)
        self.assertIn('schema:url', output)


if __name__ == "__main__":
    import sys
    sys.exit(unittest.main())

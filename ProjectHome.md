A JSON parser designed for strict compliance with [RFC 4627](http://www.ietf.org/rfc/rfc4627.txt), built using the PLY (Python Lex-Yacc) library.

Example usage:

```
  >>> import jsonply
  >>> jsonply.parse('{"foo": "bar", "arr": [1, {"a": -2.50e4}, true]}')
  {u'arr': [1, {u'a': -25000.0}, True], u'foo': u'bar'}
```

See the [source code](http://code.google.com/p/json-ply/source/browse/trunk/jsonply.py) and the [test suite](http://code.google.com/p/json-ply/source/browse/trunk/jsonply_test.py) for details.

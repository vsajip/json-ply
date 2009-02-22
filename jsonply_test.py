#!/usr/bin/python2.5
# -*- coding: utf-8 -*-#

# Copyright 2009 DeWitt Clinton All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''Unit tests for the jsonply library.'''

__author__ = 'dewitt@unto.net'

import unittest
import jsonply

class JsonPlyTest(unittest.TestCase):
  '''Tests the module-level jsonply methods.'''

  def testParse(self):
    '''Test the module-level parse method.'''
    actual = jsonply.parse('{"foo": "bar", "arr": [1, {"a": -2.50e4}, true]}')
    self.assertEqual(True, actual['arr'][2])


class JsonParserTest(unittest.TestCase):
  '''Tests the JsonParser methods.'''

  def setUp(self):
    self.parser = jsonply.JsonParser()

#  TODO(dewitt): Capture and check the SyntaxErrors
#  def testEmptyString(self):
#    '''Tests that an invalid empty input returns None.'''
#    actual = self.parser.parse('')
#    self.assertEquals(None, actual)

  def testEmptylist(self):
    '''Tests that an empty list returns [].'''
    actual = self.parser.parse('[]')
    self.assertEquals([], actual)

  def testEmptyDict(self):
    '''Tests that an empty dict returns {}.'''
    actual = self.parser.parse('{}')
    self.assertEquals({}, actual)

  def testLeadingSpace(self):
    '''Tests leading space is ignored.'''
    actual = self.parser.parse('   {}')
    self.assertEquals({}, actual)

  def testLeadingWhitespace(self):
    '''Tests leading whitespace is ignored.'''
    actual = self.parser.parse(' \t \n \r {}')
    self.assertEquals({}, actual)

  def testTrailingSpace(self):
    '''Tests trailing space is ignored.'''
    actual = self.parser.parse('{}  ')
    self.assertEquals({}, actual)

  def testTrailingWhitespace(self):
    '''Tests trailing whitespace is ignored.'''
    actual = self.parser.parse('{} \t \n \r ')
    self.assertEquals({}, actual)

  def testEmbeddedSpace(self):
    '''Tests embedded space is ignored.'''
    actual = self.parser.parse('{   }')
    self.assertEquals({}, actual)

  def testEmbeddedWhitespace(self):
    '''Tests embedded whitespace is ignored.'''
    actual = self.parser.parse('{ \t \n \r }')
    self.assertEquals({}, actual)
    
  def testTrue(self):
    '''Tests that the value for 'true' is parsed.'''
    actual = self.parser.parse('[true]')
    self.assertEquals(True, actual[0])

  def testFalse(self):
    '''Tests that the value for 'false' is parsed.'''
    actual = self.parser.parse('[false]')
    self.assertEquals(False, actual[0])

  def testNull(self):
    '''Tests that the value for 'null' is parsed.'''
    actual = self.parser.parse('[null]')
    self.assertEquals(None, actual[0])

  def testEmptyString(self):
    '''Tests that an empty string is parsed.'''
    actual = self.parser.parse('[""]')
    self.assertEquals('', actual[0])

  def testUnescapedString(self):
    '''Tests that unescaped string sequences are parsed.'''
    actual = self.parser.parse('["abcdefg"]')
    self.assertEquals('abcdefg', actual[0])

  def testLeadingSpaceString(self):
    '''Tests that leading string spaces are parsed.'''
    actual = self.parser.parse('["   a"]')
    self.assertEquals('   a', actual[0])

  def testTrailingSpaceString(self):
    '''Tests that trailing string spaces are parsed.'''
    actual = self.parser.parse('["a   "]')
    self.assertEquals('a   ', actual[0])

  def testEmbeddedSpaceString(self):
    '''Tests that embedded string spaces are parsed.'''
    actual = self.parser.parse('["a   b"]')
    self.assertEquals('a   b', actual[0])

  # TODO(dewitt): Test that embedded whitespaces raise syntax errors

  def testEscapedQuotationMarkString(self):
    '''Tests that escaped quotes are parsed.'''
    actual = self.parser.parse('["\\""]')
    self.assertEquals('"', actual[0])

  def testEscapedReverseSolidusString(self):
    '''Tests that escaped '\\' chars are parsed.'''
    actual = self.parser.parse('["\\\\"]')
    self.assertEquals('\\', actual[0])

  def testEscapedSolidusString(self):
    '''Tests that escaped '/' chars are parsed.'''
    actual = self.parser.parse('["\\/"]')
    self.assertEquals('/', actual[0])

  def testEscapedBackspaceString(self):
    '''Tests that escaped '\\b' chars are parsed.'''
    actual = self.parser.parse('["\\b"]')
    self.assertEquals('\b', actual[0])

  def testEscapedFormFeedString(self):
    '''Tests that escaped '\\f' chars are parsed.'''
    actual = self.parser.parse('["\\f"]')
    self.assertEquals('\f', actual[0])

  def testEscapedCarriageReturnString(self):
    '''Tests that escaped '\\r' chars are parsed.'''
    actual = self.parser.parse('["\\r"]')
    self.assertEquals('\r', actual[0])

  def testEscapedLineFeedString(self):
    '''Tests that escaped '\\t' chars are parsed.'''
    actual = self.parser.parse('["\\t"]')
    self.assertEquals('\t', actual[0])

  def testEscapedTabString(self):
    '''Tests that escaped '\\n' chars are parsed.'''
    actual = self.parser.parse('["\\n"]')
    self.assertEquals('\n', actual[0])

  def testEscapedUnicodeHexAscii(self):
    '''Tests that escaped 'uXXXX' chars are parsed.'''    
    actual = self.parser.parse('["\\u0061"]')
    self.assertEquals('a', actual[0])

  def testEscapedUnicodeHexNonAscii(self):
    '''Tests that an escaped 'イ' character is parsed.'''
    actual = self.parser.parse('["\\u30A4"]')
    self.assertEquals(u'\u30A4', actual[0])

  def testMixedString(self):
    '''Tests that strings containing multiple chars are parsed.'''
    actual = self.parser.parse('[" a\\u30A4b \\r\\u0063 "]')
    self.assertEquals(u' a\u30A4b \rc ', actual[0])

  def testSingleDigitInt(self):
    '''Tests that zero is parsed correctly.'''
    actual = self.parser.parse('[0]')
    self.assertEquals(0, actual[0])

  def testSingleDigitInt(self):
    '''Tests that positive single digit ints are parsed correctly.'''
    actual = self.parser.parse('[1]')
    self.assertEquals(1, actual[0])

  def testMultiDigitInt(self):
    '''Tests that positive multi digit ints are parsed correctly.'''
    actual = self.parser.parse('[123]')
    self.assertEquals(123, actual[0])

  def testSingleDigitNegativeInt(self):
    '''Tests that negative single digit ints are parsed correctly.'''
    actual = self.parser.parse('[-1]')
    self.assertEquals(-1, actual[0])

  def testMultiDigitNegativeInt(self):
    '''Tests that negative multi digit ints are parsed correctly.'''
    actual = self.parser.parse('[-123]')
    self.assertEquals(-123, actual[0])

  def testMultiDigitFloat(self):
    '''Tests that positive multi digit floats are parsed correctly.'''
    actual = self.parser.parse('[123.4]')
    self.assertEquals(123.4, actual[0])

  def testMultiDigitNegativeFloat(self):
    '''Tests that negative multi digit floats are parsed correctly.'''
    actual = self.parser.parse('[-123.4]')
    self.assertEquals(-123.4, actual[0])

  def testIntExponent(self):
    '''Tests that int exponents are parsed correctly.'''
    actual = self.parser.parse('[123e4]')
    self.assertEquals(123e4, actual[0])

  def testIntPositiveExponent(self):
    '''Tests that int positive exponents are parsed correctly.'''
    actual = self.parser.parse('[123e+4]')
    self.assertEquals(123e+4, actual[0])

  def testIntNegativeExponent(self):
    '''Tests that int positive exponents are parsed correctly.'''
    actual = self.parser.parse('[123e-4]')
    self.assertEquals(123e-4, actual[0])

  def testNegativeIntExponent(self):
    '''Tests that negative int exponents are parsed correctly.'''
    actual = self.parser.parse('[-123e4]')
    self.assertEquals(-123e4, actual[0])

  def testNegativeIntPositiveExponent(self):
    '''Tests that negative int positive exponents are parsed correctly.'''
    actual = self.parser.parse('[-123e+4]')
    self.assertEquals(-123e+4, actual[0])

  def testNegativeIntNegativeExponent(self):
    '''Tests that negative int positive exponents are parsed correctly.'''
    actual = self.parser.parse('[-123e-4]')
    self.assertEquals(-123e-4, actual[0])

  def testFloatExponent(self):
    '''Tests that float exponents are parsed correctly.'''
    actual = self.parser.parse('[1.23e4]')
    self.assertEquals(1.23e4, actual[0])

  def testFloatPositiveExponent(self):
    '''Tests that float positive exponents are parsed correctly.'''
    actual = self.parser.parse('[1.23e+4]')
    self.assertEquals(1.23e+4, actual[0])

  def testFloatNegativeExponent(self):
    '''Tests that float negative exponents are parsed correctly.'''
    actual = self.parser.parse('[1.23e-4]')
    self.assertEquals(1.23e-4, actual[0])

  def testNegativeFloatExponent(self):
    '''Tests that negative float exponents are parsed correctly.'''
    actual = self.parser.parse('[-1.23e4]')
    self.assertEquals(-1.23e4, actual[0])

  def testNegativeFloatPositiveExponent(self):
    '''Tests that negative float positive exponents are parsed correctly.'''
    actual = self.parser.parse('[-1.23e+4]')
    self.assertEquals(-1.23e+4, actual[0])

  def testNegativeFloatNegativeExponent(self):
    '''Tests that negative float negative exponents are parsed correctly.'''
    actual = self.parser.parse('[-1.23e-4]')
    self.assertEquals(-1.23e-4, actual[0])

  def testArrayOfStrings(self):
    '''Tests that arrays can contain strings.'''
    actual = self.parser.parse('["a", "b", "c"]')
    self.assertEquals([u'a', u'b', u'c'], actual)

  def testArrayOfNumbers(self):
    '''Tests that arrays can contain strings.'''
    actual = self.parser.parse('[1, 1.2, 3.4e5]')
    self.assertEquals([1, 1.2, 3.4e5], actual)

  def testArrayOfArrays(self):
    '''Tests that arrays can contain arrays.'''
    actual = self.parser.parse('[["a", "b", "c"]]')
    self.assertEquals([[u'a', u'b', u'c']], actual)

  def testArrayOfDicts(self):
    '''Tests that arrays can contain dicts.'''
    actual = self.parser.parse('[{"a": "b"}, {"c": "d"}]')
    self.assertEquals([{'a': 'b'}, {'c': 'd'}], actual)

  def testArrayOfMixedItems(self):
    '''Tests that arrays can contain mixed elements.'''
    actual = self.parser.parse('[1, true, {"a": "b"}, ["c"]]')
    self.assertEquals([1, True, {'a': 'b'}, ['c']], actual)

  def testDictOfStrings(self):
    '''Tests that dicts can contain strings.'''
    actual = self.parser.parse('{"a": "b", "c": "d"}')
    self.assertEquals({'a': 'b', 'c': 'd'}, actual)

  def testDictOfNumbers(self):
    '''Tests that dicts can contain numbers.'''
    actual = self.parser.parse('{"a": 1, "b": 2.3}')
    self.assertEquals({'a': 1, 'b': 2.3}, actual)

  def testDictOfArrays(self):
    '''Tests that dicts can contain arrays.'''
    actual = self.parser.parse('{"a": ["b", "c"], "d": [1, 2.3]}')
    self.assertEquals({'a': ['b', 'c'], 'd': [1, 2.3]}, actual)

  def testDictOfDicts(self):
    '''Tests that dicts can contain dicts.'''
    actual = self.parser.parse('{"a": {"b": "c"}, "d": {"e": "f"}}')
    self.assertEquals({'a': {'b': 'c'}, 'd': {'e': 'f'}}, actual)

  def testDictOfMixedItems(self):
    '''Tests that dicts can contain mixed elements.'''
    actual = self.parser.parse('{"a": true, "b": [1, 2.3], "c": {"d": null}}')
    self.assertEquals({'a': True, 'b': [1, 2.3], 'c': {'d': None}}, actual)


def suite():
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(JsonPlyTest))
  suite.addTests(unittest.makeSuite(JsonParserTest))
  return suite

if __name__ == '__main__':
  unittest.main()




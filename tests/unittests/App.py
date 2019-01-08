# -*- coding: utf-8 -*-
import json

from pytest import fixture

from storyscript.App import App
from storyscript.Bundle import Bundle
from storyscript.parser import Grammar


@fixture
def bundle(patch):
    patch.many(Bundle, ['from_path', 'bundle_trees', 'bundle', 'lex'])


def test_app_parse(bundle):
    """
    Ensures App.parse returns the parsed bundle
    """
    result = App.parse('path')
    Bundle.from_path.assert_called_with('path', ignored_path=None)
    Bundle.from_path().bundle_trees.assert_called_with(ebnf=None, debug=None)
    assert result == Bundle.from_path().bundle_trees()


def test_app_parse_ignored_path(bundle):
    App.parse('path', ignored_path='ignored')
    Bundle.from_path.assert_called_with('path', ignored_path='ignored')


def test_app_parse_ebnf(bundle):
    """
    Ensures App.parse supports specifying an ebnf
    """
    App.parse('path', ebnf='ebnf')
    Bundle.from_path().bundle_trees.assert_called_with(ebnf='ebnf', debug=None)


def test_app_parse_debug(bundle):
    """
    Ensures App.parse can run in debug mode
    """
    App.parse('path', debug=True)
    Bundle.from_path().bundle_trees.assert_called_with(ebnf=None, debug=True)


def test_app_compile(patch, bundle):
    patch.object(json, 'dumps')
    result = App.compile('path')
    Bundle.from_path.assert_called_with('path', ignored_path=None)
    Bundle.from_path().bundle.assert_called_with(ebnf=None, debug=False)
    json.dumps.assert_called_with(Bundle.from_path().bundle(), indent=2)
    assert result == json.dumps()


def test_app_compile_ignored_path(patch, bundle):
    patch.object(json, 'dumps')
    App.compile('path', ignored_path='ignored')
    Bundle.from_path.assert_called_with('path', ignored_path='ignored')


def test_app_compile_ebnf(patch, bundle):
    """
    Ensures App.compile supports specifying an ebnf file
    """
    patch.object(json, 'dumps')
    App.compile('path', ebnf='ebnf')
    Bundle.from_path().bundle.assert_called_with(ebnf='ebnf', debug=False)


def test_app_compile_debug(patch, bundle):
    patch.object(json, 'dumps')
    App.compile('path', debug='debug')
    Bundle.from_path().bundle.assert_called_with(ebnf=None, debug='debug')


def test_app_lex(bundle):
    result = App.lex('/path')
    Bundle.from_path.assert_called_with('/path')
    Bundle.from_path().lex.assert_called_with(ebnf=None)
    assert result == Bundle.from_path().lex()


def test_app_lex_ebnf(bundle):
    App.lex('/path', ebnf='my.ebnf')
    Bundle.from_path().lex.assert_called_with(ebnf='my.ebnf')


def test_app_grammar(patch):
    patch.init(Grammar)
    patch.object(Grammar, 'build')
    assert App.grammar() == Grammar().build()

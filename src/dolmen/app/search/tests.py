# -*- coding: utf-8 -*-

import os.path
import unittest

import doctest
import dolmen.app.search
from zope.testing import module
from zope.app.wsgi.testlayer import BrowserLayer
from zope.security.testing import Principal, Participation
from zope.security.management import newInteraction, endInteraction


def setUp(test):
    participation = Participation(Principal('zope.mgr'))
    newInteraction(participation)


def tearDown(test):
    endInteraction()


def interfaceDescription(interface):
    for name, attr in interface.namesAndDescriptions():
        print "%s: %s" % (name, attr.getDoc())


layer = BrowserLayer(dolmen.app.search)
def test_suite():
    suite = unittest.TestSuite()
    readme = doctest.DocFileSuite(
        'README.txt', setUp=setUp, tearDown=tearDown,
        optionflags=(doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS),
        globs={
            '__name__': 'dolmen.app.search.tests',
            'interfaceDescription': interfaceDescription,
            'getRootFolder': layer.getRootFolder}
        )
    readme.layer = layer
    suite.addTest(readme)
    return suite

# -*- coding: utf-8 -*-

import grokcore.viewlet as grok
from zope.interface import Interface
from zope.component import getAdapter
from dolmen.app.layout import Page, master
from dolmen.app.search import ICatalogSearcher


class Search(grok.Viewlet):
    grok.context(Interface)
    grok.name('search.viewlet')
    grok.viewletmanager(master.DolmenTop)
    grok.order(10)

    def update(self):
        self.term = self.request.form.get('search_term', u'')


class Results(Page):
    grok.context(Interface)
    grok.name('search.result')
    grok.require("dolmen.content.View")

    def update(self):
        searcher = getAdapter(
            self.context, ICatalogSearcher, 'searcher.sitecatalog')
        term = self.request.form.get('search_term', u'')
        self.results = searcher.search(term)
        self.label = u"Found %i results for %s" % (len(self.results), term)

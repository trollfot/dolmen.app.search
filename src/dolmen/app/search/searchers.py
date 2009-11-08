# -*- coding: utf-8 -*-

import grok
from martian import util

from dolmen.app import security
from dolmen.app.search import ICatalogSearcher
from dolmen.app.search import PermissionAwareResultSet

from zope.component import getUtility
from zope.interface import Interface, Attribute, moduleProvides
from zope.app.intid.interfaces import IIntIds
from zope.app.catalog.interfaces import ICatalog


class SiteCatalogSearcher(grok.GlobalUtility):
    grok.name("searcher.sitecatalog")
    grok.implements(ICatalogSearcher)

    @property
    def catalog(self):
        return getUtility(ICatalog)
    
    def search(self, term, index="searchabletext", permission="zope.View"):
        if not len(term):
            return []
        
        results = []
        catalog = self.catalog

        if not index in catalog:
            raise ValueError("Index %r does not exist" % index)

        if util.check_subclass(permission, grok.Permission):
            permission = grok.name.bind().get(permission)

        uidutil = getUtility(IIntIds)
        results = catalog[index].apply(term)
        return PermissionAwareResultSet(results, uidutil, permission)


class ISearchers(Interface):
    """Provided searchers.
    """
    SiteCatalogSearcher = Attribute(
        "ICatalogSearcher querying the application catalog. It verifies "
        "that the current user has the view right (`dolmen.content.View`).")


__all__ = list(ISearchers)

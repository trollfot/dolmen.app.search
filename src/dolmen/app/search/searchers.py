import grokcore.component as grok

from zope.interface import Interface
from zope.component import getUtility
from zope.app.catalog.interfaces import ICatalog
from zope.security.management import checkPermission
from dolmen.app.search import ICatalogSearcher


class SiteCatalogSearcher(grok.Adapter):
    grok.context(Interface)
    grok.provides(ICatalogSearcher)
    grok.name("searcher.sitecatalog")

    @property
    def catalog(self):
        return getUtility(ICatalog)
    
    def search(self, term, exact=False, permission="dolmen.content.View"):
        if not len(term):
            return []
        
        results = []
        catalog = self.catalog

        # using wildcard in the case of a match.
        if exact is not True:
            term = term + "*"
    
        matching = catalog.searchResults(searchabletext = term)
        for result in matching:
            if permission is None or checkPermission(permission, result):
                results.append(result)
        return results

# -*- coding: utf-8 -*-

from zope.schema import Object
from zope.interface import Interface
from zope.app.catalog.interfaces import ICatalog


class ISearcher(Interface):
    """Defines a component designed to seek and retrieve an element.
    """
    def search(term, exact=False, permission="dolmen.content.View"):
        """The main method. It will search the catalog for elements
        matching the term. The search can be exact and the searcher
        can check the validity of a given permission.
        """


class ICatalogSearcher(ISearcher):
    """Defines a specialized searcher using a catalog.
    """
    catalog = Object(
        title = u"Catalog in which the search has to occur.",
        schema = ICatalog,
        required = True
        )

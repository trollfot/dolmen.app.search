# -*- coding: utf-8 -*-

from dolmen.app.search.sets import PermissionAwareResultSet

from dolmen.app.search.interfaces import *
from dolmen.app.search.searchers import *

from zope.interface import moduleProvides
from dolmen.app.search.searchers import ISearchers
from dolmen.app.search.interfaces import ISearchAPI

moduleProvides(ISearchers, ISearchAPI)
__all__ = list(ISearchers) + list(ISearchAPI)

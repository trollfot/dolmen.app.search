=================
dolmen.app.search
=================

`dolmen.app.search` provides components to search objects inside a
Grok application.

Searchers
=========

`dolmen.app.search` introduces a new component : the ISearcher. This
component is dedicated in searching and returning a set of objects,
using a search term.

The provided API is::

  >>> from dolmen.app.search.interfaces import ISearchAPI
  >>> interfaceDescription(ISearchAPI)
  ISearcher: A component dedicated to search
  ICatalogSearcher: A specialized ISearcher querying a catalog


Test environment
----------------

In order to test our searchers, we need an operationnal application
with at least one index.

We prepare out imports::

  >>> import grok
  >>> from grok import index
  >>> from zope.index.text.interfaces import ISearchableText
  >>> from zope.interface import Interface
  >>> from zope.schema import TextLine

We create a model that will be cataloged::

  >>> class IRipper(Interface):
  ...   """A serial killer.
  ...   """
  ...   searchabletext = TextLine(title=u"Name of the ripper")

  >>> class Ripper(grok.Model):
  ...   grok.implements(IRipper)
  ...
  ...   def __init__(self, searchabletext):
  ...     self.searchabletext = searchabletext

We create a Grok application, that will be out site manager::

  >>> class Backstreet(grok.Container, grok.Application):
  ...   """A dark alley.
  ...   """

  >>> grok.testing.grok_component('application', Backstreet)
  True

We define an index that will be the base for our search::

  >>> class RipperIndexes(grok.Indexes):
  ...  grok.site(Backstreet)
  ...  grok.context(IRipper)
  ...  searchabletext = index.Text()

  >>> grok.testing.grok_component('indexes', RipperIndexes)
  True

Now we persist our application and set it as the default site::

  >>> from zope.site.hooks import setSite
  >>> app = Backstreet()
  >>> root = getRootFolder()
  >>> root['berner_street'] = app
 
  >>> setSite(app)

The Grok application has created the catalog::

  >>> from zope.component import getUtility
  >>> from zope.catalog.interfaces import ICatalog
  >>> catalog = getUtility(ICatalog)
  >>> catalog
  <zope.catalog.catalog.Catalog object at ...>

Our index is there::

  >>> catalog['searchabletext']
  <zope.catalog.text.TextIndex object at ...>
  >>> catalog['searchabletext'].documentCount()
  0

Indexing
--------

The catalog is ready. Now, if we create a content and persist it, the
cataloging mechanism will do the work for us::

  >>> jack = Ripper(u"Jack the knife")
  >>> grok.notify(grok.ObjectCreatedEvent(jack))
  >>> app['jack'] = jack

  >>> catalog['searchabletext'].documentCount()
  1

The searchabletext is set. That is what is cataloged in our site catalog::

  >>> jack.searchabletext
  u'Jack the knife'


Searching
---------

An ISearcher can be used as an utility. `dolmen.app.search` provides a
default implementation of an ICatalogSearcher. This component is used
to query the site catalog:: 

  >>> from dolmen.app.search import ICatalogSearcher
  >>> searcher = getUtility(ICatalogSearcher, "searcher.sitecatalog")	
  >>> searcher
  <dolmen.app.search.searchers.SiteCatalogSearcher object at ...>
  >>> searcher.catalog == catalog
  True

The search method of the ICatalogSearcher takes a search term and the
name of the index. By default, it uses the `searchabletext` index::

  >>> result = searcher.search(term="Jack")
  >>> result
  <dolmen.app.search.sets.PermissionAwareResultSet instance at ...>
  >>> list(result)
  [<dolmen.app.search.ftests.Ripper object at ...>]

If we provide a non existing index name, an error is raised::

  >>> result = searcher.search(term="Jack", index="non-existing")
  Traceback (most recent call last):
  ...
  ValueError: Index 'non-existing' does not exist


Wildcard
~~~~~~~~

A wildcard can be given, when searching a text index::

  >>> result = searcher.search("Ja")
  >>> list(result)
  []

  >>> result = searcher.search("Ja*")
  >>> list(result)
  [<dolmen.app.search.ftests.Ripper object at ...>]


Permission
~~~~~~~~~~

By default, our searcher checks the `zope.View` permission on the
objects of the result set. We can provide another permission
explicitly::

  >>> result = searcher.search("knife", permission="i-do-not-exist")
  >>> list(result)
  []

A `grok.Permision` class can be used instead of a string::

  >>> from dolmen.app.security import CanViewContent
  >>> result = searcher.search("knife", permission=CanViewContent)
  >>> list(result)
  [<dolmen.app.search.ftests.Ripper object at ...>]

If permission is set to None, nothing is checked::
   
  >>> result = searcher.search("knife", permission=None)
  >>> list(result)
  [<dolmen.app.search.ftests.Ripper object at ...>]


View and viewlet
================

`dolmen.app.search` comes with two browser components. A search form
viewlet and a result page.

Search viewlet
--------------

A search viewlet is registered to display a search form input. In
order to test the output of the viewlet, we need a view::

  >>> class GasLamp(grok.View):
  ...   """A view where the air's cold and damp
  ...   """
  ...   grok.context(IRipper)

  >>> grok.testing.grok_component('view', GasLamp)
  True

We get the view to render the viewlet:: 
 
  >>> from zope.publisher.browser import TestRequest
  >>> from zope.component import getMultiAdapter

  >>> request = TestRequest()
  >>> view = getMultiAdapter((jack, request), name="gaslamp")

The `Search` viewlet is registered for the `dolmen.app.layout.Top`
manager. We construct this manager::

  >>> from dolmen.app.layout import Top
  >>> manager = Top(jack, request, view)

We can now call, update and render the Search viewlet::

  >>> from dolmen.app.search.browser import Search
  >>> search = Search(jack, request, view, manager)
  >>> search.update()
  >>> print search.render()
  <form id="searchbox" method="post"
        action="http://127.0.0.1/berner_street/search.result">
    <input type="text" autocomplete="off" name="search_term"
           id="search-widget" value="" />
    <input type="submit" name="search_button"
           id="search-button" value="search" />
  </form>


Result page
-----------

The viewlet posts the data to the `search.result` view. This view
fetches the `search_term` from the request, queries the
ICatalogSearcher and displays the results::

  >>> request = TestRequest(form = {'search_term': 'jack'})
  >>> results = getMultiAdapter((jack, request), name="search.result")
  >>> results
  <dolmen.app.search.browser.Results object at ...>

  >>> results.update()
  >>> print results.content()
  <div class="search-result">
    <div class="search-header">
      <h1>Search</h1>
      <h3>Found 1 results for jack</h3>
    </div>
    <dl class="search-results content-listing">
      <dt>
        <a href="http://127.0.0.1/berner_street/jack"
           title="jack">
          <span>jack</span>
        </a>
      </dt>
    </dl>
  </div>

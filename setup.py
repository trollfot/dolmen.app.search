from setuptools import setup, find_packages
from os.path import join

name = 'dolmen.app.search'
version = '0.1'
readme = open(join('src', 'dolmen', 'app', 'search', 'README.txt')).read()
history = open(join('docs', 'HISTORY.txt')).read()

setup(name = name,
      version = version,
      description = 'Dolmen site search',
      long_description = "%s\n\n%s" % (readme, history),
      keywords = 'Grok Zope3 CMS Dolmen',
      author = 'Souheil Chelfouh',
      author_email = 'trollfot@gmail.com',
      url = 'http://gitweb.dolmen-project.org',
      download_url = 'http://pypi.python.org/pypi/dolmen.app.search',
      license = 'GPL',
      packages=find_packages('src', exclude=['ez_setup']),
      package_dir={'': 'src'},
      namespace_packages = ['dolmen', 'dolmen.app'],
      include_package_data = True,
      platforms = 'Any',
      zip_safe = True,
      install_requires=[
          'setuptools',
          'dolmen.app.layout',
      ],
      classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Grok',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
      ],
)

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'homeDictator',
    'author': 'Marco Zuglani',
    'url': '',
    'download_url': '',
    'author_email': 'marco.zugliani@studenti.unitn.it',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['homeDictator'],
    'scripts': [],
    'name': 'homeDictator'
}

setup(**config)
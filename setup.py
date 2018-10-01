# -*- coding: utf-8 -*-
from setuptools import setup

setup(name='data_utils',
      version='1.0',
      description=u"Libreria para manejo",
      author=u'Luis Hernández | Data - San Jorge',
      author_email='lhernandez@amsanjorge.com.ar',
      packages=['data_utils'],
      install_requires=['requests', 'python-dotenv', 'mysqlclient', 'psycopg2', 'pymssql'])
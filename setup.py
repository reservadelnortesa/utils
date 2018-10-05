# -*- coding: utf-8 -*-
from setuptools import setup

setup(name='risk_utils',
      version='1.0',
      description=u"Librería de utilería para riesgos data",
      author=u'Luis Hernández | Data - San Jorge',
      author_email='lhernandez@amsanjorge.com.ar',
      packages=['risk_utils'],
      install_requires=[
            'requests',
            'python-dotenv',
            'mysqlclient',
            'psycopg2',
            'pymssql',
            'python-dotenv',
            'boto3',
            'requests_aws4auth',
            'elasticsearch',
            'dynamodb-json',
            ])
#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
data module
"""
import os
import json

import boto3
import pymssql
import MySQLdb
import psycopg2

from datetime import datetime

from retrying import retry
# https://pypi.org/project/retrying/

# ----

from decimal import Decimal
from requests_aws4auth import AWS4Auth
from dynamodb_json import json_util as json_to_dynamodb
from elasticsearch import Elasticsearch, RequestsHttpConnection

from boto3.dynamodb.conditions import Key

# ----

from . import db_settings as cfg

# ---- 

def show_data_sources():

    sources = {
        'sqlserver_handler': cfg.SQL_SERVER_CONFIG,
        'mysql_handler': cfg.MYSQL_CONFIG,
        'psql_handler': cfg.PSQL_CONFIG
    }

    data_sources = {}
    for engine, server in sources.items():
        data_sources[engine] = {}
        for source, database in server.items():
            data_sources[engine][source] = list(database.keys())

    return data_sources

# ---- SQL

class psql_handler(object):

    class Error(Exception):
        pass
    
    @retry(stop_max_attempt_number=5)
    def __init__(self, server, database):
        try:
            self.connection = psycopg2.connect(
                host=cfg.PSQL_CONFIG[server][database]['host'],
                user=cfg.PSQL_CONFIG[server][database]['user'],
                password=cfg.PSQL_CONFIG[server][database]['password'],
                port=cfg.PSQL_CONFIG[server][database]['port'],
                dbname=cfg.PSQL_CONFIG[server][database]['database'])
            self.cursor = self.connection.cursor()
        except psycopg2.OperationalError as err:
            error_message = 'CONNECTION_ERROR - %s' % err 
            raise self.Error(error_message)
        
    def get_data_by_query(self, query, query_params=None):
        
        if query_params is not None:
            self.cursor.execute(query, query_params)
        else:
            self.cursor.execute(query)
        
        for row in self.cursor:
            yield row
        
    def __del__(self):
        self.connection.close()

class mysql_handler(object):

    def __init__(self, server, database):
        
        self.connection = MySQLdb.connect(
            host=cfg.MYSQL_CONFIG[server][database]['host'],
            user=cfg.MYSQL_CONFIG[server][database]['user'],
            passwd=cfg.MYSQL_CONFIG[server][database]['password'],
            db=cfg.MYSQL_CONFIG[server][database]['database'],
            charset='utf8')
        self.cursor = self.connection.cursor()
        
    def get_data_by_query(self, query, query_params=None):
        
        if query_params is not None:
            self.cursor.execute(query, query_params)
        else:
            self.cursor.execute(query)
        
        for row in self.cursor:
            yield row

    def __del__(self):
        self.connection.close()

class sqlserver_handler(object):
    
    def __init__(self, server, database):
        
        self.connection = pymssql.connect(
            server=cfg.SQL_SERVER_CONFIG[server][database]['host'],
            user=cfg.SQL_SERVER_CONFIG[server][database]['user'],
            password=cfg.SQL_SERVER_CONFIG[server][database]['password'],
            database=cfg.SQL_SERVER_CONFIG[server][database]['database'])
        self.cursor = self.connection.cursor()
        
    def get_data_by_query(self, query, query_params=None):
        
        if query_params is not None:
            self.cursor.execute(query, query_params)
        else:
            self.cursor.execute(query)
        
        for row in self.cursor:
            yield row
        
    def __del__(self):
        self.connection.close()

# ---- NO-SQL

## dynamodb

class dynamodb_handler(object):
    """
    TODO:
        - doc
        - get_document
        - update_document
        - query / scan : [
                from_datetime = datetime(2018, 8, 6, 12, 0, 0).strftime("%Y-%m-%dT%H:%M:%S")
                to_datetime = datetime(2018, 8, 6, 12, 5, 0).strftime("%Y-%m-%dT%H:%M:%S")
                fe = Key('timestamp').between(from_datetime, to_datetime) & \
                    Key('environment').eq('production')
                response = dd.table.scan(FilterExpression=fe)
                data = response['Items']
                while 'LastEvaluatedKey' in response:
                    response = dd.table.scan(FilterExpression=fe,
                                            ExclusiveStartKey=response['LastEvaluatedKey'])
                    data.extend(response['Items'])
            ]
    """

    def __init__(self):

        self.resource = boto3.resource(
            'dynamodb',
            endpoint_url=cfg.AWS_DYNAMODB_ENDPOINT,
            aws_access_key_id=cfg.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=cfg.AWS_SECRET_ACCESS_KEY,
            region_name=cfg.AWS_REGION_NAME)
        
        self.client = boto3.client(
            'dynamodb',
            endpoint_url=cfg.AWS_DYNAMODB_ENDPOINT,
            aws_access_key_id=cfg.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=cfg.AWS_SECRET_ACCESS_KEY,
            region_name=cfg.AWS_REGION_NAME)

    @retry(stop_max_attempt_number=1)
    def save_document(self, raw_doc, table_name):

        doc = json_to_dynamodb.dumps(raw_doc)
        doc = doc.replace('"S": ""', '"NULL": true')
        
        return self.client.put_item(TableName=table_name,
                                    Item=json.loads(doc))


## elasticsearch

class elasticsearch_handler(object):

    def __init__(self):

        if cfg.APP_ENV == 'local':
            self.client = Elasticsearch()

        else:
            awsauth = AWS4Auth(cfg.AWS_ACCESS_KEY_ID,
                               cfg.AWS_SECRET_ACCESS_KEY,
                               cfg.AWS_REGION_NAME,
                               'es')

            self.client = Elasticsearch(
                hosts=cfg.API_ELASTICSEARCH_URL,
                http_auth=awsauth,
                use_ssl=True,
                verify_certs=True,
                connection_class=RequestsHttpConnection)
    
    @retry(stop_max_attempt_number=1)
    def save_document(self, raw_doc, index_name):

        reponse = self.client.index(index=index_name,
                                    doc_type='_doc',
                                    body=raw_doc)
        
        return reponse

# ---- utils

# Helper class to convert a DynamoDB item to JSON. #
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)
# Helper class to convert a DynamoDB item to JSON. #

# Atenea

def get_policy(policy_version):
    """
    @raise: ValueError

    TODO: 
        - doc
        - implementar get_document 'dynamodb_handler'
        - integrar a 'RiskEngine'
    """
    table_name = os.environ.get('API_DDB_POLICY_TBL', '')

    try:
        version = int(policy_version.rsplit('.')[0])
        variation = int(policy_version.rsplit('.')[1])
    except ValueError as err:
        msg = { 'message': 'error getting policy', 'error': err }
        raise ValueError(msg)

    try:
        dy = dynamodb_handler()
        table = dy.resource.Table(table_name)
        response = table.query(
            KeyConditionExpression=Key('version_id').eq(version) & \
                                   Key('sub_version_id').eq(variation))
        raw_policy = json.dumps(response['Items'][0], cls=DecimalEncoder)
        raw_policy = raw_policy.replace('"false"', '"False"')
        raw_policy = raw_policy.replace('"true"', '"True"')
    except BaseException as err:
        msg = { 'message': 'error getting policy', 'error': err }
        raise ValueError(msg)

    return json.loads(raw_policy)

def put_policy(policy, policy_version, start_node=0, force=False):

    # force to update
    if not force: # FIXME: pensar en otro mecanismo mas seguro! 
        # check if exists
        # FIXME: bug cuando la versión no existe... safa con el force :)
        
        try:
            if get_policy(policy_version):
                raise ValueError('policy: %s, already exists.' % policy_version)
        except IndexError:
            pass
    
    version = int(policy_version.rsplit('.')[0])
    variation = int(policy_version.rsplit('.')[1])

    table_name = os.environ.get('API_DDB_POLICY_TBL', '')

    doc = {
        'version_id': version,
        'sub_version_id': variation,
        'start_node': start_node,
        'policy': policy,
        'created_at': datetime.now()
    }

    dy = dynamodb_handler()
    return dy.save_document(raw_doc=doc,
                            table_name=table_name)
    
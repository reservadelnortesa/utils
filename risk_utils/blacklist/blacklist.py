#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
blacklist module
"""
import json
import os
import requests
from datetime import datetime

from dotenv import load_dotenv, find_dotenv 
# https://github.com/theskumar/python-dotenv#installation

# ----

dotenv_path = find_dotenv() 
load_dotenv(dotenv_path)

# ----

class Blacklist(object):

    API_BLACKLIST_TOKEN = os.environ.get('API_BLACKLIST_TOKEN')
    API_BLACKLIST_URL = os.environ.get('API_BLACKLIST_URL')

    class Error(Exception):
        pass

    def is_in_blacklist(self, lead, verbose=False):

        # query string params
        qs_params = (
                        self.API_BLACKLIST_URL,
                        self.API_BLACKLIST_TOKEN,
                        lead.get('unique_identifier', ''),
                        lead.get('phone_number', ''),
                        lead.get('email', ''),
                        lead.get('cbu', '')
                    )
        # url formation
        url = ('%s/api/blacklist?api_token=%s&'
                                'unique_identifier=%s&'
                                'phone_number=%s&'
                                'email=%s&'
                                'cbu=%s') % (qs_params)
        # send request
        try:
            t0 = datetime.now()
            response = requests.get(url)
            t1 = datetime.now()
        except requests.ConnectionError as err:
            error_message = 'CONNECTION_ERROR - %s' % err
            raise self.Error(error_message)
        
        # handle ok response
        if response.status_code == 200:

            is_mutual_customer = False
            # TODO: pasar a else en verbose False case 

            if not verbose:
                return True
            else:
                
                res = json.loads(response.text)
                # TODO: res to raw_data
                
                if res.get('reason', 'missing') == 'SOCIO_MUTUAL':
                    is_mutual_customer = True
                
                
                return  {   
                            'data': {
                                        'is_in_blacklist': True,
                                        'is_mutual_customer': is_mutual_customer, # FIXME: esto no va aqui
                                        'blacklisted_reason': res.get('reason', 'missing'),
                                        'blacklisted_field': res.get('field', None),
                                    },
                            'response_time': t1-t0
                        } 
                # TODO: data and raw_data 
        
        # handle not ok response
        elif response.status_code == 204:
           
            if not verbose:
                return False
            else:
                return  {
                            'data': { 'is_in_blacklist': False },
                            'response_time': t1-t0
                        }
        
        # handle error response
        else:
            error_message = '%s - %s' % (response.status_code, response.text) 
            raise self.Error(error_message)


    def put_in_blacklist(self, lead, reason):

        # query string params
        qs_params = (
                        self.API_BLACKLIST_URL,
                        self.API_BLACKLIST_TOKEN,
                        'riesgos',
                        reason,
                        lead.get('unique_identifier', ''),
                        lead.get('area', ''),
                        lead.get('phone_number', ''),
                        lead.get('email', ''),
                        lead.get('cbu', ''),
                    )
        # url formation
        url = ('%s/api/blacklist?api_token=%s&'
                                'creator=%s&'
                                'reason=%s&'
                                'unique_identifier=%s&'
                                'area=%s&'
                                'phone_number=%s&'
                                'email=%s&'
                                'cbu=%s') % (qs_params)
        # send request
        try:
            t0 = datetime.now()
            response = requests.post(url)
            t1 = datetime.now()
        except requests.ConnectionError as err:
            error_message = { 
                                'error_code': 0,
                                'error_message': err
                            }
            raise self.Error(error_message)

        # handle ok response
        if response.status_code == 201:
            return  { 
                        'created': True,
                        'messsage': json.loads(response.text),
                        'response_time': t1-t0
                    }
        
        # handle error response
        else:
            error_message = { 
                                'error_code': response.status_code,
                                'error_message': response.text
                            }
            raise self.Error(error_message)


    def remove_from_blacklist(self, lead):
        
        # query string params
        qs_params = (
                        self.API_BLACKLIST_URL,
                        self.API_BLACKLIST_TOKEN,
                        lead.get('unique_identifier', ''),
                        lead.get('phone_number', ''),
                        lead.get('email', ''),
                        lead.get('cbu', '')
                    )
        # url formation
        url = ('%s/api/blacklist?api_token=%s&'
                                'unique_identifier=%s&'
                                'phone_number=%s&'
                                'email=%s&'
                                'cbu=%s') % (qs_params)
        # send request
        try:
            t0 = datetime.now()
            response = requests.delete(url)
            t1 = datetime.now()
        except requests.ConnectionError as err:
            error_message = { 
                                'error_code': 0,
                                'error_message': err
                            }
            raise self.Error(error_message)

        # handle ok response
        if response.status_code == 200:
            return { 
                        'removed': True,
                        'messsage': json.loads(response.text),
                        'response_time': t1-t0
                    }
        # handle error response
        else:
            error_message = { 
                                'error_code': response.status_code,
                                'error_message': response.text
                            }
            raise self.Error(error_message)

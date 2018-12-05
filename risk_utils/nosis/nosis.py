#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
nosis module
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

class Nosis(object):

    API_NOSIS_URL = os.environ.get('API_NOSIS_URL')

    class Error(Exception):
        pass

    def is_in_nosis(self, lead, verbose=False):
        
        # query string params
        qs_params = (   
                        self.API_NOSIS_URL,
                        lead.get('identification_number', ''),
                        lead.get('fullname', ''),
                        lead.get('sources', '')
                    )
        
        # url formation
        url =  ('%s/person?identification_number=%s&'
                          'fullname=%s&'
                          'sources=%s') % qs_params
        
        # send request
        try:
            t0 = datetime.now()
            response = requests.get(url)
            t1 = datetime.now()
        except requests.ConnectionError as err:
            error_message = { 
                                'error_code': 0,
                                'error_message': err
                            }
            raise self.Error(error_message)

        # handle ok response
        if response.status_code == 200:

            raw_data = json.loads(response.text).get('data', [])
            if raw_data:

                if not verbose:
                    return True
                else:
                    return  {
                                'data': { 'is_in_nosis': True },
                                'raw_data': raw_data,
                                'response_time': t1-t0
                            }
            else:
                if not verbose:
                    return False
                else:
                    return  {
                                'data': { 'is_in_nosis': False },
                                'response_time': t1-t0
                            }
        
        # handle not ok response
        elif response.status_code == 203:

            if not verbose:
                    return False
            else:
                return  {
                            'data': { 'is_in_nosis': False },
                            'response_time': t1-t0
                        }
        
        # handle error response
        else:

            error_message = { 
                                'error_code': response.status_code,
                                'error_message': response.text
                            }
            raise self.Error(error_message)

    def get_nosis_data(self, lead):
        
        # query string params
        qs_params = (   
                        self.API_NOSIS_URL,
                        lead.get('identification_number'),
                        lead.get('fullname', ''),
                        lead.get('sources', '')
                    )
        # url formation
        url = ('%s/lead?identification_number=%s&'
                       'fullname=%s&'
                       'sources=%s') % qs_params
        # send request
        try:
            t0 = datetime.now()
            response = requests.get(url)
            t1 = datetime.now()
        except requests.ConnectionError as err:
            error_message = { 
                                'error_code': 0,
                                'error_message': err
                            }
            raise self.Error(error_message)
        
        # handle ok response
        if response.status_code == 200:

            # get 'raw_data'
            raw_data = json.loads(response.text)['data']['financialData']['nosis']
            if raw_data:
            
                # get 'nosis_employer_since_in_days'
                employer_since_date = datetime.strptime(raw_data['employer_since'], '%m/%Y').date()
                today_date = datetime.now().date()
                nosis_employer_since_in_days = (today_date - employer_since_date).days
                # set 'data'
                data =  {
                            # OK
                            'is_in_nosis': True,
                            'nosis_currently_inactive': True if raw_data['currently_inactive'] == 1 else False,
                            'nosis_employer_since_in_days': nosis_employer_since_in_days,
                            'nosis_worst_situation_historical': raw_data['worst_situation_historical'],
                            'nosis_socioeconomic_level': raw_data['socioeconomic_level'],
                            'nosis_monotributista': True if raw_data['monotributista'] == 1 else False,
                            'nosis_has_commercial_references': True if raw_data['commercial_references'] == 1 else False,
                            'nosis_region': raw_data['region'],
                            'nosis_has_demand': True if raw_data['has_demand'] == 1 else False,
                            
                            # testing
                            'nosis_age': int(raw_data['age']),
                            'nosis_score': int(raw_data['score']),
                            'nosis_query_count': int(raw_data['query_count']),
                            'nosis_monthly_commitments': float(raw_data['monthly_commitments']),
                            
                            # dummy
                            # TODO: 
                            'nosis_has_bounced_checks': False,
                            'nosis_is_dead': False,

                            # old
                            #'nosis_count': raw_data['query_count'],
                            
                        }
                
                return  {
                            'data': data,
                            'raw_data': raw_data,
                            'response_time': t1-t0
                        }
            
            else:

                return  {
                            'data': { 'is_in_nosis': False },
                            'response_time': t1-t0
                        }

        # handle not ok response
        elif response.status_code == 203:

            return  {
                        'data': { 'is_in_nosis': False },
                        'response_time': t1-t0
                    }
        
        # handle error response
        else:

            error_message = { 
                                'error_code': response.status_code,
                                'error_message': response.text
                            }
            raise self.Error(error_message)

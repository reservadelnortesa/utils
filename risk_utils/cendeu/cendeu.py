#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
cendeu module
"""
import json
import os
import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta


from dotenv import load_dotenv, find_dotenv 
# https://github.com/theskumar/python-dotenv#installation

# ----

dotenv_path = find_dotenv() 
load_dotenv(dotenv_path)

# ----

class Cendeu(object):

    API_CENDEU_TOKEN = os.environ.get('API_CENDEU_TOKEN')
    API_CENDEU_URL = os.environ.get('API_CENDEU_URL')

    class Error(Exception):
        pass

    def is_in_cendeu(self, lead, verbose=False):
        
        # query string params
        qs_params = (
                        self.API_CENDEU_URL,
                        lead.get('unique_identifier', ''),
                        self.API_CENDEU_TOKEN
                    )
        # url formation
        url = '%s/api/cuit/%s?api_token=%s' % qs_params
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

            raw_data = json.loads(response.text).get('debts', [])
            if raw_data:

                # get 'cendeu_worst_situation'

                worst_situation_date = datetime.now().replace(day=1).date() - relativedelta(months=12)
                worst_situation_historical_date = datetime.now().replace(day=1).date() - relativedelta(months=24)
                
                cendeu_worst_situation_list = []
                cendeu_worst_situation_historical_list = []

                for i in raw_data:
                    information_date = datetime.strptime(i['information_date'], '%Y-%m-%d').date()
                    if information_date >= worst_situation_date:
                        cendeu_worst_situation_list.append(i['situation'])
                    if information_date >= worst_situation_historical_date:
                        cendeu_worst_situation_historical_list.append(i['situation'])
                
                cendeu_worst_situation = max(cendeu_worst_situation_list)
                cendeu_worst_situation_historical = max(cendeu_worst_situation_historical_list)

                data =  { 
                            'is_in_cendeu': True,
                            'cendeu_worst_situation': cendeu_worst_situation,
                            'cendeu_worst_situation_historical': cendeu_worst_situation_historical

                        }

                if not verbose:
                    return True
                else:
                    return  {
                                'data': data,
                                'raw_data': raw_data,
                                'response_time': t1-t0
                            }
            
            # ok not ok case:
            else:
                
                if not verbose:
                    return False
                else:
                    return  {
                                'data': { 'is_in_cendeu': False },
                                'response_time': t1-t0
                            }

        # handle not ok response
        elif response.status_code == 204:
            
            if not verbose:
                return False
            else:
                return  {
                            'data': { 'is_in_cendeu': False },
                            'response_time': t1-t0
                        }
        
        # handle error response
        else:
            error_message = '%s - %s' % (response.status_code, response.text) 
            raise self.Error(error_message)

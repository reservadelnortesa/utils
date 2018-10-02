#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
database settings file
"""
import os

from dotenv import load_dotenv, find_dotenv

# ----

dotenv_path = find_dotenv() 
load_dotenv(dotenv_path)

# ----

APP_ENV = os.environ.get('APP_ENV', '')

# ----

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
AWS_REGION_NAME = os.environ.get('AWS_REGION_NAME', '')

# ----

API_ELASTICSEARCH_URL = os.environ.get('API_ELASTICSEARCH_URL', '')

# ----

AWS_DYNAMODB_ENDPOINT = os.environ.get('AWS_DYNAMODB_ENDPOINT', None)

# ---- sqlserver databases config -----------------------------------------------------------------

SQL_SERVER_CONFIG = {
    
    'Riesgos': {

        'RIESGOS_BASE': {
            'host': os.environ.get('DB_RIESGOS_DATA_HOST', ''),
            'user': os.environ.get('DB_RIESGOS_DATA_USER', ''),
            'password': os.environ.get('DB_RIESGOS_DATA_PSWD', ''),
            'database': os.environ.get('DB_RIESGOS_DATA_BASE', '')
        }
    }
}

# ---- mysql databases config ---------------------------------------------------------------------

MYSQL_CONFIG = {

    'Atenea': {

        'RISK_DATA': {
            'host': os.environ.get('WH_HOST', ''),
            'user': os.environ.get('WH_USER', ''),
            'password': os.environ.get('WH_PSWD', ''),
            'port': os.environ.get('WH_PORT', 0),
            'database': os.environ.get('WH_RISKDATA_BASE', '')
        },

        'ATENEA': {
            'host': os.environ.get('WH_HOST', ''),
            'user': os.environ.get('WH_USER', ''),
            'password': os.environ.get('WH_PSWD', ''),
            'port': os.environ.get('WH_PORT', 0),
            'database': os.environ.get('WH_ATENEA_BASE', '')
        }
    },

    'Reserva': {

        'GROU_AR': {
            'host': os.environ.get('DB_GROU_AR_HOST', ''),
            'user': os.environ.get('DB_GROU_AR_USER', ''),
            'password': os.environ.get('DB_GROU_AR_PSWD', ''),
            'port': os.environ.get('DB_GROU_AR_PORT', 0),
            'database': os.environ.get('DB_TRANSFERS_BASE', '')
            },

        'ADEL_AR': {
            'host': os.environ.get('DB_ADEL_AR_HOST', ''),
            'user': os.environ.get('DB_ADEL_AR_USER', ''),
            'password': os.environ.get('DB_ADEL_AR_PSWD', ''),
            'port': os.environ.get('DB_ADEL_AR_PORT', 0),
            'database': os.environ.get('DB_TRANSFERS_BASE', '')
        },

        'CEEA_AR': {
            'host': os.environ.get('DB_CEEA_AR_HOST', ''),
            'user': os.environ.get('DB_CEEA_AR_USER', ''),
            'password': os.environ.get('DB_CEEA_AR_PSWD', ''),
            'port': os.environ.get('DB_CEEA_AR_PORT', 0),
            'database': os.environ.get('DB_TRANSFERS_BASE', '')
        }

    },

    'Otras': {

        'BUREAU': {
            'host': os.environ.get('DB_BUREAU_HOST', ''),
            'user': os.environ.get('DB_BUREAU_USER', ''),
            'password': os.environ.get('DB_BUREAU_PSWD', ''),
            'port': os.environ.get('DB_BUREAU_PORT', 0),
            'database': os.environ.get('DB_TRANSFERS_BASE', '')
        },

        'BLACKLIST': {
            'host': os.environ.get('DB_BLACKLIST_HOST', ''),
            'user': os.environ.get('DB_BLACKLIST_USER', ''),
            'password': os.environ.get('DB_BLACKLIST_PSWD', ''),
            'port': os.environ.get('DB_BLACKLIST_PORT', 0),
            'database': os.environ.get('DB_BLACKLIST_BASE', '')
        },

        'BCRA': {
            'host': os.environ.get('DB_BCRA_HOST', ''),
            'user': os.environ.get('DB_BCRA_USER', ''),
            'password': os.environ.get('DB_BCRA_PSWD', ''),
            'port': os.environ.get('DB_BCRA_PORT', 0),
            'database': os.environ.get('DB_BCRA_BASE', '')
        },

        'TRANSFERS': {
            'host': os.environ.get('DB_TRANSFERS_HOST', ''),
            'user': os.environ.get('DB_TRANSFERS_USER', ''),
            'password': os.environ.get('DB_TRANSFERS_PSWD', ''),
            'port': os.environ.get('DB_TRANSFERS_PORT', 0),
            'database': os.environ.get('DB_TRANSFERS_BASE', '')
        }
    }
}

# ---- postgresql dabases config

PSQL_CONFIG = {

    'Casarsa': {

        'ceferino': {
            'host': os.environ.get('DB_CASARSA_HOST', ''),
            'user': os.environ.get('DB_CASARSA_USER', '') ,
            'password': os.environ.get('DB_CASARSA_PSWD', '') ,
            'port': os.environ.get('DB_CASARSA_PORT', 0),
            'database': 'edb_ceferino'
        },

        'reserva': {
            'host': os.environ.get('DB_CASARSA_HOST', ''),
            'user': os.environ.get('DB_CASARSA_USER', '') ,
            'password': os.environ.get('DB_CASARSA_PSWD', '') ,
            'port': os.environ.get('DB_CASARSA_PORT', 0),
            'database': 'edb_reserva'
        },

        'sanjorge': {
            'host': os.environ.get('DB_CASARSA_HOST', ''),
            'user': os.environ.get('DB_CASARSA_USER', '') ,
            'password': os.environ.get('DB_CASARSA_PSWD', '') ,
            'port': os.environ.get('DB_CASARSA_PORT', 0),
            'database': 'edb_sanjorge_mutual'
        },

        'crediplat': {
            'host': os.environ.get('DB_CASARSA_HOST', ''),
            'user': os.environ.get('DB_CASARSA_USER', '') ,
            'password': os.environ.get('DB_CASARSA_PSWD', '') ,
            'port': os.environ.get('DB_CASARSA_PORT', 0),
            'database': 'edb_crediplat'
        },

        'mexico': {
            'host': os.environ.get('DB_CASARSA_HOST', ''),
            'user': os.environ.get('DB_CASARSA_USER', '') ,
            'password': os.environ.get('DB_CASARSA_PSWD', '') ,
            'port': os.environ.get('DB_CASARSA_PORT', 0),
            'database': 'edb_mpmx'
        }
    }
}

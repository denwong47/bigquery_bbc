import os, sys

import argparse
from concurrent.futures import ThreadPoolExecutor

import extract_http
from dict_tree import DictionaryTree

import load_datawarehouse
from load_datawarehouse.api import google, bigquery
from load_datawarehouse.bigquery import get_bigquery_table, \
                                        load_bigquery_table
import load_datawarehouse.bigquery.schema as schema
# from load_datawarehouse.exceptions import   WarehouseAccessDenied, \
#                                             WarehouseTableNotFound, \
#                                             WarehouseTableGenericError, \
#                                             WarehouseTableRowsInvalid

from main.config import DATA_PATH, \
                        PROJECT_NAME, \
                        DATASET_PRODUCTION, \
                        DATASET_STAGING, \
                        TABLE_PRODUCTION, \
                        TABLE_STAGING, \
                        EXTRACT_RULES



def main(
    args:argparse.Namespace,
):
    hr = lambda : print ("="*100, "\n"*2)

    _extract_config = EXTRACT_RULES.get(args.extract)

    if (_extract_config):
        print (f"Configuration {args.extract} found.")

        if (_extract_config.get("warehouse", None)):
            _table_path = ".".join(
            [
                PROJECT_NAME,
                DATASET_STAGING,
                TABLE_STAGING.format(
                    **_extract_config.get("warehouse", None)
                )
            ])

            print (f"Data will be loaded to {_table_path} on BigQuery.")


            print (f"Performing data extraction...")
            _data = extract_http.extract.extract(_extract_config)
            if (_data):

                hr()

                _data = _data.pop(0)

                print (f"Extracted {len(_data)} records from {args.extract}:")
                # DictionaryTree(_data)

                _client = bigquery.Client()
                _schema = schema.extract(_data)
                print ("Detected schema:")
                DictionaryTree(_schema)

                hr()

                _result = load_bigquery_table(
                    client=_client,
                    table=_table_path,
                    data=_data,
                    schema=_schema
                )
                
                

                print (f"Successfully loaded data from {args.extract}." \
                    if _result \
                        else f"Fail uploading {len(_data)} records due to {type(_result).__name__}: {str(_result)}")
            else:
                print (f"No data extracted. Check config for {args.extract}.")
        else:
            print (f"Configuration {args.extract} not complete; key 'warehouse' expected with 'source' and 'tablename' subkeys.")
    else:
        print ("No --extract option specified. Available configurations are:")
        print (", ".join(EXTRACT_RULES.keys()))
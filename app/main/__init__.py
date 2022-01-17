from modulefinder import Module
import os, sys

import argparse
# from concurrent.futures import ThreadPoolExecutor
from types import ModuleType

import extract_http
from dict_tree import DictionaryTree

import load_datawarehouse
from main.config import PROJECT_NAME, \
                        DATASET_STAGING, \
                        TABLE_STAGING, \
                        EXTRACT_RULES

from main.log import logger

if (isinstance(load_datawarehouse, ModuleType)):
    try:
        from load_datawarehouse.api import google, bigquery
        from load_datawarehouse.bigquery import get_bigquery_table, \
                                                load_bigquery_table
        import load_datawarehouse.bigquery.schema as schema
        # from load_datawarehouse.exceptions import   WarehouseAccessDenied, \
        #                                             WarehouseTableNotFound, \
        #                                             WarehouseTableGenericError, \
        #                                             WarehouseTableRowsInvalid
    except (ImportError, ModuleNotFoundError) as e:
        logger.exception("load_datawarehouse.bigquery did not initialise; check that module google-cloud-bigquery is installed, and environment variable GOOGLE_APPLICATION_CREDENTIALS is set.")
        sys.exit(1)
else:
    logger.critical(f"load_datawarehouse did not import correctly: {str(load_datawarehouse)}")
    sys.exit(1)


def main(
    args:argparse.Namespace,
):
    """
    main()
    Main process for the docker app.

    1. Gets extraction configuration from EXTRACT_RULES[EXTRACT], where EXTRACT is the commmand line argument supplied a run.sh --extract EXTRACT.
    2. Use extract_http.extract.extract() to extract data
    3. Set up BigQuery client
    4. use load_datawarehouse.bigquery to load data into bigquery.

    The table is set using PROJECT_NAME, DATASET_STAGING and TABLE_STAGING in config.py.
    """
    hr = lambda : print ("="*100, "\n"*2)

    _extract_config = EXTRACT_RULES.get(args.extract)

    if (_extract_config):
        logger.info (f"Configuration {args.extract} found.")

        if (_extract_config.get("warehouse", None)):
            _table_path = ".".join(
            [
                PROJECT_NAME,
                DATASET_STAGING,
                TABLE_STAGING.format(
                    **_extract_config.get("warehouse", None)
                )
            ])

            logger.info (f"Data will be loaded to {_table_path} on BigQuery.")


            logger.info (f"Performing data extraction...")
            _data = extract_http.extract.extract(_extract_config)
            if (_data):

                hr()

                _data = _data.pop(0)

                logger.info (f"Extracted {len(_data)} records from {args.extract}.")
                # DictionaryTree(_data)

                _client = bigquery.Client()
                _schema = schema.extract(_data)
                logger.debug (f"Detected schema:\n{DictionaryTree(_schema, echo=False).render()}")

                hr()

                if (not args.skip_load):
                    _result = load_bigquery_table(
                        client=_client,
                        table=_table_path,
                        data=_data,
                        schema=_schema
                    )

                    logger.info (f"Successfully loaded data from {args.extract}." \
                        if _result \
                            else f"Fail uploading {len(_data)} records due to {type(_result).__name__}: {str(_result)}")
                else:
                    logger.info ("skip_load specified; BigQuery Data loading skipped.")
            else:
                logger.warning (f"No data extracted. Check config for {args.extract}.")
        else:
            logger.info (f"Configuration {args.extract} not complete; key 'warehouse' expected with 'source' and 'tablename' subkeys.")
    else:
        _message = f"No --extract option specified. Available configurations are: {repr(list(EXTRACT_RULES.keys()))}"
        logger.warning (_message)
import os, sys
import argparse
import pkg_resources

from load_datawarehouse.api import bigquery

from main import main

def docker_status():
    hr = lambda : print ("="*100, "\n"*2)

    print ("Docker Image active.")
    hr()

    print ("System Information:")
    print (sys.version)
    hr()

    print ("Environment Variables")
    for _key, _value in zip(os.environ, os.environ.values()):
        print (f"{_key:67s}{_value}")
    hr()

    print ("Python Packages")
    print("\n".join([f"{package.project_name:67s}{package.version:20s}{package.location:60s}" for package in pkg_resources.working_set]))
    hr()

    client = bigquery.Client()

    print ("BigQuery Client Projects")
    print (f"{'':2s}PROJECTS:")
    for _pid, _project in enumerate(client.list_projects()):
        print (f"{'':4s}[{_pid:4d}] {_project.friendly_name:56s}{_project.project_id:64s}{_project.numeric_id}")
        print (f"{'':11s}DATASETS:")
        for  _did, _dataset in enumerate(client.list_datasets(_project.project_id)):
            print (f"{'':11s}[{_did:4d}] {_dataset.dataset_id}")
            print (f"{'':18s}TABLES:")
            for _tid, _table in enumerate(client.list_tables(_dataset)):
                _table = bigquery.table.Table(f"{_table.project}.{_table.dataset_id}.{_table.table_id}")
                print (f"{'':18s}[{_tid:4d}] {_table.table_id:42s}{_table.num_rows or 0:,d} rows / {_table.num_bytes or 0:,d} bytes")
        print ("\n")
    client.close()

if (__name__ == "__main__"):
    parser = argparse.ArgumentParser(description="Dockerised Container for loading data to warehouses.")
    parser.add_argument("--docker_status", action="store_true", help="Show docker environment attributes.")
    parser.add_argument("--extract", action="store", type=str, help="Name of configuration to perform extraction with. These settings are declared as a dict as EXTRACT_RULES in config.py.")
    args = parser.parse_args()
    
    _docker_status = args.docker_status

    if (_docker_status):
        docker_status()

    main(args)
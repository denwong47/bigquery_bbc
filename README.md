# bigquery_bbc
 Demonstration Docker image for `extract_http`and `load_datawarehouse` modules:

 `extract_http` https://github.com/denwong47/extract_http \
 `load_warehouse` https://github.com/denwong47/load_datawarehouse

 When run, this container will extract all headlines on bbc.co.uk (Usable only in UK) as well as their thumbnail images as base64, then load the data into a BigQuery table.

 It is intended to be called by a scheduler such as crontab, systemctl timers or Google Cloud Scheduler etc so that headlines can be analysed across time.

 Proof of concept, not designed for production use.


# Installation and Configuration
 ```Readme WIP```

# Execution
```Readme WIP```

# Sample Output
 https://datastudio.google.com/reporting/19c15be7-7fba-43b2-bf55-3205db1fd6fa/page/Cl5iC

# Logging
```Readme WIP```
 
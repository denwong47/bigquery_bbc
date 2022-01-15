DATA_PATH = "/data"

PROJECT_NAME = "bim-manufacturer-metadata"

DATASET_PRODUCTION = "data_manufacturers"
DATASET_STAGING = "data_staging"

TABLE_PRODUCTION = "{source}_{tablename}"
TABLE_STAGING = "{source}_{tablename}"

EXTRACT_RULES = {
  "bbc": {
    "type": "html",
    "url": "https://www.bbc.co.uk",
    "locate": [
      {
        "search_root": [
          'li[class*="-ListItem"]',
        ],
        "values": {
          "article": "span[role='text']$innerText",
          "image_src": "img$attr[src]",
          "link": "a$attr[href]",
        },
        "transform": {
          "image_base64": {
            "source":"{image_src}",
            "embed":"url",
          },
          "extract_timestamp": {
            "source":"%%UTC_ISO",
          }
        }
      }
    ],
    "warehouse": {
        "source": "bbc",
        "tablename": "headlines",
    }
  }
}
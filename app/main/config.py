
# DATA_PATH = "/data"
LOG_PATH = "/log"

# Set to your own project name
PROJECT_NAME = "bim-manufacturer-metadata"

# Define constants for Datasets if required.
# DATASET_PRODUCTION = "data_manufacturers" # Not currently used in the code.
DATASET_STAGING = "data_staging"

# Define constants for Tables if required.
# Table names will be formatted against EXTRACT_RULES[_config]["warehouse"] if found; so f-strings can be used for placeholders.
# TABLE_PRODUCTION = "{source}_{tablename}" # Not currently used in the code.
TABLE_STAGING = "{source}_{tablename}"

# Extract config for extract_http.extract.extract().
# see https://www.github.com/denwong47/extract_http for details.
# main() will look for a EXTRACT_RULES[_key] where _key is passed as the runtime argument --extract.
# e.g. to extract using EXTRACT_RULES["bbc"]
#   ./run.sh --extract bbc
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
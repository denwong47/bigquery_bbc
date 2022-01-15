# Credentials folder
 By default Google Cloud API will look for api-key.json in this folder.

 Change the following line in `Dockerfile` to modify the location:
 ```
    ENV GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/api-key.json
 ```
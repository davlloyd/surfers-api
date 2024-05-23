#! /bin/bash

# Script to generate and publish techdopcs from current directory to gcs
export GOOGLE_APPLICATION_CREDENTIALS=~/gcr.json
export AWS_ACCESS_KEY_ID=Oku06bnS0KwCVdlOX0Wo
export AWS_SECRET_ACCESS_KEY=igllRkqg81iL4O43SgaGtYGQq17ZzTAoXwMkJOQ1
export AWS_REGION=home-sydney
techdocs-cli generate --source-dir . 
techdocs-cli publish --publisher-type awsS3 --storage-name techdocs --entity alpha/Component/surfersapi --awsEndpoint http://minio.home.local:9000


#!/bin/bash
set -e

echo "Invocation de la Lambda sur LocalStack..."

# On appelle la Lambda manuellement
awslocal lambda invoke \
    --function-name business-report-generator \
    --payload '{}' \
    /dev/stdout

echo -e "\n\nVérification du contenu du bucket de sortie..."

awslocal s3 ls s3://report-output-storage/report/

echo -e "\n Fichier csv généré!"
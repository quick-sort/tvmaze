#!/bin/bash

. /app/scripts/.env
curl --header 'Content-Type: application/json' \
    --header "api-key: $API_KEY" \
    --data "{\"date\": \"$(date +%F)\", \"country\": \"US\"}" \
    -X POST -L 'http://127.0.0.1:80/api/jobs'

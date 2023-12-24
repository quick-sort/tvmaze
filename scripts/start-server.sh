#!/bin/bash

printenv | sed 's/^\(.*\)$/export \1/g' | grep -E "^export API_KEY" > /app/scripts/.env
uvicorn app.main:app --host 0.0.0.0 --port 80 $RELOAD

#!/bin/bash
#
ROOT=$(dirname $(dirname $(readlink -f $0)))
SAMPLE_DB=$ROOT/sample.sqlite
export SQLALCHEMY_DATABASE_URI=sqlite:///$SAMPLE_DB
cd $ROOT
export PYTHONPATH=$ROOT
rm $SAMPLE_DB
poetry run python app/job/crawl.py --date=2023-11-26 --country=US

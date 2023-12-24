#!/bin/bash
#
ROOT=$(dirname $(dirname $(readlink -f $0)))
SAMPLE_DB=$ROOT/sample.sqlite
TEST_DB=$ROOT/test.sqlite
cp $SAMPLE_DB $TEST_DB
cd $ROOT
API_KEY=apikey TESTING=yes SQLALCHEMY_DATABASE_URI=sqlite:///$TEST_DB poetry run pytest -o log_cli=true --cov
rm -f $TEST_DB

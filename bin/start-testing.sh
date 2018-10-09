#!/bin/bash

. .venv/bin/activate

export FLASK_ENV=development

python ./marketplace.app/marketplace/test_selenium/run_tests.py

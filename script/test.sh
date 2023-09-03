#!/bin/bash
rm -rf ./htmlcov
pytest -m unit --cov-append
pytest -m integration --cov-append
#!/bin/bash
pip install --prefer-binary -r requirements.txt
python -m spacy download en_core_web_sm --direct

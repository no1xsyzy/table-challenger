#!/bin/sh

datamodel-codegen --input ../json-schemas/gomoku.json --input-file-type jsonschema --output table_challenge_be/models/gomoku.py
datamodel-codegen --input ../json-schemas/user.json --input-file-type jsonschema --output table_challenge_be/models/user.py

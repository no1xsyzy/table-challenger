#!/usr/bin/env node

import fs from 'fs'
import { compile } from 'json-schema-to-typescript'
import $RefParser from '@apidevtools/json-schema-ref-parser'

$RefParser
  .bundle('../json-schemas/user.json')
  .then((x) => compile(x))
  .then((ts) => fs.writeFileSync('src/lib/types/user.d.ts', ts))

$RefParser
  .bundle('../json-schemas/gomoku.json')
  .then((x) => compile(x))
  .then((ts) => fs.writeFileSync('src/lib/types/gomoku.d.ts', ts))

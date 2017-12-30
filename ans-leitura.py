#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import sys
import io
import codecs

PLANOS = json.load(codecs.open('planos_de_saude.json', 'r', 'utf-8'))
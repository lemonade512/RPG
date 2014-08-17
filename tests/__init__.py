#!/usr/bin/env python
import os
from sys import path

def setup_package():
    path.append(os.path.dirname(__file__)+'/..')

def teardown_package():
    pass

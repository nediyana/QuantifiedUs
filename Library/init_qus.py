import sys
import os
import re
import argparse
import operator as op
import pandas as pd
from pandas import Series, DataFrame
import dateutil.parser as dparser
#from lib_init import *
from datetime import *
import numpy as np

def fix_columns(dframe):
    dcols = dframe.columns.values
    dcols[0] = re.sub(r"\W+","",dcols[0])
    dframe.columns = dcols

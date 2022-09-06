import datetime
import glob
import json

import pandas as pd
from dash import html, dcc
import plotly.graph_objs as go

hololivers = glob.glob("../data/light/*.json")
videos_dict = {}

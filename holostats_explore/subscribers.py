import datetime
import glob
import json

import pandas as pd
from dash import html, dcc
import plotly.graph_objs as go

hololivers = glob.glob("../data/light/*.json")
df_dict = {"member": [],
           "date": [],
           "subscribers": []}

for hololiver in hololivers:
    with open(hololiver, "r", encoding="utf-8") as f:
        data_dict = json.load(f)

        monthly_subscribers_stats = {"date": [],
                                     "subscribers": []}
        for year in data_dict["members"].keys():
            for month in data_dict["members"][year].keys():
                date = datetime.datetime(year=int(year), month=int(month), day=1)
                subscribers = data_dict["members"][year][month]["nb-members"]
                df_dict["date"].append(date)
                df_dict["subscribers"].append(subscribers)
                df_dict["member"].append(data_dict["name"])

df = pd.DataFrame.from_dict(df_dict)
fig = go.Figure()
fig.add_trace(go.Scatter(name="Gawr Gura", x=df["date"], y=df["subscribers"]))
fig.add_trace(go.Scatter(name="Sana", x=df["date"], y=df["subscribers"]*0.5))
layout_subscribers = html.Div(
    [
        html.H1("Numbers ehe", className="text-info"),
        html.Hr(),
        html.H3("Subscribers count :"),
        html.P("The following graph shows the number of subscribers having typed at least 1 message in chat for the "
               "corresponding month."),
        html.P("Note that this number is not the ACTUAL number of subscribers, because not every subscriber will type in chat. "
               "However it gives us a MINIMUM and is a pretty good estimate anyway.", className="text-danger"),
        dcc.Graph(figure=fig),

    ]
)

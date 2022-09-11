import datetime
import glob
import json
import math

import numpy as np
import pandas as pd
from dash import html, dcc
import plotly.graph_objs as go
import dash_bootstrap_components as dbc

hololivers = glob.glob("../data/full/*.json")
videos_dict = {"member": []}
for hololiver in hololivers:
    with open(hololiver, "r", encoding="utf-8") as f:
        data_dict = json.load(f)
        member = data_dict["name"]
        videos = data_dict["videos"]
        for video in videos:
            if "comment_count" in video.keys():
                videos_dict["member"].append(member)
                for key, value in video.items():
                    if key not in videos_dict and key!="stats":
                        videos_dict[key] = []
                    videos_dict[key].append(value)
for key, value in videos_dict.items():
    print(key, len(value))
df = pd.DataFrame.from_dict(videos_dict)
df_limited = df[df["member"] == "Gawr Gura"]


def engagement(comment_percent, views, member):
    df_limited = df[df["member"] == member]
    comment_percent_float = [math.log(float(percent)+1) / math.log(float(views ** 2)+1) for percent in
                             df_limited["percent_comment"]]
    min_p = min(comment_percent_float)
    max_p = max(comment_percent_float)
    engagement_rate = np.interp(math.log(float(comment_percent)+1) / math.log(float(views ** 2)+1), [min_p, max_p], [0, 1])
    return engagement_rate


gawr_videos = html.Div(
    [
        dbc.Card([html.Div(style={"height": "auto", "min-width": "20px",
                                  "background": f"rgb({255 - engagement(comment_rate, views, 'Gawr Gura') * 255},{engagement(comment_rate, views, 'Gawr Gura') * 255},{0}"},
                           className="me-1"),
                  html.Img(src=thumbnail_url, style={"height": "30vh", "width": "auto"}, className="me-2"),
                  dbc.Tabs(
                      [
                          dbc.Tab(html.P(description, style={"max-height": "30vh", "overflow-y": "scroll"}),
                                  label="Description"),
                          dbc.Tab(html.Div([html.P(f"Likes : {likes} (engagement : {float(like_rate)}%)"),
                                            html.P(
                                                f"Comments : {comments} (engagement : {float(comment_rate)}%)"),
                                            html.P(f"Views : {views} ({0}% more than median)")]),
                                  label="Statistics"), ]),
                  ],
                 className="d-flex flex-row m-1 p-3") for thumbnail_url,
                                                          description,
                                                          comment_rate,
                                                          like_rate,
                                                          views,
                                                          likes,
                                                          comments in
        zip(df_limited["thumbnail"], df_limited["description"], df_limited["percent_comment"],
            df_limited["percent_like"], df_limited["views"], df_limited["like_count"], df_limited["comment_count"])
    ], className="d-flex flex-column gap-2")
layout_details = html.Div(
    [
        html.H1("Details?", className="text-info"),
        html.Hr(),
        html.H3("Videos : "),
        gawr_videos
    ]
)

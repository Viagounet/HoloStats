from hololiver import Hololiver, Channel
import pandas as pd

df = pd.read_csv('hololivers.csv', sep=';')
hololivers = []
for _, row in df.iterrows():
    hololiver = Hololiver(name=row['name'], channel=Channel(id=row['channel_id']))
    hololiver.save()
    hololivers.append(hololiver)
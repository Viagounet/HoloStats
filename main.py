import time

import pandas as pd
import logging

from user.hololiver import Hololiver
from user.hololivers_managers import HololiversManager
from youtube.channel import Channel

logging.basicConfig(filename='app.log', filemode='a', format='%(asctime)s - %(message)s\n\n\n',
                    datefmt='%d-%b-%y %H:%M:%S')


holo_manager = HololiversManager()

df = pd.read_csv('hololivers.csv', sep=';')
for _, row in df.iterrows():
    try:
        holo_manager.add_hololiver(row['name'], row["channel_id"])
        hololiver = holo_manager.retrieve_hololiver(row["channel_id"])
        hololiver.retrieve_streams()
        hololiver.save()
    except Exception as ex:
        print(f"General exception in main loop : {ex}")
        logging.error(f"General exception in main loop", exc_info=True)
        time.sleep(120)
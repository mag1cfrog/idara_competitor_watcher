import time
from competitor_watcher.data_loading import data_loader

for i in range(10):
    data_loader()
    time.sleep(60)



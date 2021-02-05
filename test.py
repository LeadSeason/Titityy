import os
import time

time = time.time()
modify_time = os.stat("./data.json").st_mtime
time_diff = time - modify_time
print(time_diff)
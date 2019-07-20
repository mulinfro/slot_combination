
import time;
time_start=time.time();#time.time()为1970.1.1到当前时间的毫秒数
i=0;
while i<1000000:
    i+=1
time_end=time.time();#time.time()为1970.1.1到当前时间的毫秒数
print ((time_end-time_start) * 1000)

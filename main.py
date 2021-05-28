#connect to database
from module import Module
import time


count = 0
while True:
  m = Module()
  start_date = m.get_date_eth(count)
  end_date = m.get_date_eth(count+1)
  temp_date = m.get_date_eth(count+2)
  start_block, end_block = m.get_block_eth(start_date, end_date, temp_date)
  data_eth = m.call_api_eth(start_block, end_block)
  
  count+=1
  print(data_eth)
  time.sleep(300)
  
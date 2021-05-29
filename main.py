#connect to database
from module import Module
import time
import datetime

def get_chi_eth(chain_id, count) :
  m = Module()
  start_date = m.get_date_eth(count)
  end_date = m.get_date_eth(count+1)
  temp_date = m.get_date_eth(count+2)
  if start_date < datetime.date.today() :
    start_block, end_block = m.get_block_eth(start_date, end_date, temp_date, chain_id)
    while True :
      try :
        data_eth = m.call_api_eth(start_block, end_block, chain_id)
        break
      except Exception as e :
        print(e)
    to_database = m.process_data_eth(data_eth, chain_id)
  else :
    to_database = []
  return to_database

count = 0
while True:
  data_bsc = get_chi_eth(56, count)
  data_eth = get_chi_eth(1, count)
  count+=1
  time.sleep(60)
  print("done")
  

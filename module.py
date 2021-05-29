import requests
import datetime
import database

class Module:

  def __init__(self) :
    self.base = "https://api.covalenthq.com/v1/"
    self.chain_eth = 1
    self.chain_bsc = 56
    self.contract_address = "0x0000000000004946c0e9F43F4Dee607b0eF1fA1c"
    self.page_size = 999999
    self.day = 16
    self.month = 3
    self.year = 2021
    self.id = "0x0000000000000000000000000000000000000000"

  def get_date_eth(self, count) :
    date = datetime.date(self.year, self.month, self.day) + datetime.timedelta(days=count)
    return date
  
  def get_block_eth(self, start_date, end_date, temp_date, chain_id) :
    url = self.base + "{}/block_v2/{}/{}/".format(chain_id, start_date, end_date)
    r = requests.get(url).json()
    start_block = r['data']['items'][0]['height']
    url = self.base + "{}/block_v2/{}/{}/".format(chain_id, end_date, temp_date)
    r = requests.get(url).json()
    end_block = r['data']['items'][0]['height']
    return start_block, end_block

  def call_api_eth(self, start_block, end_block, chain_id) :
    url = self.base + '{}/events/address/{}/?match={{decoded.name : Transfer}}'.format(chain_id, self.contract_address)
    payload = {"page-size" : self.page_size, "starting-block" : start_block, "ending-block" : end_block}
    r = requests.get(url, params=payload).json()
    return r

  def process_data_eth(self, data, chain_id) :
    results = []
    count = 1
    deleted = False
    print('start again!')
    for i in data['data']['items'] :
      try :
        if deleted :
          results = []
          deleted = False
        tx_hash = i['tx_hash']
        test_start = i['decoded']['params'][0]['value']
        test_end = i['decoded']['params'][1]['value']
        url = self.base + "{}/transaction_v2/{}/".format(chain_id, tx_hash)
        r = requests.get(url).json()
        spent_gas = r['data']['items'][0]['gas_quote']
        if self.id == test_start :
          typed = "minted"
          sign_at = i['block_signed_at']
          address = test_end
          chain = chain_id
          total_chi = i['decoded']['params'][2]['value']
        elif self.id == test_end :
          typed = "burned"
          sign_at = i['block_signed_at']
          address = test_start
          chain = chain_id
          total_chi = i['decoded']['params'][2]['value']
        else :
          typed = "transfered"
          sign_at = i['block_signed_at']
          address = test_start
          chain = chain_id
          total_chi = i['decoded']['params'][2]['value']
        results.append((sign_at, tx_hash, address, typed, chain, spent_gas, total_chi))
        count +=1
        if count == 200 :
          print("oke gan")
          database.insert_to_db(results)
          deleted = True
          count = 1
      except Exception as e : 
        print(e)
    if len(results) != 0 :
      print('oke gan')
      database.insert_to_db(results)
    return results



        

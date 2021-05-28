import requests
import datetime


class Module:

  def __init__(self) :
    self.base = "https://api.covalenthq.com/v1/"
    self.chain_eth = 1
    self.chain_bsc = 56
    self.contract_address = "0x0000000000004946c0e9F43F4Dee607b0eF1fA1c"
    self.page_size = 999999
    self.day = 1
    self.month = 1
    self.year = 2021
    self.id = "0x0000000000000000000000000000000000000000"

  def get_date_eth(self, count) :
    date = datetime.date(self.year, self.month, self.day) + datetime.timedelta(days=count)
    return date
  
  def get_block_eth(self, start_date, end_date, temp_date) :
    url = self.base + "{}/block_v2/{}/{}/".format(self.chain_eth, start_date, end_date)
    r = requests.get(url).json()
    start_block = r['data']['items'][0]['height']
    url = self.base + "{}/block_v2/{}/{}/".format(self.chain_eth, end_date, temp_date)
    r = requests.get(url).json()
    end_block = r['data']['items'][0]['height']
    return start_block, end_block

  def call_api_eth(self, start_block, end_block) :
    url = self.base + '{}/events/address/{}/?match={{decoded.name : Transfer}}'.format(self.chain_eth, self.contract_address)
    payload = {"page-size" : self.page_size, "starting-block" : start_block, "ending-block" : end_block}
    r = requests.get(url, params=payload).json()
    return r

  def process_data_eth(self, data) :
    results = []
    for i in data['data']['items'] :
      temp = []
      test = i['decoded']['params'][0]['value']
      if self.id == test :
        type = "minted"
        
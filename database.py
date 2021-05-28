import pymysql

def connect_to_database() :
  connection = pymysql.connect(host='103.145.227.144', user='akbaridr_gani', password='Jambu21#', db='akbaridr_dnd_1inch', port=3306, cursorclass=pymysql.cursors.DictCursor)
  return connection

def insert_to_db(data) :
  con = connect_to_database()
  cur = con.cursor()
  query = "INSERT INTO `chi` ( `sign_at`, `tx_hash`, `address`, `typed `, `chain`, `spent_gas`, `total_chi`) VALUES (%s,%s,%s,%s,%s,%s,%s)"
  cur.executemany(query, data)
  cur.commit()
  con.close()

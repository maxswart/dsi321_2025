import pandas as pd
MAP_KEY = '5e8bad8d50fa1ca84ea72175e2bace34'

url = 'https://firms.modaps.eosdis.nasa.gov/mapserver/mapkey_status/?MAP_KEY=' + MAP_KEY
try:
  df = pd.read_json(url,  typ='series')
except:
  # possible error, wrong MAP_KEY value, check for extra quotes, missing letters
  print ("There is an issue with the query. \nTry in your browser: %s" % url)
  
# let's create a simple function that tells us how many transactions we have used.
# We will use this in later examples

def get_transaction_count() :
  count = 0
  try:
    df = pd.read_json(url,  typ='series')
    count = df['current_transactions']
  except:
    print ("Error in our call.")
  return count

tcount = get_transaction_count()
print ('Our current transaction count is %i' % tcount)

# let's query data_availability to find out what date range is available for various datasets
# we will explain these datasets a bit later

# this url will return information about all supported sensors and their corresponding datasets
# instead of 'all' you can specify individual sensor, ex:LANDSAT_NRT
da_url = 'https://firms.modaps.eosdis.nasa.gov/api/data_availability/csv/' + MAP_KEY + '/all'
df = pd.read_csv(da_url)

# now let's see how many transactions we use by querying this end point

start_count = get_transaction_count()
pd.read_csv(da_url)
end_count = get_transaction_count()
print ('We used %i transactions.' % (end_count-start_count))

# now remember, after 10 minutes this will reset

# in this example let's look at VIIRS NOAA-20, entire world and the most recent day
area_url = 'https://firms.modaps.eosdis.nasa.gov/api/area/csv/' + MAP_KEY + '/VIIRS_NOAA20_NRT/world/1'
start_count = get_transaction_count()
df_area = pd.read_csv(area_url)
end_count = get_transaction_count()
print ('We used %i transactions.' % (end_count-start_count))


# We can also focus on a smaller area ex. South Asia and get the last 3 days of records
area_url = 'https://firms.modaps.eosdis.nasa.gov/api/area/csv/' + MAP_KEY + '/VIIRS_NOAA20_NRT/54,5.5,102,40/3'
df_area = pd.read_csv(area_url)

countries_url = 'https://firms.modaps.eosdis.nasa.gov/api/countries'
df_countries = pd.read_csv(countries_url, sep=';')

# Let's see last four days MODIS data for Thailand
thai_url = 'https://firms.modaps.eosdis.nasa.gov/api/country/csv/' + MAP_KEY + '/VIIRS_SNPP_NRT/THA/5'
df_thai = pd.read_csv(thai_url)



import datetime

# Ensure "acq_time" is a string, then pad with zeros
df_thai["acq_time"] = df_thai["acq_time"].astype(str).str.zfill(4)

# Convert to HH:MM format
df_thai["acq_time"] = pd.to_datetime(df_thai["acq_time"], format="%H%M").dt.time
# df_thai["acq_time"] = df_thai["acq_time"].apply(lambda x: datetime.datetime.strptime(x, "%H:%M:%S").time())

# Check the result
print(df_thai.dtypes)
print(df_thai["acq_time"].head())  # Display first few converted times

unique_values = df_thai["acq_time"].unique()
print(unique_values)


# import psycopg2

# # connect default db
# pyconn = psycopg2.connect(
#     host='localhost',
#     user='postgres',
#     password='1234567890',
#     database='postgres'
# )


# # cursor
# pgcursor = pyconn.cursor()


# # required code
# from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
# pyconn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

# # drop db
# pgcursor.execute("DROP DATABASE firms_api_db")

# # create db
# pgcursor.execute("CREATE DATABASE firms_api_db")

# # commit
# pgconn.commit()

# # close
# pgconn.close()

from clickhouse_driver import Client

client = Client(host='localhost')
print(client.execute('SHOW DATABASES'))

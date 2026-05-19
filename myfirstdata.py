import pandas as pd
df = pd.read_parquet('2025-01.parquet')
df['readabletime'] = pd.to_datetime(df['timestamp'], unit='ms')
print("Shape:", df.shape)
print("Column names:", df.columns)
print("First 3 rows:")
print(df.head(3))
print("Last 3 rows:")
print(df.tail(3))
print("data types:")

print("Statistics for close price:")
print(df['close'].describe())
df.to_csv('myfirstdata.csv', index=False)

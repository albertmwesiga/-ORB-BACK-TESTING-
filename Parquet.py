
import pandas as pd

# Load the file once
df = pd.read_parquet('2025-01.parquet')

# Convert timestamp to readable time
df['readabletime'] = pd.to_datetime(df['timestamp'], unit='ms')

# Inspect the data
print("Shape:", df.shape)
print("Column names:", df.columns.tolist())
print("First 3 rows:")
print(df.head(3))
print("Last 3 rows:")
print(df.tail(3))
print("Data types:")
print(df.dtypes)
print("Statistics for close price:")
print(df['close'].describe())

# Save to CSV
df.to_csv('January-Bitcoin.csv', index=False)

# prepare for ORB -----

df['date'] = df['readabletime'].dt.date

# Get all unique dates
dates = df['date'].unique()
print("Total trading days in January:", len(dates))

# Pick the first day as an example
first_day = dates[0]
print("Example day:", first_day)



for day in dates:
    day_data = df[df['date'] == day]
    if len(day_data) < 20:
        continue
    first_15 = day_data.head(15)
    range_high = first_15['high'].max()
    range_low = first_15['low'].min()
    print(day, "High:", range_high, "Low:", range_low)

    if later['low'] <= stop_loss:
    exit_price = stop_loss      # i should trigger it here stop loss triggered
    break
elif later['high'] >= take_profit:
    exit_price = take_profit    #  i should it from here take profit triggered only if stop was not hit
    break
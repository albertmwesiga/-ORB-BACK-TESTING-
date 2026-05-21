import pandas as pd
import glob

parquet_path = r'C:\Users\JESUS\Desktop\Royal Trust\Back Testing'
all_files = glob.glob(parquet_path + '/2025-*.parquet')
print(f"Found {len(all_files)} files: {all_files}")

df_list = []
for f in sorted(all_files):
    print(f"Loading {f}...")
    df_temp = pd.read_parquet(f)
    df_list.append(df_temp)

df = pd.concat(df_list, ignore_index=True)
print(f"Total rows (all months combined): {len(df):,}")

df['time'] = pd.to_datetime(df['timestamp'], unit='ms')
df['date'] = df['time'].dt.date

ORB_MINUTES = 15
RR = 2

trades = []

for day in df['date'].unique():
    day_data = df[df['date'] == day].copy()
    if len(day_data) < 20:
        continue

    first_15 = day_data.head(ORB_MINUTES)
    range_high = first_15['high'].max()
    range_low = first_15['low'].min()

    rest = day_data.iloc[ORB_MINUTES:].copy()
    trade_taken = False

    for i in range(len(rest)):
        if trade_taken:
            break

        row = rest.iloc[i]
        price = row['close']

        if price > range_high:
            entry = price
            stop = range_low
            risk = entry - stop
            target = entry + risk * RR
            exit_price = None

            for j in range(i, len(rest)):
                later = rest.iloc[j]
                if later['low'] <= stop:
                    exit_price = stop
                    break
                elif later['high'] >= target:
                    exit_price = target
                    break

            if exit_price is None:
                exit_price = rest.iloc[-1]['close']

            pnl = exit_price - entry
            result = "WIN" if pnl > 0 else "LOSS"
            trades.append([day, "LONG", round(entry, 2), round(
                exit_price, 2), round(pnl, 2), result])
            trade_taken = True

        elif price < range_low:
            entry = price
            stop = range_high
            risk = stop - entry
            target = entry - risk * RR
            exit_price = None

            for j in range(i, len(rest)):
                later = rest.iloc[j]
                if later['high'] >= stop:
                    exit_price = stop
                    break
                elif later['low'] <= target:
                    exit_price = target
                    break

            if exit_price is None:
                exit_price = rest.iloc[-1]['close']

            pnl = entry - exit_price
            result = "WIN" if pnl > 0 else "LOSS"
            trades.append([day, "SHORT", round(entry, 2), round(
                exit_price, 2), round(pnl, 2), result])
            trade_taken = True

if trades:
    trade_sheet = pd.DataFrame(
        trades, columns=['Date', 'Type', 'Entry', 'Exit', 'PnL', 'Result'])
    print("\n===== FIRST 10 TRADES =====")
    print(trade_sheet.head(10))
    print("\n===== SUMMARY =====")
    total = len(trade_sheet)
    wins = len(trade_sheet[trade_sheet['PnL'] > 0])
    losses = len(trade_sheet[trade_sheet['PnL'] < 0])
    win_rate = wins / total * 100
    total_pnl = trade_sheet['PnL'].sum()
    print(f"Total trades: {total}")
    print(f"Wins: {wins}")
    print(f"Losses: {losses}")
    print(f"Win rate: {win_rate:.1f}%")
    print(f"Total PnL: ${total_pnl:,.2f}")
    trade_sheet.to_csv('orb_trades_all_months.csv', index=False)
else:
    print("No trades generated.")

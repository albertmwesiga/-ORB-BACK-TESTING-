import pandas as pd
df = pd.read_parquet(
    r'C:\Users\JESUS\Desktop\Royal Trust\Back Testing\2025-01.parquet')
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
    for idx, row in rest.iterrows():
        if trade_taken:
            break
        price = row['close']
        if price > range_high:
            entry = price
            stop = range_low
            risk = entry - stop
            target = entry + risk * RR
            exit_price = None
            for later_idx, later in rest.loc[idx:].iterrows():
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
            trades.append([day, "LONG", entry, exit_price, pnl, result])
            trade_taken = True
        elif price < range_low:
            entry = price
            stop = range_high
            risk = stop - entry
            target = entry - risk * RR
            exit_price = None
            for later_idx, later in rest.loc[idx:].iterrows():
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
            trades.append([day, "SHORT", entry, exit_price, pnl, result])
            trade_taken = True

if trades:
    trade_sheet = pd.DataFrame(
        trades, columns=['Date', 'Type', 'Entry', 'Exit', 'PnL', 'Result'])
    print("\n===== FIRST 10 TRADES =====")
    print(trade_sheet.head(10))
    print("\n===== SUMMARY =====")
    print(f"Total trades: {len(trade_sheet)}")
    print(f"Wins: {len(trade_sheet[trade_sheet['PnL'] > 0])}")
    print(f"Losses: {len(trade_sheet[trade_sheet['PnL'] < 0])}")
    win_rate = len(trade_sheet[trade_sheet['PnL'] > 0]
                   ) / len(trade_sheet) * 100
    print(f"Win rate: {win_rate:.1f}%")
    print(f"Total PnL: ${trade_sheet['PnL'].sum():,.2f}")
    trade_sheet.to_csv('orb_trades_jan.csv', index=False)
else:
    print("No trades generated.")

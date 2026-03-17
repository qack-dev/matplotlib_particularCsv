import csv
import random
import os
from datetime import datetime, timedelta

def generate():
    # ファイル名 (現在時刻)
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    filename = f"csv/temperature_{timestamp}.csv"

    # ヘッダー
    header = ["time", "実況値"] + [f"{i}時間10分前" for i in range(13)]

    # データ生成範囲
    start = datetime(2026, 3, 16, 0, 0, 0)
    end = datetime(2026, 3, 17, 21, 0, 0)
    
    rows = []
    curr = start

    while curr <= end:
        time_str = curr.strftime("%Y/%m/%d %H:%M:%S")
        # 実況値 (-10.0 から 35.0 の範囲)
        actual = round(random.uniform(-10.0, 35.0), 1)
        
        row = [time_str, actual]
        # 予測誤差 (右に行くほど精度を低く = 絶対値を大きく)
        for i in range(13):
            error_range = 1.0 + (i * 0.5)
            error = round(random.uniform(-error_range, error_range), 1)
            row.append(error)
        
        rows.append(row)
        curr += timedelta(hours=1)

    # 書き出し
    os.makedirs("csv", exist_ok=True)
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

    print(f"Created: {filename}")

if __name__ == "__main__":
    generate()

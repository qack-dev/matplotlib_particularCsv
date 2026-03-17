import sys
import os
import csv
import glob
import matplotlib.pyplot as plt

# 日本語フォントの設定（Windows環境を想定）
plt.rcParams['font.family'] = 'MS Gothic'

def process_csv_file(csv_path, output_dir):
    """個別のCSVファイルを処理してグラフを生成する"""
    data = []
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
    except Exception as e:
        print(f"Error reading CSV {csv_path}: {e}")
        return

    if not data:
        print(f"No data found in {csv_path}.")
        return

    # 横軸のラベル
    x_labels = [f"{i}時間10分前" for i in range(13)]
    
    # 全データの「平均絶対誤差」を計算
    errors = []
    for row in data:
        try:
            # 標準ライブラリのみで平均絶対誤差を算出
            vals = [abs(float(row[label])) for label in x_labels if label in row]
            if vals:
                errors.append(sum(vals) / len(vals))
            else:
                errors.append(0.0)
        except (ValueError, KeyError):
            errors.append(0.0)
    
    # 最大誤差を取得 (0除算を避けるため最低1.0)
    max_error = max(errors) if errors and max(errors) > 0 else 1.0

    # 元のファイル名を取得（拡張子なし）
    base_name = os.path.splitext(os.path.basename(csv_path))[0]

    # 12シリーズごとに分割して描画
    chunk_size = 12
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i + chunk_size]
        chunk_errors = errors[i:i + chunk_size]
        
        plt.figure(figsize=(14, 7))
        
        for idx, row in enumerate(chunk):
            try:
                y_vals = [float(row[label]) for label in x_labels if label in row]
                time_label = row.get('time', f"Row {i+idx}")
                
                # 平均絶対誤差に基づいて透明度(alpha)を計算
                # 誤差が大きいほど薄く（0.15〜1.0の範囲にマッピング）
                error = chunk_errors[idx]
                alpha = max(0.15, 1.0 - (error / max_error * 0.85))
                
                plt.plot(x_labels, y_vals, label=time_label, alpha=alpha, marker='o', linewidth=2)
            except (ValueError, KeyError):
                continue

        # グラフタイトルを削除
        plt.xlabel("予測時間")
        plt.ylabel("誤差 (予測値 - 実況値)")
        plt.axhline(0, color='black', linewidth=1, linestyle='-') # 0の基準線
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='x-small')
        plt.xticks(rotation=45)
        plt.tight_layout()

        # ファイル名の生成
        graph_num = (i // chunk_size) + 1
        output_filename = f"{base_name}_graph_{graph_num:02d}.png"
        save_path = os.path.join(output_dir, output_filename)
        
        plt.savefig(save_path)
        plt.close()
        print(f"Generated: {save_path}")

def main(csv_dir, output_dir):
    """ディレクトリ内の全CSVファイルを処理する"""
    if not os.path.isdir(csv_dir):
        print(f"Error: {csv_dir} is not a directory.")
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # フォルダ内のすべてのCSVファイルを取得（拡張子 .csv）
    csv_dir_abs = os.path.abspath(csv_dir)
    csv_files = glob.glob(os.path.join(csv_dir_abs, "*.csv"))
    
    if not csv_files:
        print(f"No CSV files found in {csv_dir_abs}.")
        return

    print(f"Found {len(csv_files)} CSV files in {csv_dir_abs}. Processing...")
    for csv_path in csv_files:
        process_csv_file(csv_path, output_dir)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python makeGraphWithCsv.py <csv_dir> <output_dir>")
    else:
        main(sys.argv[1], sys.argv[2])

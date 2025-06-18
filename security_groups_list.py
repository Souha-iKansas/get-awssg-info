import json
import csv
import argparse

def extract_group_ids(json_path, csv_path):
    # JSONの読み込み
    with open(json_path, 'r') as f:
        data = json.load(f)

    # GroupIdの抽出
    group_ids = [sg['GroupId'] for sg in data.get('SecurityGroups', [])]

    # CSVに書き出し
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['GroupId'])  # ヘッダー
        for gid in group_ids:
            writer.writerow([gid])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract GroupId from JSON and output to CSV')
    parser.add_argument('json_file', help='Path to input JSON file')
    parser.add_argument('csv_file', help='Path to output CSV file')

    args = parser.parse_args()
    extract_group_ids(args.json_file, args.csv_file)
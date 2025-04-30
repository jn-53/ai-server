import csv
import json


def convert_csv_to_json(csv_filename, json_filename):
    data = {}

    # 打开CSV文件
    with open(csv_filename, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # ⚡ 跳过表头
        for row in reader:
            if len(row) < 8:
                continue  # 忽略格式不对的行

            district_id = int(row[0])
            province = row[1]
            city = row[2]
            city_id = int(row[3])
            district = row[4]
            e = float(row[6])
            n = float(row[7])

            item = {
                "district_id": district_id,
                "city_id": city_id,
                "e": e,
                "n": n,
            }
            data[f"{province}-{city}-{district}"] = item

    # 保存成JSON文件
    with open(json_filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, ensure_ascii=False, indent=4)

    print(f"✅ 已成功将 {csv_filename} 转换为 {json_filename}")


if __name__ == "__main__":
    # 使用示例
    csv_file = 'weather_district_id.csv'  # 替换成你的CSV文件名
    json_file = 'weather_district_id.json'
    convert_csv_to_json(csv_file, json_file)

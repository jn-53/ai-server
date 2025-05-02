import json
import time

import Levenshtein

# === 配置 ===
JSON_FILE = 'weather_district_id.json'  # 你的行政区json文件名


# === 步骤1：加载JSON数据 ===
def load_locations(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    locations = []
    for key, value in data.items():
        # 补充fullname字段（没有就生成）
        if 'fullname' not in value:
            fullname = key.replace('-', '')
            value['fullname'] = fullname
        locations.append(value)
    return locations


# === 步骤2：根据输入地名，找最相近的行政区 ===
# def best_match(input_name, locations):
#     best_score = float('inf')
#     best_location = None
#     for loc in locations:
#         fullname = loc.get("fullname", "")
#         score = Levenshtein.distance(input_name, fullname)
#         if score < best_score:
#             best_score = score
#             best_location = loc
#     return best_location, best_score
def best_match(input_name, locations, threshold=0.25):
    best_score = -1  # Jaccard越大越好
    best_location = None

    input_parts = input_name.split()  # 将输入分词，使用空格作为分隔符（可以调整分词规则）

    for loc in locations:
        fullname = loc.get("fullname", "")
        
        # 计算Jaccard相似度，遍历输入和行政区的全名
        score = 0
        for part in input_parts:
            score += smart_jaccard_similarity(part, fullname)
        
        # 可以选择加权或者调整分数的计算方式
        score /= len(input_parts)  # 平均相似度

        if score > best_score:
            best_score = score
            best_location = loc

    if best_score < threshold:  # 如果得分太低，认为没匹配到
        return None, best_score
    return best_location, best_score



def jaccard_similarity(str1, str2):
    set1 = set(str1)
    set2 = set(str2)
    intersection = len(set1 & set2)  # 交集
    union = len(set1 | set2)          # 并集
    if union == 0:
        return 0.0
    return intersection / union


def smart_jaccard_similarity(str1, str2):
    # 字符集级Jaccard
    set1 = set(str1)
    set2 = set(str2)
    char_intersection = len(set1 & set2)
    char_union = len(set1 | set2)
    char_score = char_intersection / char_union if char_union else 0.0

    # 简单词切分（以常见行政区单位）
    def split_words(s):
        words = []
        tmp = ''
        for ch in s:
            tmp += ch
            if ch in ('省', '市', '区', '县', '州', '盟', '镇', '乡'):
                words.append(tmp)
                tmp = ''
        if tmp:
            words.append(tmp)
        return words

    word_set1 = split_words(str1)
    word_set2 = split_words(str2)
    word_intersection = len(set(word_set1) & set(word_set2))
    word_union = len(set(word_set1) | set(word_set2))
    word_score = word_intersection / word_union if word_union else 0.0

    # 取最大得分
    base_score = max(char_score, word_score)

    # 如果短输入是长输入的子串，加额外奖励
    if str1 in str2:
        bonus = 0.3  # 额外奖励分
    else:
        bonus = 0.0

    final_score = min(base_score + bonus, 1.0)  # 最多不超过1
    return final_score



# === 主程序 ===
def main():
    locations = load_locations(JSON_FILE)
    print("=== 智能天气行政区查询 ===")

    while True:
        user_input = input("请输入想查询的地名（输入q退出）：").strip()
        if user_input.lower() == 'q':
            break
        if not user_input:
            continue

        start_time = time.time()  # 开始计时
        match, score = best_match(user_input, locations)
        end_time = time.time()  # 结束计时

        elapsed_ms = (end_time - start_time) * 1000  # 转成毫秒

        if match:
            print(f"最接近的行政区：{match['fullname']}（district_id: {match['district_id']}）")
            print(f"对应经纬度：({match['n']}, {match['e']})")
            print(f"匹配得分（越大越好）：{score:.4f}")
            print(f"匹配耗时：{elapsed_ms:.2f}ms")
        else:
            print("未找到匹配项。（得分太低）")
            print(f"匹配得分：{score:.4f}")
            print(f"匹配耗时：{elapsed_ms:.2f}ms")



if __name__ == '__main__':
    main()

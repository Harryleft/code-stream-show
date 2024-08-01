import csv
import json
import chardet


def detect_encoding(file_path):
    """
    Detect the encoding of a given file.

    Args:
        file_path (str): The path to the file whose encoding is to be detected.

    Returns:
        str: The detected encoding of the file.
    """
    with open(file_path, 'rb') as file:
        raw = file.read()
    return chardet.detect(raw)['encoding']


def csv_to_json(csv_file_path, json_file_path):
    """
    Convert a CSV file to a JSON file.

    The CSV file is expected to have columns '章节' (chapter), '知识点' (knowledge point),
    and '知识点详情' (details). The resulting JSON file will be structured with chapters
    as keys, and each chapter containing knowledge points and their details.

    Args:
        csv_file_path (str): The path to the input CSV file.
        json_file_path (str): The path to the output JSON file.
    """
    # 检测文件编码
    file_encoding = detect_encoding(csv_file_path)

    # 创建字典来存储结果
    result = {}

    # 读取 CSV文件
    with open(csv_file_path, 'r', encoding=file_encoding) as csv_file:
        csv_reader = csv.DictReader(csv_file)

        # 遍历 CSV 的每一行
        for row in csv_reader:
            chapter = row['章节']
            knowledge_point = row['知识点']
            details = row['知识点详情']

            # 如果章节不在结果字典中，添加它
            if chapter not in result:
                result[chapter] = {}

            # 将知识点和详情添加到对应的章节中
            result[chapter][knowledge_point] = details

    # 将结果写入JSON文件
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(result, json_file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    knowledge_points_csv_file = '667信息管理导论.csv'
    knowledge_points_json_file = '667_knowledge_points.json'
    csv_to_json(knowledge_points_csv_file, knowledge_points_json_file)
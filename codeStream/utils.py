import json


def load_knowledge(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            points = json.load(file)
        print(f"成功加载 {len(points)} 个知识点")
        return points
    except Exception as e:
        print(f"加载文件时出错: {e}")
        return {"Python": "一种编程语言", "人工智能": "模拟人类智能的技术", "数据结构": "组织和存储数据的方式"}
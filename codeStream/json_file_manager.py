import json
from tkinter import filedialog, messagebox


class JsonFileManager:
    def __init__(self, root):
        self.root = root

    def select_json_file(self):
        """
        用户自定义选择JSON文件
        :return:
        """
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    if self.validate_json_structure(data):
                        return data
                    else:
                        raise ValueError("JSON文件格式不正确, 请确保格式正确, 例如: {'章节1': {'知识点1': '详情1'}}")
            except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
                messagebox.showerror("错误", f"{str(e)}")
        return None

    def validate_json_structure(self, data):
        """
        验证用户上传的JSON文件结构是否正确
        :param data:
        :return:
        """
        if not isinstance(data, dict):
            return False
        for chapter, knowledge_points in data.items():
            if not isinstance(knowledge_points, dict):
                return False
            for point, detail in knowledge_points.items():
                if not isinstance(point, str) or not isinstance(detail, str):
                    return False
        return True


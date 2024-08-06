import json
from tkinter import filedialog, messagebox


class JsonFileManager:
    """A class to manage JSON file operations, including selecting and validating JSON files."""

    def __init__(self, root):
        """
        Initialize the JsonFileManager with a root Tkinter window.

        Args:
            root (tk.Tk): The root Tkinter window.
        """
        self.root = root

    def select_json_file(self):
        """
        Allow the user to select a JSON file and validate its structure.

        Returns:
            dict: The loaded JSON data if the file is valid, otherwise None.
        """
        # Open a file dialog to select a JSON file
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                # Read and load the JSON file
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    # Validate the JSON structure
                    if self.validate_json_structure(data):
                        return data
                    else:
                        raise ValueError("JSON文件格式不正确, 请确保格式正确, 例如: {'章节1': {'知识点1': '详情1'}}")
            except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
                # Show an error message if the file is not found or JSON is invalid
                messagebox.showerror("错误", f"{str(e)}")
        return None

    def validate_json_structure(self, data):
        """
        Validate the structure of the JSON data.

        Args:
            data (dict): The JSON data to validate.

        Returns:
            bool: True if the structure is valid, otherwise False.
        """
        # Check if the data is a dictionary
        if not isinstance(data, dict):
            return False
        # Iterate over each chapter and knowledge point to validate their types
        for chapter, knowledge_points in data.items():
            if not isinstance(knowledge_points, dict):
                return False
            for point, detail in knowledge_points.items():
                if not isinstance(point, str) or not isinstance(detail, str):
                    return False
        return True
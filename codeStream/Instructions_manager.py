# Update InstructionsManager class to use the configuration from config.py
import json
import os
from tkinter import ttk
import tkinter as tk
import config


class InstructionsManager:
    """A class to manage the display of application instructions and configuration settings."""

    def __init__(self, root, config_path=config.INSTRUCTION_FILE_PATH):
        """
        Initialize the InstructionsManager with a root Tkinter window and configuration path.

        Args:
            root (tk.Tk): The root Tkinter window.
            config_path (str): The path to the configuration file.
        """
        self.root = root
        self.config_path = config_path
        self.config = self.load_or_create_config()

    def load_or_create_config(self):
        """
        Load the configuration from the file if it exists, otherwise create a default configuration.

        Returns:
            dict: The loaded or created configuration dictionary.
        """
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                return json.load(f)
        else:
            config = {'show_instructions': True}
            with open(self.config_path, 'w') as f:
                json.dump(config, f)
            return config

    def save_config(self):
        """Save the current configuration to the configuration file."""
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f)

    def check_and_show_instructions(self):
        """Check the configuration and show instructions if the 'show_instructions' flag is set."""
        if self.config['show_instructions']:
            self.show_instructions()

    def show_instructions(self):
        """
        Display the application usage instructions in a new window.
        """
        instructions = (
            "欢迎使用知识代码流！\n\n"
            "这是一个帮助你学习和复习知识的工具。\n"
            "使用方法：\n"
            "1. 从下拉菜单中选择一个章节。\n"
            "2. 点击\"Show\"按钮。\n\n"
            "按键说明：\n"
            "上方向键：增加知识点下落速度\n"
            "下方向键：减少知识点下落速度\n"
            "左方向键：减少知识点密度\n"
            "右方向键：增加知识点密度\n"
            "ESC键：退出全屏模式\n\n"
            "如果你不想再次看到此提示，请勾选'不再显示'。"
        )

        def on_checkbox_click():
            """Toggle the 'show_instructions' flag in the configuration when the checkbox is clicked."""
            self.config['show_instructions'] = not do_not_show_var.get()
            self.save_config()

        def on_close():
            """Close the instructions window and update the configuration if the checkbox is checked."""
            if do_not_show_var.get():
                self.config['show_instructions'] = False
                self.save_config()
            instructions_window.destroy()

        # Create a new window for instructions
        instructions_window = tk.Toplevel(self.root)
        instructions_window.title("使用说明")
        instructions_window.geometry("500x400")
        instructions_window.transient(self.root)
        instructions_window.grab_set()

        # Create a frame to hold the instructions content
        instructions_frame = ttk.Frame(instructions_window, padding="20")
        instructions_frame.pack(fill="both", expand=True)

        # Add a label to display the instructions text
        instructions_label = ttk.Label(instructions_frame, text=instructions, font=("Arial", 12), wraplength=460, justify="left")
        instructions_label.pack(pady=20)

        # Add a checkbox to allow users to disable future instructions display
        do_not_show_var = tk.BooleanVar(value=not self.config['show_instructions'])
        do_not_show_check = ttk.Checkbutton(instructions_frame, text="不再显示", variable=do_not_show_var, command=on_checkbox_click)
        do_not_show_check.pack(pady=10)

        # Add a button to close the instructions window
        close_button = ttk.Button(instructions_frame, text="关闭", command=on_close)
        close_button.pack(pady=10)
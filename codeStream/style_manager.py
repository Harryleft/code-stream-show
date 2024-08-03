import tkinter.font as tkfont
from tkinter import ttk


class StyleManager:
    def __init__(self, root):
        self.root = root
        self.setup_fonts()
        self.setup_styles()

    def setup_fonts(self):
        """
        设置应用程序的字体大小
        :return:
        """
        self.font_small = self.create_compound_font(10)
        self.font_normal = self.create_compound_font(12)
        self.font_large = self.create_compound_font(14)
        self.font_title = self.create_compound_font(28, weight="bold")

    def create_compound_font(self, size, weight="normal"):
        """
        设置字体
        :param size:
        :param weight:
        :return:
        """
        font_tuple = ("Times New Roman", "SimSun")
        return tkfont.Font(family=font_tuple, size=size, weight=weight)

    def setup_styles(self):
        """
        设置应用程序的样式
        :return:
        """
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TButton', font=self.font_normal, padding=10)
        self.style.configure('TCheckbutton', font=self.font_normal, background='#f0f0f0')
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=self.font_normal)
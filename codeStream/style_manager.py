import tkinter.font as tkfont
from tkinter import ttk


class StyleManager:
    """
    Manages the styles and fonts for the application.

    Attributes:
        root (tkinter.Tk): The root window of the application.
        font_small (tkinter.font.Font): The small font used in the application.
        font_normal (tkinter.font.Font): The normal font used in the application.
        font_large (tkinter.font.Font): The large font used in the application.
        font_title (tkinter.font.Font): The title font used in the application.
        style (ttk.Style): The style configuration for the application.
    """

    def __init__(self, root):
        """
        Initializes the StyleManager with the root window.

        Args:
            root (tkinter.Tk): The root window of the application.
        """
        self.root = root
        self.setup_fonts()
        self.setup_styles()

    def setup_fonts(self):
        """
        Sets up the font sizes for the application.
        """
        self.font_small = self.create_compound_font(10)
        self.font_normal = self.create_compound_font(12)
        self.font_large = self.create_compound_font(14)
        self.font_title = self.create_compound_font(28, weight="bold")

    def create_compound_font(self, size, weight="normal"):
        """
        Creates a compound font with the specified size and weight.

        Args:
            size (int): The size of the font.
            weight (str): The weight of the font, default is "normal".

        Returns:
            tkinter.font.Font: The created font object.
        """
        font_tuple = ("SimSun", "Times New Roman")
        return tkfont.Font(family=font_tuple, size=size, weight=weight)

    def setup_styles(self):
        """
        Sets up the styles for the application.
        """
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TButton', font=self.font_normal, padding=10)
        self.style.configure('TCheckbutton', font=self.font_normal, background='#f0f0f0')
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=self.font_normal)
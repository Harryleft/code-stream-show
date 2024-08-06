import time
import tkinter as tk
from tkinter import ttk, messagebox
import json
from codeStream.Instructions_manager import InstructionsManager
from codeStream.config import QUOTES_FILE_PATH, KNOWLEDGE_FILE_PATH
from codeStream.json_file_manager import JsonFileManager
from codeStream.knowledge_rain import KnowledgeRain
from codeStream import config
from codeStream.quotes_manager import QuotesManager
from codeStream.style_manager import StyleManager


class KnowledgeRainApp:
    """
    The main application class for the Knowledge Rain App.

    Attributes:
        root (tk.Tk): The root window of the application.
        json_file (str): Path to the knowledge points JSON file.
        quotes_file (str): Path to the quotes JSON file.
        fullscreen (tk.BooleanVar): Boolean variable to track fullscreen mode.
        chapters (dict): Dictionary to store chapters and their knowledge points.
        start_time (float): The start time of the application.
        style_manager (StyleManager): Instance of StyleManager to manage styles.
        quotes_manager (QuotesManager): Instance of QuotesManager to manage quotes.
        daily_quote (str): The daily quote.
        json_file_manager (JsonFileManager): Instance of JsonFileManager to manage JSON files.
        instructions_manager (InstructionsManager): Instance of InstructionsManager to manage instructions.
    """

    def __init__(self, root):
        """
        Initialize the KnowledgeRainApp instance.

        Args:
            root (tk.Tk): The root window of the application.
        """
        self.root = root
        self.root.title("知识代码流：你的专业课陪伴助手")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        self.root.resizable(True, True)
        self.json_file = KNOWLEDGE_FILE_PATH
        self.quotes_file = QUOTES_FILE_PATH
        self.fullscreen = tk.BooleanVar(value=False)
        self.chapters = {}
        self.start_time = time.time()

        self.style_manager = StyleManager(self.root)

        self.quotes_manager = QuotesManager(self.quotes_file)

        self.daily_quote = self.quotes_manager.get_daily_quote()

        self.json_file_manager = JsonFileManager(self.root)

        self.create_widgets()
        self.load_chapters()

        self.instructions_manager = InstructionsManager(self.root)
        self.instructions_manager.check_and_show_instructions()

    def create_widgets(self):
        """
        Create all widgets for the application.
        """
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(expand=True, fill="both")

        # Component: Daily Quote
        quote_label = ttk.Label(main_frame, text=self.daily_quote, font=self.style_manager.font_large,
                                wraplength=700, justify="center")
        quote_label.pack(pady=(0, 30))

        # Component: Title
        title_label = ttk.Label(main_frame, text="知识点代码流", font=self.style_manager.font_title)
        title_label.pack(pady=(0, 30))

        # Component: Chapter Selection Frame
        chapter_frame = ttk.Frame(main_frame)
        chapter_frame.pack(fill="x", pady=(0, 20))
        chapter_label = ttk.Label(chapter_frame, text="选择章节:", font=self.style_manager.font_normal)
        chapter_label.pack(side="left", padx=(0, 10))
        self.chapter_combobox = ttk.Combobox(chapter_frame, font=self.style_manager.font_normal, state="readonly")
        self.chapter_combobox.pack(side="left", fill="x", expand=True)

        # Component: Fullscreen Mode Checkbox
        fullscreen_frame = ttk.Frame(main_frame)
        fullscreen_frame.pack(fill="y", pady=(0, 30))

        self.fullscreen_check = ttk.Checkbutton(fullscreen_frame, text="全屏模式",
                                                variable=self.fullscreen, style='TCheckbutton')
        self.fullscreen_check.pack(side="left")

        # Component: Show All Knowledge Points Checkbox
        self.show_all_var = tk.BooleanVar(value=False)
        show_all_check = ttk.Checkbutton(fullscreen_frame, text="展示所有知识点",
                                         variable=self.show_all_var, style='TCheckbutton')
        show_all_check.pack(side="left")

        # Button Area
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="y", pady=(0, 30))

        # Component: Custom Upload JSON File Button
        self.select_file_button = ttk.Button(button_frame, text="选择JSON文件", command=self.json_file_manager.select_json_file)
        self.select_file_button.pack(side=tk.LEFT, padx=5)

        # Component: Start Button
        self.start_button = ttk.Button(button_frame, text="开始", command=self.start_knowledge_rain)
        self.start_button.pack(side=tk.LEFT, padx=5)

        # Footer
        footer_frame = ttk.Frame(self.root)
        footer_frame.pack(side="bottom", fill="x")
        footer_label = ttk.Label(footer_frame, text="© 2024 是希望", font=self.style_manager.font_normal)
        footer_label.pack(pady=10)

    def load_chapters(self):
        """
        Load chapters from the JSON file.
        """
        try:
            with open(self.json_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.chapters = data
                self.chapter_combobox['values'] = list(data.keys())
                if self.chapter_combobox['values']:
                    self.chapter_combobox.set(self.chapter_combobox['values'][0])
        except FileNotFoundError:
            messagebox.showerror("错误", f"文件未找到: {self.json_file}")
        except json.JSONDecodeError:
            messagebox.showerror("错误", "JSON文件格式错误")
        except Exception as e:
            messagebox.showerror("错误", f"加载章节时发生错误: {str(e)}")

    def start_knowledge_rain(self):
        """
        Start the knowledge rain animation.
        """
        selected_chapter = self.chapter_combobox.get()
        if not selected_chapter:
            messagebox.showwarning("警告", "请选择一个章节")
            return

        selected_knowledge = self.chapters.get(selected_chapter, {})

        if not selected_knowledge:
            messagebox.showwarning("警告", f"章节 '{selected_chapter}' 的内容为空")
            return

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        self.root.withdraw()

        try:
            if self.fullscreen.get():
                width = screen_width
                height = screen_height
            else:
                width = config.WIDTH
                height = config.HEIGHT

            rain = KnowledgeRain(width, height, selected_knowledge, fullscreen=self.fullscreen.get())
            rain.run()
        except AttributeError:
            messagebox.showerror("错误", "配置文件中缺少必要的宽度或高度设置")
        except Exception as e:
            messagebox.showerror("错误", f"启动知识雨时发生错误: {str(e)}")
        finally:
            self.root.deiconify()

    def show_all_knowledge(self):
        """
        Display all knowledge points from the JSON file.
        """
        all_knowledge = {}
        for chapter, knowledge_points in self.chapters.items():
            all_knowledge.update(knowledge_points)

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        self.root.withdraw()

        try:
            rain = KnowledgeRain(screen_width, screen_height, all_knowledge)
            rain.run()
        except Exception as e:
            messagebox.showerror("错误", f"启动知识雨时发生错误: {str(e)}")
        finally:
            self.root.deiconify()


if __name__ == "__main__":
    """
    Main function to run the application.
    """
    try:
        root = tk.Tk()
        root.configure(bg="#f0f0f0")
        KnowledgeRainApp(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("错误", f"应用程序运行时发生错误: {str(e)}")
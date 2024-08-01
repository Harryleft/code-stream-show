import os
import random
import time
import tkinter as tk
from datetime import date
from tkinter import ttk, messagebox
import json
from codeStream.knowledge_rain import KnowledgeRain
from codeStream import config
import tkinter.font as tkfont
import tkinter.filedialog as filedialog


class KnowledgeRainApp:
    def __init__(self, root):
        """
        初始化应用程序
        :param root:
        """
        self.root = root
        self.root.title("知识代码流：你的专业课陪伴助手")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        self.root.resizable(True, True)
        self.json_file = 'json_file/667_knowledge_points.json'
        self.config_file = 'json_file/user_config.json'
        self.quotes_file = 'json_file/quotes.json'
        self.fullscreen = tk.BooleanVar(value=False)
        self.chapters = {}
        self.start_time = time.time()

        self.setup_fonts()
        self.setup_styles()

        self.quotes = self.load_quotes()
        self.daily_quote = self.get_daily_quote()

        self.create_widgets()
        self.load_chapters()
        self.check_and_show_instructions()

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

    def load_quotes(self):
        """
        加载JSON名言文件
        :return:
        """
        try:
            with open(self.quotes_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return data.get('quotes', [])
        except FileNotFoundError:
            messagebox.showwarning("警告", f"未找到名言文件: {self.quotes_file}")
            return []
        except json.JSONDecodeError:
            messagebox.showerror("错误", "名言文件格式错误")
            return []
        except Exception as e:
            messagebox.showerror("错误", f"加载名言时发生错误: {str(e)}")
            return []

    def get_daily_quote(self):
        """
        获取每日名言
        :return:
        """
        if not self.quotes:
            return "今天也要加油哦！"

        # 使用日期作为随机种子，确保每天显示相同的名言
        random.seed(date.today().toordinal())
        quote = random.choice(self.quotes)
        return f"{quote['text']} \n\n—— {quote['author']}"

    def create_widgets(self):
        """
        创建应用程序的所有小部件
        :return:
        """
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(expand=True, fill="both")

        # 组件_每日名言
        quote_label = ttk.Label(main_frame, text=self.daily_quote, font=self.font_large,
                                wraplength=700, justify="center")
        quote_label.pack(pady=(0, 30))

        # 组件_标题
        title_label = ttk.Label(main_frame, text="知识点代码流", font=self.font_title)
        title_label.pack(pady=(0, 30))

        # 组件_章节选择框架
        chapter_frame = ttk.Frame(main_frame)
        chapter_frame.pack(fill="x", pady=(0, 20))
        chapter_label = ttk.Label(chapter_frame, text="选择章节:", font=self.font_normal)
        chapter_label.pack(side="left", padx=(0, 10))
        self.chapter_combobox = ttk.Combobox(chapter_frame, font=self.font_normal, state="readonly")
        self.chapter_combobox.pack(side="left", fill="x", expand=True)

        # 组件_全屏模式复选框
        fullscreen_frame = ttk.Frame(main_frame)
        fullscreen_frame.pack(fill="y", pady=(0, 30))

        self.fullscreen_check = ttk.Checkbutton(fullscreen_frame, text="全屏模式",
                                                variable=self.fullscreen, style='TCheckbutton')
        self.fullscreen_check.pack(side="left")

        # 组件_展示所有知识点复选框
        self.show_all_var = tk.BooleanVar(value=False)
        show_all_check = ttk.Checkbutton(fullscreen_frame, text="展示所有知识点",
                                         variable=self.show_all_var, style='TCheckbutton')
        show_all_check.pack(side="left")

        # 按钮区域
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="y", pady=(0, 30))

        # 组件_自定义上传JSON文件按钮
        self.select_file_button = ttk.Button(button_frame, text="选择JSON文件", command=self.select_json_file)
        self.select_file_button.pack(side=tk.LEFT, padx=5)

        # 组件_开始按钮
        self.start_button = ttk.Button(button_frame, text="开始", command=self.start_knowledge_rain)
        self.start_button.pack(side=tk.LEFT, padx=5)

        # 页脚
        footer_frame = ttk.Frame(self.root)
        footer_frame.pack(side="bottom", fill="x")
        footer_label = ttk.Label(footer_frame, text="© 2024 是希望", font=self.font_normal)
        footer_label.pack(pady=10)

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
                        self.chapters = data
                        self.chapter_combobox['values'] = list(data.keys())
                        if self.chapter_combobox['values']:
                            self.chapter_combobox.set(self.chapter_combobox['values'][0])
                        messagebox.showinfo("成功", "JSON文件加载成功")
                    else:
                        raise ValueError("JSON文件格式不正确, 请确保格式正确, 例如: {'章节1': {'知识点1': '详情1'}}")
            except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
                messagebox.showerror("错误", f"{str(e)}")

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

    def load_chapters(self):
        """
        加载章节
        :return:
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
        启动知识雨
        :return:
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

    def check_and_show_instructions(self):
        """
        检查是否需要显示应用程序的使用说明, 如果用户点击了"不再显示"，则以后不再显示
        :return:
        """
        if not os.path.exists(self.config_file):
            self.show_instructions()
        else:
            with open(self.config_file, 'r') as file:
                config = json.load(file)
                if not config.get('show_instructions', True):
                    return
            self.show_instructions()

    def show_instructions(self):
        """
        显示应用程序的使用说明
        :return:
        """
        instructions = (
            "欢迎使用知识代码流！\n\n"
            "这是一个帮助你学习和复习知识的工具。\n"
            "使用方法：\n"
            "1. 从下拉菜单中选择一个章节。\n"
            "2. 点击\"Show\"按钮。\n\n"           
            "按键说明：\n"
            "上方向键：增加知识点速度\n"
            "下方向键：减少知识点速度\n"
            "左方向键：减少知识点密度\n"
            "右方向键：增加知识点密度\n"
            "ESC键：退出全屏模式\n\n"
            "如果你不想再次看到此提示，请勾选'不再显示'。"
        )

        def on_close():
            if do_not_show_var.get():
                with open(self.config_file, 'w') as file:
                    json.dump({'show_instructions': False}, file)
            instructions_window.destroy()

        instructions_window = tk.Toplevel(self.root)
        instructions_window.title("使用说明")
        instructions_window.geometry("500x400")
        instructions_window.transient(self.root)
        instructions_window.grab_set()

        instructions_frame = ttk.Frame(instructions_window, padding="20")
        instructions_frame.pack(fill="both", expand=True)

        instructions_label = ttk.Label(instructions_frame, text=instructions, font=("Arial", 12), wraplength=460, justify="left")
        instructions_label.pack(pady=20)

        do_not_show_var = tk.BooleanVar()
        do_not_show_check = ttk.Checkbutton(instructions_frame, text="不再显示", variable=do_not_show_var)
        do_not_show_check.pack(pady=10)

        close_button = ttk.Button(instructions_frame, text="关闭", command=on_close)
        close_button.pack(pady=10)

    def show_all_knowledge(self):
        """
        展现JSON文件中的所有知识点
        :return:
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


def main():
    try:
        root = tk.Tk()
        root.configure(bg="#f0f0f0")
        KnowledgeRainApp(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("错误", f"应用程序运行时发生错误: {str(e)}")


if __name__ == "__main__":
    main()
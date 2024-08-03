import json
import random
from datetime import date
from tkinter import messagebox


class QuotesManager:
    def __init__(self, quotes_file):
        self.quotes_file = quotes_file
        self.quotes = self.load_quotes()

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
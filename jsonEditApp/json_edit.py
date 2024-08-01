import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json


class JSONEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("专业课章节知识点JSON查看/编辑器")
        self.root.geometry("800x600")

        self.json_data = {}
        self.current_chapter = tk.StringVar()
        self.current_knowledge = tk.StringVar()
        self.json_file_path = None  # Store the path of the JSON file

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        ttk.Label(left_frame, text="章节列表").pack()
        self.chapter_listbox = tk.Listbox(left_frame, width=30)
        self.chapter_listbox.pack(fill=tk.Y, expand=True)
        self.chapter_listbox.bind('<<ListboxSelect>>', self.on_chapter_select)

        ttk.Button(left_frame, text="添加章节", command=self.add_chapter).pack(fill=tk.X)
        ttk.Button(left_frame, text="删除章节", command=self.delete_chapter).pack(fill=tk.X)

        middle_frame = ttk.Frame(main_frame)
        middle_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        ttk.Label(middle_frame, text="知识点列表").pack()
        self.knowledge_listbox = tk.Listbox(middle_frame, width=30)
        self.knowledge_listbox.pack(fill=tk.Y, expand=True)
        self.knowledge_listbox.bind('<<ListboxSelect>>', self.on_knowledge_select)

        ttk.Button(middle_frame, text="添加知识点", command=self.add_knowledge).pack(fill=tk.X)
        ttk.Button(middle_frame, text="删除知识点", command=self.delete_knowledge).pack(fill=tk.X)

        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        ttk.Label(right_frame, text="知识点详情").pack()
        self.knowledge_text = tk.Text(right_frame, height=20)
        self.knowledge_text.pack(fill=tk.BOTH, expand=True)
        self.knowledge_text.bind('<KeyRelease>', self.auto_save_knowledge)

        self.auto_save_label = ttk.Label(right_frame, text="")
        self.auto_save_label.pack()

        button_frame = ttk.Frame(right_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(button_frame, text="保存知识点", command=self.save_knowledge).pack(side=tk.LEFT)
        ttk.Button(button_frame, text="载入 JSON", command=self.load_json).pack(side=tk.LEFT)
        ttk.Button(button_frame, text="保存 JSON", command=self.save_json).pack(side=tk.LEFT)

    def add_chapter(self):
        chapter_name = tk.simpledialog.askstring("添加章节", "请输入章节名称：")
        if chapter_name:
            self.json_data[chapter_name] = {}
            self.update_chapter_list()

    def delete_chapter(self):
        selected = self.chapter_listbox.curselection()
        if selected:
            chapter_name = self.chapter_listbox.get(selected[0])
            if messagebox.askyesno("删除章节", f"确定要删除章节 '{chapter_name}' 吗？"):
                del self.json_data[chapter_name]
                self.update_chapter_list()
                self.knowledge_listbox.delete(0, tk.END)
                self.knowledge_text.delete('1.0', tk.END)

    def on_chapter_select(self, event):
        selected = self.chapter_listbox.curselection()
        if selected:
            chapter_name = self.chapter_listbox.get(selected[0])
            self.current_chapter.set(chapter_name)
            self.update_knowledge_list()

    def on_knowledge_select(self, event):
        selected = self.knowledge_listbox.curselection()
        if selected:
            knowledge_name = self.knowledge_listbox.get(selected[0])
            self.current_knowledge.set(knowledge_name)
            self.knowledge_text.delete('1.0', tk.END)
            self.knowledge_text.insert(tk.END, self.json_data[self.current_chapter.get()].get(knowledge_name, ""))

    def add_knowledge(self):
        chapter_name = self.current_chapter.get()
        if not chapter_name:
            messagebox.showwarning("警告", "请先选择一个章节")
            return

        knowledge_name = tk.simpledialog.askstring("添加知识点", "请输入知识点名称：")
        if knowledge_name:
            knowledge_details = tk.simpledialog.askstring("添加知识点详情", "请输入知识点详情：")
            self.json_data[chapter_name][knowledge_name] = knowledge_details if knowledge_details else ""
            self.update_knowledge_list()

    def delete_knowledge(self):
        selected = self.knowledge_listbox.curselection()
        if selected:
            knowledge_name = self.knowledge_listbox.get(selected[0])
            if messagebox.askyesno("删除知识点", f"确定要删除知识点 '{knowledge_name}' 吗？"):
                del self.json_data[self.current_chapter.get()][knowledge_name]
                self.update_knowledge_list()
                self.knowledge_text.delete('1.0', tk.END)

    def save_knowledge(self):
        chapter_name = self.current_chapter.get()
        knowledge_name = self.current_knowledge.get()
        if chapter_name and knowledge_name:
            self.json_data[chapter_name][knowledge_name] = self.knowledge_text.get('1.0', tk.END).strip()
            if self.json_file_path:
                with open(self.json_file_path, 'w', encoding='utf-8') as file:
                    json.dump(self.json_data, file, ensure_ascii=False, indent=4)
            messagebox.showinfo("保存成功", "知识点已保存")
    def auto_save_knowledge(self, event):
        chapter_name = self.current_chapter.get()
        knowledge_name = self.current_knowledge.get()
        if chapter_name and knowledge_name:
            self.json_data[chapter_name][knowledge_name] = self.knowledge_text.get('1.0', tk.END).strip()
            if self.json_file_path:
                with open(self.json_file_path, 'w', encoding='utf-8') as file:
                    json.dump(self.json_data, file, ensure_ascii=False, indent=4)
                self.auto_save_label.config(text="知识点已自动保存", foreground="green")
                self.root.after(2000, lambda: self.auto_save_label.config(text=""))

    def load_json(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    self.json_data = json.load(file)
                self.json_file_path = file_path  # Store the file path
                self.update_chapter_list()
            except Exception as e:
                messagebox.showerror("错误", f"加载 JSON 文件时出错：{str(e)}")

    def save_json(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    json.dump(self.json_data, file, ensure_ascii=False, indent=4)
                self.json_file_path = file_path  # Store the file path
                messagebox.showinfo("保存成功", "JSON 文件已保存")
            except Exception as e:
                messagebox.showerror("错误", f"保存 JSON 文件时出错：{str(e)}")

    def update_chapter_list(self):
        self.chapter_listbox.delete(0, tk.END)
        for chapter in self.json_data.keys():
            self.chapter_listbox.insert(tk.END, chapter)

    def update_knowledge_list(self):
        self.knowledge_listbox.delete(0, tk.END)
        for knowledge in self.json_data[self.current_chapter.get()].keys():
            self.knowledge_listbox.insert(tk.END, knowledge)

def main():
    root = tk.Tk()
    app = JSONEditorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
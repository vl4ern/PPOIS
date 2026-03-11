import tkinter as tk

root = tk.Tk()
root.geometry("1400x1200")

toolbar = tk.Frame(root, bg='grey')
toolbar.pack(side=tk.TOP, fill=tk.X)

btn1 = tk.Button(toolbar, text='Добавить')
btn1.pack(side=tk.LEFT, padx=5,pady=5)

btn2 = tk.Button(toolbar, text='Удалить')
btn2.pack(side=tk.LEFT, padx=5, pady=5)

info_label = tk.Label(root, text="Основная рабочая область", bg="grey")
info_label.pack(fill=tk.BOTH, expand=True)

root.mainloop()
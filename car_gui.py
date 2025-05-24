# Nhập các thư viện cần thiết
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

def create_car_evaluation_gui():
    column_names = ['buying', 'maint', 'doors', 'persons', 'lug_boot', 'safety', 'class']
    data = pd.read_csv('car.data', names=column_names)
    encoders = {}
    data_encoded = data.copy()
    for column in data.columns:
        encoders[column] = LabelEncoder()
        data_encoded[column] = encoders[column].fit_transform(data[column])
    X = data_encoded.drop('class', axis=1)
    y = data_encoded['class']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    knn_model = KNeighborsClassifier(n_neighbors=5)
    knn_model.fit(X_train, y_train)
    root = tk.Tk()
    root.title("Hệ thống đánh giá xe hơi")
    root.geometry("900x600")
    root.resizable(True, True)
    style = ttk.Style()
    style.configure("TLabel", font=("Arial", 12))
    style.configure("TButton", font=("Arial", 12))
    style.configure("TCombobox", font=("Arial", 12))
    style.configure("Treeview", font=("Arial", 11))
    style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
    control_frame = ttk.LabelFrame(root, text="Thông tin xe", padding=10)
    control_frame.pack(fill="x", padx=10, pady=10)
    buying_var = tk.StringVar()
    maint_var = tk.StringVar()
    doors_var = tk.StringVar()
    persons_var = tk.StringVar()
    lug_boot_var = tk.StringVar()
    safety_var = tk.StringVar()
    valid_values = {
        'buying': ['vhigh', 'high', 'med', 'low'],
        'maint': ['vhigh', 'high', 'med', 'low'],
        'doors': ['2', '3', '4', '5more'],
        'persons': ['2', '4', 'more'],
        'lug_boot': ['small', 'med', 'big'],
        'safety': ['low', 'med', 'high']
    }
    ttk.Label(control_frame, text="Giá mua:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    buying_combo = ttk.Combobox(control_frame, textvariable=buying_var, values=valid_values['buying'], state="readonly", width=10)
    buying_combo.grid(row=0, column=1, padx=5, pady=5)
    buying_combo.current(0)
    ttk.Label(control_frame, text="Chi phí bảo trì:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
    maint_combo = ttk.Combobox(control_frame, textvariable=maint_var, values=valid_values['maint'], state="readonly", width=10)
    maint_combo.grid(row=0, column=3, padx=5, pady=5)
    maint_combo.current(0)
    ttk.Label(control_frame, text="Số cửa:").grid(row=0, column=4, padx=5, pady=5, sticky="w")
    doors_combo = ttk.Combobox(control_frame, textvariable=doors_var, values=valid_values['doors'], state="readonly", width=10)
    doors_combo.grid(row=0, column=5, padx=5, pady=5)
    doors_combo.current(0)
    ttk.Label(control_frame, text="Số người:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    persons_combo = ttk.Combobox(control_frame, textvariable=persons_var, values=valid_values['persons'], state="readonly", width=10)
    persons_combo.grid(row=1, column=1, padx=5, pady=5)
    persons_combo.current(0)
    ttk.Label(control_frame, text="Cốp xe:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
    lug_boot_combo = ttk.Combobox(control_frame, textvariable=lug_boot_var, values=valid_values['lug_boot'], state="readonly", width=10)
    lug_boot_combo.grid(row=1, column=3, padx=5, pady=5)
    lug_boot_combo.current(0)
    ttk.Label(control_frame, text="An toàn:").grid(row=1, column=4, padx=5, pady=5, sticky="w")
    safety_combo = ttk.Combobox(control_frame, textvariable=safety_var, values=valid_values['safety'], state="readonly", width=10)
    safety_combo.grid(row=1, column=5, padx=5, pady=5)
    safety_combo.current(0)
    result_frame = ttk.LabelFrame(root, text="Kết quả đánh giá", padding=10)
    result_frame.pack(fill="x", padx=10, pady=10)
    result_label = ttk.Label(result_frame, text="Đánh giá: ")
    result_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    result_value = ttk.Label(result_frame, text="", font=("Arial", 12, "bold"))
    result_value.grid(row=0, column=1, padx=5, pady=5, sticky="w")
    table_frame = ttk.LabelFrame(root, text="Dữ liệu đánh giá", padding=10)
    table_frame.pack(fill="both", expand=True, padx=10, pady=10)
    columns = ('buying', 'maint', 'doors', 'persons', 'lug_boot', 'safety', 'class')
    tree = ttk.Treeview(table_frame, columns=columns, show='headings')
    tree.heading('buying', text='Giá mua')
    tree.heading('maint', text='Chi phí bảo trì')
    tree.heading('doors', text='Số cửa')
    tree.heading('persons', text='Số người')
    tree.heading('lug_boot', text='Cốp xe')
    tree.heading('safety', text='An toàn')
    tree.heading('class', text='Đánh giá')
    for col in columns:
        tree.column(col, width=100, anchor='center')
    scrollbar_y = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    scrollbar_x = ttk.Scrollbar(table_frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
    tree.pack(side="left", fill="both", expand=True)
    scrollbar_y.pack(side="right", fill="y")
    scrollbar_x.pack(side="bottom", fill="x")
    for i, row in data.iterrows():
        tree.insert('', 'end', values=tuple(row))
    def predict():
        user_input = {
            'buying': buying_var.get(),
            'maint': maint_var.get(),
            'doors': doors_var.get(),
            'persons': persons_var.get(),
            'lug_boot': lug_boot_var.get(),
            'safety': safety_var.get()
        }
        input_encoded = {}
        for feature, value in user_input.items():
            input_encoded[feature] = encoders[feature].transform([value])[0]
        input_df = pd.DataFrame([input_encoded])
        knn_prediction_code = knn_model.predict(input_df)[0]
        knn_prediction = encoders['class'].inverse_transform([knn_prediction_code])[0]
        result_value.config(text=knn_prediction)
        class_meanings = {
            'unacc': 'không chấp nhận được',
            'acc': 'chấp nhận được',
            'good': 'tốt',
            'vgood': 'rất tốt'
        }
        messagebox.showinfo("Kết quả đánh giá", f"Đánh giá xe: {knn_prediction} ({class_meanings.get(knn_prediction, '')})")
        values = list(user_input.values())
        values.append(knn_prediction)
        tree.insert('', 0, values=tuple(values), tags=('new',))
        tree.tag_configure('new', background='lightgreen')
    def filter_data():
        filters = {
            'buying': buying_var.get() if buying_var.get() != "" else None,
            'maint': maint_var.get() if maint_var.get() != "" else None,
            'doors': doors_var.get() if doors_var.get() != "" else None,
            'persons': persons_var.get() if persons_var.get() != "" else None,
            'lug_boot': lug_boot_var.get() if lug_boot_var.get() != "" else None,
            'safety': safety_var.get() if safety_var.get() != "" else None
        }
        for row in tree.get_children():
            tree.delete(row)
        filtered_data = data.copy()
        for feature, value in filters.items():
            if value is not None:
                filtered_data = filtered_data[filtered_data[feature] == value]
        for i, row in filtered_data.iterrows():
            tree.insert('', 'end', values=tuple(row))
    def refresh_data():
        for row in tree.get_children():
            tree.delete(row)
        for i, row in data.iterrows():
            tree.insert('', 'end', values=tuple(row))
    button_frame = ttk.Frame(root)
    button_frame.pack(fill="x", padx=10, pady=10)
    predict_button = ttk.Button(button_frame, text="Dự đoán", command=predict)
    predict_button.pack(side="left", padx=5)
    filter_button = ttk.Button(button_frame, text="Lọc dữ liệu", command=filter_data)
    filter_button.pack(side="left", padx=5)
    refresh_button = ttk.Button(button_frame, text="Làm mới bảng", command=refresh_data)
    refresh_button.pack(side="left", padx=5)
    root.mainloop()
if __name__ == "__main__":
    create_car_evaluation_gui()
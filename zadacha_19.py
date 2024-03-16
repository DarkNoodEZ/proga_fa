import tkinter as tk
from tkinter import *
from tkinter import messagebox
import mysql.connector
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
pd.set_option('display.expand_frame_repr', False)

# Создание графического интерфейса с помощью Tkinter
class TkinterFurniture:
    def __init__(self, root):
        self.root = root
        w = self.root.winfo_screenwidth() // 3
        h = self.root.winfo_screenheight() // 4
        self.root.geometry(f'300x150+{w}+{h}')
        self.root.title("Matrix multiplication")

        self.create_db_button = tk.Button(self.root, text="Создать базу данных MySQL", command=self.create_database)
        self.create_db_button.pack()

        self.create_table_button = tk.Button(self.root, text="Создать таблицу MySQL", command=self.create_table)
        self.create_table_button.pack()

        self.add_data_button = tk.Button(self.root, text="Ввести и перемножить матрицы", command=self.add_data)
        self.add_data_button.pack()

        self.show_data_button = tk.Button(self.root, text="Показать матрицы из MySQL", command=self.show_data)
        self.show_data_button.pack()

        self.save_to_excel_button = tk.Button(self.root, text="Сохранить в Excel", command=self.save_to_excel)
        self.save_to_excel_button.pack()

    @staticmethod
    def create_database():
        # Код для создания базы данных в MySQL
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                charset='utf8mb4',
                password="root"
            )
            cursor = conn.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS db19")
            messagebox.showinfo("Базы данных", "База данных 'db' успешно создана")
            df = str(pd.read_sql("SHOW DATABASES", conn))
            window1 = Tk()
            window1.title("Databases")
            window1.geometry('400x250')
            lbl1 = Label(window1, text=df)
            lbl1.grid(column=0, row=0)
            window1.mainloop()
            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Ошибка", f"Ошибка: {err}")

    @staticmethod
    def create_table():
        def table_creation():
            # Код для создания таблицы в MySQL
            try:
                tbl_name = entry_tbl_name.get()
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="root",
                    charset='utf8mb4',
                    database="db19"
                )
                cursor = conn.cursor()
                cursor.execute(f"""
                    CREATE TABLE IF NOT EXISTS {tbl_name} (
                    ID INT AUTO_INCREMENT PRIMARY KEY,
                    Matrix_1 VARCHAR(255),
                    Matrix_2 VARCHAR(255),
                    Matrix_3 VARCHAR(255)
                    )
                    """)
                conn.commit()  # сохраняет треугольник

                messagebox.showinfo("Успешно", f"Таблица '{tbl_name}' успешно создана")
                # df = str(pd.read_sql("SELECT * FROM table_", conn))
                df1 = str(pd.read_sql("SHOW TABLES", conn))
                window1 = Tk()
                window1.title("Databases")
                window1.geometry('400x250')
                lbl1 = Label(window1, text=df1)
                lbl1.grid(column=0, row=0)
            # lbl = Label(text=f'База данных "db" успешно создана!')
            # lbl.grid(column=0, row=0)
                window1.mainloop()
                conn.close()
                return
            except mysql.connector.Error as err:
                messagebox.showerror("Ошибка", f"Ошибка: {err}")

        root = Tk()
        root.title("Enter Table Name")
        label_tbl_name = tk.Label(root, text="TableName:")
        label_tbl_name.pack()
        entry_tbl_name = tk.Entry(root)
        entry_tbl_name.pack()

        button_tbl = tk.Button(root, text="create_table", command=table_creation)
        button_tbl.pack()

        root.mainloop()

    @staticmethod
    def add_data():
        def insert_data():
            tbl_choice = entry_tbl_choice.get()
            m_1 = entry_m_1.get('1.0', END)
            m_2 = entry_m_2.get('1.0', END)
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                charset='utf8mb4',
                database="db19"
            )
            cursor = conn.cursor()
            m_1 = m_1.replace('\n','|').split('|')
            m_2 = m_2.replace('\n','|').split('|')

            matrix_1 = []
            for el in m_1:
                if el != '':
                    matrix_1.append(list(map(int, el.split())))
            matrix_2 = []
            for el in m_2:
                if el != '':
                    matrix_2.append(list(map(int, el.split())))

            try:
                result = np.dot(np.array(matrix_1), np.array(matrix_2))
                try:
                    query = f"INSERT INTO {tbl_choice} (Matrix_1, Matrix_2, Matrix_3) VALUES (%s, %s, %s)"
                    cursor.execute(query, (str(np.array(matrix_1)), str(np.array(matrix_2)), str(result)))
                    conn.commit()
                    cursor.close()
                    conn.close()
                    messagebox.showinfo("Матрицы перемножены", f"Результат:\n {result}")
                except:
                    messagebox.showerror("Ошибка", f"Таблицы {tbl_choice} нет в базе данных")
            except:
                messagebox.showerror("Ошибка", "Невозможно перемножить введённые матрицы")




    # Функция для вывода данных из базы данных
        def show_data():
            tbl_choice = entry_tbl_choice.get()
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                charset='utf8mb4',
                database="db19"
            )

            df = str(pd.read_sql(f"SELECT * FROM {tbl_choice}", conn))

            window1 = Tk()
            window1.title("Databases")
            window1.geometry('400x250')
            lbl1 = Label(window1, text=df)
            lbl1.grid(column=0, row=0)
        # lbl = Label(text=f'База данных "db" успешно создана!')
        # lbl.grid(column=0, row=0)
            window1.mainloop()

    # Создание графического интерфейса
        root = Tk()
        root.title("MySQL Data Entry")

        label_tbl_choice = tk.Label(root, text="TableName:")
        label_tbl_choice.pack()
        entry_tbl_choice = tk.Entry(root)
        entry_tbl_choice.pack()

        label_m_1 = tk.Label(root, text="Matrix 1:")
        label_m_1.pack()
        entry_m_1 = tk.Text(root, height=4, width=10)
        entry_m_1.pack()

        label_m_2 = tk.Label(root, text="Matrix 2:")
        label_m_2.pack()
        entry_m_2 = tk.Text(root, height=4, width=10)
        entry_m_2.pack()

        button_insert = tk.Button(root, text="Insert Data", command=insert_data)
        button_insert.pack()

        button_show = tk.Button(root, text="Show Data", command=show_data)
        button_show.pack()

        root.mainloop()


    @staticmethod
    def show_data():
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            charset='utf8mb4',
            database="db19"
        )
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

    # Выводим список таблиц
        tb = []
        for table in tables:
            tb.append(table[0])
    # SQL-запрос для выборки всех данных из таблицы
        df1 = ''
        for i in tb:
            df = f'Table {i}' + '\n' + str(pd.read_sql(f"SELECT * FROM {i}", conn))
            df1 += df + '\n'
        print(df1)
        window1 = Tk()
        window1.title("Databases")
        window1.geometry('400x250')
        lbl1 = Label(window1, text=df1)
        lbl1.grid(column=0, row=0)
    # lbl = Label(text=f'База данных "db" успешно создана!')
    # lbl.grid(column=0, row=0)
        window1.mainloop()
        conn.close()


    @staticmethod
    def save_to_excel():
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            charset='utf8mb4',
            database="db19"
        )
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        tb = []
        for table in tables:
            tb.append(table[0])
        # SQL-запрос для выборки всех данных из таблицы
        for i in tb:
            excel = f'{i}.xlsx'
            df = pd.read_sql(f"SELECT * FROM {i}", conn)
            df.to_excel(excel, sheet_name="Все действия", index=False)

        conn.close()


if __name__ == "__main__":
    root1 = tk.Tk()
    app = TkinterFurniture(root1)
    root1.mainloop()

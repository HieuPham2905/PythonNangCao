import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg
import psycopg2
from psycopg2 import sql

class DatabaseApp:
    def __init__(self, win):
        self.win = win
        self.win.title("Connect DB")

        self.db_name = tk.StringVar(value="dbtest")
        self.user = tk.StringVar(value="postgres")
        self.password = tk.StringVar(value="051204")
        self.host = tk.StringVar(value="localhost")
        self.port = tk.StringVar(value="5432")
        self.table_name = tk.StringVar(value="sinhvien")

        self.create_widgets()

    def create_widgets(self):
        #Frame kết nối DB
        frame1 = tk.LabelFrame(self.win, text="DB Connection", fg="blue")
        frame1.pack(pady=10)
        
        tk.Label(frame1, text="Database Name:").grid(column=0, row=0, padx=5, pady=5, sticky=tk.E)
        tk.Entry(frame1, textvariable=self.db_name).grid(column=1, row=0, padx=5, pady=5)

        tk.Label(frame1, text="User:").grid(column=0, row=1, padx=5, pady=5, sticky=tk.E)
        tk.Entry(frame1, textvariable=self.user).grid(column=1, row=1, padx=5, pady=5)

        tk.Label(frame1, text="Password:").grid(column=0, row=2, padx=5, pady=5, sticky=tk.E)
        tk.Entry(frame1, textvariable=self.password).grid(column=1, row=2, padx=5, pady=5)

        tk.Label(frame1, text="Host:").grid(column=0, row=3, padx=5, pady=5, sticky=tk.E)
        tk.Entry(frame1, textvariable=self.host).grid(column=1, row=3, padx=5, pady=5)

        tk.Label(frame1, text="Port:").grid(column=0, row=4, padx=5, pady=5, sticky=tk.E)
        tk.Entry(frame1, textvariable=self.port).grid(column=1, row=4, padx=5, pady=5)

        tk.Label(frame1, text="Table Name:").grid(column=0, row=1, padx=5, pady=5, sticky=tk.E)
        tk.Entry(frame1, textvariable=self.table_name).grid(column=1, row=2, padx=5, pady=5)

        tk.Button(frame1, text="CONNECT!", command=self.connect_db).grid(row=5, columnspan=2, pady=10)

        #Frame thực thi DB
        frame2 = tk.LabelFrame(self.win, text="Query", fg="blue")
        frame2.pack(pady=10)

        tk.Label(frame2, text="Table Name:").grid(column=0, row=0, padx=5, pady=5)
        tk.Entry(frame2, textvariable=self.table_name).grid(column=1, row=0, padx=5, pady=5)

        tk.Button(frame2, text="LOAD DATA!", command=self.load_data).grid(row=1, columnspan=2, pady=10)

        self.data_display = tk.Text(self.win, width=50, height=10)
        self.data_display.pack(pady=10)

        #Insert section
        frame3 = tk.LabelFrame(self.win)
        frame3.pack(pady=10)

        self.column1 = tk.StringVar()
        self.column2 = tk.StringVar()

        tk.Label(frame3, text="MSSV:").grid(column=0, row=0, padx=5, pady=5)
        tk.Entry(frame3, textvariable=self.column1).grid(column=1, row=0, padx=5, pady=5)

        tk.Label(frame3, text="Họ tên:").grid(column=0, row=1, padx=5, pady=5)
        tk.Entry(frame3, textvariable=self.column2).grid(column=1, row=1, padx=5, pady=5)
        tk.Button(frame3, text="INSERT!", command=self.insert_data).grid(row=2, columnspan=2, pady=10)

        #Delete sectioon
        tk.Button(frame3, text="DELETE!", command=self.delete_data).grid(row=3, columnspan=2, pady=10)

    def connect_db(self):
        try:
            self.conn = psycopg2.connect(
                dbname=self.db_name.get(),
                user=self.user.get(),
                password=self.password.get(),
                host=self.host.get(),
                port=self.port.get()
            )
            self.cur = self.conn.cursor()
            msg.showinfo("Success", "Connected to the database successfully!")
        except Exception as e:
            msg.showerror("Error", f"Error connecting to the database: {e}")

    def load_data(self):
        try:
            query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(self.table_name.get()))
            self.cur.execute(query)
            rows = self.cur.fetchall()
            self.data_display.delete(1.0, tk.END)
            for row in rows:
                self.data_display.insert(tk.END, f"{row}\n")
        except Exception as e:
            msg.showerror("Error", f"Error loading data: {e}")

    def insert_data(self):
        try:
            insert_query = sql.SQL("INSERT INTO {} (mssv, hoten) VALUES (%s, %s)").format(sql.Identifier(self.table_name.get()))
            data_to_insert = (self.column1.get(), self.column2.get())
            self.cur.execute(insert_query, data_to_insert)
            self.conn.commit()
            msg.showinfo("Success", "Data inserted successfully!")
        except Exception as e:
            msg.showerror("Error", f"Error inserting data: {e}")

    def delete_data(self):
        try :
            detele_query = sql.SQL("DELETE FROM {} where MSSV = %s").format(sql.Identifier(self.table_name.get()))
            data_to_delete = (self.column1.get(),)
            self.cur.execute(detele_query,data_to_delete)
            self.conn.commit()
            msg.showinfo("Success", "Data deleted successfully!")

        except Exception as e:
            msg.showerror("Error", f"Error deleting data: {e}")

if __name__ == "__main__":
    win = tk.Tk()
    app = DatabaseApp(win)
    win.mainloop()
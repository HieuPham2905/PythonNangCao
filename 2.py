import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
from psycopg2 import sql

class DatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Database App")
        self.root.geometry("800x600")  # Mở rộng cửa sổ

        # Database connection fields
        self.db_name = tk.StringVar(value='dbtest')
        self.user = tk.StringVar(value='postgres')
        self.password = tk.StringVar(value='051204')
        self.host = tk.StringVar(value='localhost')
        self.port = tk.StringVar(value='5432')
        self.table_name = tk.StringVar(value='sinhvien')

        # Create the GUI elements
        self.create_widgets()

    def create_widgets(self):
        # Khung trái chứa các chức năng kết nối và thao tác
        left_frame = tk.Frame(self.root, width=250)  # Tăng chiều rộng khung bên trái
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # Phần kết nối cơ sở dữ liệu
        connection_frame = tk.LabelFrame(left_frame, text="Kết nối CSDL")
        connection_frame.pack(fill=tk.X, padx=5, pady=5)

        tk.Label(connection_frame, text="Tên CSDL:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.db_name).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(connection_frame, text="Người dùng:").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.user).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(connection_frame, text="Mật khẩu:").grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.password, show="#").grid(row=2, column=1, padx=5, pady=5)

        tk.Label(connection_frame, text="Host:").grid(row=3, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.host).grid(row=3, column=1, padx=5, pady=5)

        tk.Label(connection_frame, text="Port:").grid(row=4, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.port).grid(row=4, column=1, padx=5, pady=5)

        tk.Button(connection_frame, text="Kết nối", command=self.connect_db).grid(row=5, columnspan=2, pady=10)

        # Phần chọn bảng và tải dữ liệu
        query_frame = tk.LabelFrame(left_frame, text="Tải dữ liệu")
        query_frame.pack(fill=tk.X, padx=5, pady=5)

        tk.Label(query_frame, text="Tên bảng:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(query_frame, textvariable=self.table_name).grid(row=0, column=1, padx=5, pady=5)

        tk.Button(query_frame, text="Tải dữ liệu", command=self.load_data).grid(row=1, columnspan=2, pady=10)

        # Phần chèn dữ liệu
        insert_frame = tk.LabelFrame(left_frame, text="Chèn dữ liệu")
        insert_frame.pack(fill=tk.X, padx=5, pady=5)

        self.column1 = tk.StringVar()
        self.column2 = tk.StringVar()

        tk.Label(insert_frame, text="MSSV:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(insert_frame, textvariable=self.column1).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(insert_frame, text="Họ tên:").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(insert_frame, textvariable=self.column2).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(insert_frame, text="Thêm dữ liệu", command=self.insert_data).grid(row=2, columnspan=2, pady=10)

        # Phần xóa dữ liệu
        delete_frame = tk.LabelFrame(left_frame, text="Xóa dữ liệu")
        delete_frame.pack(fill=tk.X, padx=5, pady=5)

        self.delete_mssv = tk.StringVar()

        tk.Label(delete_frame, text="Chọn MSSV:").grid(row=0, column=0, padx=5, pady=5)
        self.mssv_combobox = ttk.Combobox(delete_frame, textvariable=self.delete_mssv)
        self.mssv_combobox.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(delete_frame, text="Xóa dữ liệu", command=self.delete_data).grid(row=1, columnspan=2, pady=10)

        # Khung phải chứa bảng dữ liệu
        right_frame = tk.Frame(self.root)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(right_frame, columns=('mssv', 'hoten'), show='headings')
        self.tree.heading('mssv', text='MSSV')
        self.tree.heading('hoten', text='Họ Tên')

        # Căn chỉnh cột giống như bảng Excel
        self.tree.column('mssv', width=150, anchor="center")
        self.tree.column('hoten', width=300, anchor="w")
        self.tree.pack(pady=10, fill='both', expand=True)  # Mở rộng Treeview theo chiều rộng và chiều cao

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
            messagebox.showinfo("Thành công", "Kết nối cơ sở dữ liệu thành công!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi kết nối cơ sở dữ liệu: {e}")

    def load_data(self):
        try:
            query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(self.table_name.get()))
            self.cur.execute(query)
            rows = self.cur.fetchall()

            # Xóa dữ liệu cũ trong Treeview
            for i in self.tree.get_children():
                self.tree.delete(i)

            # Chèn dữ liệu mới vào Treeview
            for row in rows:
                self.tree.insert("", tk.END, values=row)

            # Lấy danh sách MSSV để điền vào combobox xóa
            mssv_list = [row[0] for row in rows]  # MSSV là cột đầu tiên
            self.mssv_combobox['values'] = mssv_list
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi tải dữ liệu: {e}")

    def insert_data(self):
        try:
            insert_query = sql.SQL("INSERT INTO {} (mssv, hoten) VALUES (%s, %s)").format(sql.Identifier(self.table_name.get()))
            data_to_insert = (self.column1.get(), self.column2.get())
            self.cur.execute(insert_query, data_to_insert)
            self.conn.commit()
            messagebox.showinfo("Thành công", "Dữ liệu đã được thêm!")
            self.load_data()  # Tải lại bảng sau khi thêm
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi thêm dữ liệu: {e}")

    def delete_data(self):
        try:
            selected_mssv = self.delete_mssv.get()
            if not selected_mssv:
                messagebox.showerror("Lỗi", "Vui lòng chọn MSSV cần xóa.")
                return

            delete_query = sql.SQL("DELETE FROM {} WHERE mssv = %s").format(sql.Identifier(self.table_name.get()))
            self.cur.execute(delete_query, (selected_mssv,))
            self.conn.commit()
            messagebox.showinfo("Thành công", "Dữ liệu đã được xóa!")
            self.load_data()  # Tải lại bảng sau khi xóa
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi xóa dữ liệu: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop()

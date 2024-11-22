import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
from psycopg2 import sql
import random
import string

class DatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ứng Dụng Cơ Sở Dữ Liệu")
        self.root.geometry("800x600")

        # Các trường kết nối CSDL
        self.db_name = tk.StringVar(value='dbtest')
        self.user = tk.StringVar(value='postgres')
        self.password = tk.StringVar(value='051204')
        self.host = tk.StringVar(value='localhost')
        self.port = tk.StringVar(value='5432')
        self.table_name = tk.StringVar(value='sinhvien')

        # Tạo các thành phần giao diện người dùng
        self.create_widgets()

    def create_widgets(self):
        left_frame = tk.Frame(self.root, width=250)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

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
        self.hocphi = tk.StringVar()
        self.thanhtoan = tk.StringVar(value="Chưa thanh toán")

        # Dòng lưu ý màu đỏ
        tk.Label(insert_frame, text="* là bắt buộc nhập", fg="red").grid(row=0, columnspan=2, pady=5)

        tk.Label(insert_frame, text="* MSSV:").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(insert_frame, textvariable=self.column1).grid(row=1, column=1, padx=5, pady=5)
        tk.Label(insert_frame, text="* Họ tên:").grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(insert_frame, textvariable=self.column2).grid(row=2, column=1, padx=5, pady=5)
        tk.Label(insert_frame, text="* Học phí:").grid(row=3, column=0, padx=5, pady=5)
        tk.Entry(insert_frame, textvariable=self.hocphi).grid(row=3, column=1, padx=5, pady=5)

        # Các radio button trạng thái thanh toán
        tk.Label(insert_frame, text="Trạng thái thanh toán:").grid(row=4, column=0, padx=5, pady=5)
        tk.Radiobutton(insert_frame, text="Đã thanh toán", variable=self.thanhtoan, value="Đã thanh toán").grid(row=4, column=1, padx=5, pady=2)
        tk.Radiobutton(insert_frame, text="Chưa thanh toán", variable=self.thanhtoan, value="Chưa thanh toán").grid(row=5, column=1, padx=5, pady=2)

        tk.Button(insert_frame, text="Thêm dữ liệu", command=self.insert_data).grid(row=6, columnspan=2, pady=10)

        # Phần xóa dữ liệu
        delete_frame = tk.LabelFrame(left_frame, text="Xóa dữ liệu")
        delete_frame.pack(fill=tk.X, padx=5, pady=5)

        self.delete_mssv = tk.StringVar()

        tk.Label(delete_frame, text="Chọn MSSV:").grid(row=0, column=0, padx=5, pady=5)
        self.mssv_combobox = ttk.Combobox(delete_frame, textvariable=self.delete_mssv)
        self.mssv_combobox.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(delete_frame, text="Xóa dữ liệu", command=self.delete_data).grid(row=1, columnspan=2, pady=10)

        # Phần hiển thị dữ liệu bên phải
        right_frame = tk.Frame(self.root)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(right_frame, columns=('mssv', 'hoten', 'hocphi', 'mahoadon', 'thanhtoan'), show='headings')
        self.tree.heading('mssv', text='MSSV')
        self.tree.heading('hoten', text='Họ Tên')
        self.tree.heading('hocphi', text='Học Phí')
        self.tree.heading('mahoadon', text='Mã Hóa Đơn')
        self.tree.heading('thanhtoan', text='Trạng Thái Thanh Toán')
        self.tree.column('mssv', width=150, anchor="center")
        self.tree.column('hoten', width=150, anchor="w")
        self.tree.column('hocphi', width=150, anchor="center")
        self.tree.column('mahoadon', width=200, anchor="center")
        self.tree.column('thanhtoan', width=150, anchor="center")
        self.tree.pack(pady=10, fill='both', expand=True)

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
            query = sql.SQL("SELECT mssv, hoten, hocphi, mahoadon, thanhtoan FROM {}").format(
                sql.Identifier(self.table_name.get())
            )
            self.cur.execute(query)
            rows = self.cur.fetchall()

            # Xóa dữ liệu cũ trong Treeview
            for i in self.tree.get_children():
                self.tree.delete(i)

            # Thêm dữ liệu mới vào Treeview
            mssvs = []
            for row in rows:
                hocphi_formatted = "{:,.0f}".format(row[2]).replace(",", ".") + " VNĐ" if row[2] else "N/A"
                status = "Đã thanh toán" if row[4] else "Chưa thanh toán"
                self.tree.insert('', 'end', values=(row[0], row[1], hocphi_formatted, row[3], status))
                mssvs.append(row[0])

            # Cập nhật MSSV vào Combobox
            self.mssv_combobox['values'] = mssvs
        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Lỗi", f"Lỗi tải dữ liệu: {e}")

    def insert_data(self):
        try:
            mssv = self.column1.get()
            hoten = self.column2.get()
            hocphi = float(self.hocphi.get()) if self.hocphi.get() else None
            thanhtoan = True if self.thanhtoan.get() == "Đã thanh toán" else False

            if not mssv or not hoten:
                raise ValueError("MSSV và Họ tên là bắt buộc!")

            # Mã hóa đơn tự động với 10 ký tự từ chữ và số
            mahoadon = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(10)])

            # Chèn dữ liệu vào cơ sở dữ liệu
            insert_query = sql.SQL(
                "INSERT INTO {} (mssv, hoten, hocphi, mahoadon, thanhtoan) VALUES (%s, %s, %s, %s, %s)"
            ).format(sql.Identifier(self.table_name.get()))
            self.cur.execute(insert_query, (mssv, hoten, hocphi, mahoadon, thanhtoan))
            self.conn.commit()

            # Cập nhật Treeview
            self.load_data()
            messagebox.showinfo("Thành công", "Dữ liệu đã được chèn thành công!")
        except ValueError as ve:
            messagebox.showwarning("Cảnh báo", f"Dữ liệu không hợp lệ: {ve}")
        except Exception as e:
            self.conn.rollback()  # Hủy giao dịch nếu có lỗi
            messagebox.showerror("Lỗi", f"Lỗi khi thêm dữ liệu: {e}")

    def delete_data(self):
        try:
            mssv = self.delete_mssv.get()
            if not mssv:
                raise ValueError("Vui lòng chọn MSSV để xóa!")

            delete_query = sql.SQL("DELETE FROM {} WHERE mssv = %s").format(
                sql.Identifier(self.table_name.get())
            )
            self.cur.execute(delete_query, (mssv,))
            self.conn.commit()

            # Cập nhật Treeview
            self.load_data()
            messagebox.showinfo("Thành công", "Dữ liệu đã được xóa thành công!")
        except ValueError as ve:
            messagebox.showwarning("Cảnh báo", f"{ve}")
        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Lỗi", f"Lỗi khi xóa dữ liệu: {e}")

    def __del__(self):
        if hasattr(self, 'conn') and self.conn:
            self.cur.close()
            self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop()

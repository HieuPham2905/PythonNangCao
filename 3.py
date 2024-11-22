from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
import random
import string

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Cấu hình kết nối CSDL
db_config = {
    'dbname': 'dbtest',
    'user': 'postgres',
    'password': '051204',
    'host': 'localhost',
    'port': '5432'
}

def get_db_connection():
    try:
        conn = psycopg2.connect(**db_config)
        return conn
    except Exception as e:
        flash(f"Không thể kết nối CSDL: {e}", 'error')
        return None

@app.route('/')
def index():
    try:
        conn = get_db_connection()
        if not conn:
            return render_template('index.html', data=[])
        
        cur = conn.cursor()
        cur.execute("SELECT mssv, hoten, hocphi, mahoadon, thanhtoan FROM sinhvien")
        rows = cur.fetchall()
        cur.close()
        conn.close()

        data = [
            {
                'mssv': row[0],
                'hoten': row[1],
                'hocphi': "{:,.0f}".format(row[2]).replace(",", ".") + " VNĐ" if row[2] else "N/A",
                'mahoadon': row[3],
                'thanhtoan': "Đã thanh toán" if row[4] else "Chưa thanh toán"
            }
            for row in rows
        ]

        return render_template('index.html', data=data)
    except Exception as e:
        flash(f"Lỗi khi tải dữ liệu: {e}", 'error')
        return render_template('index.html', data=[])

@app.route('/add', methods=['POST'])
def add_student():
    try:
        mssv = request.form['mssv']
        hoten = request.form['hoten']
        hocphi = float(request.form['hocphi']) if request.form['hocphi'] else None
        thanhtoan = True if request.form['thanhtoan'] == "Đã thanh toán" else False

        if not mssv or not hoten:
            flash("MSSV và Họ tên là bắt buộc!", 'warning')
            return redirect(url_for('index'))

        # Tạo mã hóa đơn ngẫu nhiên
        mahoadon = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

        conn = get_db_connection()
        if not conn:
            return redirect(url_for('index'))

        cur = conn.cursor()
        cur.execute(
            "INSERT INTO sinhvien (mssv, hoten, hocphi, mahoadon, thanhtoan) VALUES (%s, %s, %s, %s, %s)",
            (mssv, hoten, hocphi, mahoadon, thanhtoan)
        )
        conn.commit()
        cur.close()
        conn.close()

        flash("Dữ liệu đã được chèn thành công!", 'success')
        return redirect(url_for('index'))
    except Exception as e:
        flash(f"Lỗi khi thêm dữ liệu: {e}", 'error')
        return redirect(url_for('index'))

@app.route('/delete', methods=['POST'])
def delete_student():
    try:
        mssv = request.form['mssv_delete']
        if not mssv:
            flash("Vui lòng chọn MSSV để xóa!", 'warning')
            return redirect(url_for('index'))

        conn = get_db_connection()
        if not conn:
            return redirect(url_for('index'))

        cur = conn.cursor()
        cur.execute("DELETE FROM sinhvien WHERE mssv = %s", (mssv,))
        conn.commit()
        cur.close()
        conn.close()

        flash("Dữ liệu đã được xóa thành công!", 'success')
        return redirect(url_for('index'))
    except Exception as e:
        flash(f"Lỗi khi xóa dữ liệu: {e}", 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

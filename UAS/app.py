from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector

app = Flask(__name__)

# Fungsi untuk koneksi ke database
def get_db_connection():
    return mysql.connector.connect(
        host="i0bbi.h.filess.io",
        user="aybongs_tinicelot",
        port="3307",
        password="46a0c7748b8f2bb30f1826fb2e727e0f919f0746",
        database="aybongs_tinicelot"
    )

# Halaman utama
@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produk")
    products = cursor.fetchall()
    conn.close()
    return render_template('index.html', products=products)

# Tambah produk
@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        nama_produk = request.form['nama_produk']
        storage = request.form['storage']
        harga_produk = request.form['harga_produk']
        jumlah_produk = request.form['jumlah_produk']

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO produk (nama_produk, storage, harga_produk, jumlah_produk) VALUES (%s, %s, %s, %s)",
                           (nama_produk, storage, harga_produk, jumlah_produk))
            conn.commit()
        except mysql.connector.Error as err:
            return render_template('tambah-barang.html', error=f"Terjadi kesalahan: {err}")
        finally:
            conn.close()

        return redirect(url_for('index'))

    return render_template('tambah-barang.html')

# Edit produk
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        nama_produk = request.form['nama_produk']
        storage = request.form['storage']
        harga_produk = request.form['harga_produk']
        jumlah_produk = request.form['jumlah_produk']

        try:
            cursor.execute(
                "UPDATE produk SET nama_produk = %s, storage = %s, harga_produk = %s, jumlah_produk = %s WHERE id = %s",
                (nama_produk, storage, harga_produk, jumlah_produk, id)
            )
            conn.commit()
        except Exception as e:
            conn.close()
            return f"Terjadi kesalahan: {e}", 500
        finally:
            conn.close()

        return redirect(url_for('index'))

    cursor.execute("SELECT * FROM produk WHERE id = %s", (id,))
    product = cursor.fetchone()
    conn.close()

    if product is None:
        return "Produk tidak ditemukan!", 404

    return render_template('edit_product.html', product=product)

# Hapus produk
@app.route('/delete/<int:id>', methods=['POST'])
def delete_product(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM produk WHERE id = %s", (id,))
        conn.commit()
    except mysql.connector.Error as err:
        return f"Terjadi kesalahan: {err}"
    finally:
        conn.close()

    return redirect(url_for('index'))

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
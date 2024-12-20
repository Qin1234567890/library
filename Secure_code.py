from flask import Flask, render_template, request, redirect, session, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import re

from datetime import datetime, timedelta
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",  # Replace with your MySQL username
    password="123456",  # Replace with your MySQL password
    database="library_system"
)
cursor = db.cursor(dictionary=True)

# Check if user is admin
def is_admin():
    user_id = session.get('user_id')
    if user_id:
        cursor.execute("SELECT role FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        return user['role'] == 'admin' if user else False
    return False

# Route: User Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        full_name = request.form['full_name']
        email = request.form['email']
        role = request.form.get('role', 'user')  # 获取表单提交的角色，如果没有提供，则默认为 'user'
        
        # 检查用户名是否已经存在
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            flash('Username already exists, please choose another one.', 'danger')
            return redirect('/register')
        
        # 哈希密码
        hashed_password = generate_password_hash(password)
        
        # 插入新用户到数据库
        cursor.execute(
            "INSERT INTO users (username, password, full_name, email, role) VALUES (%s, %s, %s, %s, %s)",
            (username, hashed_password, full_name, email, role)
        )
        db.commit()
        flash('Registration successful! You can now log in.', 'success')
        return redirect('/')
    
    return render_template('register.html')

# Route: User Login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            role = user['role']

            if role == 'admin':
                flash('Login successful!', 'success')
                return redirect('/admin/dashboard')
            else:
                flash('Login successful!', 'success')
                return redirect('/dashboard')
        else:
            flash('Invalid credentials!', 'danger')
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')

    user_id = session['user_id']  # 获取当前用户的ID
    BORROW_PERIOD = 30  # 定义借书期限（以天为单位）

    # 获取用户当前借阅的书籍
    cursor.execute("""
    SELECT b.title, b.author, bl.borrow_date
    FROM borrow_and_return_logs bl
    JOIN books b ON bl.book_id = b.id
    WHERE bl.user_id = %s AND bl.return_date IS NULL
    """, (user_id,))
    current_borrow_records = cursor.fetchall()

    # 计算每本书的到期日期和剩余天数
    for record in current_borrow_records:
        borrow_date = record["borrow_date"]
        due_date = borrow_date + timedelta(days=BORROW_PERIOD)
        days_left = (due_date - datetime.now()).days
        record['due_date'] = due_date.strftime('%Y-%m-%d')  
        record['days_left'] = days_left
        record['is_overdue'] = days_left < 0

    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    
    return render_template('dashboard.html', username=session['username'], user=user, current_borrow_records=current_borrow_records)
@app.route('/borrow', methods=['GET', 'POST'])
def borrow():
    if 'user_id' not in session:
        return redirect('/')
    
    user_id = session['user_id']  # 获取当前用户的ID
    
    if request.method == 'POST':
        book_id = request.form['book_id']
        
        # 检查用户是否已经借了超过10本书
        cursor.execute("SELECT current_borrowed_count FROM users WHERE id = %s", (user_id,))
        result = cursor.fetchone()
        current_borrowed_count = result['current_borrowed_count'] if result else 0

        if current_borrowed_count >= 10:
            flash('You have reached the maximum limit of 10 books.', 'danger')
            return redirect('/dashboard')
        
        # 检查书籍是否存在
        cursor.execute("SELECT * FROM books WHERE id = %s", (book_id,))
        book = cursor.fetchone()

        if book and book['is_available'] == 1:
            # 更新书籍的可用性
            cursor.execute("UPDATE books SET is_available = 0 WHERE id = %s", (book_id,))
            # 记录借书交易，此时 return_date 为 NULL
            cursor.execute("INSERT INTO borrow_and_return_logs (user_id, book_id, borrow_date,return_date) VALUES (%s, %s, NOW(), NULL)", (user_id, book_id))
            # 更新用户的当前借书数量
            cursor.execute("UPDATE users SET current_borrowed_count = current_borrowed_count + 1 WHERE id = %s", (user_id,))
            db.commit()
            flash('Book borrowed successfully!', 'success')
        else:
            flash('Book is not available or does not exist!', 'danger')
        return redirect('/dashboard')

    return render_template('borrow.html')

@app.route('/return', methods=['GET', 'POST'])
def return_book():
    if 'user_id' not in session:
        return redirect('/')
    
    user_id = session['user_id']  # 获取当前用户的ID
    
    if request.method == 'POST':
        book_id = request.form['book_id']
        
        # 检查用户是否有未归还的这本书的记录
        cursor.execute("""
            SELECT id FROM borrow_and_return_logs
            WHERE user_id = %s AND book_id = %s AND return_date IS NULL
        """, (user_id, book_id))
        result = cursor.fetchone()
        
        if result is not None:
            # result 是一个元组，其中包含借书记录的ID
            borrow_log_id = result['id']  # 获取元组中的第一个元素，即借书记录的ID
            
            # 更新书籍的可用性
            try:
                cursor.execute("UPDATE books SET is_available = 1 WHERE id = %s", (book_id,))
                # 更新借书记录的 return_date
                cursor.execute("UPDATE borrow_and_return_logs SET return_date = NOW() WHERE id = %s", (borrow_log_id,))
                # 更新用户的当前借书数量
                cursor.execute("UPDATE users SET current_borrowed_count = current_borrowed_count - 1 WHERE id = %s", (user_id,))
                db.commit()
                flash('Book returned successfully!', 'success')
            except mysql.connector.Error as err:
                db.rollback()
                flash('Error returning book. Please try again.', 'danger')
        else:
            flash('You have not borrowed this book or it has already been returned.', 'danger')
        return redirect('/dashboard')

    return render_template('return.html')

# Route: Admin Dashboard
@app.route('/admin/dashboard')
def admin_dashboard():
    if not is_admin():
        return redirect('/')
    
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    
    return render_template('admin_dashboard.html', books=books, users=users, username=session['username'])

# Route: Add Book
@app.route('/admin/add_book', methods=['GET', 'POST'])
def add_book():
    if not is_admin():
        return redirect('/')
    
    if request.method == 'POST':
        book_title = request.form['title']
        book_author = request.form['author']
        
        # 检查是否已经存在相同标题和作者的书籍
        cursor.execute(
            "SELECT copy_number FROM books WHERE title = %s AND author = %s ORDER BY copy_number DESC LIMIT 1",
            (book_title, book_author)
        )
        existing_book = cursor.fetchone()
        if existing_book:
            copy_number_str = existing_book['copy_number']
            match = re.search(r'\d+', copy_number_str)
            if match:
                last_copy_number = int(match.group())
                new_copy_number = last_copy_number + 1
            else:
                new_copy_number = 1
        else:
            new_copy_number = 1
        
        try:
            cursor.execute(
                "INSERT INTO books (title, author, copy_number, is_available) VALUES (%s, %s, %s, 1)",
                (book_title, book_author, book_title + '-' + str(new_copy_number))
            )
            db.commit()
            flash('Book added successfully!', 'success')
            return redirect('/admin/dashboard')
        except mysql.connector.Error as err:
            db.rollback()
            flash(f'Error: {err}', 'danger')
    
    return render_template('add_book.html')

@app.route('/admin/delete_book/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    if not is_admin():
        return redirect('/')
    
    try:
        # 首先，找到当前借了这本书的用户ID
        cursor.execute("""
        SELECT user_id FROM borrow_and_return_logs
        WHERE book_id = %s AND return_date IS NULL
        """, (book_id,))
        borrowed_users = cursor.fetchall()

        for user in borrowed_users:
            # 更新借书用户的当前借书数量
            cursor.execute("UPDATE users SET current_borrowed_count = current_borrowed_count - 1 WHERE id = %s", (user['user_id'],))
        
        # 删除书籍的借阅和归还记录
        cursor.execute("DELETE FROM borrow_and_return_logs WHERE book_id = %s", (book_id,))
        cursor.execute("DELETE FROM books WHERE id = %s", (book_id,))
        db.commit()
        flash('Book and all related records deleted successfully!', 'success')
    except mysql.connector.Error as err:
        db.rollback()
        flash(f'Error: {err}', 'danger')
    
    return redirect('/admin/dashboard')

@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if not is_admin():
        return redirect('/')
    
    try:
        cursor.execute("UPDATE books SET is_available = 1 WHERE id IN (SELECT book_id FROM borrow_and_return_logs WHERE user_id = %s)", (user_id,))
        # 删除用户的借阅和归还记录
        cursor.execute("DELETE FROM borrow_and_return_logs WHERE user_id = %s", (user_id,))
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        db.commit()
        flash('User and all related records deleted successfully!', 'success')
    except mysql.connector.Error as err:
        db.rollback()
        flash(f'Error: {err}', 'danger')
    
    return redirect('/admin/dashboard')

# Route: Add User
@app.route('/admin/add_user', methods=['GET', 'POST'])
def add_user():
    if not is_admin():
        return redirect('/')
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        full_name = request.form['full_name']
        email = request.form['email']
        role = request.form['role']
        
        try:
            cursor.execute(
                "INSERT INTO users (username, password, full_name, email, role) VALUES (%s, %s, %s, %s, %s)",
                (username, generate_password_hash(password), full_name, email, role)
            )
            db.commit()
            flash('User added successfully!', 'success')
            return redirect('/admin/dashboard')
        except mysql.connector.Error as err:
            db.rollback()
            flash(f'Error: {err}', 'danger')
    
    return render_template('add_user.html')

# Route: Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect(r'\\XEON\share\database.db')
    conn.row_factory = sqlite3.Row
    return conn

def close_db_connection(conn):
    conn.close()

def init_db():
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, intro TEXT NOT NULL, content TEXT NOT NULL)')
    conn.close()

@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/<int:post_id>')
def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()
    return render_template('post.html', post=post)

@app.route('/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if len(request.form['intro']):
            intro = request.form['intro']
        else:
            intro = request.form['content'][0:101]
        conn = get_db_connection()
        conn.execute('INSERT INTO posts (title, intro, content) VALUES (?, ?, ?)', (title, intro, content))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    return render_template('add_post.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    conn = get_db_connection()
    conn.execute(f'DELETE FROM posts WHERE id = {post_id}')
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.before_request
def before_first_request():
    init_db()

if __name__ == '__main__':
    app.run()
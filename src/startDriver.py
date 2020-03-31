import os
from flask import Flask, render_template, flash, request, redirect
import sqlite3
from werkzeug.utils import secure_filename
from TextParser import extract
from database import databaseUtils

UPLOAD_FOLDER = '/database'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route('/viewAll', methods=['GET'])
def api_all():
    conn = sqlite3.connect('database/pythonsqlite.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_contacts = cur.execute('SELECT * FROM cards;').fetchall()
    return render_template("databaseResult.html", items=all_contacts)


@app.route('/delete', methods=['POST', 'GET'])
def delete():
    if request.method == 'POST':
        result = request.form
    name = str(request.form["Name"])
    databaseUtils.delete_user(name)
    return render_template("resultdeleted.html", result=result)


@app.route('/deleteUser')
def deleteuser():
    return render_template('delete.html')


@app.route('/searchUser')
def searchuser():
    return render_template('searchform.html')


@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        pass
    name = str(request.form["Name"])
    conn = sqlite3.connect('database/pythonsqlite.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    sql = """ SELECT * FROM cards WHERE name=?; """
    all_contacts = cur.execute(sql, (name,)).fetchall()
    conn.commit()

    return render_template("searchresult.html", result=all_contacts)


@app.route('/addUser')
def users():
    return render_template('users.html')


@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form
    name = str(request.form["Name"])
    phone = str(request.form["Phone"])
    email = str(request.form["Email"])
    address = str(request.form["Address"])
    databaseUtils.insertVaribleIntoTable(name, phone, email, address)

    return render_template("result.html", result=result)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join('uploads', filename))
            text = extract.ocr('uploads/' + filename)
            return render_template("parsedresult.html", result=text)

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


@app.errorhandler(404)
def page_not_found():
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


if __name__ == "__main__":
    app.run(debug=True)

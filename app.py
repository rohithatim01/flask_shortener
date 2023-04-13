import sqlite3
from hashids import Hashids
from flask import Flask, render_template, request, flash, redirect, url_for

# connect sqlite3 to database
def get_db_connection():
    conn = sqlite3.connect('database.db')
    # set name based access to columns
    conn.row_factory = sqlite3.Row
    return conn

# app details
app = Flask(__name__)
# set salt
app.config['SECRET_KEY'] = 'LrX2NsiBuc'
# set requirements for generating hashID
hashids = Hashids(min_length=4, salt=app.config['SECRET_KEY'])

# index root app accepts both req
@app.route('/', methods=('GET', 'POST'))
def index():
    conn = get_db_connection()

    if request.method == 'POST':
        # get the url which user typed
        url = request.form['url']

        if not url:
            flash('the URL is required! ')
            return redirect(url_for(index))
        
        # insert data into database 'url' with url
        url_data = conn.execute('INSERT INTO urls (original_url) VALUES (?)',
                                (url,))
        # save & close
        conn.commit()
        conn.close()

        # lastrowid retrieves ID of last inserted row
        url_id = url_data.lastrowid
        # contruct hash
        hashid = hashid.encode(url_id)
        # host_url is root url of app
        short_url = request.host_url + hashid

        return render_template('index.html', short_url = short_url)
    
    return render_template('index.html')




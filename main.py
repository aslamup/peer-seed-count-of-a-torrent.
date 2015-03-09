import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import sqlite3
from flask import Flask, redirect
from flask import render_template
from flask import redirect
from flask import Blueprint
from flask import request
from flask.ext.paginate import Pagination
app = Flask(__name__)
mod = Blueprint('torrents', __name__)

@app.route('/')
def home():
    return redirect("/torrent_list/", code=302)
PER_PAGE = 20
START = 0

@app.route('/torrent_list/')
def torrent_list():
    search = False
    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        page = 1
    conn = sqlite3.connect('torrent.db')
    cur = conn.cursor()
    cur.execute("select count(*) from torrents")
    count = cur.fetchall()[0][0]
    to = PER_PAGE
    if page == 1:
        START = 0
    else:
        START = (page-1)*PER_PAGE
    cur.execute("select name,id from torrents limit "+str(START)+","+str(to))
    #cur.execute("select name from torrents limit 10")
    torrents = [dict(name=str(row[0]).encode('utf-8'), id=row[1]) for row in cur.fetchall()]
    pagination = Pagination(page=page, total=count, search=search, record_name='torrents', per_page=PER_PAGE,
                            prev_label="Prev", next_label="Next", link_size=10)
    return render_template('torrentlist.html',torrents=torrents, pagination=pagination, skip=START)


@app.route('/getcount/')
def getcount():
    conn = sqlite3.connect('torrent.db')
    cur = conn.cursor()
    id = request.args.get('id')
    cur.execute("select seeders,leechers from torrents where id=" +"id")
    r_dict = [dict(l_count=str(row[0]), s_count=str(row[1])) for row in cur.fetchall()][0]
    return "seeders : " + r_dict['s_count'] + "\n" + "leechers : " + r_dict['l_count']

 
if __name__ == '__main__':
    app.debug = True
    app.run()

import os
import sqlite3
from sqlite3 import Error
from flask import Flask, request, session, g, redirect, url_for, abort, render_template
from datetime import date

app = Flask(__name__) 
app.config.from_object(__name__)


app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'blog.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='password'
))

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def startup():
    con = sqlite3.connect('blog.db')
    cur = con.cursor()
    SQLString = 'UPDATE tblUsers SET LoginStatus = \'False\''
    cur.execute(SQLString)
    con.commit()
    

@app.route('/')
def index():
    db = get_db()
    cur = db.execute('SELECT * FROM tblUsers')
    bloglist  = cur.fetchall()
    session['logged_in'] = True
    if session['logged_in']:
        print('logged in')
    else:
        print('not logged in')
    return render_template('index.html',bloglist=bloglist)


@app.route('/chooseblog')
def chooseblog():
    if session['logged_in'] != True:
        return redirect('/login')
    else:
        db = get_db()
        cur = db.execute('SELECT BlogTitle FROM tblUsers')
        bloglist  = cur.fetchall()
        return render_template('index.html',bloglist=bloglist)


@app.route('/login',methods=['GET','POST'])
def login():
    error=None
    if request.method == 'POST':
        db = get_db()
        MyUser = request.form['username']
        MyPass = request.form['password']

        SQLString = "SELECT UserID FROM tblUsers WHERE UserLogin LIKE \'" + MyUser + "\' AND UserPass LIKE \'" + MyPass + "\'"

        cur=db.execute(SQLString)

        if cur.fetchone() is not None:
            SQLString2 = 'UPDATE tblUsers SET LoginStatus = \'True\' WHERE UserLogin = \'' + MyUser + "\'"
            db.execute(SQLString2)
            db.commit()
            cur=db.execute(SQLString)
            myID = cur.fetchone()[0]
            print(myID)
            return redirect('/dashboard/' + str(myID))
        else:
            error= "Username or Password is incorrect. Please try again"
            return render_template('login.html',error=error)
    elif request.method == 'GET':
        return render_template('login.html',error=error)

@app.route('/activeblogpost/<id>',methods=['GET','POST'])
def activeblogpost(id):
    db = get_db()
    SQLString = "SELECT PublishStatus FROM tblBlogPosts WHERE BlogID = " + str(id)
    cur = db.execute(SQLString)
    active  = cur.fetchone()[0]

    SQLString2 = "SELECT UserIDRef FROM tblBlogPosts WHERE BlogID = " + str(id)
    cur = db.execute(SQLString2)
    idRef = cur.fetchone()[0]

    activeVal = ""
    if active == "ACTIVE":
        activeVal = "INACTIVE"
    elif active == "INACTIVE":
        activeVal = "ACTIVE"
    else:
        activeVal = "INACTIVE"

    MyError=""
    try:
        db = get_db()
        MYSQLQUERY = 'UPDATE tblBlogPosts SET PublishStatus = \'' + activeVal + '\' WHERE BlogID = ' + str(id)
        print (MYSQLQUERY)
        db.execute(MYSQLQUERY)
        db.commit()
        print("SUCCESS")
        return redirect('/dashboard/' + str(idRef))

    except Error as e:
        MyError = e
        print("FAIL")
        return redirect('/dashboard/' + str(idRef))


@app.route('/categoryview/<id>',methods=['GET','POST'])
def category(id):
    db = get_db()
    SQLString = "SELECT * FROM tblBlogPosts WHERE CategoryIDRef = " + str(id)
    cur = db.execute(SQLString)
    BlogPostSelects = cur.fetchall()

    MyFound =""
    if len(BlogPostSelects) == 0:
        MyFound="None Found"

    SQLString2 = "SELECT CategoryName FROM tblCategories WHERE CategoryID = " + str(id)
    cur=db.execute(SQLString2)
    active = cur.fetchone()[0]
    return render_template('categoryview.html',BlogPostSelects=BlogPostSelects, active = active,MyFound = MyFound)

@app.route('/dashboard/<id>',methods=['GET','POST'])
def dashboard(id):

    db = get_db()

    SQLString = "Select * FROM tblBlogPosts where UserIDRef = " + str(id) + " ORDER BY PublishDate DESC"
    cur = db.execute(SQLString)
    blogposts  = cur.fetchall()

    SQLString2 = "SELECT * FROM tblUsers WHERE UserID = " + str(id)
    cur = db.execute(SQLString2)
    user = cur.fetchall()

    SQLString3 = "SELECT * FROM tblCategories WHERE UserIDRef = " + str(id)
    cur = db.execute(SQLString3)
    categories = cur.fetchall()

    SQLString4 = """Select a.UserID, a.LoginStatus,
    b.BlogID, b.PostTitle, b.PostContent, b.PublishDate, b.PublishStatus

    FROM tblBlogPosts AS b  
     INNER JOIN tblUsers AS a ON b.UserIDRef = a.UserID 

    WHERE a.UserID = """ + str(id)
    cur = db.execute(SQLString4)
    joined = cur.fetchall()

    return render_template('dashboard.html',blogposts=blogposts,user=user,categories=categories,joined=joined)

@app.route('/addpost/<id>',methods=['GET','POST'])
def addpost(id):
    if request.method == 'GET':
        db = get_db()
        SQLString2 = "SELECT * FROM tblUsers WHERE UserID = " + str(id)
        cur = db.execute(SQLString2)
        user = cur.fetchall()
        SQLString3 = "SELECT * FROM tblCategories WHERE UserIDRef = " + str(id)
        cur = db.execute(SQLString3)
        categories = cur.fetchall()
        return render_template('addblogpost.html',user=user,categories=categories)
    elif request.method == 'POST':
        MyError=""
        try:
            db = get_db()
            today = date.today()
            PT = request.form["PostTitle"]
            BC = request.form["BlogContent"]
            if request.form["AddCategory"].isnumeric():
                AC = int(request.form["AddCategory"])
            else:           
                AC = ""

            db.execute('insert into tblBlogPosts (PostTitle,PostContent,UserIDRef,PublishDate,PublishStatus,CategoryIDRef) values (?,?,?,?,?,?)',(PT,BC,id,today,"ACTIVE",AC))
            db.commit()
            return redirect('/dashboard/' + id)
        except Error as e:
            MyError = e
            return redirect('/dashboard/' + id)

   

@app.route('/readpost/<id>',methods=['GET','POST'])
def readpost(id):
        if request.method == 'GET':
            db = get_db()
            SQLString = """Select a.FirstName, a.LastName, a.BlogTitle,
            b.BlogID, b.PostTitle, b.PostContent, b.PublishDate,
            c.CategoryName, c.CategoryID 

            FROM tblBlogPosts AS b  
            INNER JOIN tblUsers AS a ON b.UserIDRef = a.UserID 
            LEFT JOIN tblCategories AS c on c.CategoryID = b.CategoryIDRef

            WHERE b.BlogID = """ + str(id)
            
            cur = db.execute(SQLString)
            post  = cur.fetchall()
            return render_template('readblogpost.html',post=post)

@app.route('/editblogpost/<id>',methods=['GET','POST'])
def editblogpost(id):
    if request.method == 'GET':
        db = get_db()   
        SQLString = "SELECT * FROM tblBlogPosts WHERE BlogID = " + str(id)
        cur = db.execute(SQLString)
        blogpost = cur.fetchall()

        SQLString3 = """SELECT c.CategoryID, c.CategoryName
        FROM tblBlogPosts as B 
        INNER JOIN tblCategories as C ON c.UserIDRef = b.UserIDref
        WHERE b.BlogID = """ + str(id)
        cur = db.execute(SQLString3)
        categories = cur.fetchall()

        return render_template('editpost.html',blogpost=blogpost,categories=categories)
    elif request.method == 'POST':
        db = get_db()
        MyError=""
        try:
            db = get_db()
            PT = request.form["PostTitle"]
            BC = request.form["BlogContent"]
            if request.form["AddCategory"].isnumeric():
                AC = int(request.form["AddCategory"])
            else:           
                AC = ""
            MYSQLQUERY = 'UPDATE tblBlogPosts SET PostTitle = \'' + PT + '\', PostContent = \'' + BC + '\', CategoryIDRef = \'' + str(AC) + '\'  WHERE BlogID = ' + str(id)
            print (MYSQLQUERY)
            db.execute(MYSQLQUERY)
            db.commit()
            SQLString2 = "SELECT UserIDRef From tblBlogPosts WHERE BlogID = " + str(id)
            cur=db.execute(SQLString2)
            active = cur.fetchone()[0]
            return redirect('/dashboard/' + str(active))
        except Error as e:
            MyError = e
            SQLString2 = "SELECT UserIDRef From tblBlogPosts WHERE BlogID = " + str(id)
            cur=db.execute(SQLString2)
            active = cur.fetchone()[0]
            return redirect('/dashboard/' + str(active))


@app.route('/deleteblogpost/<id>',methods=['GET','POST'])
def deleteblogpost(id):
    db = get_db()
    SQLString = "SELECT UserIDRef From tblBlogPosts WHERE BlogID = " + str(id)
    cur=db.execute(SQLString)
    active = cur.fetchone()[0]

    SQLString2 = "DELETE FROM tblBlogPosts WHERE BlogID = " + str(id)
    db.execute(SQLString2)
    db.commit()
    return redirect('/dashboard/' + str(active))


if __name__ == '__main__':
    startup()
    app.run(debug=True)
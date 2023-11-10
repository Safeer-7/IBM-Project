from unicodedata import name
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mail import Mail, Message
# import ibm_db
import hashlib ,secrets
import re
import json
from flask_mysqldb import MySQL
from flask_mysqldb import MySQL
import MySQLdb.cursors
import mysql.connector


app = Flask(__name__)
mail = Mail(app)

# configuration of mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'team.personelexpensetracker@gmail.com'
app.config['MAIL_PASSWORD'] = 'ggdiidnpqiqacncu'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

#connection to MySQL Database

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Jeffrey@08'
app.config['MYSQL_DB'] = 'pet' 

mysql = MySQL(app)

app.secret_key = 'a'
# conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=fbd88901-ebdb-4a4f-a32e-9822b9fb237b.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32731;Security=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=hlv21927;PWD=42CWpSQmvebEyNjl;",'','')

@app.route('/')
@app.route('/index')
def home():
    return render_template('index.html')

@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'Name' in request.form and 'Password' in request.form and 'Email' in request.form :
        username = request.form['Name']
        password = request.form['Password']
        hashpass = hashlib.sha256(password.encode()).hexdigest()
        email = request.form['Email']
        mobileno=request.form['Mobileno']
        job=request.form['Job']
        amount=request.form['Amount']
        limits=request.form['Limit']
        # stmt = ibm_db.prepare(conn,'SELECT * FROM users WHERE name = ?')
        # ibm_db.bind_param(stmt,1,username)
        # ibm_db.execute(stmt)
        # account = ibm_db.fetch_assoc(stmt)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE name = % s', [username] )
        account = cursor.fetchone()

        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO users VALUES ( % s, % s, % s, % s, % s, % s, %s)', [username, email, hashpass, mobileno, job, amount, limits,])
            mysql.connection.commit()

            # prep_stmt = ibm_db.prepare(conn,"INSERT INTO users(name, email, password, mobileno, job, amount, limit) VALUES(?, ?, ?, ?, ?, ?, ?)")
            # ibm_db.bind_param(prep_stmt, 1, username)
            # ibm_db.bind_param(prep_stmt, 2, email)
            # ibm_db.bind_param(prep_stmt, 3, password)
            # ibm_db.bind_param(prep_stmt, 4, mobileno)
            # ibm_db.bind_param(prep_stmt, 5, job)
            # ibm_db.bind_param(prep_stmt, 6, amount)
            # ibm_db.bind_param(prep_stmt, 7, limit)
            # ibm_db.execute(prep_stmt)
            msg = 'You have successfully registered !'

            
    
        return render_template('register.html', msg = msg)
    return render_template('register.html')

@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'Name' in request.form and 'Password' in request.form:
        username = request.form['Name']
        password = request.form['Password']
        hashpass = hashlib.sha256(password.encode()).hexdigest()
        # stmt = ibm_db.prepare(conn,'SELECT * FROM users WHERE name = ? AND password = ?')
        # ibm_db.bind_param(stmt,1,username)
        # ibm_db.bind_param(stmt,2,password)
        # ibm_db.execute(stmt)
        # account = ibm_db.fetch_assoc(stmt)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(" SELECT * FROM users WHERE password = %s ", [hashpass ])   
        account = cursor.fetchone()
        


        if account:
            session['loggedin'] = True
            session['name'] = account['name']
            return redirect(url_for('dashboard'))
        else:
            msg = 'Incorrect username / password !'
            return render_template('login.html', a = msg)
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    uid = session['name']
    return render_template('dashboard.html',name=uid)



@app.route('/graph')
def graph():
    if 'name' in session:
        uid = session['name']

        # stmt1 = ibm_db.prepare(conn, '    SELECT EXTRACT(MONTH FROM expensedate) as month ,sum(amount) as amount FROM expense Where uid= ? group by month(expensedate)')
        # ibm_db.bind_param(stmt1, 1, uid)    
        # ibm_db.execute(stmt1)
        # acc1  = ibm_db.fetch_assoc(stmt1)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT EXTRACT (MONTH FROM expesnedate)as month , sum(amount) as amount FROM expense Where uid = % s group by month(expensedate)", [uid])
        acc1 = cursor.fetchall()

        data = []
        while acc1 != False:
              data.append(acc1)
            #   acc1 = ibm_db.fetch_assoc(stmt1)
              acc1 = cursor.fetchall()

        print(data)

        # stmt2 = ibm_db.prepare(conn, ' SELECT category as cat,sum(amount) as amt FROM expense Where uid= ? group by category order by category ')
        # ibm_db.bind_param(stmt2, 1, uid)    
        # ibm_db.execute(stmt2)
        # acc2  = ibm_db.fetch_assoc(stmt2)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT category as cat , sum(amount) as amt FROM expense Where uid = %s group by category order by category" , [uid])
        acc2 = cursor.fetchall()

        datat = []
        while acc2 != False:
              datat.append(acc2)
            #   acc2 = ibm_db.fetch_assoc(stmt2)
              acc2 = cursor.fetchall()

        print(datat)
        return render_template('graph.html',tdata = data,name=uid , data1 = datat) 


    render_template('graph.html')
  


@app.route('/report' ,methods=["POST","GET"])
def report():
    
       if 'name' in session:
           uid = session['name']
          

        #    stmt = ibm_db.prepare(conn, 'SELECT * FROM users WHERE name = ? ')
        #    ibm_db.bind_param(stmt, 1, uid)    
        #    ibm_db.execute(stmt)
        #    acc = ibm_db.fetch_tuple(stmt)
           cursor = mysql.connection.cursor()
           cursor.execute("SELECT * FROM  users Where name = %s",(uid))
           acc = cursor.fetchall()


        #    stmt1 = ibm_db.prepare(conn, 'SELECT expensedate, expensename, category, amount FROM expense WHERE uid = ? order by expensedate desc ')
        #    ibm_db.bind_param(stmt1, 1, uid)    
        #    ibm_db.execute(stmt1)
        #    acc1  = ibm_db.fetch_assoc(stmt1)
           cursor = mysql.connection.cursor()
           cursor.execute("SELECT expensedate , expensename , category , amount FROM expense Where uid = %s , order by expensedate desc ",[uid])
           acc1 = cursor.fetchall()


           data = []
           while acc1 != False:
              data.append(acc1)
            #   acc1 = ibm_db.fetch_assoc(stmt1)
              acc1 = cursor.fetchall()

           print(data)
           return render_template('report.html',username=acc[1],email=acc[2],mobileno=acc[4],w=acc[6],l=acc[7],tdata = data) 
       return render_template('report.html')



  

@app.route('/profile',methods=["POST","GET"])
def profile():
    if 'name' in session:
        uid = session['name']
        # stmt = ibm_db.prepare(conn, 'SELECT * FROM users WHERE name = ?')
        # ibm_db.bind_param(stmt, 1, uid)    
        # ibm_db.execute(stmt)
        # acc = ibm_db.fetch_tuple(stmt) 
        cursor = mysql.connection.cursor()        
        cursor.execute ("SELECT * FROM users Where name = %s",[uid])
        users = cursor.fetchall()
        return render_template('profile.html',username=users[1],email=users[2],mobileno=users[4],job=users[5],income=users[6],family=users[7])
    return render_template('profile.html')

@app.route('/edit', methods =['GET', 'POST'])
def edit():
   
    if request.method == 'POST' :
        
        msg = ''
        if 'name' in session:
            uid = session['name']
            username = request.form['Name']
            email = request.form['Email']
            mobileno=request.form['Mobileno']
            job=request.form['Job']
            limits=request.form['Limit']
            # prep_stmt = ibm_db.prepare(conn,"UPDATE users SET name = ?, email = ?, mobileno = ?, job = ?, limit = ? WHERE name = ?")
            # ibm_db.bind_param(prep_stmt, 1, username)
            # ibm_db.bind_param(prep_stmt, 2, email)
            # ibm_db.bind_param(prep_stmt, 3, mobileno)
            # ibm_db.bind_param(prep_stmt, 4, job)
            # ibm_db.bind_param(prep_stmt, 5, limits)
            # ibm_db.bind_param(prep_stmt, 6, uid)
            # ibm_db.execute(prep_stmt)
            cursor = mysql.connection.cursor()
            query = ("UPDATE users SET name = %s , email = %s , mobileno = %s , job = %s , limit = %s Where name = %s",(username,email,mobileno,job,limits,uid))
            cursor.execute(query)
            msg = 'You have successfully updated !'
            return render_template('edit.html', msg = msg)
    return render_template('edit.html')

    
@app.route('/add',methods=["POST","GET"])
def add():
    if request.method == "POST":
        if 'name' in session:
            msg1 = ''
            uid=session['name']
            paymode = request.form['paymode']
            expensename = request.form['expensename']
            expensedate = request.form['expensedate']
            category = request.form['category']
            amount = request.form['amount']
            # sqlselect = "SELECT * FROM users WHERE name = ?"
            # stmt = ibm_db.prepare(conn,sqlselect)
            # ibm_db.bind_param(stmt, 1, uid)
            # ibm_db.execute(stmt)
            # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor = mysql.connection.cursor()
            query1 = ("SELECT * FROM users Where name = %s",[uid])
            cursor.execute(query1)
            # sqlinsert = 'INSERT INTO expense(uid, paymode, expensename , expensedate, category, amount ) VALUES (?, ?, ?, ?, ?, ?)'
            # prep_stmt = ibm_db.prepare(conn,sqlinsert)
            # ibm_db.bind_param(prep_stmt, 1, uid)
            # ibm_db.bind_param(prep_stmt, 2, paymode)
            # ibm_db.bind_param(prep_stmt, 3, expensename)
            # ibm_db.bind_param(prep_stmt, 4, expensedate)
            # ibm_db.bind_param(prep_stmt, 5, category)
            # ibm_db.bind_param(prep_stmt, 6, amount)
            # ibm_db.execute(prep_stmt)
            query2 = ("INSERT INTO expense (uid =%s , paymode =%s , expensename =%s , expensedate=%s , category =%s , amount =%s )",(uid,paymode,expensename,expensedate,category,amount))
            cursor.execute(query2)
            # prep_stmt1 = ibm_db.prepare(conn, "UPDATE users SET amount = amount - ? WHERE name = ?")
            # ibm_db.bind_param(prep_stmt1, 1, amount)
            # ibm_db.bind_param(prep_stmt1, 2, uid)
            # ibm_db.execute(prep_stmt1)
            query3 = ("UPDATE users SET  amount = amount - %s , Where name = %s",(amount,uid))
            cursor.execute(query3)
            msg1 = 'You have successfully added your expense'

            # sqlselect = "SELECT * FROM users WHERE name = ?"
            # stmt2 = ibm_db.prepare(conn,sqlselect)
            # ibm_db.bind_param(stmt2, 1, uid)
            # ibm_db.execute(stmt2)
            # acc = ibm_db.fetch_tuple(stmt2)  
            cursor.execute("SELECT * FROM users Where name = %s",(uid))
            acc = cursor.fetchone()

            wallet=acc[6]
            limits=acc[7]
            email=acc[2]

            wal = str(wallet)
            lim = str(limits)

            if wallet <= limits:
                 msg = Message('Hello', sender = 'team.personelexpensetracker@gmail.com', recipients = [email])
                 msg.body = " Hello" + uid +", You exceed your wallet limit fo Rs. "+ lim + ".Now your Wallet Balance is Rs."+ wal +" ,Please add balance or do necessary action :)"
                 mail.send(msg)
                
        return render_template('add.html',a = msg1)
    return render_template('add.html')

@app.route('/wallet',methods=["POST","GET"])
def wallet():
    if request.method == "POST":
        if 'name' in session:
            msg = ''
            name=session['name']
            amount=request.form['Amount']
            # prep_stmt = ibm_db.prepare(conn, "UPDATE users SET amount = amount + ?  WHERE name = ?")
            # ibm_db.bind_param(prep_stmt, 1, amount)
            # ibm_db.bind_param(prep_stmt, 2, name)
            # ibm_db.execute(prep_stmt)
            cursor = mysql.connection.cursor()
            query = ("UPDATE users SET  amount = amount + %s Where name = %s",(amount,name))
            cursor.execute(query)
            msg = 'You have successfully added your amount' 

            # sqlselect = "SELECT * FROM users WHERE name = ?"
            # stmt2 = ibm_db.prepare(conn,sqlselect)
            # ibm_db.bind_param(stmt2, 1, name)
            # ibm_db.execute(stmt2)
            # acc = ibm_db.fetch_tuple(stmt2) 
            cursor.execute("SELECT * FROM users Where name = %s",(name))
            acc = cursor.fetchone()

            wallet = acc[6]
            limits = acc[7]
                
              	
        return render_template('wallet.html',a = msg,s= wallet,l=limits,name = name)
    return render_template('wallet.html')




@app.route('/help')
def help():
    uid=session['name']
    return  render_template('help.html',name=uid)





@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('Name', None)
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0',port=8080)

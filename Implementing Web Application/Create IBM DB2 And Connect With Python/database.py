from __future__ import print_function
from flask import Flask, render_template, url_for, request, redirect, session
import sqlite3 as sql
import re
import ibm_db
conn =ibm_db.connect("DATABASE=bludb;HOSTNAME=21fecfd8-47b7-4937-840d-d791d0218660.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31864;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=qqq18090;PWD=UmfcRew1ejxVxq34",'','')

app=Flask(__name__)
app.secret_key ='kgsp1106'

@app.route('/')
def signin():
    return render_template('account.html')



@app.route('/user/<id>')
def user_info(id):
    with sql.connect('inventorymanagement.db') as con:
        con.row_factory=sql.Row
        cur =con.cursor()
        cur.execute(f'SELECT * FROM register WHERE email="{id}"')
        user = cur.fetchall()
    return render_template("index.html", user=user[0])

@app.route('/login',methods =['GET', 'POST'])
def login():
    global userid
    msg = ''
   
  
    if request.method == 'POST' :
        un = request.form['username']
        pd = request.form['password_1']
        sql = "SELECT * FROM register WHERE username =? AND password_1=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,un)
        ibm_db.bind_param(stmt,2,pd)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print (account)
        if account:
            session['loggedin'] = True
            session['id'] = account['USERNAME']
            userid=  account['USERNAME']
            session['username'] = account['USERNAME']
            msg = 'Logged in successfully !'
            
            return render_template('index.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('account.html', msg = msg)

        
@app.route('/accessbackend', methods=['POST','GET'])
def accessbackend():
    mg=''
    if request.method == "POST":
        username=request.form['username']
        email=request.form['email']
        pw=request.form['password'] 
        sql='SELECT * FROM register WHERE email =?'
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.execute(stmt)
        acnt=ibm_db.fetch_assoc(stmt)
        print(acnt)
            
        if acnt:
            mg='Account already exits!!'
            
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mg='Please enter the avalid email address'
        elif not re.match(r'[A-Za-z0-9]+', username):
            ms='name must contain only character and number'
        else:
            insert_sql='INSERT INTO register VALUES (?,?,?,?,?,?)'
            pstmt=ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(pstmt,1,username)
            ibm_db.bind_param(pstmt,2,"firstname")
            ibm_db.bind_param(pstmt,3,"lastname")
            ibm_db.bind_param(pstmt,4,"123456789")
            ibm_db.bind_param(pstmt,5,email)
            ibm_db.bind_param(pstmt,6,pw)
            ibm_db.execute(pstmt)
            mg='You have successfully registered click signin!!'
            return render_template("account.html")    

            
            
         
    elif request.method == 'POST':
        msg="fill out the form first!"
    return render_template("account.html",meg=mg)    

 

if __name__ == '__main__':
    app.run(debug=True)
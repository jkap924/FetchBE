import sqlite3
import json
from flask import Flask, render_template, request, url_for, redirect, Response
from datetime import datetime

#a method that will connect to the database and return the connection variable
def get_db_connection():
    conn = sqlite3.connect('database.db')
    #conn.row_factory = sqlite3.Row
    return conn

#will connect to the database and print all of it to the console
#will not return anything
def print_db():
    conn = get_db_connection()
    cur = conn.cursor()
    with conn:
        cur.execute('SELECT * FROM posts')
        print(cur.fetchall())
    conn.close()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'jihjbok'

#adds a route for a basic home page
@app.route('/')
def index():
    return render_template('index.html')

#adds a route with a form to insert payer, points, and timestamp
@app.route('/addTransaction', methods=('GET', 'POST'))
def addTransaction():
    if request.method == 'POST':
        payer = request.form['payer']
        points = request.form['points']
        time = request.form['time']

        conn = get_db_connection()
        conn.execute('INSERT INTO posts (payer, points, time) VALUES (?, ?, ?)',
                     (payer, points, time))
        conn.commit()
        conn.close()
        return Response('{"message":"Transaction Added"}', status=202)
            
        
    return render_template('addTransaction.html')

@app.route('/spendPoints', methods=('GET', 'POST'))
def spendPoints():
    if request.method == 'POST':
        #get points from from
        spendPoints = int(request.form['points'])

        #connect to database
        conn = get_db_connection()
        cur = conn.cursor()

        response = {}
        cur.execute('SELECT payer, points FROM posts ORDER BY time ASC')
        result = cur.fetchone()

        #loop while there are more transactions and more points to spend
        while (result != None) and (spendPoints > 0):
            payer, points = result

            if payer not in response:
                response[payer] = 0

            #if transaction has less points than the user is trying to spend
            if spendPoints > points:
                #use everything in this transaction
                spendPoints -= points
                #log the payer in the response
                response[payer] -= points
            else:
                #if the transaction has enough to finish spending, use the rest 
                response[payer] -= spendPoints
                spendPoints = 0

            #get next transaction
            result = cur.fetchone()

        #get current date and time for new transactions
        now = datetime.now()
        timestamp = now.strftime("%Y-%d-%mT%H:%M:%SZ")

        #loop through updated transactions and insert into database
        for payer, points in response.items():
                cur.execute('INSERT INTO posts (payer, points, time) VALUES (?, ?, ?)',
                         (payer, points, timestamp))

        #return response
        return json.dumps(response)

    return render_template('spendPoints.html')  

#adds a route that will display the current point balance as a JSON
@app.route('/pointsBalance', methods=['GET'])
def pointsBalance():
    conn = get_db_connection()
    cur = conn.cursor()
    balance = {}
    cur.execute('SELECT payer, points FROM posts ORDER BY time ASC')
    result = cur.fetchone()

    #loop through list until out of transactions
    while result != None:
        payer, points = result

        #check if payer is already in list
        if payer not in balance:
            balance[payer] = 0

        balance[payer] += points
        # get next transaction
        result = cur.fetchone()

    return (json.dumps(balance))
        
    conn.close()
    

if __name__ == "__main__":
    app.run(debug=True, port='5000')

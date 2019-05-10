from flask import Flask, render_template, request
import sqlite3 as sql
import pandas as pd
import numpy as np
app = Flask(__name__)
import os
import matplotlib as mpl
mpl.use('Agg')
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
from scipy.spatial import distance

#import time
#import random
#import redis

#Kevin Thomas
#4593

#conn = sqlite3.connect('database.db')
# print("Opened database successfully")
#conn.execute('drop table earthquake')
#conn.execute('CREATE TABLE Earthquake (time text,latitude real,longitude real,depth real,mag real,magType text,nst real,gap real,dmin real,rms real,net text,id text,updated text,place text,type text,horizontalError real,depthError real,magError real,magNst real,status text,locationSource text,magSource text)')
# print("Table created successfully")
# conn.close()

port = int(os.getenv('PORT', 8000))
@app.route('/')
def home():
   return render_template('home.html')

@app.route('/enternew')
def upload_csv():
   return render_template('upload.html')

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
       con = sql.connect("database.db")
       csv = request.files['myfile']
       file = pd.read_csv(csv)
       file.to_sql('Earthquake', con, schema=None, if_exists='replace', index=True, index_label=None, chunksize=None, dtype=None)	  
       con.close()
       return render_template("result.html",msg = "Record inserted successfully")
	   
@app.route('/list')
def list():
   con = sql.connect("database.db")
 
   
   cur = con.cursor()
   cur.execute("select * from Earthquake")
   
   rows = cur.fetchall();
   con.close()
   return render_template("list.html",rows = rows)

@app.route('/course')
def course():
   return render_template('course.html')
   
@app.route('/options' , methods = ['POST', 'GET'])
def options():
   con = sql.connect("database.db")
   print (request.form['val1'])
   cur = con.cursor()
   cur.execute('select Instructor from Earthquake WHERE Course = ?',(request.form['val1'], ))
   rows = cur.fetchall()
   con.close()
   return render_template("list1.html",rows =rows)   
   
@app.route('/instructor')
def instructor():
   return render_template('instructor.html')
   
@app.route('/values' , methods = ['POST', 'GET'])
def values():
   con = sql.connect("database.db")
   print (request.form['val1'])
   cur = con.cursor()
   cur.execute('select Course,Section,Room from Earthquake WHERE Instructor = ?',(request.form['val1'], ))
   rows = cur.fetchall()
   con.close()
   return render_template("list2.html",rows =rows)   
   



   
if __name__ == '__main__':
   app.run(host='0.0.0.0', port=port,debug = True)

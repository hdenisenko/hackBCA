from flask import Flask, redirect, request, render_template
from pymongo import MongoClient
import math, random


app=Flask(__name__)

def make_cat_ratings(cats):
    ratings = {}
    for c in cats:
        ratings[c]=random.randrange(10)
    return ratings

def make_all_ratings(users,cats):
    ratings=[]
    #print users
    for u in users:
        u["cat_rating"] = make_cat_ratings(cats)
        ratings.append(u) 
    return ratings

def dist(a,b):
    s = 0
    for c in a.keys():
        if c in b:
            s = s + pow(a[c]-b[c],2)
        return 1/(1+math.sqrt(s))

def calc_similarities(ratings):
    #print ratings
    for i in ratings:
        v = i['cat_rating']
        for j in v:
            print v['cat1']
            #print j.value
            #print i,j,dist(ratings[i],ratings[j])
            

# c = Connection()
client = MongoClient('mongodb://localhost:27017/')
db = client.testdb
users = db.users

list_of_users=[]

def getUsers():
    res = users.find({},{'_id':False})
    return [x for x in res]

def changepassword(username,password):
    res = users.update({'username':username},
                       {'$set':{'password':password}})
    return None


def addUser(username,password):
    res = users.find({'username':username})
    if res.count()>0:
        return None
   
    result = users.insert({'username':username,'password':password}) 
    return {'username':username,'password':password}


def checkCredentials(username,password):
    res=users.find({"username":username,"password":password})
    return res.count()==1

#@app.route("/user", methods=['get','post'])
#def user():
    

@app.route("/register", methods=['get','post'])
def register():
    if request.method=="GET":
        return render_template("Register.html")
    if request.method=="POST":
        u=request.form['username']
        p=request.form['pwd']
        e=request.form['email']
    # if request.form['submit']=='Submit':
        check = addUser(u,p)
        users_list=users.find({})
        for user in users_list:
            list_of_users.append(user)
        cats = ['cat1', 'cat2', 'cat3']
        ratings = make_all_ratings(list_of_users,cats)
        #print ratings
        similarity = calc_similarities(ratings)
        #print ratings
        return render_template("Index.html")

##@app.route('/home', methods = ['get', 'post'])
##def test():
##    if request.method=="POST":
##        u=request.form['username']
##        p=request.form['password']
##        e=request.form['email']
##        #if request.form['submit']=='Submit':
##        check= addUser(u,p,e)
##        users_list=users.find({})
##        for user in users_list:
##            list_of_users.append(user)
##        cats = ['cat1', 'cat2', 'cat3']
##        ratings = make_all_ratings(list_of_users, cats)
##        #print ratings
##        similarity = calc_similarities(ratings)
##        #print ratings
##        return render_template("Index.html")
    

@app.route('/Signin',methods=['get','post'])
def signin():
    if request.method=="GET":
        return render_template("Register.html")
##    u=request.form['username']
##    q=request.form['password']
##    if request.form['submit']=="Submit":
##        check=addUser(u,q)
##        return render_template("Register.html")
    
@app.route("/", methods=['get'])
def index():
    return render_template("Index.html")



if __name__=="__main__":
    app.secret_key="cattastic"
    app.debug=True
    app.run()
    

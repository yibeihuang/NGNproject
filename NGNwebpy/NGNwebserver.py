#!/usr/bin/env python
import MySQLdb
import web
import json
#import newtable
from time import strftime
from web import form

render = web.template.render('templates/')
db = web.database(dbn='mysql', user='root',pw='Perfectfox1992',db='NGNproject')

urls = (
   '/','index','/read','read','/login','login', '/calcuBill', 'calcuBill','/add','add', '/register','register',
   '/login_user','login_user','/add_account','add_account'
)

vpass = form.regexp(r".{3,20}$", 'must be between 3 and 20 characters')
#vemail = form.regexp(r".*@.*", "must be a valid email address")
vip = form.regexp(r"((?:(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d))))", "must be a valid ip address")#the regexp of IP

register_form = form.Form(
    form.Textbox("username", description="Username"),
    #form.Textbox("email", vemail, description="E-Mail"),
    form.Textbox("ip", vip, description="IP Address"),
    form.Password("password", vpass, description="Password"),
    form.Password("password2", description="Repeat password"),
    form.Button("submit", type="submit", description="Register"),
    validators = [
        form.Validator("Passwords did't match", lambda i: i.password == i.password2)]

)

Manager_login = form.Form(
    form.Textbox("Username", description="Username"),
    form.Password("Password", description="Password"),
	# form.regexp('\d+', "Must be a digit"), form.Validator("Password Invalid", lambda x: x.Password == 123)),
    form.Button("submit", type="submit", description="Login"),
    validators = [
        form.Validator("User doesn't exist", lambda i: i.Username == "Manager"),
	form.Validator("Invalid Password", lambda x:x.Password == 123)]

)

global UserData
UserData = [["IPs","UserName","Electricity","Time","Bill"]]
global tp
tp = [0,0,0]
global new
new = MySQLdb.connect("localhost","root","Perfectfox1992",'NGNproject')
global cursor
cursor = new.cursor()


class index:
    def POST(self):
	data = web.input()
        db.insert('generator', IPs = data.IPs, Electricity = data.Electricity, Time = data.Time)

class read:
    def GET(self):
        #new = MySQLdb.connect("localhost","root","Perfectfox1992",'NGNproject')
        #cursor = new.cursor()
        cursor.execute ("select IPs, Electricity, Time, Bill, UserName from generator")
        table = cursor.fetchall ()
        new.close()

        for row in table:
                IPs = row[0] #transform the format of IPs
                UserName = row[4]
                Electricity = row[1]
                Time = row[2]
                Time = Time.isoformat() #to fit in the format of jason
                Bill = row[3]
                tp = [IPs, UserName, Electricity, Time, Bill]
                UserData.append(tp)

        return render.chart1(json.dumps(UserData))

#add calculated bill to database
class add: 
    def POST(self):
    	receive = web.input()
	#print receive
	for key in receive:
            db.update('generator', where="UserName='"+key+"'", Bill=receive[key])
        raise web.seeother('/read')

class calcuBill:
    def GET(self):
    	todos = db.select('generator')
    	cssfiles = "/static/body2.css" #path must be added here, not applicable in html files
	return render.calcuBill(todos, cssfiles)

class register:
    def GET(self):
        # do $:f.render() in the template
	print 'reached get func'
	print '================='
        f = register_form()
        cssfiles = "/static/body2.css" #path must be added here, not applicable in html files
        return render.register(f, cssfiles)
	
    def POST(self):
        f = register_form()
	    cssfiles = "/static/body2.css" #path must be added here, not applicable in html files
        if not f.validates():
            return render.register(f, cssfiles)
        else:
        #    receive = web.input()
	    print '============POST==========='
	    try:
            	db.insert('User', UserName=f.d.username , IPs=f.d.ip, Password=f.d.password)
            except:
		pass
        #    cursor.execute("UPDATE generator INNER JOIN User ON generator.IPs=User.IPs SET generator.UserName=User.UserName")
            db.update('generator', where="IPs='"+f.d.ip+"'", UserName=f.d.username)
            new.commit()
	   # myvar = dict(name=f.d.username)
           # result = db.select('generator', myvar, where="UserName = $name")
	    insert_stmt = (
  "SELECT*FROM generator where UserName =  "
  " %s "
)
            data = (f.d.username)
            cursor.execute(insert_stmt, data) 
	   #print cursor.execute("SELECT*FROM generator")
	    result = cursor.fetchall()
	    print result
	    print "=======******=========="
	    cssfiles = "/static/body2.css" #path must be added here, not applicable in html files

	    return render.userAccount(result,cssfiles)

class login:
    def GET(self):
        f = Manager_login()
        cssfiles = "/static/body2.css"
        return render.Login_Manager(f, cssfiles)
    def POST(self):
        f = Manager_login()
        cssfiles = "/static/body2.css" #path must be added here, not applicable in html files
        if not f.validates():
            return render.Login_Manager(f, cssfiles)
        else:
            raise web.seeother('/calcuBill')

class login_user:
    def GET(self):
        return render.Login_User()

class add_account:
    def POST(self):
        receive = web.input()
        print receive
        print receive.UserName
        cursor.execute ("select UserName, Password from User")
        table = cursor.fetchall ()
        cssfiles = "/static/body2.css" #path must be added here, not applicable in html files
        print "=================="
	print table
        print table[0][1]
        ####fetch data from database
        for i in range(len(table)):
                if table[i][0] == receive.UserName and str(table[i][1]) == receive.Password:
            		data = (receive.UserName)
			cursor.execute("SELECT*FROM generator where UserName='"+receive.UserName+"'")
            		result = cursor.fetchall()                    
			return render.userAccount(result,cssfiles)
        raise web.seeother('/login_user')

if __name__ == "__main__":
    app = web.application(urls,globals())
    app.run()



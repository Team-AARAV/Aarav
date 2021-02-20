from flask import Flask , redirect, url_for,render_template, request,session,flash
#from flask_sqlalchemy import sqlalchemy
from dbconnect import connection
from wtforms import Form, TextField,BooleanField,PasswordField,validators,StringField
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart
import gc
import smtplib
from flask_mail import Mail,Message
from mail import *
app = Flask(__name__)
app.config.update(
		DEBUG = True,
		#EMAIL SETTINGS
		MAIL_SERVER = 'smtp.gmail.com',
		MAIL_PORT = 465,
		MAIL_USE_SSL = True,
		MAIL_USERNAME = 'pythonmac9@gmail.com',
		MAIL_PASSWORD = 'hitman31macintosh9'

		)
mail = Mail(app)




app.secret_key="warmachineroxxx"

app.static_folder='static'
@app.route("/")
def home():
	return render_template("index.html")

@app.route("/login",methods=["POST","GET"])
def login():
	error=''
	try:
		c,conn = connection()
		#if "username" in session:
				#return redirect(url_for("dashboard"))
		#return render_template("login.html")
		if request.method == "POST":
			data = c.execute("SELECT * FROM Users WHERE username=(%s)",(thwart(request.form['nm'],),))
			data = c.fetchone()[2]
		


		#if not data:
			#flash("Invalid Credentials, please try again.")
			#return render_template("login.html")



			if sha256_crypt.verify(request.form['psw'], data):
				session['logged_in'] = True
				session['username'] = request.form['nm']

				#flash("you are now logged in")
				user = session['username']
				#return render_template("user.html",user=user)
				return redirect(url_for("dashboard"))

			
			elif "username" in session:
				return redirect(url_for("dashboard"))



			else:
			
				gc.collect()
				flash("Invalid Credentials, please Try again.") 
				return render_template("login.html",error=error)        


	   
			#user = request.form["nm"]
			#session["username"] = user
			#return redirect(url_for("dashboard"))

		elif(session['logged_in_new']==True):
			session['logged_in_new']=False	
			return render_template("login.html")

		elif "username" in session:
			return redirect(url_for("dashboard"))

		if request.method == "GET" and "username" not in session:
			return render_template("login.html")

			

		else:
			return render_template("login.html",error=error)	
	
	except Exception as e:

		if "username" in session:
			return redirect(url_for("dashboard"))
		if request.method == "GET" and "username" not in session:
			return render_template("login.html")	
			

		flash("Invalid Credentials, please Try again.") 
		return render_template("login.html",error=error)




	
@app.route("/dashboard")
def dashboard():
	if "username" in session:
		user = session["username"]
		return render_template("user.html",user=user)
	else:
		return redirect(url_for("login"))


@app.route("/logout")
def logout():

	if "username" not in session:
		flash("login first!")
		return redirect(url_for("login"))
	

	 
	flash(f"You have been logged out!","info")
	session.pop("username",None)
	
	return redirect(url_for(("login")))


@app.route("/fitMe")
def fitme():
	return render_template("indexx.html")

@app.route("/textovervideo")
def yoga():
	return render_template("textovervideo.html")

@app.route("/2ndpage")
def yoga2():
	return render_template("2ndpage.html")

@app.route("/reciept")
def reciept():
	return render_template("reciept.html")


@app.errorhandler(404)

def page_not_found(e):
	return render_template("404.html")


class RegistrationForm(Form):
	username = TextField('Username',[validators.Length(min=4,max=20)])
	email = TextField('Email Address',[validators.Length(min=6,max=50)])
	password = PasswordField('Password',[validators.Required(),
										 validators.EqualTo('confirm',message="Passwords Must Match.")])
	confirm = PasswordField('Repeat Password')
	#accept_tos = BooleanField('I accept the <a href="/tos/>Terms of Service </a>and the <a href="/privacy/">Privacy Notice</a>',[validators.Required()])

class ForgotPassword(Form):
	email_id = TextField('Email Address',[validators.Length(min=6,max=50)])



@app.route("/register/",methods=["POST","GET"])
def register_page():
	try:	
		form = RegistrationForm(request.form)
		if request.method == "POST" and form.validate():

			username = form.username.data
			email = form.email.data
			ps = form.password.data
			print("information",username,email,ps)
			password = sha256_crypt.encrypt((str(form.password.data)))
			c,conn = connection()
			x = c.execute("SELECT uid FROM Users WHERE username = (%s)",(thwart(username,),))

			if x:
				
				flash("That username is already taken, please choose another")
				print("<h1>iam working!</h1>")

				return render_template('login.html',form=form)



			else:
				c.execute("INSERT INTO Users(username,password,email,tracking) VALUES(%s,%s,%s,%s)",(thwart(username,),thwart(password,),thwart(email,),thwart("/login/"),))

				conn.commit()

				flash("Thanks for registering!")
				c.close()
				conn.close()
				gc.collect()

				session['logged_in_new'] = True
				session['username'] = username
				
				return redirect(url_for("login"))
		


		return render_template("register.html",form=form)

		
	except Exception as e:
		return(str(e))





@app.route("/mmail")
def mmail():
	return render_template("forgot_password.html")		

@app.route('/send_mail',methods=["GET","POST"])
def sendd_mail():
	
		
		if request.method=="POST":

			email = request.form["Email"]
			c,conn = connection()
			x = c.execute("SELECT uid FROM Users WHERE email = (%s)",(thwart(email,),))
			if x:
				
				msg = Message("send mail tutroial!",
		  		  sender = "pythonmac9@gmail.com",
		  		  recipients = [email])
				msg.body = "Yo!Its me Aryan! Sent this message through the Flask app"
				mail.send(msg)
				return('Mail-sent')

				
			else:

				return redirect(url_for("mmail"))
		return("Invalid try again")


@app.route("/menu")
def menu():
	return render_template("menu.html")


@app.route("/checkout",methods = ["GET","POST"])
def checkout():
	items = ['kadhai paneer','kulcha']
	confirm = list()
	if request.method=="POST":
		req = request.form
		print(req)
		return redirect(request.url)
		

	return render_template("menu.html")		




if __name__ == "__main__":
	app.run(debug=True)






'''username = TextField('Username',[validators.Length(min=4,max=20)])
email = TextField('Email Address',[validators.Length(min=6,max=50)])
password = PasswordField('Password',[validators.Required(),
										 validators.EqualTo('confirm',message="Passwords Must Match.")])
confirm = PasswordField('Repeat Password')'''


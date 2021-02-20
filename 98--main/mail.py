from flask import Flask , redirect, url_for,render_template, request,session,flash

from flask_mail import Mail,Message

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
				msg.body = "Yo!\nIts me Aryan! Sent this message through the Flask app"
				mail.send(msg)
				return('Mail-sent')

				
			else:

				return redirect(url_for("mmail"))

		return("Invalid try again")

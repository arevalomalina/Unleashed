from flask import Flask, render_template, redirect, request
import model

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("form.html")

@app.route("/login", methods=['POST'])
def login():
	new_user = model.User( 
						first_name='dummy', 
						last_name='wiesen', 
						telephone=request.form['Phone'],
						address='some address',
						ICE='ICE',
						email='email@email',
						password='password')
	model.session.add(new_user)
	model.session.commit()
	
	return render_template("login.html")

if __name__=="__main__":
	app.run(debug = True)
from flask import Flask, render_template, redirect, request
import model

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("form.html")

@app.route("/login", methods=['POST'])
def login():
	print request.form
	new_user = model.User(first_name=request.form['First_Name'], 
						last_name=request.form['Last_Name'], 
						telephone=request.form['Phone'],
						address=request.form['Address'],
						ICE_name=request.form['ICE_Name'],
						ICE_phone=request.form['ICE_Phone'],
						email=request.form['Email'],
						password=request.form['Password'])

	new_dog = model.Dog(name=request.form['Dog_Name'],
						breed=request.form['Dog_Breed'],
						age=request.form['Age'],
						gender=request.form['Gender'],
						weight=request.form['Weight'])

	new_vet = model.Veterinarian(first_name=request.form['vet_name_first'],
								last_name=request.form['vet_name_last'],
								address=request.form['address'],
								telephone=request.form['telephone'])

	model.session.add(new_user)
	model.session.add(new_dog)
	model.session.add(new_vet)
	model.session.commit()

	
	return render_template("login.html")

if __name__=="__main__":
	app.run(debug = True)
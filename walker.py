from flask import Flask, render_template, redirect, request
import model
import hashlib
import datetime

app = Flask(__name__)
@app.route("/")
def land():
	return render_template("landing.html")

@app.route("/register")
def view_form():
	return render_template("form.html")

@app.route("/login", methods=['GET'])
def login():
	return render_template("login.html")

@app.route("/login", methods=['POST'])
def login_post():
	user = model.session.query(model.User).filter_by(email = request.form['Email']).filter_by(password = sha1(request.form['Password'])).first()
	if user is not None:
		return redirect('/book')
	else:
		return redirect('/login')

@app.route("/register", methods=['POST'])
def register():
	print request.form
	new_user = model.User(first_name=request.form['First_Name'], 
						last_name=request.form['Last_Name'], 
						telephone=request.form['Phone'],
						address=request.form['Address'],
						ICE_name=request.form['ICE_Name'],
						ICE_phone=request.form['ICE_Phone'],
						email=request.form['Email'],
						password=sha1(request.form["Password"]))

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

	return redirect('/login')
	
@app.route('/book', methods=['GET'])
def appointment_form():
	return render_template("calendar.html")

@app.route('/book', methods=['POST'])
def appointment_book():
	d = request.form['date']
	mydate = datetime.datetime.strptime(d, "%Y-%m-%d")
	new_appt = model.Appointment(date=mydate,
								time_slot=request.form['time_slots'])

	model.session.add(new_appt)
	model.session.commit()
	return redirect('/')


def sha1(str):
	sha1 = hashlib.sha1()
	sha1.update(str)
	return sha1.hexdigest()

if __name__=="__main__":
	app.run(debug = True)
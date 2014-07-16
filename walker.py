from flask import Flask, render_template, redirect, request, make_response
import model
import hashlib
import datetime, os
import stripe
import jinja2

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "/Users/Malina/src/walker_webapp/static/img"
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
        user_id = request.cookies.get('user_id')
        resp = make_response(redirect('/profile'))
        resp.set_cookie('user_id', str(user.id))
        return resp
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
                        weight=request.form['Weight'],
                        nickname=request.form['Nickname'])

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
    return redirect('/payment')

@app.route('/payment', methods=['GET'])
def get_card():
    return render_template("payment.html")

@app.route('/payment', methods=['POST'])
def payment():
    stripe.api_key = ""
    token = request.form.get('stripeToken')

    try:
        charge = stripe.Charge.create(
            amount=1000, # amount in cents, again
            currency="usd",
            card=token,
            description="payinguser@example.com")

    except stripe.CardError, e:
        return "error"
  # The card has been declined
        pass
    return "success"

@app.route('/profile')
def user_profile():
    user_id = request.cookies.get('user_id')
    user = model.get_user_by_id(user_id)
    if model.User.query.get(user_id) is not None:
        return render_template('profile.html', display_user = user)
    else:
        redirect('/login')

@app.route('/photo_upload', methods=['POST'])
def send_photo():
    user_id = request.cookies.get('user_id')
    pic = request.files['file']
    filename = "%s_%s" % (user_id, pic.filename)
    pic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename ))
    model.update_profile_pic(filename, user_id)
    return redirect ('/profile')

@app.route('/logout')
def logout():
    user_id = request.cookies.get('user_id')
    resp = make_response(redirect('/'))
    resp.set_cookie('user_id', expires=0)
    return resp


def sha1(str):
    sha1 = hashlib.sha1()
    sha1.update(str)
    return sha1.hexdigest()

if __name__=="__main__":
    app.run(debug = True)
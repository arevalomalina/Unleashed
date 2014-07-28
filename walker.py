import datetime
from flask import Flask, render_template, redirect, request, make_response
import model
import hashlib
import datetime, os
import stripe
import jinja2
from flask_wtf import Form
import form_validation

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "/Users/Malina/src/walker_webapp/static/img"
@app.route("/")
def land():
    return render_template("landing.html")


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

@app.route("/register")
def view_form():
    form = form_validation.RegistrationForm()
    print form
    print dir(form)
    return render_template("form.html", form = form)

"""@app.route('/register', methods=['POST'])
def register():
    form = form_validation.RegistrationForm(request.form)
    print form.validate()
    if form.validate():
        print "success"
        return render_template('index.html')
    else:
        return render_template('newform.html', form=form)

"""
@app.route("/register", methods=['POST'])
def register():
    new_user = model.User(first_name=request.form['First_Name'], 
                        last_name=request.form['Last_Name'], 
                        telephone=request.form['Phone'],
                        address=request.form['Address'],
                        ICE_name=request.form['ICE_Name'],
                        ICE_phone=request.form['ICE_Phone'],
                        email=request.form['Email'],
                        password=sha1(request.form["Password"]))
    model.session.add(new_user)

    counter = 1
    while True:
        if 'Dog_Name%s' % counter in request.form:
            new_dog = model.Dog(name=request.form['Dog_Name%s' %counter],
                breed=request.form['Dog_Breed%s' %counter ],
                age=request.form['Age%s' %counter],
                gender=request.form['Gender%s' %counter],
                weight=request.form['Weight%s' %counter],
                nickname=request.form['Nickname%s' %counter])

            user_dog = model.User_Dog(dog=new_dog, 
                                    user=new_user)

            model.session.add(user_dog)
            model.session.add(new_dog)
            counter +=1 
        else:
            break

    model.session.commit()

    return redirect('/login') 

@app.route('/book', methods=['GET'])
def appointment_form():
    return render_template("calendar.html")

@app.route('/book', methods=['POST'])
def appointment_book():
    d = request.form['date']
    mydate = datetime.datetime.strptime(d, "%Y-%m-%d")
    recurring_boolean = request.form['repeat'] == 'True'
    #if line 93 is true is will return the bool True otherwise will return bool False

    user_id = request.cookies.get('user_id')
    user_dogs = model.session.query(model.User_Dog).filter_by(user_id=user_id)
    user_dog_id = user_dogs[0].dog_id


    new_appt = model.Appointment(date=mydate,
                                time_slot=request.form['time_slots'],
                                recurring=recurring_boolean) 
                                

    model.session.add(new_appt)
    model.session.commit()


    dog_appt = model.Dog_Appointment(appointment_id = new_appt.id, dog_id = user_dogs[0].dog_id )

    model.session.add(dog_appt)
    model.session.commit()

    return redirect('/payment')

#testing to see if I get the right dates.
    user_dogs = session.query(model.User_Dog)
    for user_dog in user_dogs:
        dog_appts = session.query(Dog_Appointment).filter_by(dog_id=user_dog.dog_id).all()
        for dog_appt in dog_appts:
            print dog_appt.appointment.date


@app.route('/payment', methods=['GET'])
def get_card():
    return render_template("payment.html")

@app.route('/payment', methods=['POST'])
def payment():

    new_payment = model.Payment(payment_date=datetime.datetime.today(),
                                payment_amount=2600)

    model.session.add(new_payment)
    model.session.commit()


    stripe.api_key = "sk_test_4UEKhN2p6DLJxhYU5fCgu1Pg"
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
    return redirect('/profile')

    #this_payment = the number of appointments * 2600

@app.route('/profile')
def user_profile():
    user_id = request.cookies.get('user_id')
    user = model.get_user_by_id(user_id)
    if model.User.query.get(user_id) is not None:
        user_dogs = model.session.query(model.User_Dog).filter_by(user_id=user.id)
        nicknames = []
        for user_dog in user_dogs:
            dog = model.session.query(model.Dog).get(user_dog.dog_id)
            nicknames.append(dog.nickname)
            

        return render_template('profile.html', display_user = user, nicknames = nicknames)
    else:
        return redirect('/login')


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
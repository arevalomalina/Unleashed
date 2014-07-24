import datetime
from flask.ext.script import Manager

from walker import app
import model

manager = Manager(app)


# @manager.command means you can run this function from the command line by typing
# python task.py hello
@manager.command
def hello():
    num_users = model.session.query(model.User).count()
    message = "hello.  There are %d users in the database as of %s" % (num_users, datetime.datetime.now())
    fh = open('/tmp/walker', 'a')
    fh.write(message + '\n')
    print message

@manager.command
def appointment_maker():
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=6)
    last_week_appts = model.session.query(model.Appointment).filter(
        model.Appointment.date >= start_date,
        model.Appointment.date <= today, model.Appointment.recurring==True)
    for appt in last_week_appts:
        new_appt_date = appt.date + datetime.timedelta(days=7)

        new_appt = model.Appointment(date=new_appt_date,
                                time_slot=appt.time_slot,
                                recurring=True) 
                                
        model.session.add(new_appt)
        model.session.commit()
        
        print new_appt.id

        dog_appointment = model.session.query(model.Dog_Appointment).filter_by(appointment_id=appt.id).one()
        print dog_appointment.dog_id

        dog_appt = model.Dog_Appointment(appointment_id=new_appt.id, dog_id=dog_appointment.dog_id)

        model.session.add(dog_appt)
        model.session.commit()


    #for dog_appointment in dog_appointments:
        #print dog_appointment.id


    

if __name__ == "__main__":
    manager.run()
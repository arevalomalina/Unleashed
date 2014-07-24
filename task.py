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
	print list(last_week_appts)
	

if __name__ == "__main__":
    manager.run()
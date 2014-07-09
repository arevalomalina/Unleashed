from sqlalchemy.orm import relationship, backref

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey

from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine("sqlite:///walker.db", echo=False)
session = scoped_session(sessionmaker(bind=engine,
										autocommit = False,
										autoflush = False))

Base = declarative_base()
Base.query = session.query_property()

### Class declarations go here

class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key =True)
	first_name = Column(String(64), nullable=True)
	last_name= Column(String(64), nullable=True)
	telephone= Column(String(64), nullable=True)
	address= Column(String(64), nullable=True)
	ICE= Column(String(64), nullable=True)
	email = Column(String(64), nullable=True)
	password = Column(String(64), nullable=True)

class Appointment(Base):
	__tablename__ = "appointments"

	id = Column(Integer, primary_key =True)

	"""not completely sure what information I need to collect here."""

class Dog(Base):
	__tablename__ = "dogs"
	__table_args__ = {'sqlite_autoincrement': True}

	id = Column(Integer, primary_key=True)
	vet_id = Column(Integer, ForeignKey('veterinarians.id'))
	name = Column(String, nullable=True)
	breed = Column(String, nullable=True)
	age = Column(String(64), nullable=True)
	gender = Column(String(64), nullable=True)
	weight = Column(String(64), nullable=True)

	vet = relationship("Veterinarian",
        backref=backref("dogs", order_by=id))

class Dog_Appointment(Base):
	__tablename__ = "dog_appointments"
	__table_args__ = {'sqlite_autoincrement': True}

	id = Column(Integer, primary_key=True)
	dog_id = Column(Integer, ForeignKey('dogs.id'))
	appointment_id = Column(Integer, ForeignKey('appointments.id'))

	dog = relationship("Dog",
        backref=backref("dog_appointments", order_by=id))

	appointment = relationship("Appointment",
        backref=backref("dog_appointments", order_by=id))

class User_Dog(Base):
	__tablename__ = "user_dogs"
	__table_args__ = {'sqlite_autoincrement': True}

	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey('users.id'))
	dog_id = Column(Integer, ForeignKey('dogs.id'))

	user = relationship("User",
        backref=backref("user_dogs", order_by=id))

	dog = relationship("Dog",
        backref=backref("user_dogs", order_by=id))

class Veterinarian(Base):
	__tablename__ = "veterinarians"

	id = Column(Integer, primary_key=True)
	first_name = Column(String, nullable=True)
	last_name = Column(String, nullable=True)
	address = Column(String, nullable=True)
	telephone = Column(String, nullable=True)

class Payment(Base):
	__tablename__ = "payments"

	id = Column(Integer, primary_key=True)

'''def connect():
    global ENGINE
    global Session


    return Session()'''


### End class declarations

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
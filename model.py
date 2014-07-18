from sqlalchemy.orm import relationship, backref

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey, Date

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
    first_name = Column(String(64), nullable=False)
    last_name= Column(String(64), nullable=False)
    telephone= Column(String(64), nullable=False)
    address= Column(String(64), nullable=False)
    ICE_name= Column(String(64), nullable=False)
    ICE_phone= Column(String(64), nullable=False)
    email = Column(String(64), nullable=False)
    password = Column(String(64), nullable=False)
    profile_pic = Column(String(64), nullable=True)

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key =True)
    date = Column(Date, nullable=False)
    time_slot = Column(String(64), nullable=False)

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
    nickname = Column(String(64), nullable=False, unique=True)

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
        backref=backref("dog_users", order_by=id))

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

def get_user_by_id(id):
    """Query for a specific user in the database by the primary key"""
    user = session.query(User).get(id)
    return user

def update_profile_pic(filename, user_id):
    user = session.query(User).get(user_id)
    user.profile_pic = filename
    session.commit()


### End class declarations

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
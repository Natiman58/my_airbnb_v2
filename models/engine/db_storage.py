#!/usr/bin/python3
"""
    A Database storage engine
"""

from sqlalchemy import create_engine
from os import getenv
from models.base_model import Base, BaseModel
from sqlalchemy.orm import Session
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from sqlalchemy.orm import sessionmaker, scoped_session

class DBStorage:
    """
        A class representing the DB object
    """
    __engine = None
    __session = None
    
    def __init__(self):
        """ Initialize the class """
        # create the engine
        username = getenv('HBNB_MYSQL_USER')
        password = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST', 'localhost')
        database = getenv('HBNB_MYSQL_DB')
        env = getenv('HBNB_ENV')
        
        # if the environment is set to "test"
        # drop all the tables in the db using the engine
        if env == "test":
            self.__engine = create_engine(f"mysql+mysqldb://{username}:{password}@{host}/{database}", pool_pre_ping=True)
            Base.metadata.drop_all(bind=self.__engine)
        else:
            # else create the engine and then the tables using the engine
            # dialect+driver://username:password@host:port/database
            self.__engine = create_engine(f"mysql+mysqldb://{username}:{password}@{host}/{database}", pool_pre_ping=True)
            Base.metadata.create_all(bind=self.__engine)

    def all(self, cls=None):
        """
            returns all the objects depending on the cls name
        """
        objects = {}
        if cls:
            print(cls)
            query = self.__session.query(cls)
            print(query)
            for obj in query.all():
                key = f"{type(obj).__name__}.{obj.id}"
                objects[key] = obj
        else:
            classes = [State, City]
            for clss in classes:
                query = self.__session.query(clss)
                print(query)
                for obj in query.all():
                    key = f"{type(obj).__name__}.{obj.id}"
                    objects[key] = obj
        return objects

    def new(self, obj):
        """
            adds new obj into the db session
        """
        self.__session.add(obj)

    def save(self):
        """
            commit all the changes of the current db session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
            deletes obj from the db session
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
            create all tables in the database
            and create a thread safe session
        """
        Base.metadata.create_all(bind=self.__engine)
        Session = scoped_session(sessionmaker(bind=self.__engine, expire_on_commit=False))
        self.__session = Session()




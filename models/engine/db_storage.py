#!/usr/bin/python3
"""
Database storage engine
"""

from sqlalchemy import create_engine
from models.base_model import Base
from os import getenv
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from sqlalchemy.orm import sessionmaker, scoped_session


classes = {"User": User, "State": State, "City": City,
           "Amenity": Amenity, "Place": Place, "Review": Review}


class DBStorage:
    """database storage for sqlalchemy"""
    __engine = None
    __session = None

    def __init__(self):
        """instantiate the database storage  instance"""
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD') 
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')

        self.__engine = create_engine(
                'mysql+mysqldb://{}:{}@{}/{}'.format(
                                           HBNB_MYSQL_USER,
                                           HBNB_MYSQL_PWD,
                                           HBNB_MYSQL_HOST,
                                           HBNB_MYSQL_DB
                                       ), pool_pre_ping=True)
        if HBNB_ENV == 'test':
            Base.metadata.drop_all(self.__engine) 

    def all(self, cls=None):
        """query on the current database session (self.__session)
        all objects depending of the class name (argument cls)
        """
        dct = {}
        if cls is None:
            for k in classes.values():
                objct = self.__session.query(k).all()
                for obj in objct:
                    key = obj.__class__.__name__ + '.' + obj.id
                    dct[key] = obj
        else:
            objct = self.__session.query(cls).all()
            for obj in objct:
                    key = obj.__class__.__name__ + '.' + obj.id
                    dct[key] = obj
        return dct

    def new(self, obj):
        """
        add the object to the current database session (self.__session)
        """
        if obj is not None:
            try:
                self.__session.add(obj)
                self.__session.flush()
                self.__session.refresh(obj)
            except Exception as ex:
                self.__session.rollback()
                raise ex
    
    def save(self):
        """
        commit all changes of the current database session (self.__session)
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        delete from the current database session obj if not None
        """
        if obj is not None:
            self.__session.query(type(obj)).filter(
                    type(obj).id == obj.id).delete()

    def reload(self):
        """
        create all tables in the database (feature of SQLAlchemy)
        (WARNING: all classes who inherit from Base must be imported
        before calling Base.metadata.create_all(engine))
        """
        Base.metadata.create_all(self.__engine)
        session_reload = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_reload)()

    def close(self):
        """
        Closes the working database session.
        """
        self.__session.close()

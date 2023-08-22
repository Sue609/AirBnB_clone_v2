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

#classes = [User, State, City, Amenity, Place, Review]


class DBStorage:
    """database storage for sqlalchemy"""
    __engine = None
    __session = None

    def __init__(self):
        """instantiate the database storage  instance"""
        USER = getenv('HBNB_MYSQL_USER')
        PWD = getenv('HBNB_MYSQL_PWD') 
        HOST = getenv('HBNB_MYSQL_HOST')
        DB = getenv('HBNB_MYSQL_DB')
        ENV = getenv('HBNB_ENV')
        self.__engine = create_engine(f'mysql+mysqldb://{USER}:{PWD}@{HOST}/{DB}', pool_pre_ping=True)
        if ENV == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session (self.__session)
        all objects depending of the class name (argument cls)
        """
        dct = {}
        if cls:
            query = self.__session.query(cls).all()
        else:
            query = self.__session.query(User, City, Amenity, Place, Review).all()
        for obj in query:
            key = f"{obj.__class__.__name__}.{obj.id}"
            dct[key] = obj
        return dct
    
    def new(self, obj):
        """
        add the object to the current database session (self.__session)
        """
        self.__session.add(obj)
    
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
            obj_type = type(obj)
            query = self.__session.query(obj_type).filter_by(id=obj.id).first()
            if query:
                self.__session.delete(query)
                self.__session.commit()
    
    def reload(self):
        """
        create all tables in the database (feature of SQLAlchemy)
        (WARNING: all classes who inherit from Base must be imported
        before calling Base.metadata.create_all(engine))
        """
        Base.metadata.create_all(self.__engine)
        session_reload = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self__session = scoped_session(session_reload)

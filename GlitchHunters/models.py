from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

dataBase = declarative_base()
    
# login table model
class Login(dataBase):
    __tablename__ = "login"
    __table_args__ = {"sqlite_autoincrement": True}  # this should add auto increment
        
#    loginID = Column("loginID", Integer, index=True, unique=True, primary_key=True, autoincrement=True)
    loginID = Column("loginID", Integer, unique=True, primary_key=True)
    userName = Column("userName", String, nullable=False)
    password = Column("password", String, nullable=False)
    firstName = Column("firstName", String)
    lastName = Column("lastName", String)
    loginType = Column("loginType", String)
        
#    def __init__(self, userName, password, firstName, lastName, loginType):
    def __init__(self, loginID, userName, password, firstName, lastName, loginType):
        self.loginID = loginID
        self.userName = userName
        self.password = password
        self.firstName = firstName
        self.lastName = lastName
        self.loginType = loginType
            
    def __repr__(self):
        return f"({self.loginID}) {self.userName} {self.password} {self.firstName} {self.lastName} {self.loginType}"
#        return f"( {self.userName} {self.password} {self.firstName} {self.lastName} {self.loginType}"

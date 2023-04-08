from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# verify if the database already exists
database_filename = "appdb.db"

if os.path.exists(database_filename):
    print(f"The database file {database_filename} already exists")

# Create the database if it does not exist already
else:
    dataBase = declarative_base()
    
    # login table model
    class Login(dataBase):
        __tablename__ = "login"
        
        loginID = Column("loginID", Integer, primary_key=True)
        userName = Column("userName", String)
        password = Column("password", String)
        firstName = Column("firstName", String)
        lastName = Column("lastName", String)
        loginType = Column("loginType", String)
        
        def __init__(self, loginID, userName, password, firstName, lastName, loginType):
            self.loginID = loginID
            self.userName = userName
            self.password = password
            self.firstName = firstName
            self.lastName = lastName
            self.loginType = loginType
            
        def __repr__(self):
            return f"({self.loginID}) {self.userName} {self.password} {self.firstName} {self.lastName} {self.loginType}"

    # Employee table model
    class Employee(dataBase):
        __tablename__ = "employee"
        
        employeeID = Column("employeeID", Integer, primary_key=True)
        employeeName = Column("employeeName", String)
        employeeLastName = Column("employeeLastName", String)
        employeeTitle = Column("employeeTitle", String)
        employeeType = Column("employeeType", String)
        employeeNotes = Column("employeeNotes", String)
        employeeStatus = Column("employeeStatus", String)
        loginID = Column(Integer, ForeignKey("login.loginID"))
        
        def __init__(self, employeeID, employeeName, employeeLastName, employeeTitle, employeeType, employeeNotes, employeeStatus, loginID):
            self.employeeID = employeeID
            self.employeeName = employeeName
            self.employeeLastName = employeeLastName
            self.employeeTitle = employeeTitle
            self.employeeType = employeeType
            self.employeeNotes = employeeNotes
            self.employeeStatus = employeeStatus
            self.loginID = loginID
            
        def __repr__(self):
            return f"({self.employeeID}) {self.employeeName} {self.employeeLastName} {self.employeeTitle} {self.employeeType} {self.employeeNotes} {self.employeeStatus} {self.loginID}"

    # Ticket table model
    class Ticket(dataBase):
        __tablename__ = "ticket"
        
        ticketID = Column("ticketID", Integer, primary_key=True)
        ticketName = Column("ticketName", String)
        ticketDescription = Column("ticketDescription", String)
        projectID = Column(Integer, ForeignKey("project.projectID"))
        employeeID = Column(Integer, ForeignKey("employee.employeeID"))
        priority = Column("priority", String)
        status = Column("status", String)
        
        def __init__(self, ticketID, ticketName, ticketDescription, projectID, employeeID, priority, status):
            self.ticketID = ticketID
            self.ticketName = ticketName
            self.ticketDescription = ticketDescription
            self.projectID = projectID
            self.employeeID = employeeID
            self.priority = priority
            self.status = status

        def __repr__(self):
            return f"({self.ticketID}) {self.ticketName} {self.ticketDescription} {self.projectID} {self.employeeID} {self.priority} {self.status}"

    # Project table model
    class Project(dataBase):
        __tablename__ = "project"
        
        projectID = Column("projectID", Integer, primary_key=True)
        projectName = Column("projectName", String)
        projectNumber = Column("projectNumber", Integer)
        projectDescription = Column("projectDescription", String)
        projectManager = Column("projectManager", String)
        customerID = Column(Integer, ForeignKey("customer.customerID"))
        projectClient = Column("projectClient", String)
        projectStatus = Column("projectStatus", String)
        
        def __init__(self, projectID, projectName, projectNumber, projectDescription, projectManager, customerID, projectClient, projectStatus):
            self.projectID = projectID
            self.projectName = projectName
            self.projectNumber = projectNumber
            self.projectDescription = projectDescription
            self.projectManager = projectManager
            self.customerID = customerID
            self.projectClient = projectClient
            self.projectStatus = projectStatus
            
        def __repr__(self):
            return f"({self.projectID}) {self.projectName} {self.projectNumber} {self.projectDescription} {self.projectManager} {self.customerID} {self.projectClient} {self.projectStatus}"

    # Project table model
    class Customer(dataBase):
        __tablename__ = "customer"
        
        customerID = Column("customerID", Integer, primary_key=True)
        customerName = Column("customerName", String)
        customerLastName = Column("customerLastName", Integer)
        customerPhoneNumber = Column("customerPhoneNumber", String)
        customerAddress = Column("customerAddress", String)
        customerEmail = Column(Integer, ForeignKey("customer.customerID"))
        customerType = Column("projectClient", String)
        customerStatus = Column("projectStatus", String)
        customerNotes = Column("customerNotes", String)
        
        def __init__(self, customerID, customerName, customerLastName, customerPhoneNumber, customerAddress, customerEmail, customerType, customerStatus, customerNotes):
            self.customerID = customerID
            self.customerName = customerName
            self.customerLastName = customerLastName
            self.customerPhoneNumber = customerPhoneNumber
            self.customerAddress = customerAddress
            self.customerEmail = customerEmail
            self.customerType = customerType
            self.customerStatus = customerStatus
            self.customerNotes = customerNotes
            
        def __repr__(self):
            return f"({self.customerID}) {self.customerName} {self.customerLastName} {self.customerPhoneNumber} {self.customerAddress} {self.customerEmail} {self.customerType} {self.customerStatus} {self.customerNotes}"

    engine = create_engine(f"sqlite:///{database_filename}", echo=True)
    dataBase.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Sample user login credentials
    login = Login(1, "demo", "demo", "John", "Walker", "Demo")
    session.add(login)
    session.commit()
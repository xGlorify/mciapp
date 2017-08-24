from mciapp import db, bcrypt
from datetime import datetime

link_table = db.Table('link_table',
	db.Column('id', db.Integer, primary_key=True),
    db.Column('workorder_id', db.Integer, db.ForeignKey('workorder.id')),
    db.Column('materials_id', db.Integer, db.ForeignKey('materials.id')),
    db.Column('hours_id', db.Integer, db.ForeignKey('hours.id')),
    db.Column('attachments_id', db.Integer, db.ForeignKey('attachments.id'))
    )

class Workorder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column('Customer', db.String(50), nullable = False)
    date = db.Column('Date', db.DateTime())
    customer_po = db.Column('Customer PO', db.String(10))
    requested_by = db.Column('Requested By', db.String(50))
    work_description = db.Column('Work Description', db.String(128))
    work_notes = db.Column('Work Notes', db.String(1000))
    status = db.Column('Status', db.String(25))

    def __init__(self, customer, customer_po, requested_by, work_description, work_notes, status, date=None):
        self.customer = customer
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.customer_po = customer_po
        self.requested_by = requested_by
        self.work_description = work_description
        self.work_notes = work_notes
        self.status = status

##  Will have to be adjusted when connection to Ideal API is made. ##
class Materials(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column('Material Description', db.String(128))
    cost = db.Column('Material Cost', db.Float)
    quantity = db.Column('Materials Ordered', db.Integer)
    used = db.Column('Materials Used', db.Integer)
    supplier = db.Column('Supplier', db.String(50))
    attachment = db.Column('Attachment', db.String(100))
    ##  Creates backref on Workorder table making all variables in this table referr-able via work_order_materials object. ##
    work_order = db.relationship('Workorder', secondary = link_table, backref = db.backref('work_order_materials'), lazy = 'dynamic')

    def __init__(self, description, cost, quantity, used, supplier, attachment):
    	self.description = description
    	self.cost = cost
    	self.quantity = quantity
    	self.used = used
        self.supplier = supplier
        self.attachment = attachment

class Hours(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column('Date', db.String(26))
    name = db.Column('Employee Name', db.String(128))
    regular_hours = db.Column('Regular Hours', db.Integer)
    ot_onehalf = db.Column('1.5 x OT Hours', db.Integer)
    ot_double = db.Column('2.0 x OT Hours', db.Integer)
    ##  Creates backref on Workorder table making all variables in this table referr-able via work_order_hours object. ##
    hours = db.relationship('Workorder', secondary = link_table, backref = db.backref('work_order_hours'), lazy = 'dynamic')

    def __init__(self, date, name, regular_hours, ot_onehalf, ot_double):
    	self.date = date
    	self.name = name
    	self.regular_hours = regular_hours
    	self.ot_onehalf = ot_onehalf
    	self.ot_double = ot_double

class Attachments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column('Description', db.String(50))
    file_location = db.Column('File Location', db.String(75))
    attachments = db.relationship('Workorder', secondary = link_table, backref = db.backref('work_order_attachments'), lazy = 'dynamic')

    def __init__(self, description, file_location):
        self.description = description
        self.file_location = file_location

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column('First Name', db.String(25), nullable=False)
    last_name = db.Column('Last Name', db.String(25), nullable=False)
    email = db.Column('Email', db.String(50), nullable=False)
    phone = db.Column('Phone', db.String(50), nullable=False)
    #company = db.Column('Company', db.String(30))
    role = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, first_name, last_name, email, phone, role, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        #self.company = company
        self.role = role
        self.password = bcrypt.generate_password_hash(password)
        
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

class Company(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    company_name = db.Column('Company Name', db.String(50), unique = True)
    company_address = db.Column('Company Address', db.String(50))
    company_city = db.Column('Company City', db.String(25))
    company_postal = db.Column('Company Postal', db.String(15))
    company_phone = db.Column('Company Phone', db.String(15))

    def __init__(self, company_name, company_address, company_city, company_postal, company_phone):
        self.company_name = company_name
        self.company_address = company_address
        self.company_city = company_city
        self.company_postal = company_postal
        self.company_phone = company_phone

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, FileField, SelectField, TextAreaField, DecimalField, PasswordField, HiddenField, BooleanField, RadioField, DateField, DateTimeField
from wtforms.widgets import HTMLString, html_params
from flask_wtf.file import FileRequired
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Optional, EqualTo, Email

class SubmitWorkorderForm(FlaskForm):
    customer = SelectField('Customer', coerce=int, validators=[DataRequired()])
    customer_po = StringField('Customer PO', validators=[DataRequired()])
    requested_by = StringField('Requested By', validators=[Optional()])
    work_description = StringField('Work Description', validators=[Optional()])
    work_notes = TextAreaField('Work Notes', validators=[Optional()])
    status = SelectField('Status', choices=[('Quote', 'Quote'), ('Pending', 'Pending'), ('WIP', 'WIP'), ('Complete', 'Complete'), ('TBI', 'TBI'), ('Invoiced', 'Invoiced')])

class EditWorkorderForm(FlaskForm):
    id = IntegerField('id', validators=[DataRequired()])
    customer = SelectField('Customer', coerce=int, validators=[DataRequired()])
    customer_po = StringField('Customer PO', validators=[DataRequired()])
    requested_by = StringField('Requested By', validators=[Optional()])
    work_description = StringField('Work Description', validators=[Optional()])
    work_notes = TextAreaField('Work Notes', validators=[Optional()])
    status = SelectField('Status', choices=[('Quote', 'Quote'), ('Pending', 'Pending'), ('WIP', 'WIP'), ('Complete', 'Complete'), ('TBI', 'TBI'), ('Invoiced', 'Invoiced')])

class CreateCompanyForm(FlaskForm):
	company_name = StringField('Company Name', validators=[DataRequired()])
	company_address = StringField('Company Address', validators=[DataRequired()])
	company_city = StringField('Company City', validators=[DataRequired()])
	company_postal = StringField('Company Postal', validators=[DataRequired()])
	company_phone = IntegerField('Company Phone', validators=[DataRequired()])

class MaterialsForm(FlaskForm):
    workorder_id = HiddenField('workorder_id', validators=[DataRequired()])
    description = StringField('Material Description', validators=[DataRequired()])
    cost = DecimalField('Cost', places = 2, validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    used = IntegerField('Materials Used', validators=[DataRequired()])
    supplier = SelectField('Supplier', choices=[('Ideal Supply', 'Ideal Supply'), ('Home Depot', 'Home Depot'), ('HD Supply', 'HD Supply'), ('Torbram Electric Supply', 'Torbram Electric Supply'), ('Westburne', 'Westburne')])
    attachment = FileField('Attachment', validators=[FileRequired()])

class HoursForm(FlaskForm):
    workorder_id = HiddenField('Hours ID', validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    employee_name = SelectField('Employee name', coerce=int, validators=[DataRequired()])
    regular_hours = IntegerField('Regular Hours', validators=[Optional()])
    ot_onehalf = IntegerField('1.5 x OT Hours', validators=[Optional()])
    ot_double = IntegerField('2.0 x OT Hours', validators=[Optional()])

class SignupForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    user_email = StringField('Email', validators=[DataRequired(), Email()])
    user_phone = StringField('Phone Number', validators=[DataRequired()])
    user_role = SelectField('User Role', choices=[('Administrator', 'Administrator'), ('Standard', 'Standard')])
    password = PasswordField('Password', validators=[DataRequired()])
    password_check = PasswordField('Password Confirm', validators=[DataRequired(), EqualTo('password')])
    
class LoginForm(FlaskForm):
    login_email = StringField('login_email', validators=[DataRequired(), Email()])
    login_password = PasswordField('login_password', validators=[DataRequired()])

class HoursEditForm(FlaskForm):
    hour_id = HiddenField('Hours ID', validators=[DataRequired()])
    date = StringField('Date', validators=[DataRequired()])
    employee_name = SelectField('Employee name', coerce=int, validators=[DataRequired()])
    regular_hours = IntegerField('Regular Hours', validators=[Optional()])
    ot_onehalf = IntegerField('1.5 x OT Hours', validators=[Optional()])
    ot_double = IntegerField('2.0 x OT Hours', validators=[Optional()])

class WorkorderAttachmentsForm(FlaskForm):
    workorder_id = HiddenField('Workorder ID', validators=[DataRequired()])
    woa_description = StringField('Description', validators=[DataRequired()])
    woa_attachment = FileField('Attachment', validators=[FileRequired()])

class FilterWorkorderForm(FlaskForm):
    id = IntegerField('id', validators=[Optional()])
    date = DateField('Date', validators=[Optional()])
    #customer = SelectField('Customer', coerce=int, validators=[Optional()])
    customer_po = StringField('Customer PO', validators=[Optional()])
    requested_by = StringField('Requested By', validators=[Optional()])
    work_description = StringField('Work Description', validators=[Optional()])
    status = SelectField('Status', choices=[('Quote', 'Quote'), ('Pending', 'Pending'), ('WIP', 'WIP'), ('Complete', 'Complete'), ('TBI', 'TBI'), ('Invoiced', 'Invoiced')])

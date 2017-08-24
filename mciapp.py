from flask import Flask, render_template, request, jsonify, flash, url_for, redirect, g, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from sqlalchemy.sql import exists
from flask_bcrypt import Bcrypt
from forms import SubmitWorkorderForm, CreateCompanyForm, MaterialsForm, EditWorkorderForm, SignupForm, LoginForm, HoursForm, HoursEditForm, WorkorderAttachmentsForm, FilterWorkorderForm
from flask_wtf.csrf import CsrfProtect
from flask_login import login_user, login_required, current_user, logout_user, LoginManager
from werkzeug.utils import secure_filename
from werkzeug.datastructures import CombinedMultiDict

app = Flask(__name__, static_folder='static')
app.config.from_object('config')

login_manager = LoginManager()
login_manager.init_app(app)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
CsrfProtect(app)

from models import *

#db.drop_all()
#db.create_all()
#db.session.commit()



############################### FLASK_LOGIN REQUIREMENT ROUTES ################################

@login_manager.user_loader
def load_user(user_id):
    return Users.query.filter(Users.id == int(user_id)).first()

@app.before_request #Define headersearchform globally as it runs on every page with header.
def before_request():
    g.current_user = current_user

login_manager.login_view = "login"

@app.route('/')
def global_redirect():
    return redirect(url_for('login'))

################################################################################################

@app.route('/attachments/materials/<filename>')
def materials_static(filename):
    return send_from_directory(app.config['CUSTOM_MATERIALS_STATIC_PATH'], filename)

@app.route('/attachments/workorder/<filename>')
def workorder_static(filename):
    return send_from_directory(app.config['CUSTOM_WORKORDER_STATIC_PATH'], filename)

@app.route('/view_users', methods=['GET'])
@login_required
def view_users():
	users = Users.query.all()
	return render_template('view_users.html', users = users)

@app.route('/logout', methods=['GET', 'POST'])
@login_required 
def logout():
    logout_user()
    flash('You were logged out.')
    return redirect(url_for('login'))

@app.route('/users/login', methods = ['GET', 'POST'])
def login():
	form = LoginForm()
	if request.method == 'POST':
		if form.validate_on_submit():
			user = Users.query.filter_by(email = form.login_email.data).first()
			if user is not None and bcrypt.check_password_hash(user.password, form.login_password.data):
				login_user(user)
				return redirect(url_for('view_workorders'))
			else:
				flash('Incorrect username or password.')
	return render_template('login.html', form=form)

@app.route('/users/register_user')
def register_user():
	form = SignupForm()
	return render_template('register_user.html', form=form)

@app.route('/users/<name>', methods=['GET'])
@login_required
def user_profile(name):
	users_workorders = Workorder.query.filter(Workorder.work_order_hours.any(name=name)).all()
	users_hours = Hours.query.filter_by(name=name).all()
	return render_template('user_profile.html', users_workorders = users_workorders, users_hours = users_hours)

@app.route('/workorders/submit_work_order')
@login_required
def submit_work_order():
	form1 = SubmitWorkorderForm()
	form2 = MaterialsForm()
	form3 = HoursForm()
	form1.customer.choices = [(cus.id, cus.company_name) for cus in Company.query.order_by('id')]
	form2.workorder_id.choices = [(work.id, work.id) for work in Workorder.query.order_by(desc('id'))]
	form3.employee_name.choices = [(e.id, e.first_name + " " + e.last_name) for e in Users.query.order_by('id')]
	return render_template('submitworkorder.html', form1 = form1, form2 = form2, form3 = form3)

@app.route('/workorders/view_workorders', methods=['GET'])
@login_required
def view_workorders():
	workorders = Workorder.query.all()
	return render_template('view_workorders.html', workorders = workorders)

@app.route('/workorders/<id>')
@login_required
def workorder_profile(id):
	form = EditWorkorderForm()
	form2 = HoursForm()
	form3 = MaterialsForm()
	form4 = WorkorderAttachmentsForm()
	form2.employee_name.choices = [(e.id, e.first_name + " " + e.last_name) for e in Users.query.order_by('id')]
	form.customer.choices = [(cus.id, cus.company_name) for cus in Company.query.order_by('id')]
	workorder = Workorder.query.filter_by(id = id).first_or_404()
	form3.workorder_id.data = workorder.id
	form4.workorder_id.data = workorder.id
	form.work_notes.data = workorder.work_notes
	form.status.data = workorder.status
	form.customer.data = workorder.customer
	return render_template('workorder_profile.html', form = form, form2 = form2, form3 = form3, form4 = form4, workorder = workorder)

@app.route('/hours/<id>')
@login_required
def edit_hours(id):
	form = HoursEditForm()
	workorder = Workorder.query.filter(Workorder.work_order_hours.any(id=id)).all()
	form.employee_name.choices = [(e.id, e.first_name) for e in Users.query.order_by('id')]
	hour_entry = Hours.query.filter_by(id = id).first_or_404()
	form.hour_id.data = hour_entry.id
	form.date.data = hour_entry.date
	form.employee_name.data = hour_entry.name
	form.regular_hours.data = hour_entry.regular_hours
	form.ot_onehalf.data = hour_entry.ot_onehalf
	form.ot_double.data = hour_entry.ot_double
	return render_template('edit_hours.html', form = form, hour_entry = hour_entry, workorder = workorder)

@app.route('/companies/create_company', methods=['GET'])
@login_required
def create_company():
	form = CreateCompanyForm()
	return render_template('create_company.html', form = form)

@app.route('/companies/view_companies', methods=['GET'])
@login_required
def view_companies():
	companies = Company.query.all()
	return render_template('view_companies.html', companies = companies)

@app.route('/reports/filter_workorder', methods=['GET', 'POST'])
@login_required
def filter_workorder():
	results = None
	form = FilterWorkorderForm()
	if request.method == 'POST':
		if form.validate_on_submit():
			try:
				filter_data = {'id' : form.id.data, 'date' : form.date.data, 'customer_po' : form.customer_po.data, 'requested_by' : form.requested_by.data, 
				'work_description' : form.work_description.data, 'status' : form.status.data}
				filter_data = {key: value for (key, value) in filter_data.items() if value}
				results = Workorder.query.filter_by(**filter_data).all()
			except Exception as e:
				db.session.rollback()
				flash(e)
		return render_template('filter_workorder.html', form = form, results = results)
	return render_template('filter_workorder.html', form = form)

#@app.route('/reports/hours_reports', methods=['GET', 'POST'])
#def hours_reports():


@app.route('/api/create_company', methods=['POST'])
def create_company_api():
	error_data = None
	form = CreateCompanyForm()
	if form.validate_on_submit():
		company_name = form.company_name.data
		exists = db.session.query(Company).filter_by(company_name = company_name).scalar() is not None
		if exists:
			return jsonify ({'error' : 'This company already exists in the database.'})
		else:
			company_name = form.company_name.data
			company_address = form.company_address.data
			company_city = form.company_city.data
			company_postal = form.company_postal.data
			company_phone = form.company_phone.data
			pass_to_db = Company(company_name, company_address, company_city, company_postal, company_phone)
			db.session.add(pass_to_db)
			db.session.commit()
			return jsonify({'company' : company_name})
	else:
		for field, errors in form.errors.items():
	    		for error in errors:
	        		error_data = (u"Error in the %s field - %s" % (getattr(form, field).label.text, error))
	return jsonify({'error' : error_data})


@app.route('/api/submitworkorder', methods=['POST'])
def submit_work_order_api():
	form = SubmitWorkorderForm()
	form.customer.choices = [(cus.id, cus.company_name) for cus in Company.query.order_by('id')]
	print form.data
	if form.validate_on_submit():
		company_id = form.customer.data
		company = Company.query.filter_by(id = company_id).first_or_404()
		company_name = company.company_name
		customer_po = form.customer_po.data
		requested_by = form.requested_by.data
		work_description = form.work_description.data
		work_notes = form.work_notes.data
		status = form.status.data
		pass_to_db = Workorder(company_name, customer_po, requested_by, work_description, work_notes, status)
		db.session.add(pass_to_db)
		db.session.commit()
		workorder = Workorder.query.order_by(Workorder.id.desc()).first()
		return jsonify({'company' : company.company_name, 'customer_po' : customer_po, 'workorder_id' : workorder.id})
	else:
		for field, errors in form.errors.items():
	    		for error in errors:
	        		error_data = (u"Error in the %s field - %s" % (getattr(form, field).label.text, error))
	return jsonify({'error' : error_data})

@app.route('/api/submit_materials', methods=['POST'])
def submit_materials_api():
	form = MaterialsForm()
	form.workorder_id.choices = [(work.id, work.id) for work in Workorder.query.order_by(desc('id'))]
	if form.validate_on_submit():
		workorder_id = form.workorder_id.data
		workorder = Workorder.query.filter_by(id = workorder_id).first_or_404()
		description = form.description.data
		cost = form.cost.data
		quantity = form.quantity.data
		used = form.used.data
		supplier = form.supplier.data
		attachment = form.attachment.data
		filename = secure_filename(str(workorder_id) + '_' + attachment.filename)
		form.attachment.data.save('attachments/materials/' + filename)
		materials = Materials(description, cost, quantity, used, supplier, filename)
		workorder.work_order_materials.append(materials)
		db.session.add(materials)
		db.session.commit()
		return jsonify({'materials' : materials.description, 'workorder_id' : workorder_id, 'quantity' : quantity})
	else:
		for field, errors in form.errors.items():
	    		for error in errors:
	        		error_data = (u"Error in the %s field - %s" % (getattr(form, field).label.text, error))
	return jsonify({'error' : error_data})

@app.route('/api/submit_workorder_attachment', methods=['POST'])
def submit_workorder_attachment():
	form = WorkorderAttachmentsForm()
	if form.validate_on_submit():
		file_location = None
		workorder_id = form.workorder_id.data
		workorder = Workorder.query.filter_by(id = workorder_id).first_or_404()
		description = form.woa_description.data
		attachment = form.woa_attachment.data
		file_location = secure_filename(str(workorder_id) + '_' + attachment.filename)
		form.woa_attachment.data.save('attachments/workorder/' + file_location)
		attachment = Attachments(description, file_location)
		workorder.work_order_attachments.append(attachment)
		db.session.add(attachment)
		db.session.commit()
		return jsonify({'description' : attachment.description, 'workorder_id' : workorder_id})
	else:
		for field, errors in form.errors.items():
	    		for error in errors:
	        		error_data = (u"Error in the %s field - %s" % (getattr(form, field).label.text, error))
	return jsonify({'error' : error_data})

@app.route('/api/submit_hours', methods=['POST'])
def submit_hours():
	form = HoursForm()
	form.employee_name.choices = [(e.id, e.first_name) for e in Users.query.order_by('id')]
	if form.validate_on_submit():
		employee_id = form.employee_name.data
		employee = Users.query.filter_by(id = employee_id).first_or_404()
		workorder_id = form.workorder_id.data
		workorder = Workorder.query.filter_by(id = workorder_id).first_or_404()
		employee_name = str(employee.first_name) + " " + str(employee.last_name)
		date = form.date.data
		regular_hours = form.regular_hours.data
		ot_onehalf = form.ot_onehalf.data
		ot_double = form.ot_double.data
		hours = Hours(date, employee_name, regular_hours, ot_onehalf, ot_double)
		workorder.work_order_hours.append(hours)
		db.session.add(hours)
		db.session.commit()
		return jsonify({'employee_name' : employee_name})
	else:
		for field, errors in form.errors.items():
	    		for error in errors:
	        		error_data = (u"Error in the %s field - %s" % (getattr(form, field).label.text, error))
	return jsonify({'error' : error_data})

@app.route('/api/edit_hours', methods=['POST'])
def edit_hours_api():
	form = HoursEditForm()
	form.employee_name.choices = [(e.id, e.first_name) for e in Users.query.order_by('id')]
	if form.validate_on_submit():
		employee_id = form.employee_name.data
		employee = Users.query.filter_by(id = employee_id).first_or_404()
		employee_name = str(employee.first_name) + " " + str(employee.last_name)
		hour_entry = Hours.query.filter_by(id = form.hour_id.data).first_or_404()
		hour_entry.date = form.date.data
		hour_entry.name = employee_name
		hour_entry.regular_hours = form.regular_hours.data
		hour_entry.ot_onehalf = form.ot_onehalf.data
		hour_entry.ot_double = form.ot_double.data
		db.session.commit()
		return jsonify({'employee_name' : hour_entry.name, 'date' : hour_entry.date})
	else:
		for field, errors in form.errors.items():
	    		for error in errors:
	        		error_data = (u"Error in the %s field - %s" % (getattr(form, field).label.text, error))
	return jsonify({'error' : error_data})

@app.route('/api/delete_hours/<id>')
def delete_hours_api(id):
	hour_entry = Hours.query.filter_by(id=id).first_or_404()
	db.session.delete(hour_entry)
	db.session.commit()
	flash("%s hour entry on %s successfully deleted." % (hour_entry.name, hour_entry.date))
	return redirect(url_for('view_workorders'))


@app.route('/api/update_workorder', methods=['POST'])
def update_workorder():
	form = EditWorkorderForm()
	form.customer.choices = [(cus.id, cus.company_name) for cus in Company.query.order_by('id')]
	if form.validate_on_submit():
		customer = Company.query.filter_by(id = form.customer.data).first_or_404()
		company_name = customer.company_name
		workorder = Workorder.query.filter_by(id = form.id.data).first_or_404()
		workorder.id = form.id.data
		workorder.customer = company_name
		workorder.customer_po = form.customer_po.data
		workorder.requested_by = form.requested_by.data
		workorder.work_description = form.work_description.data
		workorder.work_notes = form.work_notes.data
		workorder.status = form.status.data
		db.session.commit()
		return jsonify({'workorder_id' : workorder.id})
	else:
		for field, errors in form.errors.items():
	    		for error in errors:
	        		error_data = (u"Error in the %s field - %s" % (getattr(form, field).label.text, error))
	return jsonify({'error' : error_data})

@app.route('/api/register_user', methods=['POST'])
def register_user_api():
	form = SignupForm()
	if form.validate_on_submit():
		new_user = Users(first_name = form.first_name.data, last_name = form.last_name.data, email = form.user_email.data,
		phone = form.user_phone.data, role = form.user_role.data, password = form.password.data)
		db.session.add(new_user)
		db.session.commit()
		first_name = form.first_name.data
		last_name = form.last_name.data
		return jsonify({'first_name' : first_name, 'last_name' : last_name})
	else:
		for field, errors in form.errors.items():
			for error in errors:
				error_data = (u"Error in the %s field - %s" % (getattr(form, field).label.text, error))
	return jsonify({'error' : error_data})


if __name__ == "__main__":
  app.run(host="192.168.168.65", debug = True, threaded = True)

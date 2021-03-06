
from flask import render_template, Flask, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.secret_key = 'example'

class SubmitWorkorderForm(FlaskForm):
    customer = StringField('customer', validators=[DataRequired()])

@app.route('/')
def home():
    form = SubmitWorkorderForm()
    return render_template('example.html', form=form)


@app.route('/something/', methods=['post'])
def something():
    form = SubmitWorkorderForm()
    if form.validate_on_submit():
        return jsonify(data={'message': 'hello {}'.format(form.customer.data)})
    return jsonify(data=form.errors)

if __name__ == '__main__':
    app.run(host="192.168.168.65", debug = True, threaded = True)
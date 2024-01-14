from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Your_Secret_Key'
Bootstrap5(app)

coffee_list = ['✘', '☕', '☕☕', '☕☕☕', '☕☕☕☕']
wifi_list = ['✘', '💪', '💪💪', '💪💪💪', '💪💪💪💪']
power_list = ['✘', '🔌', '🔌🔌', '🔌🔌🔌', '🔌🔌🔌🔌']


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Location', validators=[URL()])
    open_time = StringField('Open Time', validators=[DataRequired()])
    close_time = StringField('Close Time', validators=[DataRequired()])
    coffee = SelectField('Coffee', choices=coffee_list)
    wifi = SelectField('WiFi', choices=wifi_list)
    power = SelectField('Power', choices=power_list)
    submit = SubmitField('Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print("True")
        cafe_name = form.data['cafe']
        location = form.data['location']
        open_time = form.data['open_time']
        close_time = form.data['close_time']
        coffee = form.data['coffee']
        wifi = form.data['wifi']
        power = form.data['power']
        with open('cafe-data.csv', mode='a') as csv_file:
            csv_file.write(f'{cafe_name}, {location}, {open_time}, {close_time}, {coffee}, {wifi}, {power} \n')
        return render_template('index.html')
    return render_template('add.html', form=form)

@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)



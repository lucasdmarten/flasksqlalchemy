from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate
from flask import render_template
from flask import request
from flask import redirect


flaskapp = Flask(__name__)
flaskapp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

sqldb = SQLAlchemy(flaskapp)
sqldb_migrate = Migrate(flaskapp, sqldb)

class Profile(sqldb.Model):
    id = sqldb.Column(sqldb.Integer, primary_key=True)
    first_name = sqldb.Column(sqldb.String(20), unique=False, nullable=False)
    last_name = sqldb.Column(sqldb.String(20), unique=False, nullable=False)
    age = sqldb.Column(sqldb.Integer, nullable=False)
    second_id = sqldb.Column(sqldb.String(20), unique=True,  nullable=False)

    def __repr__(self):
        return f"Name : {self.first_name}, Age: {self.age}"

@flaskapp.route('/')
def index():
    profiles = Profile.query.all()
    return render_template('index.html', profiles=profiles)

@flaskapp.route('/add_data', methods=['POST', 'GET'])
def add_data():
    return render_template('add_profile.html')

@flaskapp.route('/delete/<int:id>')
def erase(id):
    data = Profile.query.get(id)
    sqldb.session.delete(data)
    sqldb.session.commit()
    return redirect('/')

@flaskapp.route('/error')
def error_page():
    return render_template('error.html')

@flaskapp.route('/add', methods=["POST"])
def profile():
    try:
        p = Profile(**dict(request.form))
        sqldb.session.add(p)
        sqldb.session.commit()
    except Exception as e:
        print(e)
        return str(e)
    else:
        return redirect('/')
    

if __name__ == '__main__':
    with flaskapp.app_context():
        sqldb.create_all()
    flaskapp.run(debug=True, host='0.0.0.0', port=9090)
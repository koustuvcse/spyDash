from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/visitors'
db = SQLAlchemy(app)

class Visitor(db.Model):
    __tablename__ = 'visitors'
    visitor_id = db.Column(db.Integer, primary_key=True)
    visitor_name = db.Column(db.String(50))
    visitor_phone = db.Column(db.String(20))
    comments = db.Column(db.Text)
    created_by = db.Column(db.String(50))
    created_on = db.Column(db.DateTime)
    modified_by = db.Column(db.String(50))
    modified_on = db.Column(db.DateTime)

@app.route('/', methods=['GET', 'POST'])
def index():
    modified_by_filter = request.form.get('modified_by')

    # Query unique modified_by users
    modified_by_users = db.session.query(Visitor.modified_by).distinct().all()

    # Get the current time
    last_updated = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Filter data based on selected modified_by user
    query = Visitor.query
    if modified_by_filter:
        query = query.filter_by(modified_by=modified_by_filter)
    data = query.all()

    return render_template('index.html', data=data,  modified_by_users=modified_by_users,
                           selected_modified_by=modified_by_filter, last_updated=last_updated)

if __name__ == '__main__':
    app.run(debug=True)

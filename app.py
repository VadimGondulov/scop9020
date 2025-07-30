from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import inspect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://CHANGEMELOGIN:CHANGEMEPASSWORD@localhost/mydatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class FormData(db.Model):
    __tablename__ = 'form_data'
    id = db.Column(db.Integer, primary_key=True)
    inputs = db.Column(JSONB)


with app.app_context():
    inspector = inspect(db.engine)
    if not inspector.has_table("form_data"):
        db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/submit", methods=['POST'])
def submit():
    data = request.form.to_dict()
    print('submit data:', data)
    entry = FormData(inputs=data)
    db.session.add(entry)
    db.session.commit()
    return "Saved!"


@app.route("/view")
def view_data():
    entries = FormData.query.all()
    all_pairs = []
    for entry in entries:
        if entry.inputs:
            for key, value in entry.inputs.items():
                all_pairs.append((key, value))
    return render_template("view_data.html", pairs=all_pairs)


if __name__ == "__main__":
    app.run(debug=True)
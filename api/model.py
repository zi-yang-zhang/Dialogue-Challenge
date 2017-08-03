from database import db


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    birth_date = db.Column(db.Date)
    sex = db.Column(db.String)

    def __init__(self, email, first_name, last_name, birth_date, sex):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.sex = sex

    def __repr__(self):
        return '<User email: %s, first_name: %s, last_name: %s, birth_date: %s, sex: %s>'.format(self.email,
                                                                                                 self.first_name,
                                                                                                 self.last_name,
                                                                                                 self.birth_date,
                                                                                                 self.sex)

from . import db

class Mondecubs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Numeric)
    y = db.Column(db.Numeric)
    z = db.Column(db.Numeric)
    colorhex = db.Column(db.String(7), index=True)
    usuari = db.Column(db.String(20), index=True)

    def __repr__(self):
        return '<Mondecubs {}>'.format(self.id)

class Gent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Numeric)
    y = db.Column(db.Numeric)
    z = db.Column(db.Numeric)
    #colorhex = db.Column(db.String(7), index=True)
    usuari = db.Column(db.String(20), index=True)

    def __repr__(self):
        return '<Gent {}>'.format(self.id)

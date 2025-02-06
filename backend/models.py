from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String, nullable=False)
    message = db.Column(db.String, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp,
            'message': self.message
        }

class Rule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rule = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)

    def update(self, data):
        for key, value in data.items():
            setattr(self, key, value)

    def to_dict(self):
        return {
            'id': self.id,
            'rule': self.rule,
            'description': self.description
        }
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Interaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_input = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)
    suggestions = db.Column(db.JSON)  # Alterado para JSON
    sentiment = db.Column(db.String(20))
    grammar_corrections = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

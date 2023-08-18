from db import db
from datetime import datetime

class BlocklistModel(db.Model):
    __tablename__ = "Blocklist"
    
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
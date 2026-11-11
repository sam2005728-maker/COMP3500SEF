import uuid
from Application import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Official.query.get(str(user_id))

class Official(db.Model, UserMixin):
    __tablename__ = 'Officials'

    OfficialUId = db.Column(db.String(38), primary_key=True)
    FirstName = db.Column(db.String(50), nullable=False)
    Surname = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(255), unique=True, nullable=False)
    PwdHash = db.Column(db.String(255), nullable=False)
    IsAdmin = db.Column(db.Integer, default=0)

    def get_id(self):
        return str(self.OfficialUId)

    def __repr__(self):
        return f"User('{self.Email}')"

class Election(db.Model, UserMixin):
    __tablename__ = 'Election'

    Id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255), nullable=False)
    StartDate = db.Column(db.DateTime, nullable=False)
    EndDate = db.Column(db.DateTime, nullable=False)

class Candidates(db.Model, UserMixin):
    title = db.Column(db.String(60), primary_key=True)

class PoliticalParty(db.Model):
    __tablename__ = 'political_party'
    UId = db.Column(db.String(38), primary_key=True)
    Name = db.Column(db.String(255), nullable=False)


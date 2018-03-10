# app/models.py
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager

library = db.Table('library',
	db.Column('games_id', db.Integer, db.ForeignKey('games.id'), primary_key=True),
	db.Column('gamers_id', db.Integer, db.ForeignKey('gamers.id'), primary_key=True)
)

class Gamer(UserMixin, db.Model):
	"""
	Create Gamer table
	"""
	
	__tablename__ = 'gamers'
	
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(60), index=True, unique=True)
	username = db.Column(db.String(60), index=True, unique=True)
	first_name = db.Column(db.String(60), index=True)
	last_name = db.Column(db.String(60), index=True)
	password_hash = db.Column(db.String(128))
	is_admin = db.Column(db.Boolean, default=False)
	library = db.relationship('Games', secondary=library, lazy='subquery',
		backref=db.backref('Gamer', lazy=True))
	
	@property
	def password(self):
		"""
		Prevent password from being read
		"""
		raise AttributeError('password is not a readable attribute!')
			
	@password.setter
	def password(self, password):
		"""
        Set password to a hashed password
        """
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		"""
		Compare hash and password
		"""
        
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return '<Gamer: {}>'.format(self.username)
		
# user_loader
@login_manager.user_loader
def load_user(user_id):
	return Gamer.query.get(int(user_id))
	
class Games(db.Model):
    """
    Create Games table
    """

    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    # gamer = db.relationship('Gamer', backref='games', lazy='dynamic')

    def __repr__(self):
        return '<Games: {}>'.format(self.name)

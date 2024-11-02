from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators
    @validates('name')
    def vldtd_nm(self, key, value):
        existing_name = self.__class__.query.filter_by(name=value).filter(self.__class__.id != self.id).first()
        if not value:
            raise ValueError("Name required.")
        elif existing_name:
            raise ValueError("Name must be unique.")  
        return value
    
    @validates('phone_number')
    def vldt_phnm(self, key, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be exactly 10 digits")
        return value

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
        
    @validates('title')
    def validate_title(self, key, value):
        if not value:
            raise ValueError("Title required.")
        clickbait_phrases = ["Won't Believe", "Secret", "Top", "Guess"]

        if not any(phrase in value for phrase in clickbait_phrases):
            raise ValueError("Title must contain at least one clickbait phrase.")
        
        existing_title = self.__class__.query.filter_by(title=value).filter(self.__class__.id != self.id).first()
        if existing_title:
            raise ValueError("Title must be unique.")
        return value
        
    @validates('content')
    def vldt_cntnt(self, key, value):
        if len(value) < 250:
            raise ValueError("Content must be 250 chars or more.")
        return value
    
    @validates('summary')
    def vldt_smmry(self, key, value):
        if len(value) > 250:
            raise ValueError("Content muse be less than 250 chars.")
        return value
    
    @validates('category')
    def vldt_ctgry(self, key, value):
        if not (value == "Fiction" or value == "Non-Fiction"):
            raise ValueError("Category should be '/Fiction' or '/Non-Fiction'.")
        return value
    
    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'

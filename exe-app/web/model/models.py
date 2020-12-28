from datetime import datetime
from web import app, db, ma

# columns
# book, col_1(chapter), col_2(page), author, work, lib, cap, par, pag, lin.7
# genre, palce_origin, time_of_origin # added information
# author, name_of_work # abbreviation
class Abbreviation(db.Model):
    __tablename__ = "abbrivations"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)    
    author = db.Column(db.String(30), nullable=False)
    name_of_work = db.Column(db.String(30), nullable=False)
    updated_on = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean)    

    def __init__(self, author, name_of_work, is_active=True):
        self.author = author
        self.name_of_work = name_of_work
        self.updated_on = datetime.utcnow()
        self.is_active = is_active

# books shedma
class AbbvSchema(ma.Schema):
    class meta:
        fileds = ('id', 'author', 'name_of_work', 'updated_on', 'is_active')
             
# Init schema
abbv_schema = AbbvSchema()
abbvs_schema = AbbvSchema(many=True)


class Book(db.Model):
    __tablename__ = "book"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book = db.Column(db.String(20), nullable=False)
    col_1 = db.Column(db.String(20))
    col_2 = db.Column(db.String(20))
    author = db.Column(db.String(20))
    work = db.Column(db.String(20))
    lib = db.Column(db.String(20))
    cap = db.Column(db.String(20))
    par = db.Column(db.String(20))
    pag = db.Column(db.String(20))
    line = db.Column(db.String(20))
    #added info
    genre = db.Column(db.String(20))
    origin_place = db.Column(db.String(20))
    origin_time = db.Column(db.String(20))
    
    updated_on = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean)

    def __init__(self, book="", col_1="", col_2="", author="", work="", lib="", cap="", par="", pag="", line="", genre="", origin_place="", origin_time="", updated_on=None, is_active=True):
        self.book = book
        self.col_1 = col_1
        self.col_2 = col_2
        self.author = author
        self.work = work
        self.lib = lib
        self.cap = cap
        self.par = par
        self.pag = pag
        self.line = line
        
        self.genre = genre
        self.origin_place = origin_place
        self.origin_time = origin_time
        if updated_on is None:
            updated_on = datetime.utcnow()
        self.updated_on = updated_on
        self.is_active = is_active
    

# books shedma
class BookSchema(ma.Schema):
    class meta:
        fileds = ('id', 'book', 'col_1', 'col_2', 'author', 'work', 'lib','cap',
         'par', 'pag', 'line', 'genre', 'origin_place', 'origin_time', 'updated_on', 'is_active')
             
# Init schema
book_schema = BookSchema()
books_schema = BookSchema(many=True)

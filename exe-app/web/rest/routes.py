from operator import length_hint
from re import search
from flask import Blueprint, request, jsonify
from flask.helpers import url_for
import os
from datetime import datetime
import json
from flask_sqlalchemy import SQLAlchemy

from web import db, app
from web.model.models import Book, book_schema, books_schema
from web.model.models import Abbreviation, abbv_schema, abbvs_schema
from sqlalchemy.sql import text

api = Blueprint('api', __name__)
DATA_PATH = os.path.join(app.static_folder, 'data', 'data.json')

COL_LIST = ["id", "book", "col_1", "col_2", "author", "work", "lib", "cap", "par", "pag", "line", "genre", "origin_place", "origin_time", "updated_on"]

# Create a Record
@api.route('/', methods=['POST'])
def add_product():
    id = str(request.form['pk'])
    field = request.form['name']
    value = request.form['value']    
    # result = db.engine.execute('select * from abbrivations')#.execution_options(autocommit=True))     
    
    if id == '':        
        # new insertion
        if field == 'book':        
            query = "insert into book ({}, updated_on, is_active) values ('{}', '{}', 1)".format(field, value, datetime.utcnow())
        else:
            query = "insert into book ({}, {}, updated_on, is_active) values ('{}','{}', '{}', 1)".format("book",  field, "No book", value, datetime.utcnow())
        
        insert = db.engine.execute(query)
        db.session.commit()
        
        return {"id": insert.lastrowid, "success": True}
    else:
        # updating 
        query = "update book set {}='{}', updated_on='{}' where id = {}".format(field, value, datetime.utcnow(), id)

        db.engine.execute(query)
        db.session.commit()        
        
        return {"id": id, "success": True}

    # return jsonify(result)


    # new_product = Product(name, description, price, qty)

    # # open data
    # with open(DATA_PATH) as file:
    #     data = json.load(file)
    # # append data

    # data["data"].append([12, field_value, "", "", "", "", "", "", "", "", "", "", "", ""])

    # # save data
    # with open(DATA_PATH, 'w') as f:
    #     json.dump(data, f)

    # return {"id":12, "success": field_value}

# Get all products
@api.route('/', methods=['GET'])
def get_products():
    query = "select id, book, col_1, col_2, author, work, lib, cap, par, pag, line, genre, origin_place, origin_time from book "    
    searchOn = str(request.args.get("search[value]"))
    start = request.args.get("start")
    length = request.args.get("length")
    draw = int(request.args.get("draw"))

    if (searchOn):
        query += "WHERE (book LIKE '%"+searchOn+"%' OR "
        query += "col_1 LIKE '%"+searchOn+"%' OR "
        query += "col_2 LIKE '%"+searchOn+"%' OR "
        query += "author LIKE '%"+searchOn+"%' OR "
        query += "work LIKE '%"+searchOn+"%' OR "
        query += "lib LIKE '%"+searchOn+"%' OR "
        query += "cap LIKE '%"+searchOn+"%' OR "
        query += "par LIKE '%"+searchOn+"%' OR "
        query += "pag LIKE '%"+searchOn+"%' OR "
        query += "line LIKE '%"+searchOn+"%' OR "
        query += "genre LIKE '%"+searchOn+"%' OR "
        query += "origin_place LIKE '%"+searchOn+"%' OR "
        query += "origin_time LIKE '%"+searchOn+"%') AND "
        query += "is_active=1 "
    else:
        query += "WHERE is_active=1 "
    # COL_LIST
    orderDir = request.args.get("order[0][dir]")
    columnIdx = request.args.get("order[0][column]")

    query += "order by "+COL_LIST[int(columnIdx)]+" "+orderDir+ " "

    query1 = ''
    if length != -1:
        query1 += "limit {} , {}".format(start, length)
        
    statement = db.engine.execute(query)    
    
    number_filter_row = len(list(statement))
        
    total = db.engine.execute("SELECT count(id) FROM book where is_active=1")
    
    results = db.engine.execute(query+query1)

    data = { "draw" : draw,
            "recordsTotal": int(list(total)[0][0]),
            "recordsFiltered": number_filter_row,   
            "data": [], }
    
    addTimes = int(request.args.get("add_times"))
    if addTimes > 0:        
        newData = ['']*14
        if addTimes > 5:
            addTimes = 5        
        data["data"] = [newData]*addTimes

        
    print("true new entry")

    for result in results:
        data["data"].append(list(result))
    print(query)
    print(query+query1)
    # data["recordsFiltered"] = len(data["data"])-addTimes

    print(data)
    return data

# @api.route('/')
# def index():
#     with open(DATA_PATH) as file:
#         data = json.load(file)
#     return data

# Delete data
@api.route('/<id>', methods=['DELETE'])
def delete_data(id):    
    # query = "DELETE FROM book WHERE id="+id
    query = "update book set is_active=0, updated_on='{}' where id = {}".format(datetime.utcnow(), id)
    db.engine.execute(query)
    db.session.commit()

    return {"id": id, "success": True}

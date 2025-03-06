from flask import Flask, render_template,session, request, make_response, g, redirect, url_for
from extendsForm import SearchForm, FilterForm
from database import get_db, close_db
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime, timedelta


@app.route('/logout')
def logout():
    session.clear()
    session.modified = True
    return redirect(url_for('index'))

@app.route('/shop')
@log_check
def shop():
    db = get_db()
    pets = db.execute('''
        SELECT * FROM goods;''').fetchall
    search_form = SearchForm()
    filter_form = FilterForm()
    query = '%' + '%'
    if search_form.validate_on_submit():
        query = '%' + search_form.keyword.data + '%'
    if filter_form.validate_on_submit():
        query += ''''AND XXX ='' '''
    return render_template('shop.html', pets = pets, query = query, search_form = search_form, filter_form = filter_form)


@app.route('/shop/<goods_id>')
@log_check
def goods(goods_id):
    db = get_db()
    recommendation_key = '%' + goods_id[4:8] +'%'
    goods = db.execute('''
        SELECT * FROM goods WHERE goods_id = ?;''',(goods_id,)).fetchone()
    recommendation_num = db.execute('''
        SELECT COUNT(*) FROM goods WHERE goods_id LIKE %s;''',(recommendation_key,)).fetchone
    recommendation_num = int(recommendation_num)
    recommendation = db.execute('''
            SELECT * FROM goods 
            WHERE goods_id = %s
            LIMIT 4;''',(recommendation_key,)).fetchall()
    if recommendation_num < 4:
        recommendation_left = 4 - recommendation_num
        recommendation_key = '%' + goods_id[4:5] +'%'
        recommendation2 = db.execute('''
        SELECT * 
        FROM goods 
        WHERE goods_id = %s AND NOT IN (SELECT * FROM goods 
                                        WHERE goods_id LIKE %s
                                        )
        LIMIT %i;''',(recommendation_key,recommendation_left)).fetchall()
        recommendation += recommendation2

    return render_template('goods.html', goods = goods, recommendation = recommendation)

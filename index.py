#-*- coding:utf-8 -*-
from flask import Flask, render_template, request, session
import pymysql
import datetime as dt
import sys
reload(sys)
sys.setdefaultencoding('utf8')


app = Flask(__name__)


def sellersignup(seller_id, password, sign_date, marketname):
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='1417yoo21!!', db='delivery')
    cursor = conn.cursor()
    sql = 'INSERT INTO seller (seller_id, password, sign_date, marketname) VALUES (%s, %s, %s, %s)'
    val = (seller_id, password, sign_date, marketname)
    cursor.execute(sql, val)
    conn.commit()
    conn.close()


def sellersignout(seller_id, password):
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='1417yoo21!!', db='delivery')
    cursor = conn.cursor()
    sql = 'DELETE FROM seller WHERE seller_id = %s and password = %s'
    val = (seller_id, password)
    cursor.execute(sql, val)
    conn.commit()
    conn.close()


def buyersignup(buyer_id, name, password, sign_date, phone_number):
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='1417yoo21!!', db='delivery')
    cursor = conn.cursor()
    sql = 'INSERT INTO buyer (buyer_id, name, password, sign_date, phone_number) VALUES (%s, %s, %s, %s, %s)'
    val = (buyer_id, name, password, sign_date, phone_number)
    cursor.execute(sql, val)
    conn.commit()
    conn.close()


def buyersignout(buyer_id, password):
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='1417yoo21!!', db='delivery')
    # 커서 가져오기
    cursor = conn.cursor()
    # SQL 문 만들기
    sql = 'DELETE FROM buyer WHERE buyer_id = %s and password = %s'
    val = (buyer_id, password)
    cursor.execute(sql, val)
    conn.commit()
    conn.close()

def delmenu(menu_id, seller_id):
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='1417yoo21!!', db='delivery')
    # 커서 가져오기
    cursor = conn.cursor()
    # SQL 문 만들기
    sql = 'DELETE FROM menu WHERE menu_id = %s and seller_id = %s'
    val = (menu_id, seller_id)
    cursor.execute(sql, val)
    conn.commit()
    conn.close()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signupseller.html')
def signupseller():
    return render_template('signupseller.html')


@app.route('/signupseller', methods=['GET', 'POST'])
def signupfin():
    if request.method == 'POST':
        id = request.form['seller_id']
        id = str(id)
        pw = request.form['seller_pw']
        pw = str(pw)
        markname = request.form['marketname']
        markname = str(markname)
        sellersignup(id, pw, dt.datetime.now(), markname)
    return render_template('signupfin.html')


@app.route('/signoutseller.html')
def signoutseller():
    return render_template('signoutseller.html')


@app.route('/signoutseller', methods=['GET', 'POST'])
def signoutfin():
    if request.method == 'POST':
        id = request.form['seller_id']
        id = str(id)
        pw = request.form['seller_pw']
        pw = str(pw)
        sellersignout(id, pw)
    return render_template('signoutfin.html')


@app.route('/signupbuyer.html')
def signupbuyer():
    return render_template('signupbuyer.html')


@app.route('/signupbuyer', methods=['GET', 'POST'])
def buyersignupfin():
    if request.method == 'POST':
        id = request.form['buyer_id']
        id = str(id)
        name = request.form['name']
        name = str(name)
        pw = request.form['buyer_pw']
        pw = str(pw)
        pn = request.form['pn']
        pn = str(pn)
        buyersignup(id, name, pw, dt.datetime.now(), pn)
    return render_template('signupfin.html')


@app.route('/signoutbuyer.html')
def signoutbuyer():
    return render_template('signoutbuyer.html')


@app.route('/signoutbuyer', methods=['GET', 'POST'])
def signoutbuyerfin():
    if request.method == 'POST':
        id = request.form['buyer_id']
        id = str(id)
        pw = request.form['buyer_pw']
        pw = str(pw)
        buyersignout(id, pw)
    return render_template('signoutbuyerfin.html')


@app.route('/loginseller.html')
def loginseller():
    return render_template('loginseller.html', msg=' ')


@app.route('/loginseller', methods=['GET', 'POST'])
def loginsellerop():
    msg = ' '
    if request.method == 'POST' and 'id' in request.form and 'pw' in request.form:
        # 쉬운 checking을 위해 변수에 값 넣기
        id = request.form['id']
        id = str(id)
        pw = request.form['pw']
        pw = str(pw)
        # MySQL DB에 해당 계정 정보가 있는지 확인
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='1417yoo21!!', db='delivery')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM seller WHERE seller_id = %s AND password = %s', (id, pw))
        # 값이 유무 확인 결과값 account 변수로 넣기
        account = cursor.fetchone()
        # 정상적으로 유저가 있으면 새로운 세션 만들고, 없으면 로그인 실패 문구 출력하며 index 리다이렉트
        if account:
            session['seller_id'] = id
            cursor.execute('SELECT * FROM buy WHERE seller_id = %s', (id))
            data_list = cursor.fetchall()
            return render_template('sellmanage.html', id=id, data_list=data_list)
        else:
            msg = 'Incorrect id/password!'
            return render_template('loginseller.html', msg=msg)
        # Show the login form with message (if any)


@app.route('/loginbuyer.html')
def loginbuyer():
    return render_template('loginbuyer.html', msg=' ')


@app.route('/loginbuyer', methods=['GET', 'POST'])
def loginbuyerop():
    msg = ' '
    if request.method == 'POST' and 'id' in request.form and 'pw' in request.form:
        # 쉬운 checking을 위해 변수에 값 넣기
        id = request.form['id']
        id = str(id)
        pw = request.form['pw']
        pw = str(pw)
        # MySQL DB에 해당 계정 정보가 있는지 확인
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='1417yoo21!!', db='delivery')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM buyer WHERE buyer_id = %s AND password = %s', (id, pw))
        # 값이 유무 확인 결과값 account 변수로 넣기
        account = cursor.fetchone()
        # 정상적으로 유저가 있으면 새로운 세션 만들고, 없으면 로그인 실패 문구 출력하며 index 리다이렉트
        if account:
            session['buyer_id'] = id
            cursor.execute('select distinct marketname from menu')
            # 값이 유무 확인 결과값 account 변수로 넣기
            data_list = cursor.fetchall()
            return render_template('buy.html', id=id, data_list=data_list)
        else:
            msg = 'Incorrect id/password!'
            return render_template('loginbuyer.html', msg=msg)
        # Show the login form with message (if any)


@app.route('/sellermenuman')
def sellermenuman():
    seller_id = session['seller_id']
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='1417yoo21!!', db='delivery')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM menu WHERE seller_id = %s', seller_id)
    data_list = cursor.fetchall()
    return render_template('sellermenuman.html', data_list=data_list)


@app.route('/deletemenu', methods=['GET', 'POST'])
def sellermenudel():
    menu_id = request.form['menu']
    seller_id = session['seller_id']
    delmenu(menu_id, seller_id)

    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='1417yoo21!!', db='delivery')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM menu WHERE seller_id = %s', seller_id)
    data_list = cursor.fetchall()
    return render_template('sellermenuman.html', data_list=data_list)


@app.route('/sellmenuadd')
def sellermenuadd():
    return render_template('sellermenuadd.html')


@app.route('/sellmenuadded', methods=['GET', 'POST'])
def sellermenuadded():
    if request.method == 'POST' and 'menu' in request.form and 'price' in request.form:
        menu_id = request.form['menu']
        menu_id = str(menu_id)
        price = request.form['price']
        price = str(price)
        seller_id = session['seller_id']
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='1417yoo21!!', db='delivery')
        # 커서 가져오기
        cursor = conn.cursor()
        cursor.execute('SELECT marketname from seller where seller_id = (%s)', (session['seller_id']))
        marname = cursor.fetchall()
        # SQL 문 만들기
        sql = 'INSERT INTO menu VALUES (%s, %s, %s, %s)'
        val = (menu_id, price, seller_id, marname[0][0])
        cursor.execute(sql, val)
        conn.commit()
    return render_template('sellermenuadd.html')


@app.route('/order', methods=['GET', 'POST'])
def order():
    marketname = request.form['market']
    marketname = str(marketname)
    session['marketname'] = marketname
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='1417yoo21!!', db='del'
                                                                                              'ivery')
    # 커서 가져오기
    cursor = conn.cursor()
    cursor.execute('SELECT menu_id, price from menu where marketname = (%s)', (marketname))
    data_list = cursor.fetchall()
    return render_template('order.html', id=marketname, data_list=data_list)


@app.route('/ordering', methods=['GET', 'POST'])
def ordering():
    menu_id = request.form['menu']
    menu_id = str(menu_id)
    marketname = session['marketname']
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='1417yoo21!!', db='delivery')
    # 커서 가져오기
    cursor = conn.cursor()
    cursor.execute('SELECT price from menu where marketname = (%s) and menu_id = (%s)', (marketname, menu_id))
    list1 = cursor.fetchall()
    price = list1[0][0]
    data_list = (menu_id, marketname, price)
    session['menu_id'] = menu_id
    session['price'] = price
    return render_template('ordering.html', id=menu_id, data_list=data_list)


@app.route('/ordersuccess', methods=['GET', 'POST'])
def ordersuccess():
    if request.method == 'POST' and 'paytype' in request.form and 'address' in request.form:
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='1417yoo21!!', db='delivery')
        # 커서 가져오기
        cursor = conn.cursor()
        cursor.execute('SELECT seller_id from menu where marketname = (%s)', (session['marketname']))
        a = cursor.fetchall()
        seller_id = a[0][0]
        seller_id = str(seller_id)
        cursor.execute('SELECT phone_number from buyer where buyer_id = (%s)', (session['buyer_id']))
        b = cursor.fetchall()
        phone_number = b[0][0]
        phone_number = str(phone_number)
        pay_type = request.form['paytype']
        pay_type = str(pay_type)
        address = request.form['address']
        address = str(address)
        cursor.execute('INSERT INTO buy VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                       (pay_type, session['menu_id'], session['price'], dt.datetime.now(),
                        dt.datetime.now().strftime("%H:%M:%S"), '접수중', address, session['buyer_id'], seller_id,
                        phone_number, session['marketname']))
        conn.commit()
    return render_template("ordersuccess.html")


@app.route('/sellmanage', methods=['GET', 'POST'])
def sellmanage():
    if request.method == 'POST' and 'date' in request.form and 'time' in request.form and 'orderstate' in request.form:
        date = request.form['date']
        date = str(date)
        time = request.form['time']
        time = str(time)
        order_state = request.form['orderstate']
        order_state = str(order_state)
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='1417yoo21!!', db='delivery')
        # 커서 가져오기
        cursor = conn.cursor()
        cursor.execute('UPDATE buy SET order_state = (%s) WHERE order_date = (%s) and order_time = (%s)',
                       (order_state, date, time))
        cursor.execute('SELECT * FROM buy WHERE seller_id = %s', session['seller_id'])
        data_list = cursor.fetchall()
        conn.commit()
        return render_template('sellmanage.html', id=session['seller_id'], data_list=data_list)


@app.route('/buylist', methods=['GET', 'POST'])
def buylist():
    if request.method == 'POST' and 'buyerid' in request.form:
        bid = request.form['buyerid']
        bid = str(bid)
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='1417yoo21!!', db='delivery')
        # 커서 가져오기
        cursor = conn.cursor()
        cursor.execute('SELECT marketname, pay_type, menu_id, price, order_date, order_time, order_state, address FROM buy WHERE buyer_id = (%s)', (bid))
        data_list = cursor.fetchall()
        conn.commit()
        return render_template('buylist.html', id=bid, data_list=data_list)


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run()
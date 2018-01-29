import os
import re
import time
from datetime import datetime
from multiprocessing.pool import Pool

import multiprocessing
from PIL import Image
from flask import request, redirect, url_for, render_template, flash
from flask_login import current_user
from pytesseract import pytesseract
from werkzeug.utils import secure_filename

from app import app, db
from app.checkParser import common_parse
from app.models.Goods import Goods
from app.models.Purchase import Purchase
from app.models.PurchaseConsist import PurchaseConsist
from app.models.Users import Users
from app.models.UsersPurchase import UsersPurchase
from app.sliceImage import slice_image

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def getText(filename):
    text = pytesseract.image_to_string(Image.open(filename), lang="eng+rus")
    os.remove(filename)
    return text


@app.route('/image', methods=['GET', 'POST'])
def image():
    if current_user.is_authenticated:
        if request.method == 'POST':
            try:
                file = request.files['image']

                if file.filename == '':
                    return redirect(request.url, error='No selected file')

                if file and allowed_file(file.filename):
                    filename = str(current_user) + secure_filename(file.filename)
                    path = "".join([app.config['UPLOAD_FOLDER'], filename])
                    print(path)
                    file.save(path)

                image = Image.open(path)
                images = slice_image(image, os.path.splitext(filename)[0] + '_slice')
                os.remove(path)

                text = ''

                cpuCount = multiprocessing.cpu_count()
                pool = Pool(cpuCount)
                result = pool.map(getText, images)
                pool.close()

                for res in result:
                    text += '\n'
                    text += res

                # for image in images:
                #     text += '\n'
                #     text += pytesseract.image_to_string(Image.open(image), lang="eng+rus")
                #     os.remove(image)


                result = text.split('\n')

                result, shop, address, buy_date, sum, items, payment_type = common_parse(result)
                print(shop, address, sum)

            except Exception as e:
                print(e)
                return render_template("image.html", errors=e,
                                       username=Users.query.filter_by(id=current_user.id).first().username)

            flag = False
            try:
                purchase = Purchase(buy_date, shop, float(sum), payment_type)
                purchase_new = Purchase.query.filter_by(purchase_date=purchase.purchase_date, shop=purchase.shop,
                                                        price=purchase.price).first()
                if purchase_new is None:
                    db.session.add(purchase)
                    db.session.commit()
                else:
                    purchase = purchase_new
                    print(purchase)
                    flag = True

            except Exception as e:
                print(e)
                db.session.rollback()
                return render_template("image.html", errors=e,
                                       username=Users.query.filter_by(id=current_user.id).first().username)

            try:
                user_purchase = UsersPurchase(current_user.get_id(), purchase.id)
                user_purchase_new = UsersPurchase.query.filter_by(user_id=user_purchase.user_id,
                                                                  purchase_id=user_purchase.purchase_id).first()
                if user_purchase_new is None:
                    db.session.add(user_purchase)
                    db.session.commit()
                else:
                    print(user_purchase)
                    user_purchase = user_purchase_new
                    if flag:
                        return render_template("image.html", errors="Такой чек уже есть",
                                               username=Users.query.filter_by(id=current_user.id).first().username)
            except Exception as e:
                print(e)
                db.session.rollback()
                db.session.delete(purchase)
                db.session.commit()
                return render_template("image.html", errors=e,
                                       username=Users.query.filter_by(id=current_user.id).first().username)

            goods = []
            purchases_goods = []

            for item in items:
                try:
                    good = Goods(item.get('name'), float(item.get('cost')))
                    find_good = Goods.query.filter_by(name=good.name, price=good.price).first()
                    if find_good is None:
                        db.session.add(good)
                        db.session.commit()
                        goods.append(good)
                    else:
                        good = find_good
                except Exception as e:
                    print(e)
                    db.session.rollback()
                    for g in goods:
                        db.session.delete(g)
                    for pg in purchases_goods:
                        db.session.delete(pg)
                    db.session.delete(user_purchase)
                    db.session.delete(purchase)
                    db.session.commit()
                    return render_template("image.html", errors=e,
                                           username=Users.query.filter_by(id=current_user.id).first().username)

                try:
                    purchase_consist = PurchaseConsist(good.id, user_purchase.id, item.get('number'))
                    db.session.add(purchase_consist)
                    db.session.commit()
                    purchases_goods.append(purchase_consist)
                except Exception as e:
                    print(e)
                    db.session.rollback()
                    for g in goods:
                        db.session.delete(g)
                    for pg in purchases_goods:
                        db.session.delete(pg)
                    db.session.delete(user_purchase)
                    db.session.delete(purchase)
                    db.session.commit()
                    return render_template("image.html", errors=e,
                                           username=Users.query.filter_by(id=current_user.id).first().username)
            return redirect(url_for('index'))
        else:
            return render_template("image.html", username=Users.query.filter_by(id=current_user.id).first().username)
    else:
        return redirect(url_for('login'))


@app.route('/purchase', methods=['GET', 'POST'])
def purchase():
    if current_user.is_authenticated:
        if request.method == 'POST':
            purchase_date = request.form.get("purchase_date")
            shop = request.form.get("shop")
            price = request.form.get("price")
            type = request.form.get("payment_type")

            shop_rex = '^[A-ZА-Яa-zа-я 0-9]*'
            price_rex = '[1-9]+[0-9]*(\.?[0-9]+)?'
            date_rex = '^(0[1-9]|1[0-2])/(0[1-9]|[1-2][0-9]|3[0-1])/[1-2][0-9]{3}'

            print("{} {} {} {}".format(purchase_date, shop, price, type))

            try:
                if not purchase_date:
                    raise ValueError("Дата покупки не может быть пустой")

                if not shop:
                    raise ValueError("Название магазина не может быть пустым")

                if not price:
                    raise ValueError("Сумма не может быть пустой")

                regex = re.compile(shop_rex)
                if not regex.match(shop):
                    raise ValueError("Название магазина может содержать только буквы, цифры, числа и пробел")

                regex = re.compile(price_rex)
                if not regex.match(price):
                    raise ValueError("Цена может быть щаписана только в формате ZZZ,ZZ")

                regex = re.compile(date_rex)
                if not regex.match(purchase_date):
                    raise ValueError("Дата должна быть в формате MM/DD/YYYY")

                buy_date = datetime.strptime(purchase_date, '%m/%d/%Y')

                if datetime.now() < buy_date:
                    raise ValueError("Дата не может превыщать текущую")
            except Exception as e:
                return render_template("add_purchase.html", errors=e)

            try:

                purchase = Purchase(buy_date, shop, float(price), type)
                db.session.add(purchase)
                db.session.commit()
            except Exception as e:
                print(e)
                db.session.rollback()
                return render_template("add_purchase.html", errors=e)

            try:
                print(current_user.get_id())
                user_purchase = UsersPurchase(current_user.get_id(), purchase.id)
                db.session.add(user_purchase)
                db.session.commit()
            except Exception as e:
                print(e)
                db.session.rollback()
                db.session.delete(purchase)
                db.session.commit()
                return render_template("add_purchase.html", errors=e)

            return redirect(url_for('index'))
        else:
            return render_template("add_purchase.html")
    else:
        return redirect(url_for('login'))

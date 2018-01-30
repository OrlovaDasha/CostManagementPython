from flask import request, url_for, jsonify, render_template, json
from datatables import DataTable
from flask_login import login_required, current_user

from app import app, db
from app.models.Goods import Goods
from app.models.PurchaseConsist import PurchaseConsist
from app.models.UsersPurchase import UsersPurchase


@app.route('/goods/<purchase_id>')
@login_required
def goods(purchase_id):
    print("get 1 {}".format(purchase_id))
    return render_template('goods.html', purchase_id=purchase_id)


@app.route("/get_goods/<purchase_id>", methods=['GET'])
@login_required
def get_goods(purchase_id):

    param = request.args.to_dict()
    user = current_user.id
    user_purchase = db.session.query(UsersPurchase).filter(UsersPurchase.purchase_id == purchase_id).first()
    print(user_purchase.id)

    result = db.session.query(Goods.name, Goods.price).join(PurchaseConsist).filter(
        PurchaseConsist.purchase_id == user_purchase.id).all()
    for i in result:
        print(i.name)

    table = DataTable(param, Goods,
                      db.session.query(Goods.name, Goods.price, PurchaseConsist.category).join(PurchaseConsist).filter(PurchaseConsist.purchase_id == user_purchase.id),
                      [
                          "name",
                          "price",
                          "category"
                          # ("edit", lambda
                          #     value: '<a class="btn btn-xs btn-block btn-info" href="%s"> <span class="glyphicon glyphicon-edit">'
                          #            '</span> Изменение</a>' % url_for('edit_class', class_id=value.id)),
                      ])

    return jsonify(table.json())

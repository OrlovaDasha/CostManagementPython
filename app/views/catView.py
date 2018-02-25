import operator
import re

from flask import request, jsonify
from flask_login import current_user

from app import app, db
from app.models.Category import Category
from app.models.Goods import Goods
from app.models.Products import Products
from app.views.imageView import get_items


@app.route('/add_category', methods=['POST'])
def add_category():
    if current_user.is_authenticated:
        if request.method == 'POST':
            category_name = request.form.get("new_category")
            category = db.session.query(Category).filter_by(name=category_name, user_id=current_user.id).first()
            if category is None:
                category = db.session.query(Category).filter_by(name=category_name, user_id=None).first()
                if category is None:
                    try:
                        db.session.add(Category(category_name, current_user.id))
                        db.session.commit()
                    except Exception as e:
                        print(e)
                        db.session.rollback()
                        return jsonify({"Error": e})
                    return jsonify({"Name": category_name})
            return jsonify({"Error": "Category is already in use"})


@app.route('/auto_categorization', methods=['POST'])
def auto_categorization():
    regex = re.compile('[^a-zA-Zа-яА-Я]')
    if current_user.is_authenticated:
        if request.method == 'POST':
            purchase_id = request.form.get("purchase")
            items = get_items(request)
            print(items)
            categories = db.session.query(Products).all()
            for category in categories:
                for key, value in items.items():
                    print(key + " " + items[key]["name"])
                    text = regex.sub('', items[key]["name"].replace(" ", ""))
                    word = category.name.replace(" ", "")
                    if len(text) > len(word):
                        for i in range(0, len(text) - len(word)):
                            lev = levenstein(text[i:i + len(word)].lower(), word, 1)
                            if lev <= 1:
                                print(text[i:i + len(word)].lower() + " " + word)
                                if "word" not in items[key]:
                                    items[key]["word"] = word
                                    items[key]["category"] = category.category
                                else:
                                    if len(items[key]["word"]) < len(word) or lev == 0:
                                        items[key]["word"] = word
                                        items[key]["category"] = category.category
            print(items)
            return jsonify(items)


def levenstein(word, pattern, k):
    patternLen, wordLen = len(pattern), len(word)
    prevString = [x for x in range(patternLen + 1)]

    for i in range(1, wordLen + 1):
        currentString = [i] + [None] * patternLen
        for j in range(1, patternLen + 1):
            if abs(i - j) <= k:
                if pattern[j - 1] == word[i - 1]:
                    currentString[j] = prevString[j - 1]
                else:
                    insert = currentString[j - 1] if currentString[j - 1] is not None else 100
                    delete = prevString[j] if prevString[j] is not None else 100
                    change = prevString[j - 1] if prevString[j - 1] is not None else 100
                    diff = 0 if pattern[j - 1] == word[i - 1] else 1
                    currentString[j] = min(insert + 1, delete + 1, change + diff)
        prevString = currentString
    return prevString[patternLen]


def levenstein3(word, pattern, k):
    patternLen, wordLen = len(pattern), len(word)
    diffMat = [[x for x in range(patternLen + 1)]] + [[x + 1] + [None] * patternLen for x in range(wordLen)]

    for i in range(1, wordLen + 1):
        for j in range(1, patternLen + 1):
            if abs(i - j) <= k:
                insert = diffMat[i][j - 1] if diffMat[i][j - 1] is not None else 100
                delete = diffMat[i - 1][j] if diffMat[i - 1][j] is not None else 100
                change = diffMat[i - 1][j - 1] if diffMat[i - 1][j - 1] is not None else 100
                diff = 0 if pattern[j - 1] == word[i - 1] else 1
                diffMat[i][j] = min(insert + 1, delete + 1, change + diff)
    return diffMat[wordLen][patternLen]


@app.route('/categorise', methods=['GET', 'POST'])
def categorise():
    text = "ФОАпепьсинОтборный,кг"
    word = "апельсин"

    for i in range(0, len(text) - len(word)):
        if levenstein(text[i:i + len(word)].lower(), word, 3) <= 3:
            print(text[i:i + len(word)])
    return None

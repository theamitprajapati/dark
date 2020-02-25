
import functools
import json
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,jsonify
)

from flaskr.db import get_db
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd


bp = Blueprint('admin', __name__, url_prefix='/admin')




products=[] #List to store name of the product
prices=[] #List to store price of the product
ratings=[] #List to store rating of the product


def scrap_row(url):
    products=[] #List to store name of the product
    #driver = webdriver.Chrome()
    page = requests.get(url)
    content = page.content
    html = BeautifulSoup(content,'html.parser')
    for box in html.findAll('div'):
        b = box.find('input', attrs={'class':'form-control'})
        products.append(b)
    return {'results':str(products)}    


def get_html(url):
    return scrap_row(url)



@bp.route('/dashboard')
def dashboard():
    return render_template('admin/dashboard.html')


@bp.route('/etenders')
def etenders():
    return render_template('admin/etenders.html')


@bp.route('/scrap',methods=['GET','POST'])
def scrap():
    url = request.form.get('url')
    res = get_html(url) 
    return (res)
    

from flask import Flask, render_template
import logging 
import os
from src.carinder import CarGrSearch 


log = logging.getLogger(__name__)

app = Flask(__name__,static_folder="templates",template_folder="templates")


def find_adds():
    search = "https://www.car.gr/classifieds/bikes/?fs=1&condition=used&offer_type=sale&make=22&make=22&model=1534&model=1546&model=3845&registration-from=%3E2014&significant_damage=f&rg=3&modified=2"
    results =  CarGrSearch(search)  
    return results 



@app.route("/")
def root():
    results = find_adds()
    response = []
    for add in results:
        response.append(add)
     
    return render_template("add.html",adds = response)

app.run(host="0.0.0.0")

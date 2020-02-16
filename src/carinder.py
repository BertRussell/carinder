#!/usr/bin/env python

import requests
import bs4
import re
from datetime import datetime, timedelta
from .utils import timed 
class Ad(object):
    
    @timed
    def __init__(self,url):
        html = requests.get(url)
        self.ad_soup = bs4.BeautifulSoup(html.content,"html.parser")
        self._parse()
        self.url = url 
        
    @timed 
    def _parse(self):
        self.title         = self.ad_soup.find("span",id=re.compile("^clsfd_title_")).contents[0]
        self.details_table = self.ad_soup.find("table",{"class":["vtable","table","table-striped","table-condensed"]})
        self.price       = self.details_table.find("span",{"class":"p_p","itemprop":"price"}).contents[0]
        self.upload_date = str(self._find_upload_date())
    
    @timed
    def _find_upload_date(self):
        rows = self.details_table.findChildren(['tr'])
        last_ad_update = ''
        for row in rows:
            cells = row.findChildren(['td'])
            if 'Τελευταία αλλαγή:' == cells[0].contents[0].strip():
                last_ad_update  = cells[1].contents[0]
                break
        print(last_ad_update)
        time,time_id=last_ad_update.split(" ")
        if time_id.strip() == "δευτερόλεπτα":
            return datetime.now() - timedelta(seconds=int(time))
        elif time_id.strip() == "μέρες":
            return datetime.now() - timedelta(days=int(time))
        elif time_id.strip() == "λεπτά":
            return datetime.now() - timedelta(minutes=int(time))
        elif time_id.strip() in  ["ώρες","ώρα"] :
            return datetime.now() - timedelta(hours=int(time))               

    def __str__(self):
        s =  ""
        s += "--------------------\n"
        s += "Title: {:^13}\n".format(self.title)
        s += "Price: {:^13}\n".format(self.price)
        s += "Upload date: {:^13}\n".format(self.upload_date)
        s += "Url:   {:^13}\n".format(self.url)
        s += "--------------------\n"
        return s


class CarGrSearch(object):
    
    def __init__(self,search_url:str):
        self.prefix       = "https://car.gr"
        self.search       = search_url
        self.current_page_url  = search_url
        self.current_page = self.parse_page()
        self._iter_add      = None 
        self._cur_iter_list =  self.get_adds_of_page()

    
    def __iter__(self):
        return self
    
    def __next__(self):
        return self.next()
    
    def next(self):
        if self._cur_iter_list == []:
            self.current_page_url = self.next_page_url()
            if self.current_page_url != None :
                self.current_page = self.parse_page()
                self._cur_iter_list = self.get_adds_of_page()
            else:
                raise StopIteration
        return Ad(self._cur_iter_list.pop(0))
    
    def next_page_url(self):
        next_page = self.current_page.findAll("a",{"class":"next"})
        if len(next_page) == 0:
            return None
        else:
            return self.prefix + next_page[0]["href"]
    def parse_page(self):
        html = requests.get(self.current_page_url)
        soup = bs4.BeautifulSoup(html.content,"html.parser")
        return soup 

    def get_adds_of_page(self):
        l = self.current_page.findAll("a",{"class":["vehicle","list-group-item","clsfd_list_row"]},href=True)
        return [self.prefix + a_tag["href"] for a_tag in l]


#if __name__ == "__main__":
#    search = "https://www.car.gr/classifieds/bikes/?fs=1&condition=used&offer_type=sale&make=22&make=22&model=1534&model=1546&model=3845&registration-from=%3E2014&significant_damage=f&rg=3&modified=2"
#    #search = input('search: ')
#    moto_search = CarGrSearch(search)
#    for a in moto_search:
#        print(a)

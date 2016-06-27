# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from tavrat.models import Item
from django.template.defaulttags import register
import datetime


class Owe:
    def __init__(self, a,b,c):
        self.who = a
        self.whom = b
        self.amount = c


def index(request,language='sk'):

    ###########
    # SETTINGS
    ###########

    #It's dictionary, so it contains users like nick:[fullname,fullname in dativ(only for czechoslovaks names)]
    #examle users = {'john':['John Smith','John Smithovi']}

    #users = {}
    users = {'filip': ['Filip','Filipovi'], 'kabell': ['Kabell','Kabellovi'], 'janci': ['Janči','Jančimu'],'js': ['JS','JS'] }

    #currency
    mena = u'kč'

    if request.POST:
        kto = request.POST.get(key="kto")
        komu = request.POST.get(key="komu")
        poznamka = request.POST.get(key="poznamka")
        kolko = float(request.POST.get(key="kolko").replace(',', '.'))
        datum = datetime.datetime.now().date()
        zmazane = False
        i = Item(kto=kto, komu=komu, poznamka=poznamka,kolko=kolko, datum=datum,zmazane=zmazane)
        i.save()

    table = {}
    history = {}

    for i in users:
        table[i] = {}
        history[i] = []
        for j in users:
            table[i][j] = 0


    for x in Item.objects.filter(zmazane=False):
        table[x.kto][x.komu] += int(x.kolko*100)
        history[x.kto].append(x)

    #pre istotu keby sa to náhodou zacyklilo
    for i in range(100000):
        ok = False

        #odstranime zaporne hrany
        for x in users:
            for y in users:
                if x == y:
                    continue
                if table[x][y]<0:
                    table[y][x] += -table[x][y]
                    ok = True


        #aj x dlzi y a y dlzi z, tak to prehod na x dlzi z
        for x in users:
            for y in users:
                for z in users:
                    if (not (x == y or y==z)) and table[x][y] > 0 and table[y][z] > 0:
                        mi = min(table[x][y],table[y][z])
                        table[x][y] -= mi
                        table[y][z] -= mi
                        table[x][z] += mi
                        ok = True

        #nikto nedlzi sam sebe
        for x in users:
            table[x][x] = 0

        #ak si nespravil 6iadnu zmenu, tak konci
        if not ok:
            break

    owes = []
    #roztriedime dlhy podla usera
    for x in users:
        for y in users:
            if table[x][y]>0:
                    owes.append(Owe(users[x][0], users[y][1], table[x][y]/100.0))

    return render_to_response('index_'+language+'.html', locals())


def delete(request,id):
    obj = Item.objects.get(id=id)
    obj.zmazane = True
    obj.save()

    return index(request,['Polozka bola uspesne zmazana. '])

@register.filter
def get_item(dictionary, key):
    return dictionary[key]

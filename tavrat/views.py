from django.shortcuts import render_to_response
from django.template import RequestContext
from tavrat.models import Item
import datetime

FILIP = 'filip'
KABELL = 'kabell'
JANCI = 'janci'

def index(request,messages=[]):

    if request.POST:
        kto = request.POST.get(key="kto")
        komu = request.POST.get(key="komu")
        poznamka = request.POST.get(key="poznamka")
        kolko = float(request.POST.get(key="kolko").replace(',','.'))
        datum = datetime.datetime.now().date()
        zmazane = False
        i = Item(kto=kto, komu=komu, poznamka=poznamka,kolko=kolko, datum=datum,zmazane=zmazane)
        i.save()

    kabell_to_filip = 0.0
    filip_to_janci = 0.0
    janci_to_kabell = 0.0


    kabell=[]
    for x in Item.objects.filter(kto=KABELL):
        if not x.zmazane:
            if x.komu == FILIP:
                kabell_to_filip += x.kolko
            elif x.komu == JANCI:
                janci_to_kabell -= x.kolko
            kabell.append(x)

    filip=[]
    for x in Item.objects.filter(kto=FILIP):
        if not x.zmazane:
            if x.komu == KABELL:
                kabell_to_filip -= x.kolko
            elif x.komu == JANCI:
                filip_to_janci += x.kolko
            filip.append(x)

    janci=[]
    for x in Item.objects.filter(kto=JANCI):
        if not x.zmazane:
            if x.komu == FILIP:
                filip_to_janci -= x.kolko
            elif x.komu == KABELL:
                janci_to_kabell += x.kolko
            janci.append(x)



    najm = min([kabell_to_filip,filip_to_janci,janci_to_kabell])
    kabell_to_filip -= najm
    filip_to_janci -= najm
    janci_to_kabell -=najm


    najv = max([kabell_to_filip,filip_to_janci,janci_to_kabell])

    sucet = kabell_to_filip + filip_to_janci + janci_to_kabell

    sucet1 = abs(kabell_to_filip + filip_to_janci + janci_to_kabell-3*najv)

    smer = 1

    if sucet>sucet1:
        smer=2
        kabell_to_filip = abs(kabell_to_filip - najv)
        filip_to_janci = abs(filip_to_janci - najv)
        janci_to_kabell = abs(janci_to_kabell - najv)

    return render_to_response('index.html', locals())


def delete(request,id):
    obj = Item.objects.get(id=id)
    obj.zmazane = True
    obj.save()

    return index(request,['Polozka bola uspesne zmazana. '])

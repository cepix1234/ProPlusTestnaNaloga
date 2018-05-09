# ProPlusTestnaNaloga
Poženi server.py v pythonu.
preko brskalnika se poveži na http://localhost:8080/cron se prvič požene python skripta za pridobivanje RSS podatkov izdarsa
ob klicu na http://localhost:8080/events se prikažejo dogotki ki so bili pridobljeni s RSS strani + 2 argumenta za prikazs samo avtocest in glavnih cest

json format RSS podatkov se shrnjuje lokalno v besedilni datoteki. ob klicu events se ti podatki vnesejov html stran kater potem uporabi javascript za prikaz.

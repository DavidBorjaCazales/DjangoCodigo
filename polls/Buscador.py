#!/usr/bin/env python
# -*- coding: utf-8 -*-

from algoritmo_testing import Recomendaciones
#Laptop Dell Inspiron 15-5558 Core i7 6 GB RAM 1TB	Computadoras#f-computo-laptops#l-laps-dell	16499.0
Phi=15
precio=16499.0
Historial=[]
CategoriaSitio="Computadoras,f-computo-laptops,l-laps-dell"
algoritmo=Recomendaciones()
print  algoritmo.Recomendar(["Laptop Dell Inspiron 15-5558 Core i7 6 GB RAM 1TB"],precio,CategoriaSitio,Historial,Phi)

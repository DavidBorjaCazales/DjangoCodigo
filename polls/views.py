# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#!/usr/bin/env python
# -*- coding: utf-8 -*-


from rest_framework import status
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from polls.models import Restaurants
from rest_framework.renderers import JSONRenderer
from polls.serializers import RestaurantsSerializer
from django.conf import settings
#from geopy.distance import vincenty
#from algoritmo_testing import Buscador
# Create your views here.


class Statics(APIView):
    """
    Metodos permitidos GET
    Regresa un JSON con los campos promedio de Raiting,Desviacion,Promedio de Raiting.
    """

    def get(self, request,latitude,longitude,radius, format=None):

        r = Restaurants.objects.all()

        latitude=float(latitude)
        longitude=float(longitude)
        radius=float(radius)

        PointA=(latitude,longitude)
        ratings=0.0
        desviacion=0.0
        count=0
        list_ratings=[]
        Avg=0.0

        for a in r:
         PointB=(a.lat,a.lng)
         distance=vincenty(PointA,PointB).meters

         if distance <= radius:
          count=count+1
          ratings=ratings+a.rating
          list_ratings=list_ratings+[a.rating]

        if count>0:
         Avg= float(ratings)/float(count)

        sumatoria=0

        for a in list_ratings:
         sumatoria= sumatoria+((Avg-float(a))**2)
        
        if count>0:
         desviacion=((sumatoria/(count-1))**0.5)

        a={"Count":count,"Avg":Avg,"S":desviacion}
        return Response(a)


class Busqueda(APIView):
    """
    Metodos permitidos GET
    Lista todos los productos dado el nombre de producto
    """

    def get(self, request, producto ,format=None):
        #r = Restaurants.objects.all()
        #serializer = RestaurantsSerializer(r, many=True)
        #PatronRecomendaciones=[producto]
        #Phi=50
        #Historial=[]
        #algoritmo=Buscador()
        #ListaProductos=algoritmo.Buscar(PatronRecomendaciones,Historial,Phi)
        ListaProductos=["1","2","3"]
        a={"Productos":ListaProductos}
        return Response(a)



class Restaurants_detail(APIView):
    """
    Metodos permitidos GET,UPDATE,POST, PUT y DELETE
    Retrieve, update, create or delete a code Restaurant with the id.
    """

    def get_object(self, pk):
        try:
            return Restaurants.objects.get(pk=pk)
        except Restaurants.DoesNotExist:
            raise Http404


    def get(self, request, pk, format=None):
        r = self.get_object(pk)
        serializer = RestaurantsSerializer(r)
        return Response(serializer.data)


    def post(self, request, format=None):
        serializer = RestaurantsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, pk, format=None):
        r = self.get_object(pk)
        serializer = RestaurantsSerializer(r, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        r = self.get_object(pk)
        r.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

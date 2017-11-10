from rest_framework import serializers
from polls.models import Restaurants

# Serializacion del modelo Restaurants y sus respectivos campos:
# 'id','rating','name','site','email','phone','street','city','state','lat','lng'

class RestaurantsSerializer(serializers.ModelSerializer):
    class Meta:
     model = Restaurants
     fields=('id','rating','name','site','email','phone','street','city','state','lat','lng')

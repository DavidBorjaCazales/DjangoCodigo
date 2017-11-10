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

from django.db import models

# Create your models here.


#Modelo Restaurants
 
class Restaurants (models.Model):
 rating= models.IntegerField() #INTEGER, -- Number between 0 and 4
 name=models.CharField(max_length=100) #TEXT -- Name of the restaurant
 site=models.CharField(max_length=100) #TEXT -- Url of the restaurant
 email=models.CharField(max_length=100) #TEXT,
 phone=models.CharField(max_length=100) #TEXT
 street=models.CharField(max_length=100) #TEXT
 city=models.CharField(max_length=100) #TEXT
 state=models.CharField(max_length=100) #TEXT
 lat=models.FloatField() #FLOAT -- Latitude
 lng=models.FloatField() #FLOAT -- Longitude

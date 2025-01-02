#services/service_layer.py
from django.db import models


class ServiceLayer:
    def __init__(self,model:models.Model):
        self.model = model

    def create(self,**kwargs):
        return self.model.objects.create(**kwargs)

    def get(self, **kwargs):
        return self.model.objects.get(**kwargs)


    def filter(self,**kwargs):
        return self.model.objects.filter(**kwargs)

    def update(self,pk,**kwargs):
        return self.model.objects.filter(pk=pk).update(**kwargs)  

    def delete(self,pk):
        return self.model.objects.filter(pk=pk).delete()
    
    def all(self):
        return self.model.objects.all()

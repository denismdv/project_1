from django.db import models

class Mebel(models.Model):
    link = models.TextField("Ссылка")
    price = models.DecimalField("Цена", decimal_places=2, max_digits=12)
    description = models.TextField("Название автомобиля")
    
    def __str__(self):
        return f'{self.price} | {self.description}'

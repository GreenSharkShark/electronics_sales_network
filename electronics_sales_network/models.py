from django.db import models


NULLABLE = {'null': True, 'blank': True}


class Contact(models.Model):
    email = models.EmailField(verbose_name='почта')
    country = models.CharField(max_length=100, verbose_name='страна')
    city = models.CharField(max_length=100, verbose_name='город')
    street = models.CharField(max_length=100, verbose_name='улица')
    house_number = models.CharField(max_length=10, verbose_name='номер дома')

    def __str__(self):
        return f"{self.email} - {self.city}, {self.country}"


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='название')
    model = models.CharField(max_length=255, verbose_name='модель')
    release_date = models.DateField(verbose_name='дата выхода на рынок')

    def __str__(self):
        return f"{self.name} - {self.model}"


class ChainLink(models.Model):
    name = models.CharField(max_length=255, verbose_name='название')
    contacts = models.ForeignKey(Contact, on_delete=models.CASCADE, verbose_name='контакты')
    products = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='продукты')
    supplier = models.ForeignKey('self', on_delete=models.CASCADE, related_name='suppliers', verbose_name='поставщик',
                                 **NULLABLE)
    debt_to_the_supplier = models.DecimalField(max_digits=10, decimal_places=2,
                                               verbose_name='задолженность перед поставщиком', **NULLABLE)
    date_of_creation = models.DateTimeField(auto_now_add=True)
    is_factory = models.BooleanField(default=False, verbose_name='завод')
    is_retail_network = models.BooleanField(default=False, verbose_name='розничная сеть')
    is_individual_entrepreneur = models.BooleanField(default=False, verbose_name='индивидуальный предприниматель')

    def __str__(self):
        if self.is_factory:
            return f"{self.name}, завод"
        elif self.is_retail_network:
            return f"{self.name}, розничная сеть"
        elif self.is_individual_entrepreneur:
            return f"{self.name}, индивидуальный предприниматель"
        else:
            return f"{self.name}, тип занятости не указан"

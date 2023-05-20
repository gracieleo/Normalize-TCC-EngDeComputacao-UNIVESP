from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

STATE_CHOICES = (
    ('Acre', 'Acre'),('Alagoas', 'Alagoas'),('Amapá', 'Amapá'),('Amazonas', 'Amazonas'),
    ('Bahia', 'Bahia'),('Ceará', 'Ceará'),('Espírito Santo', 'Espírito Santo'),('Goiás', 'Goiás'),
    ('Maranhão', 'Maranhão'),('Mato Grosso', 'Mato Grosso'),('Mato Grosso do Sul', 'Mato Grosso do Sul'),
    ('Minas Gerais', 'Minas Gerais'),('Pará', 'Pará'),('Paraíba', 'Paraíba'),('Paraná', 'Paraná'),
    ('Pernambuco', 'Pernambuco'),('Piauí', 'Piauí'),('Rio de Janeiro', 'Rio de Janeiro'),
    ('Rio Grande do Norte', 'Rio Grande do Norte'),('Rio Grande do Sul', 'Rio Grande do Sul'),
    ('Rondônia', 'Rondônia'),('Roraima', 'Roraima'),('Santa Catarina', 'Santa Catarina'),
    ('São Paulo', 'São Paulo'),('Sergipe', 'Sergipe'),('Tocantins', 'Tocantins'),('Distrito Federal', 'Distrito Federal'),
)

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=50)

    def __str__(self):
        return str(self.id)


CATEGORY_CHOICES = (
    ('PC', 'Proteção Cabeça'),
    ('PA', 'Proteção Auditiva'),
    ('PR', 'Proteção Respiratória'),
    ('PM', 'Proteção Mãos'),
    ('PP', 'Proteção Pés'),
)

class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=2)
    sub_category = models.TextField()
    product_image = models.ImageField(upload_to='productimg')


    def __str__(self):
        return str(self.id)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

STATUS_CHOICES = (
    ('Aceito','Aceito'),
    ('Enviado','Enviado'),
    ('A Caminho','A Caminho'),
    ('Entregue','Entregue'),
    ('Cancelado','Cancelado')
)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pendente')

    @property
    def total_cost(self):
      return self.quantity * self.product.discounted_price




from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class tshirtproperty(models.Model):
     title=models.CharField( max_length=50)
     slug=models.CharField( max_length=50,unique=True)
     class Meta:
         abstract=True
     def __str__(self):
          return self.title

class Occasion(tshirtproperty):
  pass
class Idealfor(tshirtproperty):
  pass
class Necktype(tshirtproperty):
   pass

class Sleeve(tshirtproperty):
  pass
class Brand(tshirtproperty):
   pass

class Color(tshirtproperty):
   pass

class Tshirt(models.Model):
    name=models.CharField( max_length=50)
    slug=models.CharField( max_length=200)
    desc=models.CharField( max_length=50)
    discount=models.IntegerField(default=0)
    image=models.ImageField( upload_to="upload/images", )
    occasion=models.ForeignKey(Occasion, on_delete=models.CASCADE)
    brand=models.ForeignKey(Brand, on_delete=models.CASCADE)
    color=models.ForeignKey(Color, on_delete=models.CASCADE)
    necktype=models.ForeignKey(Necktype, on_delete=models.CASCADE)
    idealfor=models.ForeignKey(Idealfor, on_delete=models.CASCADE)
    sleeve=models.ForeignKey(Sleeve, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class blogcomment(models.Model):
    comment=models.TextField()
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    tshirt=models.ForeignKey(Tshirt, on_delete=models.CASCADE)
    parent=models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timestamp=models.DateTimeField()

    def __str__(self):
        return self.comment

class Sizevariant(models.Model):
    SIZES=(
        ('S','Small'),
        ('M','Medium'),
        ('L','Large'),
        ('XL','Xtra Large'),
    )
    price=models.IntegerField()
    tshirt=models.ForeignKey(Tshirt, on_delete=models.CASCADE)
    size=models.CharField(choices=SIZES, max_length=50)
class Cart(models.Model):
  sizevariant=models.ForeignKey(Sizevariant, on_delete=models.CASCADE)
  quantity=models.IntegerField(default=1)
  user=models.ForeignKey(User, on_delete=models.CASCADE)

class Order(models.Model):
  orderstatus=(
    ('PENDING','Pending'),
    ('PLACE','Place'),
    ('CANCELLED','Cancelled'),
    ('COMPLETED','Completed'),
    
  )
  method=(
    ('COD','Cash On Delivery'),
    ('ONLINE','Online'),

  )
  order_status=models.CharField( max_length=50,choices=orderstatus)
  payment_method=models.CharField( max_length=50,choices=method)
  shipping_adress=models.CharField( max_length=500)
  phone=models.CharField( max_length=50)
  user=models.ForeignKey(User, on_delete=models.CASCADE)
  total=models.IntegerField()
  date=models.DateTimeField( auto_now_add=True)

class Orderitem(models.Model):
  order=models.ForeignKey(Order, on_delete=models.CASCADE)
  tshirt=models.ForeignKey(Tshirt, on_delete=models.CASCADE)
  size=models.ForeignKey(Sizevariant, on_delete=models.CASCADE)
  quantity=models.IntegerField()
  price=models.IntegerField()
  dare=models.DateTimeField( auto_now_add=True)

class Payment(models.Model):
  order=models.ForeignKey(Order, on_delete=models.CASCADE)
  payment_status=models.CharField( max_length=50,default='Failed')
  payment_id=models.CharField(max_length=100)
  payment_request_id=models.CharField(max_length=100, unique=True)
  date=models.DateTimeField(auto_now_add=True)



  
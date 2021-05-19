from django import template
from math import floor

register=template.Library()


@register.simple_tag
def is_in_cart(tshirt,cart,size):
  for i in cart:
      if i['tshirt']==tshirt.id and i['size']==size:
          return True
  return False


@register.simple_tag
def cart_quantity(tshirt, cart,size):
    for i in cart:
        if i['tshirt'] == tshirt.id and i['size']==size:
            return i['quantity']
        
      
      

@register.simple_tag
def sale_price(tshirt):
    price=min_price(tshirt)
    discount=tshirt.discount
    return floor(price-(price*(discount/100)))
   
@register.simple_tag
def min_price(tshirt):
    min_price=tshirt.sizevariant_set.all().order_by('price').first()
    return floor(min_price.price)
    
@register.filter(name='get_val')
def get_val(dict,key):
    return dict.get(key)

@register.filter
def totalamount(cart):
    total=0
    for c in cart:
        discount=c.get('tshirt').discount
        price=c.get('size').price
        pricetotal=floor(price-(price * (discount/100)))
        totalofsingle=pricetotal * c.get('quantity')
        total= total + totalofsingle
    return total
@register.filter
def gettotal(order):
    total=0
    for oi in order.orderitem_set.all():
        single=oi.price * oi.quantity
        total = [total + single]
        return sum(total)

@register.simple_tag
def emty(orders):
    if len(orders) == 0:
        return "No Item Cart Yet"
   
    

@register.simple_tag
def multiply(a,b):
   return a*b


@register.simple_tag
def price(price,discount):
   return floor(price-(price * (discount/100)))

    

    


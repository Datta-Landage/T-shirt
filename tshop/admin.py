from django.contrib import admin
from .models import blogcomment,Sleeve,Color,Occasion,Tshirt,Brand,Necktype,Idealfor,Sizevariant,Cart,Order,Orderitem,Payment

# Register your models here.

class adminconfi(admin.TabularInline):
    model=Sizevariant

class admintshirt(admin.ModelAdmin):
    inlines=[adminconfi]

admin.site.register(Tshirt,admintshirt)
admin.site.register(Sleeve)
admin.site.register(Color)
admin.site.register(blogcomment)
admin.site.register(Occasion)
admin.site.register(Brand)
admin.site.register(Necktype)
admin.site.register(Idealfor)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Orderitem)
admin.site.register(Payment)



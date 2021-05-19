from django.shortcuts import render
from django.contrib.auth import authenticate
from django.shortcuts import render,redirect,HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import Signupform,loginform,adressform,pachange,profilechangeform

from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.csrf import csrf_exempt
from time import time
from datetime import datetime
from .models import blogcomment,Tshirt,Sizevariant,Cart,Order,Orderitem,Payment,Brand,Occasion,Color,Sleeve,Necktype,Idealfor
from math import floor
from django.contrib.auth.decorators import login_required
from instamojo_wrapper import Instamojo
from newproject.settings import API_KEY,AUTH_TOKEN
api = Instamojo(api_key=API_KEY, auth_token=AUTH_TOKEN, endpoint='https://test.instamojo.com/api/1.1/');


# Create your views here.
def deleteitem(request):
    if request.method =="POST":
        tshirt=request.POST.get("tshirt")
        cart=request.session.get('cart')
        for item in cart:
            if item.get('tshirt')==int(tshirt):
                cart.remove(item)
           
        request.session['cart']=cart
        return redirect('cart')
def userprofile(request):
    if request.method=="POST":
        form=profilechangeform(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request,"Profile Updated Successfully..!")
        return HttpResponseRedirect("/")
    else:
        form=profilechangeform(instance=request.user)
    return render(request,"profile.html",{"form":form})
def index(request):
    tshirts=None
    occasions=Occasion.objects.all()
    colors=Color.objects.all()
    sleeves=Sleeve.objects.all()
    necktypes=Necktype.objects.all()
    idealfors=Idealfor.objects.all()
    brands=Brand.objects.all()
    tshirts=Tshirt.objects.all()
    color=request.GET.get('color')
    sleeve=request.GET.get('sleeve')
    brand=request.GET.get('brand')
    necktype=request.GET.get('necktype')
    occasion=request.GET.get('occasion')
    idealfor=request.GET.get('idealfor')
    if color:
        tshirts=Tshirt.objects.filter(color=color)
    if sleeve:
        tshirts=Tshirt.objects.filter(sleeve=sleeve)
    if necktype:
        tshirts=Tshirt.objects.filter(necktype=necktype)
    if brand:
        tshirts=Tshirt.objects.filter(brand=brand)
    if idealfor:
        tshirts=Tshirt.objects.filter(idealfor=idealfor)
    if occasion:
        tshirts=Tshirt.objects.filter(occasion=occasion)

    return render(request,"index.html",{"tshirts":tshirts,'colors':colors,'brands':brands,'sleeves':sleeves,'necktypes':necktypes,'idealfors':idealfors,'occasions':occasions})

def userlogin(request):
    if not request.user.is_authenticated:
        if request.method=="POST":
            form=loginform(request=request, data=request.POST)
           
            if form.is_valid():
                username=form.cleaned_data['username']
                password=form.cleaned_data['password']
                user=authenticate(username=username,password=password)
                if user is not None:
                    login(request,user)
                    messages.success(request,"Succesfully Login")
                    session_cart=request.session.get('cart')
                    if session_cart is None:
                        session_cart=[]
                    else:
                        for c in session_cart:
                            size=c.get('size')
                            tshirt_id=c.get('tshirt')
                            quantity=c.get('quantity')
                            cart_obje=Cart()
                            cart_obje.sizevariant=Sizevariant.objects.get(size=size,tshirt=tshirt_id)
                            cart_obje.quantity=quantity
                            cart_obje.user=user
                            cart_obje.save()
                    cart=Cart.objects.filter(user=user)
                    session_cart=[]
                    for c in cart:
                        obje={"size":c.sizevariant.size,"tshirt":c.sizevariant.tshirt.id,"quantity":c.quantity}
                        session_cart.append(obje)
                    request.session['cart']=session_cart 
                    next_page=request.session.get('next_page')   
                    if next_page is None:
                        next_page='home'
                    
                    return redirect(next_page)
                
        else:
            form=loginform()
            next_page=request.GET.get('next')
            if next_page is not None:
                request.session['next_page']=next_page
        return render(request,'login.html',{"form":form})
    else:
        return redirect('/')


def signup(request): 
    if not request.user.is_authenticated:
        if request.method=="POST":

            form=Signupform(request.POST)
            if form.is_valid():

                form.save()
                form=Signupform()
                messages.success(request,"Congratutions!!! Welcome")
                return redirect('login')
        else:
          form=Signupform()
        return render(request,'signup.html',{"form":form})
    else:
        return redirect('/')

def userlogout(request):
    logout(request)
    return redirect('/')

# def usersignup(request):
#     return render(request,"signup.html")

def productpage(request,slug):
    cart=request.session.get('cart')
    tshirt=Tshirt.objects.get(slug=slug)
    size=request.GET.get('size')
    if size is None:
         size=tshirt.sizevariant_set.all().order_by('price').first()
    else:
        size=tshirt.sizevariant_set.get(size=size)
    size.price =floor(size.price)
    discount=size.price-(size.price*(tshirt.discount/100))
    discount=floor(discount)
    activesize=size
    comment=blogcomment.objects.filter(tshirt=tshirt,parent=None)
    replies=blogcomment.objects.filter(tshirt=tshirt).exclude(parent=None)
    replydict={}
    for reply in replies:
        if reply.parent.id not in replydict.keys():
            replydict[reply.parent.id]=[reply]
        else:
            replydict[reply.parent.id].append(reply)
    print(replydict)
    return render(request,"product.html",{"tshirt":tshirt,"comment":comment,"replydict":replydict,"sell_price":size.price,"discount":discount,"activesize":activesize,"cart":cart})

               
def removequantity(request,slug,size):
    cart=request.session.get('cart')
    if cart is  None:
        cart=[]
    tshirt=Tshirt.objects.get(slug=slug)
    tshirtsize=Sizevariant.objects.get(size=size,tshirt=tshirt)
    for cart_obje in cart:
        tshirt_id=cart_obje.get("tshirt")
        size_short=cart_obje.get('size')
        if tshirt_id==tshirt.id and size_short==size:
            cart_obje['quantity']=cart_obje['quantity']-1
            if cart_obje['quantity']==0:
                cart_obje['quantity']=cart_obje['quantity']+1
                messages.info(request,"Please Quantity Not Zero!!!")
           

    request.session['cart']=cart
    return_url=request.GET.get('return_url')
    return redirect(return_url)


def add_to_cart(request,slug,size):
    user=None
    if request.user.is_authenticated:
        user=request.user
    
    cart=request.session.get('cart')
    
    if cart is  None:
        cart=[]
    tshirt=Tshirt.objects.get(slug=slug)
    tshirtsize=Sizevariant.objects.get(size=size,tshirt=tshirt)
    flag =True
    for cart_obje in cart:
        tshirt_id=cart_obje.get("tshirt")
        size_short=cart_obje.get('size')
        if tshirt_id==tshirt.id and size_short==size:
            flag=False
            cart_obje['quantity']=cart_obje['quantity']+1
       
    if flag:
        cart_obje={
            'tshirt':tshirt.id,'size':size,'quantity':1
        }
        cart.append(cart_obje)
        messages.success(request,"Item Added Successfully:")
    if user is not None:       
        existing=Cart.objects.filter(user=user,sizevariant=tshirtsize)
        if len(existing) > 0:
            obje=existing[0]
            obje.quantity=obje.quantity + 1
            obje.save()
        
        else:
            c= Cart()
            c.user=user
            c.sizevariant=tshirtsize
            c.quantity=1
            c.save()   
    
       
    request.session['cart']=cart
    return_url=request.GET.get('return_url')
    return redirect(return_url)
def cartitem(request):
    cart=request.session.get('cart')
    
    # if cart is None:
    #     cart=[]
    # for c in cart:
    #     tshirt_id=c.get('tshirt')
    #     tshirt=Tshirt.objects.get(id=tshirt_id)
    #     c['size']=Sizevariant.objects.get(tshirt=tshirt_id, size=c['size'])
    #     c['tshirt']=tshirt
    if cart is None:
        cart=[]
    for c in cart:
        tshirt_id=c.get('tshirt')
        tshirt=Tshirt.objects.get(id=tshirt_id)
        c['size']=Sizevariant.objects.get(tshirt=tshirt_id, size=c['size'])
        c['tshirt']=tshirt
    return render(request,"cart.html",{"cart":cart})

def passchange(request):
    if request.method=="POST":

        form=pachange(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request," Your Password Update Successfully..!!")
            return HttpResponseRedirect("/")

    else:
        form=pachange(user=request.user)

    return render(request,"passchange.html",{"form":form})

    
def removeitem(request):
    cart=request.session.get('cart')
    if 'cart' in request.session:
        del request.session['cart']
    
    return redirect('cart')
    
def totalamount(cart):
    total=0
    for c in cart:
       
        discount=c.get('tshirt').discount
        price=c.get('size').price
        pricetotal=floor(price-(price * (discount/100)))
        totalofsingle=pricetotal * c.get('quantity')
        total= total + totalofsingle
    return total

@login_required(login_url='login')
def checkout(request):
    if request.method=="GET":
        form=adressform()
        cart=request.session.get('cart')
        if cart is None:
            cart=[]
        for c in cart:
            size_str=c.get('size')
            tshirt_id=c.get('tshirt')
            size_obje=Sizevariant.objects.get(size=size_str,tshirt=tshirt_id)
            c['size']=size_obje
            c['tshirt']=size_obje.tshirt
        return render(request,"checkout.html",{"form":form,"cart":cart})
    else:
        form=adressform(request.POST)
        user=None
        if request.user.is_authenticated:
            user=request.user
        if form.is_valid():
            cart=request.session.get('cart')
            if cart is None:
                cart=[]
            for c in cart:
                size_str=c.get('size')
                tshirt_id=c.get('tshirt')
                size_obje=Sizevariant.objects.get(size=size_str,tshirt=tshirt_id)
                c['size']=size_obje
                c['tshirt']=size_obje.tshirt
            shipping_adress=form.cleaned_data.get('shipping_adress')
            phone=form.cleaned_data.get('phone')
            payment_method=form.cleaned_data.get('payment_method')
            total=totalamount(cart)
            order=Order()
            order.shipping_adress=shipping_adress
            order.phone=phone
            order.payment_method=payment_method
            order.total=total
            order.order_status='PENDING'
            order.user=user
            order.save()
            for c in cart:
                order_item=Orderitem()
                order_item.order=order
                size=c.get('size')
                tshirt=c.get('tshirt')
                order_item.price=floor(size.price-(size.price * (tshirt.discount/100)))
                order_item.quantity=c.get('quantity')
                order_item.size=size
                order_item.tshirt=tshirt
                order_item.save()
            response = api.payment_request_create(
            amount=order.total,
            purpose='For Tshirt',
            buyer_name=user.first_name,
            send_email=True,
            email=user.email,
            redirect_url="http://127.0.0.1:8000/validate_payment" )
            payment_request_id=response['payment_request']['id']
            url=response['payment_request']['longurl']
            payment=Payment()
            payment.order=order
            payment.payment_request_id=payment_request_id
            payment.save()
            return redirect(url)
          

def validate_payment(request):
    user=None
    if request.user.is_authenticated:
        user=request.user
    payment_request_id=request.GET.get('payment_request_id')
    payment_id=request.GET.get('payment_id')
    print(payment_request_id,payment_id)
    response = api.payment_request_payment_status(payment_request_id,payment_id)   
    status= response.get('payment_request').get('payment').get('status')
    print(status)  
    if status != "Failed":
        try:
            payment=Payment.objects.get(payment_request_id=payment_request_id)
            payment.payment_id=payment_id
            payment.payment_status=status
            payment.save()
            order=payment.order
            order.order_status='PLACE'
            order.save()
            cart=[]
            request.session['cart']=cart
            Cart.objects.filter(user=user).delete()

            
        except:
            return render(request,"paymentfailed.html")
    else:
        return render(request,"paymentfailed.html")
    return redirect('order')
@login_required(login_url='login')
def orderpage(request):
    user=request.user
    orders=Order.objects.filter(user=user).order_by('-date').exclude(order_status='PENDING')
    return render(request,"order.html",{"orders":orders})
        
def delete_session(request,id):

    the_id=request.session['tshirt_id']
    cart=Cart.objects.get(id=the_id)
    cart.delete()
    
    return redirect('cart')
def search(request):
    query=request.GET['query']
    if len(query) > 50:
        tshirt=[]
    else:
        tshirtname=Tshirt.objects.filter(name__icontains=query)
        tshirtdesc=Tshirt.objects.filter(desc__icontains=query)
        tshirts=tshirtname.union(tshirtdesc)
    return render(request,"search.html",{"tshirts":tshirts,"query":query})

def postcommentss(request):
    if request.method=="POST":
        comment=request.POST.get('comment')
        user=request.user
        tshirtslug=request.POST.get('tshirtslug')
        tshirt=Tshirt.objects.get(slug=tshirtslug)
        parentSno=request.POST.get('parentSno')
        if parentSno=="":

            comment=blogcomment(comment=comment,user=user,tshirt=tshirt,timestamp=datetime.today())
            comment.save()
            messages.success(request,"Comment Added Successfully")
        else:
            parent=blogcomment.objects.get(id=parentSno)
            comment=blogcomment(comment=comment,user=user,tshirt=tshirt,timestamp=datetime.today(),parent=parent)
            comment.save()
            messages.success(request,"Reply Comment Added Successfully")
    
    return redirect(f"/product/{tshirt.slug}")


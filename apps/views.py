from django.contrib import auth
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import doctor, appointment, booking, admin_table, user_detls, products, med_history, cart
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.mail import EmailMessage

from django.contrib.auth import authenticate, login
import pymongo
from django.conf import settings


# Create your views here.
# client = pymongo.MongoClient()
# db = client['Hospital']

# ________________________Admin________________________#


# User & Admin Login
def login(request):
    try:
        if request.method == "POST":
            temp = admin_table.objects.get(name=request.POST['uname'])
            if temp.password == request.POST['password']:
                request.session['user_id'] = temp.id
                return redirect('adminhome')
            else:
                messages.error(request, 'Invalid username or password!!')
                return redirect('login')
        else:
            if 'user_id' in request.session:
                return redirect('adminhome')
            else:
                return redirect('login_page')

    except:
        if request.method == "POST":
            username = request.POST['uname']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('userhome')
            else:
                messages.error(request, 'Invalid username or password!!')
                return redirect('login')
        else:
            return render(request, 'login.html')


def login_page(request):
    return render(request, 'login.html')


def admin_logout(request):
    del request.session['user_id']
    return redirect('login')


def adminhome(request):
    if 'user_id' in request.session:
        return render(request, 'admin/adminpg.html')
    else:
        return redirect('login')


def adddoc(request):
    if 'user_id' in request.session:
        if request.method == "POST":
            dname = request.POST['dname']
            spec = request.POST['spec']
            gdr = request.POST['gender']
            user = doctor.objects.create(name=dname, specialization=spec, gender=gdr)
            user.save()
            return redirect('adddoc')
        else:
            return render(request, 'admin/adddoc.html')
    else:
        return redirect('login')


def viewdoc(request):
    if 'user_id' in request.session:
        d = doctor.objects.all()
        return render(request, 'admin/viewdoc.html', {'doctor': d})
    else:
        return redirect('login')


def viewusers(request):
    if 'user_id' in request.session:
        user = User.objects.all()
        dets = user_detls.objects.all()
        return render(request, 'admin/userview.html', {'user': user, 'details': dets})
    else:
        return redirect('login')


"""def add_date(request, id):
    if 'user_id' in request.session:
        if request.method == "POST":
            d_date = request.POST['date']
            a = appointment.objects.create(date=d_date, doctor_id=id)
            a.save()
            return redirect('add_date', id)

        else:
            doc = doctor.objects.filter(id=id)
            dates = appointment.objects.filter(doctor_id=id)
            return render(request, 'admin/available_dates.html', {'doct': doc, 'date': dates})
    else:
        return redirect('login')"""


def del_date(request, id):
    if 'user_id' in request.session:
        temp = appointment.objects.get(id=id)
        d1 = doctor.objects.get(id=temp.doctor_id)
        doc = doctor.objects.filter(id=d1.id)
        dates = appointment.objects.filter(doctor_id=d1)
        appointment.objects.get(id=id).delete()
        return render(request, 'admin/available_dates.html', {'doct': doc, 'date': dates})
    else:
        return redirect('login')


def add_medicine(request):
    if 'user_id' in request.session:
        if request.method == "POST":
            mname = request.POST['med_name']
            desc = request.POST['desc']
            price = request.POST['price']
            warng = request.POST['warning']
            qty = request.POST['quantity']
            med = products.objects.create(product_name=mname, description=desc, price=price, warning=warng,
                                          quantity=qty)
            med.save()
            return redirect(add_medicine)
        else:
            return render(request, 'admin/add_med.html')
    else:
        return redirect('login')


def view_medicine(request):
    if 'user_id' in request.session:
        m = products.objects.all()
        return render(request, 'admin/view_med.html', {'det': m})


def del_medicine(request, id):
    if 'user_id' in request.session:
        products.objects.get(id=id).delete()
        return redirect('view_medicine')


def del_doc(request, id):
    if 'user_id' in request.session:
        doctor.objects.get(id=id).delete()
        return redirect('viewdoc')


def del_user(request, id):
    if 'user_id' in request.session:
        User.objects.get(id=id).delete()
        return redirect('viewusers')


def view_booking(request):
    if 'user_id' in request.session:
        user = User.objects.all()
        dets = booking.objects.all()
        return render(request, 'admin/booking_dtls.html', {'usr': user, 'details': dets})
    else:
        return redirect('login')


def view_purchase(request):
    if 'user_id' in request.session:
        user = User.objects.all()
        temp = med_history.objects.all()
        return render(request, 'admin/purchase_summary.html', {'usr': user, 'tmp': temp})
    else:
        return redirect('login')


# ________________________user_________________________ #

def signup(request):
    return render(request, 'reg.html')


def reg(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        uname = request.POST['name']
        email = request.POST['email']
        passwd = request.POST['password']
        repasswd = request.POST['repassword']
        phone = request.POST['phone']
        if passwd == repasswd:
            if User.objects.filter(username=uname).exists():
                messages.error(request, 'Username already exists')
                return redirect('signup')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email already exists')
                    return redirect('signup')
                else:
                    user = User.objects.create_user(first_name=fname, last_name=lname, username=uname, email=email,
                                                    password=passwd)
                    user.save()
                    usr = User.objects.get(username=uname)
                    det = user_detls.objects.create(user_ids=usr.id, phone_number=phone)
                    det.save()
                    return redirect('login_page')
        else:
            messages.error(request, 'Password does not match')
            return redirect('signup')
    else:
        return redirect('signup')


@login_required
def userhome(request):
    d = doctor.objects.all()
    return render(request, 'home.html', {'doctor': d})


@login_required
def appoint(request, id):
    a = doctor.objects.filter(id=id)
    return render(request, 'select_date.html', {'dates': a})


@login_required
def confirm_appoint(request, id):
    if request.method == "POST":
        slots = request.POST['slot']
        doc = appointment.objects.get(id=id)
        doct = doctor.objects.get(id=doc.doctor_id)
        users = request.user.id
        emp = User.objects.get(id=users)
        if slots == "1":
            appointment.objects.filter(id=id).update(slot_1=1)
            b = booking.objects.create(b_date=doc.date, slot="9.00 - 10.00", doc_name=doct.name, b_user_id=emp.id)
            b.save()
            temp = booking.objects.filter(b_user_id=emp.id).latest('date')
            one = booking.objects.filter(date=temp.date)
            return render(request, 'booked.html', {'details': one})
        elif slots == "2":
            appointment.objects.filter(id=id).update(slot_2=1)
            b = booking.objects.create(b_date=doc.date, slot="10.00 - 11.00", doc_name=doct.name, b_user_id=emp.id)
            b.save()
            temp = booking.objects.filter(b_user_id=emp.id).latest('date')
            one = booking.objects.filter(date=temp.date)
            return render(request, 'booked.html', {'details': one})
        elif slots == "3":
            appointment.objects.filter(id=id).update(slot_3=1)
            b = booking.objects.create(b_date=doc.date, slot="11.00 - 12.00", doc_name=doct.name, b_user_id=emp.id)
            b.save()
            temp = booking.objects.filter(b_user_id=emp.id).latest('date')
            one = booking.objects.filter(date=temp.date)
            return render(request, 'booked.html', {'details': one})
        elif slots == "4":
            appointment.objects.filter(id=id).update(slot_4=1)
            b = booking.objects.create(b_date=doc.date, slot="2.00 - 3.00", doc_name=doct.name, b_user_id=emp.id)
            b.save()
            temp = booking.objects.filter(b_user_id=emp.id).latest('date')
            one = booking.objects.filter(date=temp.date)
            return render(request, 'booked.html', {'details': one})
        elif slots == "5":
            appointment.objects.filter(id=id).update(slot_5=1)
            b = booking.objects.create(b_date=doc.date, slot="3.00 - 4.00", doc_name=doct.name, b_user_id=emp.id)
            b.save()
            temp = booking.objects.filter(b_user_id=emp.id).latest('date')
            one = booking.objects.filter(date=temp.date)
            return render(request, 'booked.html', {'details': one})
    else:
        return redirect('userhome')


@login_required
def user_date(request, id):
    if request.method == "POST":
        u_date = request.POST['date']
        if appointment.objects.filter(doctor_id=id).exists():
            if appointment.objects.filter(Q(date=u_date) & Q(doctor_id=id)).exists():
                slots = appointment.objects.filter(Q(date=u_date) & Q(doctor_id=id))
                return render(request, 'slot.html', {'dates': slots})
            else:
                a = appointment.objects.create(date=u_date, doctor_id=id)
                a.save()
                slots = appointment.objects.filter(Q(date=u_date) & Q(doctor_id=id))
                return render(request, 'slot.html', {'dates': slots})
        else:
            a = appointment.objects.create(date=u_date, doctor_id=id)
            a.save()
            slots = appointment.objects.filter(Q(date=u_date) & Q(doctor_id=id))
            return render(request, 'slot.html', {'dates': slots})
    else:
        return redirect('userhome')


@login_required
def history(request):
    users = request.user.id
    emp = User.objects.get(id=users)
    temp = booking.objects.filter(b_user_id=emp.id).order_by('-id')
    return render(request, 'history_pg.html', {'details': temp})


@login_required
def m_history(request):
    users = request.user.id
    emp = User.objects.get(id=users)
    temp = med_history.objects.filter(u_id=emp.id)
    return render(request, 'product_history.html', {'details': temp})


@login_required
def pharmacy(request):
    meds = products.objects.all()
    return render(request, 'Pharmacy.html', {'meds': meds})


@login_required
def payment(request):
    users = request.user.id
    if cart.objects.filter(p_user_id=users).exists():
        if request.method == 'POST':
            qty = int(request.POST['med_qty'])
            md_name = request.POST['med_name']
            md_price = int(request.POST['med_price'])
            total = int(request.POST['total'])
            med = products.objects.get(product_name=md_name)
            medc = products.objects.filter(product_name=md_name)
            price = {total}
            qtys = {qty}
            return render(request, 'payment.html', {'med': medc, 'price': price, 'qty': qtys})
    else:
        return redirect('cart_view')

@login_required
def success(request):
    users = request.user.id
    crt = cart.objects.filter(p_user_id=users)
    for i in crt:
        product = products.objects.get(product_name=i.p_name)
        med_history.objects.create(u_id=users, p_name=i.p_name, p_description=product.description,
                                   p_quantity=i.p_qty,
                                   p_price=i.p_price, ).save()
        temp = product.quantity - int(i.p_qty)
        product.quantity = temp
        product.save()
    cart.objects.filter(p_user_id=users).delete()
    return render(request, 'success.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def medicine_view(request, id):
    medc = products.objects.filter(id=id)
    return render(request, 'medic_view.html', {'medic': medc})


def mail_check(request):
    if request.method == 'POST':
        mail = request.POST['email']
        if User.objects.filter(email=mail).exists():
            temp = User.objects.get(email=mail)
            ids = temp.id
            temp = User.objects.filter(id=ids)
            return render(request, 'change_pass.html', {'temp': temp})
        else:
            messages.error(request, 'Invalid E-mail ID!!')
            return redirect('login')
    else:
        return redirect('login')


# def change_pass(request, id):


def reset_pass(request, id):
    if request.method == 'POST':
        passw = request.POST['password']
        repassw = request.POST['repassword']
        if passw == repassw:
            temp = User.objects.get(id=id)
            temp.set_password(passw)
            temp.save()
            messages.success(request, 'Password Updated')
            return redirect('login')
        else:
            messages.error(request, 'Password does not match')
            return redirect('change_pass')
    else:
        return redirect('change_pass')


@login_required
def cart_view(request):
    users = request.user.id
    crt = cart.objects.filter(p_user_id=users)
    prices = 0
    for i in crt:
        prices = i.p_price + prices
    temp = {prices}
    return render(request, 'cart.html', {'cart': crt, 'total': temp})


@login_required
def add_to_cart(request, id):
    if request.method == 'POST':
        qty = int(request.POST['quantity'])
        temp = products.objects.get(id=id)
        t_price = int(temp.price) * qty
        users = request.user.id
        emp = User.objects.get(id=users)
        crt = cart.objects.create(p_name=temp.product_name, p_qty=qty, p_price=t_price, p_user_id=users
                                  )
        crt.save()
        return redirect('pharmacy')
    else:
        pass


@login_required
def remove_from_cart(request, id):
    det = cart.objects.get(id=id)
    det.delete()
    return redirect('cart_view')

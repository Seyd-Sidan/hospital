from django.urls import path
from . import views

urlpatterns = [

    # --------------------------User--------------------------#

    path('', views.userhome, name='userhome'),

    path('signup', views.signup, name='signup'),
    path('reg', views.reg, name='reg'),
    path('login', views.login, name='login'),
    path('login_page', views.login_page, name='login_page'),
    path('logout_view', views.logout_view, name='logout_view'),
    path('userhome', views.userhome, name='userhome'),
    path('appoint/<id>', views.appoint, name='appoint'),
    path('confirm_appoint/<id>', views.confirm_appoint, name='confirm_appoint'),
    path('history', views.history, name='history'),
    path('m_history', views.m_history, name='m_history'),
    # path('', views.date_test, name='date_test'),
    # path('get_date', views.get_date, name='get_date'),
    path('user_date/<id>', views.user_date, name='user_date'),
    path('payment', views.payment, name='payment'),
    path('success', views.success, name='success'),
    path('pharmacy', views.pharmacy, name='pharmacy'),
    path('medicine_view/<id>', views.medicine_view, name='medicine_view'),
    # path('medicine_history/<id>',views.medicine_history,name='medicine_history'),
    path('mail_check', views.mail_check, name='mail_check'),
    # path('change_pass/<id>', views.change_pass, name='change_pass'),
    path('reset_pass/<id>', views.reset_pass, name='reset_pass'),
    path('cart_view', views.cart_view, name='cart_view'),
    path('add_to_cart/<id>', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<id>', views.remove_from_cart, name='remove_from_cart'),

    # --------------------------Admin--------------------------#

    path('adminhome', views.adminhome, name='adminhome'),
    path('adddoc', views.adddoc, name='adddoc'),
    path('viewdoc', views.viewdoc, name='viewdoc'),
    path('viewusers', views.viewusers, name='viewusers'),
    path('view_booking', views.view_booking, name='view_booking'),
    path('view_purchase', views.view_purchase, name='view_purchase'),
    path('view_medicine', views.view_medicine, name='view_medicine'),
    # path('add_date/<id>', views.add_date, name='add_date'),
    path('del_date/<id>', views.del_date, name='del_date'),
    path('del_doc/<id>', views.del_doc, name='del_doc'),
    path('del_user/<id>', views.del_user, name='del_user'),
    path('admin_logout', views.admin_logout, name='admin_logout'),
    path('add_medicine', views.add_medicine, name='add_medicine'),
    path('del_medicine/<id>', views.del_medicine, name='del_medicine'),

]

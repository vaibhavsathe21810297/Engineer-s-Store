from django.contrib import admin
from django.urls import path
from CrazyThings import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from CrazyThings.forms import LoginForm, MyPasswordChangeForm, MyPasswordConfirmForm, MyPasswordResetForm,feedbackForm
from django.contrib import admin

urlpatterns = [

    path('', views.ProductView.as_view(), name="home"),
    path('product-detail/<int:pk>',views.ProductDetailView.as_view(), name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart),

    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('passwordchange/',
         auth_views.PasswordChangeView.as_view(template_name='passwordchange.html', form_class=MyPasswordChangeForm,
                                               success_url='/passwordchangedone/'), name='passwordchange'),
    path('passwordchangedone/', auth_views.PasswordChangeView.as_view(template_name='passwordchangedone.html'),
         name='passwordchangedone'),

    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='password_reset.html', form_class=MyPasswordResetForm),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='password__reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html',
                                                     form_class=MyPasswordConfirmForm), name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),

    path('cricket/', views.cricket, name='cricket'),
    path('cricket/<slug:data>', views.cricket, name='cricketdata'),

    path('badminton/', views.badminton, name='badminton'),
    path('badminton/<slug:data>', views.badminton, name='badmintondata'),

    path('cycling/', views.cycling, name='cycling'),
    path('cycling/<slug:data>', views.cycling, name='cyclingdata'),

    path('football/', views.football, name='football'),
    path('football/<slug:data>', views.football, name='footballdata'),

    path('swimming/', views.swimming, name='swimming'),
    path('swimming/<slug:data>', views.swimming, name='swimmingdata'),

    path('volleyball/', views.volleyball, name='volleyball'),
    path('volleyball/<slug:data>', views.volleyball, name='volleyballdata'),

    path('basketball/', views.basketball, name='basketball'),
    path('basketball/<slug:data>', views.basketball, name='basketballdata'),

    path('tabletennis/', views.tabletennis, name='tabletennis'),
    path('tabletennis/<slug:data>', views.tabletennis, name='tabletennisdata'),

    path('camera/', views.camera, name='camera'),
    path('camera/<slug:data>', views.camera, name='cameradata'),

    path('headset/', views.headset, name='headset'),
    path('headset/<slug:data>', views.headset, name='headsetdata'),

    path('laptop/', views.laptop, name='laptop'),
    path('laptop/<slug:data>', views.laptop, name='laptopdata'),

    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>', views.mobile, name='mobiledata'),

    path('printer/', views.printer, name='printer'),
    path('printer/<slug:data>', views.printer, name='printerdata'),

    path('smartwatches/', views.smartwatches, name='smartwatches'),
    path('smartwatches/<slug:data>', views.smartwatches, name='smartwatchesdata'),

    path('speaker/', views.speaker, name='speaker'),
    path('speaker/<slug:data>', views.speaker, name='speakerdata'),

    path('television/', views.television, name='television'),
    path('television/<slug:data>', views.television, name='televisiondata'),

    path('beds/', views.beds, name='beds'),
    path('beds/<slug:data>', views.beds, name='bedsdata'),

    path('sofas/', views.sofas, name='sofas'),
    path('sofas/<slug:data>', views.sofas, name='sofasdata'),

    path('chairs/', views.chairs, name='chairs'),
    path('chairs/<slug:data>', views.chairs, name='chairsdata'),

    path('tables/', views.tables, name='tables'),
    path('tables/<slug:data>', views.tables, name='tablesdata'),

    path('wardrobes/', views.wardrobes, name='wardrobes'),
    path('wardrobes/<slug:data>', views.wardrobes, name='wardrobesdata'),

    path('shelves/', views.shelves, name='shelves'),
    path('shelves/<slug:data>', views.shelves, name='shelvesdata'),

    path('cabinets/', views.cabinets, name='cabinets'),
    path('cabinets/<slug:data>', views.cabinets, name='cabinetsdata'),


path('children/', views.children, name='children'),
    path('children/<slug:data>', views.children, name='childrendata'),

    path('comic/', views.comic, name='comic'),
    path('comic/<slug:data>', views.comic, name='comicdata'),

    path('exam/', views.exam, name='exam'),
    path('exam/<slug:data>', views.exam, name='examdata'),

    path('university/', views.university, name='university'),
    path('university/<slug:data>', views.university, name='universitydata'),

    path('school/', views.school, name='school'),
    path('school/<slug:data>', views.school, name='schooldata'),


    path('air/', views.air, name='air'),
    path('air/<slug:data>', views.air, name='airdata'),

    path('cooler/', views.cooler, name='cooler'),
    path('cooler/<slug:data>', views.cooler, name='coolerdata'),

    path('fan/', views.fan, name='fan'),
    path('fan/<slug:data>', views.fan, name='fandata'),

    path('washing/', views.washing, name='washing'),
    path('washing/<slug:data>', views.washing, name='washingdata'),

    path('refrigerator/', views.refrigerator, name='refrigerator'),
    path('refrigerator/<slug:data>', views.refrigerator, name='refrigeratordata'),

    path('fruitvegetable/', views.fruitvegetable, name='fruitvegetable'),
    path('fruitvegetable/<slug:data>', views.fruitvegetable, name='fruitvegetabledata'),

    path('beverages/', views.beverages, name='beverages'),
    path('beverages/<slug:data>', views.beverages, name='beveragesdata'),

    path('foodgrains/', views.foodgrains, name='foodgrains'),
    path('foodgrains/<slug:data>', views.foodgrains, name='foodgrainsdata'),
    path('cookies/', views.cookies, name='cookies'),
    path('cookies/<slug:data>', views.cookies, name='cookiesdata'),
    path('noodles/', views.noodles, name='noodles'),
    path('noodles/<slug:data>', views.noodles, name='noodlesdata'),
    path('oil/', views.oil, name='oil'),
    path('oil/<slug:data>', views.oil, name='oildata'),

    path('snacks/', views.snacks, name='snacks'),
    path('snacks/<slug:data>', views.snacks, name='snacksdata'),

    path('deo/', views.deo, name='deo'),
    path('deo/<slug:data>', views.deo, name='deodata'),




    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html',authentication_form=LoginForm), name='login' ),
    path('logout/',auth_views.LogoutView.as_view(next_page='login'),name='logout'),
    path('customerregistration/',views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('feedbacks/',views.Feedbacks.as_view(), name='feedbacks'),
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/',views.payment_done, name='paymentdone'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



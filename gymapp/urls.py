from django.urls import path
from .views import *
from .utils import *


app_name = 'gymapp'

urlpatterns = [


    # CLIENT PATHS ##
    # CLIENT PATHS ##
    # CLIENT PATHS ##
    # CLIENT PATHS ##

    # general pages

    path('', ClientHomeView.as_view(), name='clienthome'),
    path('about/', ClientAboutView.as_view(), name='clientabout'),
    path('contact/', ClientContactCreateView.as_view(), name='clientcontact'),
    # path('makeanappointment/', ClientAppointmentCreateView.as_view(),
    #      name='clientappointmentcreate'),
    path('products/', ClientProductListView.as_view(), name='clientproductlist'),
    path('product/<int:pk>/detail/',ClientProductDetailView.as_view(), 
        name='clientproductdetail'),
    path('trainers/', ClientTrainerListView.as_view(), name='clienttrainerlist'),
    path('trainer/<slug:slug>/detail/', ClientTrainerDetailView.as_view(),
         name='clienttrainerdetail'),
    path('services/', ClientServiceListView.as_view(),
         name='clientservicelist'),
    path('services/<slug:slug>/detail/',
         ClientServiceDetailView.as_view(), name='clientservicedetail'),
    path('schedule/<slug:slug>/detail/',
         ClientScheduleDetailView.as_view(), name='clientscheduledetail'),
    path('testimonial/',
         TestimonialListView.as_view(), name='testimoniallist'),
    # path('slider/',
    #      SliderListView.as_view(), name='sliderlist'),
    path('facilities/', ClientFacilityListView.as_view(),
         name='clientfacilitylist'),
    path('facilities/<slug:slug>/details',
         ClientFacilityDetailView.as_view(), name='clientfacilitydetail'),
    path('events/', ClientEventListView.as_view(),
         name='clienteventlist'),
    path('events/<slug:slug>/details',
         ClientEventDetailView.as_view(), name='clienteventdetail'),
    path('notices/', ClientNoticeListView.as_view(), name='clientnoticelist'),
    path('notices/<slug:slug>/details',
         ClientNoticeDetailView.as_view(), name='clientnoticedetail'),
    path('pages/<slug:slug>/details',
         ClientPageDetailView.as_view(), name='clientpagedetail'),
    path('images/', ClientImageListView.as_view(), name='clientimagelist'),
    path('videos/', ClientVideoListView.as_view(), name='clientvideolist'),
    path('blogs/', ClientBlogListView.as_view(), name='clientbloglist'),
    path('blogs/<slug:slug>/details',
         ClientBlogDetailView.as_view(), name='clientblogdetail'),
    path('schedules/', ClientScheduleListView.as_view(), name='clientschedulelist'),
    path('404/', ClientPageNotFoundView.as_view(), name='clientpagenotfound'),
    path('subscribe/', ClientSubscriberCreateView.as_view(),
         name='clientsubscribercreate'),
    path('search/result/', SearchResultView.as_view(), name="searchresult"),
    path('login/', ClientLoginView.as_view(), name='clientlogin'),
    path('logout/', ClientLogoutView.as_view(), name='clientlogout'),
    path('register/', ClientRegistrationView.as_view(), name='clientcreate'),
    path('cart_update',cart_update,name = 'cart_update'),
    path('carts/<int:pk>/items/total/',ClientCartTotalView.as_view(), name='clientcarttotal'),
]

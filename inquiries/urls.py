from django.urls import path
from . import views

app_name = 'inquiries'

urlpatterns = [
    path('video-call/', views.video_call_booking, name='video_call_booking'),
    path('video-call/book/', views.book_video_call, name='book_video_call'),
    path('video-call/my-calls/', views.my_calls, name='my_calls'),
    path('contact/', views.contact, name='contact'),
    path('order/', views.order_form, name='order_form'),
    path('chatbot/enquiry/', views.chatbot_enquiry, name='chatbot_enquiry'),
]

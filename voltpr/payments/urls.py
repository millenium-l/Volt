from django.urls import path

from .views import stk_push, mpesa_callback


urlpatterns = [
    path("stk-push/",stk_push,name="stk_push",),
    path("callback/",mpesa_callback,name="mpesa_callback",),
]
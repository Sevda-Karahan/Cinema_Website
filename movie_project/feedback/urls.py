from django.urls import path,include
from . import views
urlpatterns = [   
    path('submit_feedback/', views.submit_feedback, name='submit_feedback'),
    path('feedback_success/', views.feedback_success, name='feedback_success'),
]
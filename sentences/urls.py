from django.urls import path

from . import views


urlpatterns = [
    path('api/text/', views.text_list),
    path('api/text/<int:pk>/', views.text_detail),
    path('api/text/<int:text_pk>/sentence/<int:sentence_pk>/', views.sentence_detail),
    path('api/text/<int:text_pk>/sentence/<int:sentence_pk>/similar/', views.sentence_similar_list),
]
from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('session-list', views.SessionListViewSet)

#/session-list / -get
#/session-list/-post
#/session-list/{session-list_id}-get
#/session-list/{session-list_id}-put
#/session-list/{session-list_id}-delete

urlpatterns = [
    path('', include(router.urls)),
    path('train-word2vec/', views.TrainWord2VecAPIView.as_view(), name='train-word2vec'),
    path('get-suggest/', views.GetListCodeProductView.as_view(), name='get-suggest')
]

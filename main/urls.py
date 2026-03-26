from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views 

# API configuration
router = DefaultRouter()
router.register(r'api/plants', views.IrisPlantViewSet)

urlpatterns = [
    # Home and Login
    path('', views.login_view, name='login_root'),  
    path('list/', views.list_view, name='list_view'), 
    
    # Support for .html links
    path('list.html', views.list_view, name='list_html_legacy'),

    # Authentication
    path('register/', views.register_view, name='register_view'),
    path('register.html', views.register_view, name='register_view_legacy'),
    
    path('login/', views.login_view, name='login_view'), 
    path('logout/', views.logout_view, name='logout'),

    # Features
    path('add/', views.add_view, name='add_view'),
    path('add.html', views.add_view, name='add_view_legacy'),

    path('search/', views.search_view, name='search_view'),
    path('search.html', views.search_view, name='search_view_legacy'),

    path('predict/', views.predict_view, name='predict_view'),
    path('predict.html', views.predict_view, name='predict_view_legacy'),
    
    path('delete/<int:id>/', views.delete_view, name='delete_view'),
    path('update/<int:id>/', views.update_view, name='update_view'),

    # CSV operations 
    path('export/', views.export_iris_csv, name='export_iris_csv'),
    path('import/', views.import_iris_csv, name='import_iris_csv'),

    path('', include(router.urls)),
]
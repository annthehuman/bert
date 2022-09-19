from django.urls import path
from . import views
from django.conf import settings
from django.views.generic import TemplateView

urlpatterns = [
    path('classificate', views.classificate, name='classificate'),
    path('get_data', views.get_data, name='get_data'),
]

# react_routes = getattr(settings, 'REACT_ROUTES', [])

# for route in react_routes:
#     urlpatterns += [
#         path('{}'.format(route), TemplateView.as_view(template_name='frontend/index.html'))
#     ]
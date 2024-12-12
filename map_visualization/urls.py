from django.urls import path
from .views import get_geotagged_data
from django.views.generic import TemplateView

urlpatterns = [
    path('map_visualization/api/geotagged-data/', get_geotagged_data, name='geotagged-data'),  # API endpoint for geotagged data
    path('', TemplateView.as_view(template_name='map_visualization/map_visualization.html'), name='map'),  # Map visualization page
]

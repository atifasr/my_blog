from django.urls import path
from.views import *

app_name = 'my_blog'

urlpatterns = [
    path('', home, name='home'),
    path('get_article/', get_article, name='get_article'),
    path('add_post/', add_post, name='add_post'),
    path('login_admin/', login_admin, name='login_admin'),
    path('get_categories/', get_categories, name='get_categories'),
    path('add_post/', add_post, name='add_post'),
    path('update_post/<topic_id>/', update_post, name='update_post'),
]

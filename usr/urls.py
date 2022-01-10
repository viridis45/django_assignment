from django.urls import path
from .views import *


urlpatterns= [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('signout/', Signout.as_view(), name='signout'),
    path('entry/', EntryView.as_view(), name='entry'),
    path('entry/<int:entry_id>/', entry_get, name='entry_get'),
    path('entry/delete/<int:entry_id>/', entry_delete, name='entry_delete'),
    path('entry_put/<int:entry_id>/', entry_put, name='entry_put'),
    path('entry_revert/<int:entry_id>/', entry_revert, name='entry_revert'),
    path('entry_deleteds/', Deleteds.as_view(), name='entry_deleteds'),
    
    ]
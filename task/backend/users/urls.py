from django.urls import path
from .views import UserRegisterView, UserMeView, UserListView, change_password, notification_list, activity_log_list, me

urlpatterns = [
    path('users/register/', UserRegisterView.as_view(), name='user-register'),
    path('users/me/', UserMeView.as_view(), name='user-me'),
    path('users/me/change_password/', change_password, name='user-change-password'),
    path('users/me/activity/', activity_log_list, name='user-activity-log'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('notifications/', notification_list, name='notification-list'),
    path('me/', me, name='me'),
] 
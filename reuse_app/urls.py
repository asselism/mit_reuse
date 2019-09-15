from django.urls import path

from . import views

app_name = 'reuse_app'
urlpatterns = [
    path('', views.ListingList.as_view(), name='index'),
    path('mine', views.ListingListUser.as_view(), name='listings_list_user'),
    path('register', views.Register.as_view(), name='register'),
    path('login', views.Login.as_view(), name='login'),
    path('logout', views.logout, name='logout'),
    path('create', views.ListingCreate.as_view(), name='listing_create'),
    path('update/<int:pk>', views.ListingUpdate.as_view(), name='listing_update'),
    path('view/<int:pk>', views.ListingView.as_view(), name='listing_view'),
    path('mark_taken/<int:pk>', views.ListingTaken.as_view(), name='listing_taken'),
    path('still_available/<int:pk>', views.ListingStillAvailable.as_view(),
        name='listing_still_available'),
    path('delete/<int:pk>', views.ListingDelete.as_view(),
        name='listing_delete'),
]

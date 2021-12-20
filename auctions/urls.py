from django.urls import path
from . import views



urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"), 
    path("category/<str:categories>/",
         views.category, name='category'),
    path("new_listing", views.new_listing, name="new_listing"),
    path("new_comment",
         views.new_comment, name="new_comment"),
   path("listing/<int:listing_id>/",views.listing, name="listing"),
    path("close_auction/<int:listing_id>",
         views.close_auction, name="close_auction"),
    path("watchlist", views.watchlist,  name="watchlist"),
    path("watchlist/add_to_watchlist/<int:listing_id>/", views.add_to_watchlist,  name="add_to_watchlist"),
]

from django.contrib import admin

# Register your models here.
from .models import User,Category,Comment,Auction_Listings,Watchlist,Listing,Bid

admin.site.register(User) 
admin.site.register(Listing)


@admin.register(Auction_Listings)
class Auction_ListingsAdmin(admin.ModelAdmin):
    list_display = ('category', 'title','description','price','seller','date_listing','end_datetime')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'item')


@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'listing')
    
@admin.register(Comment) 
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'body', 'comment_date_created','allowed')


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ('price','bidder', 'bid', 'listing','date')

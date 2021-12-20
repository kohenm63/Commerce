
from django.contrib.auth.models import *
from django.db import models
from django.db.models.fields import URLField
import django.utils.timezone


class User(AbstractUser):
    pass



# Category model
class Category (models.Model):
    name = models.CharField(max_length=100)
    item = models.ForeignKey(
        'Auction_Listings', on_delete=models.CASCADE, blank=True, null=True, related_name='category_item')

def __str__(self):
    return f"{self.id},{self.name},{self.category_item}"
                
class Auction_Listings(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, blank=True, null=True,related_name='category')
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=2000, blank=True, null=True)
    price = models.DecimalField(default=1.00, decimal_places=2, max_digits=7)
    image = models.CharField(max_length=1000, default="", blank=True)
    seller = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    date_listing = models.DateTimeField(
        default=django.utils.timezone.localtime)
    bidder = models.ManyToManyField(User, related_name="user")
    end_datetime = models.DateTimeField(
        null=False, blank=False, default=django.utils.timezone.localtime)
    bid = models.DecimalField(default=1.00, decimal_places=2, max_digits=7)
    comment = models.CharField(max_length=2000,null=True, blank=True)
   
    winner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bidder", null=True, blank=True)
    user_watchlist = models.ManyToManyField(User, default=None, blank=True, related_name="user_watchlist")

    def __str__(self):
        return f"{self.category},{self.title},{self.description},{self.price},{self.image},{self.seller},{self.end_datetime},{self.date_listing},{self.winner},{self.bid}"

# order by date_listing
class Meta:
    ordering = ['-date_listing']


class Bid(models.Model):
    listing = models.ForeignKey(
        Auction_Listings, on_delete=models.CASCADE, null=True, related_name="bids")
    bidder = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True,related_name="userid")
    bid = models.DecimalField(default=1.00, decimal_places=2, max_digits=10)

    date = models.DateTimeField(default=django.utils.timezone.localtime)
    price = models.ForeignKey(
        Auction_Listings, on_delete=models.CASCADE, null=True, related_name="listings")

    closed = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.id},{self.date},{self.bid},{self.bidder},{self.listing}"

class Comment(models.Model):
    listing = models.ForeignKey(
        Auction_Listings, on_delete=models.CASCADE,related_name="comments",null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_date_created = models.DateTimeField(default=django.utils.timezone.localtime)
    body = models.TextField(max_length=250)
    allowed = models.BooleanField(default = False)
    
class Meta:
    ordering = ('-comment_date_created')
    
    def __str__(self):
        return f"{self.id},{self.body},{self.user},{self.comment_date_created},{self.listing}"


class Listing(models.Model):
    details = models.ForeignKey(
        Auction_Listings, on_delete=models.CASCADE, null=True, blank=True)
    added_to_watchlist = models.ManyToManyField(User, related_name="add_to_watchlist",blank=True)
    
    def __str__(self):
        return f"{self.id},{self.details},{self.added_to_watchlist}"


class Watchlist(models.Model):
     user = models.ForeignKey(
         User, on_delete=models.CASCADE)
     listing = models.ForeignKey(
         Auction_Listings, on_delete=models.CASCADE)
     
     def __str__(self):
       return f"{self.user},{self.listing}"

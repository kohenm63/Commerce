from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import  Max 
from .forms import *
from .models import *



@login_required
def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html",
                  {
                      'categories': categories,
                  })


@login_required
def category(request,categories):
    
    # category = Category.objects.get(str=categories)
    category_items = Auction_Listings.objects.filter(category = categories)
    return render(request, "auctions/category.html",
                  {
                       'categories': categories,
                        'category_items': category_items,
                  })
   
def index(request):
    all_listings = Auction_Listings.objects.all()
    return render(request, "auctions/index.html", {
        'all_listings': all_listings,
    })

# listings
"""
[x]show list of all bids made so far: the highest wins the auction!
[x ]add an iten to favourites
[x]show list of comments and let the user to add a comment
"""
"""
[x]If the user is signed in, the user should be able to add the item to their “Watchlist.” 
[x]If the item is already on the watchlist, the user should be able to remove it.
[x]   If the user is signed in, the user should be able to bid on the item. 
[]  The bid must be at least as large as the starting bid, and must be greater 
    than any other bids that have been placed (if any). 
[]   If the bid doesn’t meet those criteria, the user should be presented 
    with an error.
[x]  If the user is signed in and is the one who created the listing, 
    the user should have the ability to “close” the auction from this
    page,
        [x]which makes the highest bidder the winner of the auction and 
        makes the listing no longer active.
        If a user is signed in on a closed listing page, and the user has
       [] won that auction, the page should say so.
    Users who are signed in should be able to add comments to the listing page. 
    The listing page should display all comments that have been made on the listing.
    """



@login_required
def listing(request, listing_id):
    listing = get_object_or_404(Auction_Listings,id=listing_id)
    comments = listing.comments.filter(allowed=True)
    comments = listing.comments.order_by('-comment_date_created')
    bids = listing.bids.filter(closed=True)
    bids = listing.bids.order_by('-bid')
    max_bid=listing.bids.aggregate(Max('bid'))
#by default there's no comments or bids
    user_bid = None
    if request.method == 'POST':
          bid_form = BidForm(data=request.POST)
          if  bid_form.is_valid:
            # Create  objects but don't save them to the db
            user_bid = bid_form.save(commit=True)
            user_bid.listing = listing
            # Save the comment to the database  
            user_bid.save()
            return render(request, "auctions/listing.html",
                          {
                              'listing': listing,
                             
                          })
    else:
        return render(request, "auctions/listing.html",
                      {
                          'listing': listing,   
                          'comments':comments,
                          'bids': bids,
                          'user_bid': user_bid,
                          'max_bid':max_bid,
                          'bid_form': BidForm()
                      })


@login_required
def new_comment(request):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
           form.save()
           return HttpResponseRedirect(reverse("index"))

    else:
            return render(request, "auctions/new_comment.html", {
                "form": CommentForm(),
                'message': "smt went wrong 😞"
            })

    
    
@login_required   
def close_auction(request, listing_id):  
#select the listing the user has clicked on
    listing = get_object_or_404(Auction_Listings, id=listing_id)
#if listing exists inside the table announce the winner
    if listing.winner.filter(id=request.user.id).exists():
        listing.winner.update(request.user)
    return render(request, "auctions/listing.html",
                  {
                      'listing': listing,
                      
                  })
   

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


# list of categories without duplicates
@login_required
def categories_list(request):
    categories = Category.objects.all()
    print(categories)
    context = {'categories': categories}
    return render(request, "auctions/categories.html", context)


# add new listing and save it to our db
# only signed in users
@ login_required
def new_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "auctions/new_listing.html", {
                'form': form,
                'message': "smt went wrong 😞"
                })
    else:
        return render(request, "auctions/new_listing.html", {
            "form": ListingForm()
        })



@login_required
def add_to_watchlist(request, listing_id):
    #select the listing the user has clicked on
    listing = get_object_or_404(Auction_Listings, id=listing_id)
#if listing exists inside the table=> remove it ,
# else=> add it to the table
    if listing.user_watchlist.filter(id=request.user.id).exists():
        listing.user_watchlist.remove(request.user)
    else:
        listing.user_watchlist.add(request.user)
    return HttpResponseRedirect(reverse('watchlist'))


@login_required
def watchlist(request):
    watchlist = Auction_Listings.objects.filter(user_watchlist=request.user)
    return render(request, "auctions/watchlist.html",
                  {
                      'watchlist': watchlist,
                  })


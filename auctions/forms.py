from django.core import validators
from django import forms
from django.forms import ModelForm
from.models import *

# Listing form
class ListingForm(forms.ModelForm):
    class Meta:
        model = Auction_Listings
        fields = ["category", "title", "description",
                  "price", "image","seller", "end_datetime","winner"]
        


# Bids form
class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ["bid", "listing","bidder","date"]
        price = forms.DecimalField(initial = 1.0)
#build in validation:  
def clean_bid(self):
            bid = self.cleaned_data.get("bid")
            price = self.cleaned_data.get("price")
            if self.bid < price:
             raise forms.ValidationError(
                    'Bid must be greater than the price')

            if self.bid < bid:
              raise forms.ValidationError('Bid must be greater than the current bid')
            else:
               return bid
    
        
# # Close auction form
# class CloseForm(forms.ModelForm):
#     class Meta:
#         model = Bids
#         fields = ["item", "bidder", "date"]
        
# Comments form
class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = [ "body", "comment_date_created", "user"]
       



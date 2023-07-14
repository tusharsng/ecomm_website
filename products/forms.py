from django import forms
from .models import Apply, Product, Profile
PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
                                choices=PRODUCT_QUANTITY_CHOICES,
                                coerce=int)
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        
        fields = [ 'pro_pic','bio']
class ApplyForm(forms.ModelForm):
    class Meta:
        model = Apply
        
        fields = [ 'documents',]

class EditproductForm(forms.ModelForm):
    class Meta:
        model = Product
        
        fields = [ 'name','image','price','old_price','description','feature1','feature2','feature3','category']
        exclude=['created','creator','slug']

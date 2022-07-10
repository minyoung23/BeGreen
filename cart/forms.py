from django import forms

class AddItemForm(forms.Form):
    quantity=forms.IntegerField()
    is_update=forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput) #상세페이지에서 추가할 때 장바구니넹서 수량을 바꿀 때 동작하는 방식 다르게 함
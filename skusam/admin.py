from django.contrib import admin
from skusam.models import Article, Tag,Address, Contact, Category, Page, UserProfile
from django import forms
# class ChoiceInline(admin.TabularInline):
# 	model=Choice
# 	extra=5
# Register your models here.
# class AddressAdmin(admin.ModelAdmin):
# 	field=['address','city','state','zip']
# admin.site.register(Address,AddressAdmin)
# admin.site.register(Contact)

class PageAdmin(admin.ModelAdmin):
   list_display=('title','category','url')

# Register your models here.
# class FormPost(forms.ModelForm):
# 	content=forms.CharField(widget=forms.Textarea)
class AdminPost(admin.ModelAdmin):
   fields=['title','content','author']
class AdminArticle(admin.ModelAdmin):
   fields=['title','content','author','category','voices']
   list_display=('title','category')

      # forms=FormPost'

admin.site.register(Article, AdminArticle)
admin.site.register(Tag)
admin.site.register(Address)
admin.site.register(Contact)
admin.site.register(Category)
admin.site.register(Page,PageAdmin)
admin.site.register(UserProfile)
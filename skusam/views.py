from django.shortcuts import render,render_to_response,HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse
from skusam.models import Address,Article, Tag,Contact,Category,Page,UserProfile
from django.views.generic import CreateView,UpdateView,ListView,UpdateView,DeleteView,DetailView

from django.contrib.auth.models import User,Group

from django.contrib.auth import authenticate, login, logout
from skusam.forms import UserForm,UserProfileForm,UsergroupForm
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
# @login_required
# def restricted(request):
#     return HttpResponse("Since you're logged in, you can see this text!")


# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/rango/')

def problems(request):
    return render(request,'problem_list.html',{})    

def study(request):
     # Obtain the context from the HTTP request.
    context = RequestContext(request)

    # Query for categories - add the list to our context dictionary.
    category_list = Category.objects.all()
    context_dict = {'categories': category_list}

    # The following two lines are new.
    # We loop through each category returned, and create a URL attribute.
    # This attribute stores an encoded URL (e.g. spaces replaced with underscores).
    for category in category_list:
        category.url = category.name.replace(' ', '_')

    # Render the response and return to the client.
    return render_to_response('study_list.html', context_dict, context)


def accountprofile(request):
     # Obtain the context from the HTTP request.
    context = RequestContext(request)

    # Query for categories - add the list to our context dictionary.
    category_list = Category.objects.all()
    context_dict = {'categories': category_list}

    # The following two lines are new.
    # We loop through each category returned, and create a URL attribute.
    # This attribute stores an encoded URL (e.g. spaces replaced with underscores).
    for category in category_list:
        category.url = category.name.replace(' ', '_')

    # Render the response and return to the client.
    return render_to_response('front_page.html', context_dict, context)

def front(request):
     # Obtain the context from the HTTP request.
    context = RequestContext(request)

    # Query for categories - add the list to our context dictionary.
    category_list = Category.objects.all()
    context_dict = {'categories': category_list}

    # The following two lines are new.
    # We loop through each category returned, and create a URL attribute.
    # This attribute stores an encoded URL (e.g. spaces replaced with underscores).
    for category in category_list:
        category.url = category.name.replace(' ', '_')

    # Render the response and return to the client.
    return render_to_response('index.html', context_dict, context)
def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render_to_response(
            'register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)

def index(request):
    context = RequestContext(request)

    # Query the database for a list of ALL categories currently stored.
    # Order the categories by no. likes in descending order.
    # Retrieve the top 5 only - or all if less than 5.
    # Place the list in our context_dict dictionary which will be passed to the template engine.
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}

    # Render the response and send it back!
    return render_to_response('index.html', context_dict, context)


def category(request, category_name_url):
    
        # Request our context from the request passed to us.
    context = RequestContext(request)
    

    # Change underscores in the category name to spaces.
    # URLs don't handle spaces well, so we encode them as underscores.
    # We can then simply replace the underscores with spaces again to get the name.
    category_name = category_name_url.replace('_', ' ')

    # Create a context dictionary which we can pass to the template rendering engine.
    # We start by containing the name of the category passed by the user.
    context_dict = {'category_name': category_name}

    try:
        # Can we find a category with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        category = Category.objects.get(name=category_name)

        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance.
        pages = Page.objects.filter(category=category)

        # Adds our results list to the template context under name pages.
        context_dict['pages'] = pages
        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['category'] = category
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass

    article_list=Article.objects.filter(category=category).order_by('title')
    paginator=Paginator(article_list, 10)
    page=request.GET.get('page')
    try:
        articlesss=paginator.page(page)
    except PageNotAnInteger:
        articlesss=paginator.page(1)
    except EmptyPage:
        articless=paginator.page(paginator.num_pages) 

    article_list=Article.objects.filter(category=category)
    pom=[]
    for item in article_list:
        count=item.voices.count()
        novy=[count,item]
        pom.append(novy)
    pom.sort()
    pom.reverse()
   
    context_dict['articlesss']=articlesss  
    
    context_dict['article_list']=[item[1] for item in pom[0:5]] 

    # Go render the response and return it to the client.
    return render_to_response('category.html', context_dict, context)


def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/rango/account/')
                #return render(request,'front.html',{})

            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('login.html', {}, context)


def my_home(request):
    'title page'
    return render(request,'base.html')


def my_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            # Redirect to a success page.
      #  else:
           # Return a 'disabled account' error message
    #else:
        # Return an 'invalid login' error message.



def logout_view(request):
    logout(request)
# from forms import UserForm
# from django.contrib.auth import login
# from django.http import HttpResponseRedirect

# def lexusadduser(request):
#     if request.method == "POST":
#         form = UserForm(request.POST)
#         if form.is_valid():
#             new_user = User.objects.create_user(**form.cleaned_data)
#             login(new_user)
#             # redirect, or however you want to get to the main view
#             return HttpResponseRedirect('main.html')
#     else:
#         form = UserForm() 

#     return render(request, 'adduser.html', {'form': form}) 

# class UpdateContactView(UpdateView):

#     model = Contact
#     template_name = 'edit_contact.html'

#     def get_success_url(self):
#         return reverse('contacts-list')


# class ArticlesofuserListView(ListView):
#      model=Article
#      template_name='articlesofuser_list.html'




# def get_category_list():
#     cat_list = Category.objects.all()

#     for cat in cat_list:
#         cat.url = encode_url(cat.name)

#     return cat_list

@login_required
def userprofile(request):
    context = RequestContext(request)
   # cat_list = get_category_list()
    #context_dict = {'cat_list': cat_list}
    # u = User.objects.get(username=request.user)

    # try:
    #     up = UserProfile.objects.get(user=u)
    # except:
    #     up = None

   # context_dict['user'] = u
   # context_dict['userprofile'] = up
    return render_to_response('userprofile.html', {}, context)

def view_author(request,username):
    'shows author'
    return render(request,'front.html',{})




# def article_voice(request):
    
#     artic=Article.objects.get(id=1)
#     artic.voices=30
#     artic.save()
#     return render(request,'article_detail.html', {}) 

class UserListView(ListView):
    model = User
    template_name = 'profil_info.html'

class UserprofileListView(ListView):
    model = User
    template_name = 'userprofile.html'



class UsergroupsListView(ListView):
    model = User
    template_name = 'usergroups_info.html'



class ArticleDetailView(DetailView):
       model=Article
       template_name='article_detail.html'
       def get_context_data(self,**kwargs):
         context=super(ArticleDetailView,self).get_context_data(**kwargs)
         context['tags']=Tag.objects.all()
         return context

class ArticleDetailuserView(DetailView):
       model=Article
       template_name='article_detail.html'
       def get_context_data(self,**kwargs):
         context=super(ArticleDetailuserView,self).get_context_data(**kwargs)
         context['action'] = reverse('article-view',kwargs={'category_name_url':self.get_object().category.id,'pk': self.get_object().id})
         return context


class TagDetailView(DetailView):
   model = Tag
   template_name = 'tag_detail.html'
   slug_field = 'title'
   slug_url_kwarg = 'title'

def my_home(request):
    return render(request,'base.html')
    
def view_author(request,username):
    'shows author'
    author=User.objects.get(username=username)
    articles=author.article_set.all()
    return render(request,'author.html',{'author':author,'articles':articles})   

class ArticleDeleteView(DeleteView):

    model = Article
    template_name = 'delete_article.html'

    def get_success_url(self):
        return reverse('studypage') 

    # def get_context_data(self, **kwargs):
    #     context = super(ArticleDeleteView, self).get_context_data(**kwargs)
    #     context['action'] = reverse('article-delete',kwargs={'category_name_url':self.get_object().category.id,'pk': self.get_object().id})
    #     return context 


class ArticleUpdateView(UpdateView):

    model = Article
    template_name = 'edit_article.html'
    fields = ['title','content']

    def get_success_url(self):
        return reverse('studypage') 

    def get_context_data(self, **kwargs):
        context = super(ArticleUpdateView, self).get_context_data(**kwargs)
        context['action'] = reverse('article-edit',kwargs={'category_name_url':self.get_object().category.id,'pk': self.get_object().id})
        return context


class ArticleVoicesUpdateView(UpdateView):

    model = Article
    template_name = 'article_detail.html'
    #fields = ['title','voices']


    def get_success_url(self):
 
        return reverse('article-view') 

    def get_context_data(self, **kwargs):
        context = super(ArticleVoicesUpdateView, self).get_context_data(**kwargs)
        context['action'] = reverse('article-voices',kwargs={'category_name_url':self.get_object().id,'pk': self.get_object().id})
        user=self.request.user
        artic=Article.objects.get(id=self.get_object().id)
        artic.voices.add(user.userprofile)
        artic.save()
        return context

 

class CategoryDetailView(DetailView):
    model=Category
    slug_field = 'id'
    #paginate_by=3
    template_name='categoryyy.html' 
   

    # Change underscores in the category name to spaces.
    # URLs don't handle spaces well, so we encode them as underscores.
    # We can then simply replace the underscores with spaces again to get the name.
    # context = RequestContext(request)
    # category_name = category_name_url.replace('_', ' ')

    # # Create a context dictionary which we can pass to the template rendering engine.
    # # We start by containing the name of the category passed by the user.
    # context_dict = {'category_name': category_name}

    # try:
    #     # Can we find a category with the given name?
    #     # If we can't, the .get() method raises a DoesNotExist exception.
    #     # So the .get() method returns one model instance or raises an exception.
    #     category = Category.objects.get(name=category_name)

    #     # Retrieve all of the associated pages.
    #     # Note that filter returns >= 1 model instance.
    #     pages = Page.objects.filter(category=category)

    #     # Adds our results list to the template context under name pages.
    #     context_dict['pages'] = pages
    #     # We also add the category object from the database to the context dictionary.
    #     # We'll use this in the template to verify that the category exists.
    #     context_dict['category'] = category
    # except Category.DoesNotExist:
    #     # We get here if we didn't find the specified category.
    #     # Don't do anything - the template displays the "no category" message for us.
    #     pass

    # Go render the response and return it to the client.
   # return render_to_response('category.html', context_dict, context)

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        context['action'] = reverse('article-view-category',kwargs={'slug': self.get_object().id})
        
        return context 

class ArticleStudyListView(ListView): 
   model=Article
   template_name='article_view_pagin.html' 
   paginate_by=5
   # contact_list=Category.article_set.all() 
   # paginator = Paginator(contact_list, 25) # Show 25 contacts per page

   # page = request.GET.get('page')
   # try:
   #  contacts = paginator.page(page)
   # except PageNotAnInteger:
   #  # If page is not an integer, deliver first page.
   #  contacts = paginator.page(1)
   # except EmptyPage:
   #  # If page is out of range (e.g. 9999), deliver last page of results.
   #     contacts = paginator.page(paginator.num_pages)

   #return render_to_response('article_view_pagin.html', {"contacts": contacts})


class ArticleCreateView(CreateView):

    model = Article
    template_name = 'edit_article.html'
    def form_valid(self,form):
        user=self.request.user
        form.instance.author=user
        return super(ArticleCreateView,self).form_valid(form)

    # def form_valid(self,form):
    #     self.object=form.save(commit=False)
    #     self.object.author=self.request.user
    #     self.object.save()
    #     return super(ModelFormMixin,self).form_valid(form)


    #queryset=Article.objects.all()
    
    #initial={category:'Analysis'} 
    #fields = ['first_name', 'last_name','phone']
    # def get_initial(self):
    #       return {'author':self.request.user}
    fields = ['title','content','category']

    def get_success_url(self):
       return reverse('studypage') 
    def get_context_data(self, **kwargs):
        context = super(ArticleCreateView, self).get_context_data(**kwargs)
        context['action'] = reverse('article-new',kwargs={'category_name_url':Category.objects.get(id=3)})
        return context
     #def get_initial(self):
      
class UpdateUsergroupsView(UpdateView):
    form_class=UsergroupForm
    model =  User
    template_name = 'usergroups_edit.html'
    #fields = ['groups']
    # def get_success_url(self):
    #     return reverse('usergroups-list',kwargs={'pk': self.get_object().id}) 
    # def form_valid(self,form):
    #     user=self.request.user
    #     form.instance.user=user
    #     return super(UpdateUsergroupsView,self).form_valid(form)
    # def form_valid(self,form):
    #     user=self.request.user
    #     form.instance.user=user
    #     return super(UpdateUserprofileView,self).form_valid(form)



class UpdateUserprofileView(UpdateView):

    model =  UserProfile
    template_name = 'userprofile_edit.html'
    fields = ['info', 'website']
    def get_success_url(self):
        return reverse('userprofile-list',kwargs={'pk': self.get_object().user.id}) 
    def form_valid(self,form):
        user=self.request.user
        form.instance.user=user
        return super(UpdateUserprofileView,self).form_valid(form)

    # def get_context_data(self, **kwargs):
    #     context = super(UpdateUserprofileView, self).get_context_data(**kwargs)
    #     context['action'] = reverse('userprofile-edit',kwargs={'pk': self.get_object().id})
    #     return context   


class UpdateUseraddressView(UpdateView):

    model =  Address
    template_name = 'address_edit.html'
    fields=['address','city','state','zip']
    def form_valid(self,form):
        user=self.request.user
        form.instance.user=user
        return super(UpdateUseraddressView,self).form_valid(form)

    #fields = ['address','city','zip','state']
    def get_success_url(self):
        return reverse('personalprofil-list',kwargs={'pk': self.get_object().user.id}) 

    # def get_context_data(self, **kwargs):
    #     context = super(UpdateUseraddressView, self).get_context_data(**kwargs)
    #     context['action'] = reverse('address-edit',kwargs={'pk': self.get_object().id})
    #     return context   

class UpdateUserView(UpdateView):

    model =  UserForm
    template_name = 'profil_edit.html'
    fields = ['first_name', 'last_name','email']
    def get_success_url(self):
        return reverse('personalprofil-list',kwargs={'pk': self.get_object().id}) 

    def get_context_data(self, **kwargs):
        context = super(UpdateUserView, self).get_context_data(**kwargs)
        context['action'] = reverse('personalprofil-edit',kwargs={'pk': self.get_object().id})
        return context    


class UpdatePasswordView(UpdateView):

    model =  User
    template_name = 'password_edit.html'
    fields = ['password','password', 'password']
    def get_success_url(self):
        return reverse('profil-list') 

    # def get_context_data(self, **kwargs):
    #     context = super(UpdateUserView, self).get_context_data(**kwargs)
    #     context['action'] = reverse('profil-edit',kwargs={'pk': self.get_object().id})
    #     return context    



class ListContactView(ListView):

    model = Contact
    template_name = 'contact_list.html'
   
class AccountbalanceListView(ListView):

    model = User
    template_name = 'accountbalance_list.html'


class CreateContactView(CreateView):

    model = Contact
    template_name = 'edit_contact.html'
    #fields = ['first_name', 'last_name','phone']

    def get_success_url(self):
        return reverse('contacts-list')

    def get_context_data(self, **kwargs):
        context = super(CreateContactView, self).get_context_data(**kwargs)
        context['action'] = reverse('contacts-new')
        return context
class UpdateContactView(UpdateView):

    model = Contact
    template_name = 'edit_contact.html'

    def get_success_url(self):
        return reverse('contacts-list') 

    def get_context_data(self, **kwargs):
        context = super(UpdateContactView, self).get_context_data(**kwargs)
        context['action'] = reverse('contacts-edit',kwargs={'pk': self.get_object().id})
        return context

class DeleteContactView(DeleteView):

    model = Contact
    template_name = 'delete_contact.html'

    def get_success_url(self):
        return reverse('contacts-list')


from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView  


class PostReadUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    model = Contact
class PostCreateReadView(ListCreateAPIView):
    model = Contact    
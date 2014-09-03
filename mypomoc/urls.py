from django.conf.urls import patterns, include, url

from django.contrib import admin
from skusam import views
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:    url(r'^rango/register/$', views.register, name='register'),
    url(r'^rango/login/$', views.user_login, name='login'),
   
  
    #url(r'^rango/account/(?P<user_id>\d+)$', views.front, name='front'),
    url(r'^rango/account/$',views.accountprofile,name='frontpage'),
    url(r'^rango/study/$',views.study,name='studypage'),
    url(r'^rango/problem/$',views.problems,name='problempage'),

    url(r'^rango/study/(?P<category_name_url>\w+)/$', views.category, name='category'),
    url(r'^rango/study/(?P<category_name_url>\w+)/article/new/$', views.ArticleCreateView.as_view(), name='article-new'),
    #url(r'^rango/account/$',views.front,name=''),
    url(r'^rango/account/personalprofile/(?P<pk>\d+)/$', views.UserListView.as_view(),name='personalprofil-list',),
    url(r'^rango/account/userprofile/edit/(?P<pk>\d+)/$', views.UpdateUserprofileView.as_view(),name='userprofile-edit',),
    url(r'^rango/account/userprofile/(?P<pk>\d+)/$', views.UserprofileListView.as_view(),name='userprofile-list',),
    url(r'^rango/account/personalprofile/edit/(?P<pk>\d+)/$', views.UpdateUserView.as_view(),name='personalprofil-edit',),
    url(r'^rango/account/groups/(?P<pk>\d+)/$', views.UsergroupsListView.as_view(),name='usergroups-list',),
    url(r'^rango/account/accountbalance/(?P<pk>\d+)/$', views.AccountbalanceListView.as_view(),name='accountbalance-list',),
    url(r'^rango/account/accountbalance/edit/(?P<pk>\d+)/$', views.AccountbalanceListView.as_view(),name='accountbalance-edit',),
    url(r'^rango/account/groups/edit/(?P<pk>\d+)/$', views.UpdateUseraddressView.as_view(),name='groups-edit',),
    url(r'^rango/account/address/edit/(?P<pk>\d+)$', views.UpdateUseraddressView.as_view(),name='address-edit',),
    url(r'^rango/account/password/edit/(?P<pk>\d+)/$', views.UpdatePasswordView.as_view(),name='password-edit',),
    url(r'^rango/register/$', views.register, name='register'),
   
    url(r'^rango/studyyy/(?P<slug>\w+)/$',views.CategoryDetailView.as_view(),name='article-view-category'),
    url(r'^rango/$', views.front, name='front'),
    url(r'^rango/studyy/nove/$',views.ArticleStudyListView.as_view(),name='article-view-pagin'),
    url(r'^rango/study/(?P<category_name_url>\w+)/article/(?P<pk>\d+)/$',views.ArticleDetailuserView.as_view(),name='article-view'),
    url(r'^rango/logout/$', views.user_logout, name='logout'),
    url(r'^rango/study/(?P<category_name_url>\w+)/article/delete/(?P<pk>\d+)/$', views.ArticleDeleteView.as_view(),name='article-delete'),
    url(r'^rango/study/(?P<category_name_url>\w+)/article/edit/(?P<pk>\d+)/$', views.ArticleUpdateView.as_view(),name='article-edit',),
    # url(r'^$', 'mypomoc.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^$', 'my_home', name='my_home',),
    url(r'^$', views.ListContactView.as_view(),name='contacts-list',), 
    url(r'^new$', views.CreateContactView.as_view(),name='contacts-new',),
    url(r'^edit/(?P<pk>\d+)/$', views.UpdateContactView.as_view(),name='contacts-edit',),
    #url(r'^$', views.ListContactView.as_view(),name='contacts-list',), 
    url(r'^delete/(?P<pk>\d+)/$', views.DeleteContactView.as_view(),name='contacts-delete',),
    url(r'^admin/', include(admin.site.urls)),
    url(r'articles/(?P<pk>\d+)$',views.ArticleDetailView.as_view(),name='article_detail'),
  
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
  
    url(r'tags/(?P<title>\w+)$', views.TagDetailView.as_view(),name='tag_detail'),
    url(r'authors/(?P<username>\w+)$','view_author',name='view_author'),

    url(r'^accounts/logout/$','django.contrib.auth.views.logout',{'template_name': 'login.html'},),
    url(r'^articles/new$', views.ArticleCreateView.as_view(),name='article-new',),
   
    
    # url(r'/$', view_home_method, 'home_url_name'),
    # url(r'/services/$', view_services_method, 'services_url_name'),
    # url(r'/contact/$', view_contact_method, 'contact_url_name'),
)
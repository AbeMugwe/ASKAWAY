from django.urls import path
from .views import home,detail,save_comment,save_upvote,save_downvote,register,ask_q,tag,profile,tags


app_name = "app"

urlpatterns=[
    path('',home,name='home'),
    path('content/<int:id>',detail,name='content'),
    path('save-comment',save_comment,name='saved'), 
    path('save-upvote',save_upvote,name='up'),
    path('save-downvote',save_downvote,name='down'),
    #Register
    path('accounts/sign-in/',register,name='sign-in'),
    #ask_q
    path('ask-question',ask_q,name='ask-question'),
    #tags
    path('tags/<str:tag>',tag,name='tag'),
    #Profile
    path('accounts/profile/',profile,name='profile'),
    #tags-page
    path('tagz',tags,name='tags'),

]
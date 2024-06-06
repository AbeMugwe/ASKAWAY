from django.contrib import admin
from .models import Q,A,Comments,Upvotes,Downvotes,CustomUser

# Register your models here.
class Questionadmin(admin.ModelAdmin):
    list_display=('title','user')
    search_fields=('title','content')

class UpvoteAdmin(admin.ModelAdmin):
    list_display=('answer','user')

class DownvoteAdmin(admin.ModelAdmin):
    list_display=('answer','user')


admin.site.register(Q,Questionadmin)
admin.site.register(A)
admin.site.register(Comments)
admin.site.register(Upvotes,UpvoteAdmin)
admin.site.register(Downvotes,DownvoteAdmin)
admin.site.register(CustomUser)


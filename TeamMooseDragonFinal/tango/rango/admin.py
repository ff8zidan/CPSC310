from django.contrib import admin
from rango.models import *
from rango.forms import *

admin.site.register(ImportData)
admin.site.register(Er_Room)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Post, PostAdmin)
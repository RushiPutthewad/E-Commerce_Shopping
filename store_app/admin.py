from django.contrib import admin

# Register your models here.
from . models import *

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Color)
admin.site.register(Filter_Price)
admin.site.register(Product)
admin.site.register(UserProfile)
admin.site.register(Order)
# admin.site.register(TShirtDesign)Design
admin.site.register(Design)
admin.site.register(Designer)
admin.site.register(SampleImage)

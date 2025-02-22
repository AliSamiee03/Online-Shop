from django.contrib import admin
from .models import CustomUser, Address, Staff, Role

admin.site.register([CustomUser, Address, Staff, Role])

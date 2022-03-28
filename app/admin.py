from django.contrib import admin
from . import models
from django.contrib.auth.admin import UserAdmin #使用django自己的UserAdmin来注册
from django.utils.translation import gettext, gettext_lazy as _
from .models import User

class UserAdmin(UserAdmin):
    #重写fieldsets在admin后台加入自己新增的字段
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Teacherinfo'), {'fields': ('TeacherID', 'TeacherClass')}),
    )

admin.site.register(User, UserAdmin)
# Register your models here.
admin.site.register(models.ClassGrade)
admin.site.register(models.AllClassGrade)
admin.site.register(models.AllTest)

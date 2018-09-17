from django.contrib import admin

from crm import models

# Register your models here.

class CustomerInfoAdmin(admin.ModelAdmin):

    list_display = ['name','contact_type','contact','source','referral_form','cousult_content','status','consultant','date']
    list_filter = ['source','consultant','status','date']


    search_fields = ['contact','consultant__name'] #外键







admin.site.register(models.Role)
admin.site.register(models.CustomerInfo, CustomerInfoAdmin)
admin.site.register(models.Student)
admin.site.register(models.CustomerfollowUp)
admin.site.register(models.Course)
admin.site.register(models.ClassList)
admin.site.register(models.CourseRecord)
admin.site.register(models.StudyRecord)
admin.site.register(models.Branch)
admin.site.register(models.Menus)
admin.site.register(models.UserProfile)

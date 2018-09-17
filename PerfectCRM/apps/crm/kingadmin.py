from kingadmin.sites import site
from crm import models

from kingadmin.kingadmin_base import BaseKingAdmin


class CustomerInfoAdmin(BaseKingAdmin):

    list_display = ['name','contact_type','contact','source','referral_form','cousult_content','status','consultant','date']
    list_filter = ['source','consultant','status','date']
    search_fields = ['contact','consultant__name'] #外键


class RoleAdmin(object):
    list_display= ['name']

class CustomerfollowUpAdmin(object):
    list_display = ['content','status_choices','status','data',]





site.register(models.CustomerInfo,CustomerInfoAdmin)
site.register(models.Role,RoleAdmin)
site.register(models.CustomerfollowUp,CustomerInfoAdmin)
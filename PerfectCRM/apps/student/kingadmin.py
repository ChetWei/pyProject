from kingadmin.sites import site
from student import models
from kingadmin.kingadmin_base import BaseKingAdmin

print("student kingadmin...........")
class TestAdmin(BaseKingAdmin):

    list_display = ['name']


site.register(models.Test,TestAdmin)
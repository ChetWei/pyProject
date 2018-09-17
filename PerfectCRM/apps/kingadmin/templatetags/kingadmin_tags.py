from django.template import Library
from django.utils.safestring import mark_safe
register = Library()

@register.simple_tag
def build_table_row(obj,admin_class):
    """生成一条记录的html element"""

    ele = ""
    for column_name in admin_class.list_display:
        #获取每一个字段对象
        column_obj = admin_class.model._meta.get_field(column_name)
        #如果这个字段对象有choices方法，则更换显示内容
        if column_obj.choices:
            column_data = getattr(obj,'get_%s_display' %column_name)()
        else:
            # 通过反射获取列的数据，两个参数，一个是object，一个是列名
            column_data = getattr(obj,column_name)

        td_ele = "<td>%s</td>" % column_data
        ele += td_ele

    return mark_safe(ele)
#   -*-coding:utf-8 -*-
#   @Author: 'ChetWei'
#   @Time: '2018/9/17 23:08'

from wtforms import Form,StringField,IntegerField
from wtforms.validators import Length, NumberRange, DataRequired


#继承第三方验证
class SearchForm(Form):
    q = StringField(validators=[DataRequired(),Length(min=1,max=30)])
    page = IntegerField(validators=[NumberRange(min=1,max=90)],default=1)
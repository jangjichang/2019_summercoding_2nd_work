from django import template
register = template.Library()

"""work_form.html에서 index로 value 가져오기 위해 추가한 tag"""
@register.filter
def get_at_index(object_list, index):
    return object_list[index]

from django import template
from django.template import Context
from django.db import connection
from django.utils.safestring import mark_safe

from menu.models import MenuItem

register = template.Library()


def render_menu(root, active_ids, depth=0):
    if not root:
        return ''
    html = '<ul  style= "list-style-type: disc;">'
    for node in root:
        item = node['item']
        children = node['children']
        is_active = item.id in active_ids
        should_expand = is_active or depth < 1
        html += '<li>'
        html += f'<a href="{item.url}">{item.title}</a>'
        if should_expand and children:
            html += render_menu(children, active_ids, depth + 1)
        elif is_active and children:
            html += render_menu(children, active_ids, depth + 1)
        html += '</li>'
    html += '</ul>'
    return html


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    current_url = request.path
    menu_items = MenuItem.objects.filter(menu_name=menu_name)
    menu_dict = {item.id: {'item': item, 'children': []} for item in menu_items}
    root = []
    for item in menu_items:
        if item.parent_id and item.parent_id in menu_dict:
            menu_dict[item.parent_id]['children'].append(menu_dict[item.id])
        else:
            root.append(menu_dict[item.id])
    active_ids = set()
    active_item = None
    for item in menu_items:
        item_url = item.url
        if item_url == current_url:
            active_item = item
            break

    if active_item:
        stack = [active_item]
        while stack:
            current = stack.pop()
            active_ids.add(current.id)
            if current.parent_id and current.parent_id in menu_dict:
                parent_item = menu_dict[current.parent_id]['item']
                if parent_item.id not in active_ids:
                    stack.append(parent_item)
    print(active_ids)
    menu_html = render_menu(root, active_ids)
    print("Количество обращений к БД: ", len(connection.queries))
    return mark_safe(menu_html)

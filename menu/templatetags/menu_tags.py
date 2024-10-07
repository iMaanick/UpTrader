from typing import Dict, Any, Optional, Union
from django import template
from django.template import Context
from django.db import connection
from django.utils.safestring import mark_safe, SafeString

from menu.models import MenuItem

register = template.Library()


def render_menu(root: list[int], active_ids: set[int], menu_dict: dict, depth: int = 0,) -> str:
    if not root:
        return ''
    html = '<ul  style= "list-style-type: disc;">'
    for node_id in root:
        item_data = menu_dict[node_id]
        item = item_data['item']
        children = item_data['children']
        is_active = item.id in active_ids
        should_expand = is_active or depth < 1
        html += '<li>'
        html += f'<a href="{item.url}">{item.title}</a>'
        if should_expand and children:
            html += render_menu(children, active_ids, menu_dict, depth + 1)
        elif is_active and children:
            html += render_menu(children, active_ids, menu_dict, depth + 1)
        html += '</li>'
    html += '</ul>'
    return html


def get_active_item(menu_dict: Dict[int, Dict[str, Any]], current_url: str) -> Optional[MenuItem]:
    active_item = None
    for item in menu_dict.values():
        if item['item'].url == current_url:
            active_item = item['item']
            return active_item
    return active_item


def get_active_ids(menu_dict: Dict[int, Dict[str, Any]], current_url: str) -> set:
    active_ids: set[int] = set()
    active_item = get_active_item(menu_dict, current_url)
    if not active_item:
        return active_ids
    stack = [active_item]
    while stack:
        current = stack.pop()
        active_ids.add(current.id)
        if current.parent_id and current.parent_id in menu_dict:
            parent_item = menu_dict[current.parent_id]['item']
            if parent_item.id not in active_ids:
                stack.append(parent_item)
    return active_ids


@register.simple_tag(takes_context=True)
def draw_menu(context: Context, menu_name: str) -> SafeString:
    current_url = context['request'].path
    menu_items = MenuItem.objects.filter(menu_name=menu_name)
    menu_dict = {item.id: {'item': item, 'children': []} for item in menu_items}
    root = []
    for item in menu_items:
        if item.parent_id and item.parent_id in menu_dict:
            menu_dict[item.parent_id]['children'].append(item.id)
        else:
            root.append(item.id)
    active_ids = get_active_ids(menu_dict, current_url)
    menu_html = render_menu(root, active_ids, menu_dict, 0,)
    print("Количество обращений к БД: ", len(connection.queries))
    return mark_safe(menu_html)

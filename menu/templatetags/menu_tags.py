from typing import Dict, Optional, Tuple
from django import template
from django.template import Context
from django.utils.safestring import mark_safe, SafeString

from menu.models import MenuItem, MenuDict

register = template.Library()


def render_menu(root_ids: list[int],
                active_ids: set[int],
                menu_dict: Dict[int, MenuDict],
                ) -> str:
    if not root_ids:
        return ''
    html = '<ul style="list-style-type: disc;">'
    for node_id in root_ids:
        menu_data = menu_dict[node_id]
        item = menu_data['item']
        children = menu_data['children']
        should_expand = item.id in active_ids
        html += '<li>'
        html += f'<a href="{item.get_url()}">{item.title}</a>'

        if should_expand and children:
            html += render_menu(children, active_ids, menu_dict)

        html += '</li>'
    html += '</ul>'
    return html


def get_active_item(menu_dict: Dict[int, MenuDict], current_url: str) -> Optional[MenuItem]:
    active_item = None
    for item in menu_dict.values():
        if item['item'].get_url() == current_url:
            active_item = item['item']
            return active_item
    return active_item


def get_active_ids(menu_dict: Dict[int, MenuDict], current_url: str) -> set[int]:
    active_ids: set[int] = set()
    active_item = get_active_item(menu_dict, current_url)

    while active_item:
        active_ids.add(active_item.id)
        parent_id = active_item.parent_id
        if isinstance(parent_id, int) and parent_id in menu_dict:
            active_item = menu_dict[parent_id]['item']
        else:
            break
    return active_ids


def build_menu_dict(menu_items: list[MenuItem]) -> Tuple[Dict[int, MenuDict], list[int]]:
    menu_dict: Dict[int, MenuDict] = {item.id: {'item': item, 'children': []} for item in menu_items}
    root_ids: list[int] = []

    for item in menu_items:
        if isinstance(item.parent_id, int) and item.parent_id in menu_dict:
            menu_dict[item.parent_id]['children'].append(item.id)
        else:
            root_ids.append(item.id)

    return menu_dict, root_ids


def draw_menu(context: Context, menu_name: str) -> SafeString:
    current_url = context['request'].path
    menu_items = MenuItem.objects.filter(menu_name=menu_name)

    menu_dict, root_ids = build_menu_dict(menu_items)
    active_ids = get_active_ids(menu_dict, current_url)
    menu_html = render_menu(root_ids, active_ids, menu_dict)
    return mark_safe(menu_html)


register.simple_tag(draw_menu, takes_context=True)

from typing import Dict, Any, Optional
from django.core.management.base import BaseCommand
from django.db import transaction, IntegrityError
from menu.models import MenuItem


class Command(BaseCommand):
    help: str = 'Clears the MenuItem table and fills it with test data'

    MENUS: list[Dict[str, Any]] = [
        {
            'menu_name': 'Main Menu',
            'items': [
                {'title': 'Home', 'url': '/home/', 'children': []},
                {'title': 'About', 'url': '/about/', 'children': [
                    {'title': 'Team', 'url': '/about/team/', 'children': []},
                    {'title': 'Careers', 'url': '/about/careers/', 'children': []},
                ]},
                {'title': 'Services', 'url': '/services/', 'children': [
                    {'title': 'Web Development', 'url': '/services/web-development/', 'children': []},
                    {'title': 'SEO', 'url': '/services/seo/', 'children': []},
                ]},
                {'title': 'Contact', 'url': '/contact/', 'children': []},
            ]
        },
        {
            'menu_name': 'Footer Menu',
            'items': [
                {'title': 'Privacy Policy', 'url': '/privacy/', 'children': []},
                {'title': 'Terms of Service', 'url': '/terms/', 'children': []},
                {'title': 'Support', 'url': '/support/', 'children': []},
            ]
        },
        {
            'menu_name': 'Sidebar Menu',
            'items': [
                {'title': 'Dashboard', 'url': '/dashboard/', 'children': []},
                {'title': 'Settings', 'url': '/settings/', 'children': [
                    {'title': 'Profile', 'url': '/settings/profile/', 'children': []},
                    {'title': 'Security', 'url': '/settings/security/', 'children': [
                        {'title': 'Password', 'url': '/settings/security/password/', 'children': [
                            {'title': 'Change Password', 'url': '/settings/security/password/change/',
                             'children': []},
                            {'title': 'Reset Password', 'url': '/settings/security/password/reset/',
                             'children': []},
                        ]},
                        {'title': '2FA', 'url': '/settings/security/2fa/', 'children': [
                            {'title': 'Enable 2FA', 'url': '/settings/security/2fa/enable/', 'children': []},
                            {'title': 'Disable 2FA', 'url': '/settings/security/2fa/disable/', 'children': []},
                        ]},
                    ]},
                ]},
                {'title': 'Logs', 'url': '/logs/', 'children': []},
            ]
        },
    ]

    def clear_menu_items(self) -> None:
        self.stdout.write('Deleting existing MenuItem objects...')
        MenuItem.objects.all().delete()
        self.stdout.write('Existing MenuItem objects deleted.')

    def fill_menu_items(self) -> None:
        self.stdout.write('Creating menu test data...')

        for menu in Command.MENUS:
            menu_name = menu['menu_name']
            items = menu['items']
            self.create_menu_items(items, parent=None, menu_name=menu_name)

    def handle(self, *args: Any, **options: Any) -> None:
        try:
            with transaction.atomic():
                self.clear_menu_items()
                self.fill_menu_items()
            self.stdout.write(self.style.SUCCESS(
                'The MenuItem table has been successfully filled with test data.'))
        except IntegrityError as e:
            self.stderr.write(self.style.ERROR(f'Failed to fill MenuItem table, error {e}'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Unexpected error: {e}'))

    def create_menu_items(self,
                          items: list[Dict[str, Any]],
                          parent: Optional[MenuItem] = None,
                          menu_name: Optional[str] = None
                          ) -> None:
        for item in items:
            menu_item = MenuItem.objects.create(
                title=item['title'],
                url=item['url'],
                parent=parent,
                menu_name=menu_name
            )
            if item['children']:
                self.create_menu_items(item['children'], parent=menu_item, menu_name=menu_name)

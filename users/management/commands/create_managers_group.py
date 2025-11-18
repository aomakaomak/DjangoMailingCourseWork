from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = 'Создаёт группу "Менеджеры" и назначает ей права согласно ТЗ'

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name="Менеджеры")

        if created:
            self.stdout.write(self.style.SUCCESS('Группа "Менеджеры" создана'))
        else:
            self.stdout.write(self.style.WARNING('Группа "Менеджеры" уже существует'))

        # список нужных прав (codename, app_label)
        perms_to_add = [
            # mailing.Client
            ("view_all_clients", "mailing"),
            # mailing.SendMail
            ("view_all_sendmails", "mailing"),
            ("disable_sendmail", "mailing"),
            # users.CustomUser
            ("view_user_list", "users"),
            ("block_user", "users"),
        ]

        for codename, app_label in perms_to_add:
            try:
                perm = Permission.objects.get(
                    codename=codename, content_type__app_label=app_label
                )
                group.permissions.add(perm)
                self.stdout.write(
                    self.style.SUCCESS(f"Добавлено право {app_label}.{codename}")
                )
            except Permission.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f"Право {app_label}.{codename} не найдено")
                )

        self.stdout.write(self.style.SUCCESS('Группа "Менеджеры" настроена'))

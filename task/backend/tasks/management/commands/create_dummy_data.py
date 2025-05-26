from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from tasks.models import Task, Project
import random
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'ダミーユーザーとダミータスクを作成します'

    def handle(self, *args, **options):
        User = get_user_model()

        # ダミーユーザー作成
        users = []
        for i in range(1, 6):
            username = f'user{i}'
            email = f'user{i}@example.com'
            password = 'testpass123'
            user, created = User.objects.get_or_create(username=username, defaults={'email': email})
            if created:
                user.set_password(password)
                user.save()
                self.stdout.write(self.style.SUCCESS(f'ユーザー作成: {username} / {password}'))
            users.append(user)

        # ダミープロジェクト作成
        projects = []
        for i in range(1, 4):
            project, _ = Project.objects.get_or_create(name=f'プロジェクト{i}', defaults={'description': f'これはプロジェクト{i}の説明です'})
            projects.append(project)

        # 既存のダミータスク削除
        Task.objects.filter(title__startswith='ダミータスク').delete()

        # ダミータスク作成
        today = date.today()
        kanban_statuses = ['not_started', 'in_progress', 'review', 'done']
        for i in range(1, 41):
            assignee = random.choice(users)
            creator = random.choice(users)
            # 開始日を今日から-30日〜+30日の範囲でランダムに
            start = today + timedelta(days=random.randint(-30, 30))
            # 終了日は開始日から7〜30日後
            end = start + timedelta(days=random.randint(7, 30))
            project = random.choice(projects)
            status = random.choice(kanban_statuses)
            task = Task.objects.create(
                title=f'ダミータスク{i}',
                description=f'これはダミータスク{i}の説明です',
                assignee=assignee,
                creator=creator,
                status=status,
                start_date=start,
                end_date=end,
                project=project
            )
            self.stdout.write(self.style.SUCCESS(f'タスク作成: {task.title}（担当: {assignee.username}、プロジェクト: {project.name}、ステータス: {status}）'))

        self.stdout.write(self.style.SUCCESS('ダミーデータ作成完了！')) 
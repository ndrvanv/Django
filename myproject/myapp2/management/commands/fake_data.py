from django.core.management.base import BaseCommand
from myapp2.models import Post, Author

class Command(BaseCommand):
    help = "Generate fake authors and posts"

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='User ID')

    def handle(self, *args, **kwargs):
        count = kwargs.get('count')
        for i in range(1, count + 1):
            author = Author(name=f'Name_{i},', email=f'mail{i}@gmail.com')
            author.save()
            for j in range(1, count + 1):
                post = Post(
                    title=f'Title{j}',
                    content=f'Text from {author.name} #{j} is very long text',
                    author=author
                )
                post.save()
import os.path

from django.contrib.auth.models import User
from django.db import models
from markdownx.models import MarkdownxField
from markdownx.utils import markdown

# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/recruit-post/tag/{self.slug}'

    class Meta:
        verbose_name_plural = 'Tags'


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)  # unique: 같은 이름을 가진 카테고리를 만들지 못하도록 설정
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)  # url의 주소를 만들어주는 Slug, 한글 Url(Slug)을 사용하고 싶다면, unicode를 허용해야한다.

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/recruit-post/category/{self.slug}'

    class Meta:
        verbose_name_plural = 'Categories'


class RecruitPost(models.Model):
    title = models.CharField(max_length=30)  # 제목
    content = MarkdownxField()  # 내용
    hook_message = models.TextField(blank=True)  # 미리보기 내용

    numberOfMembers = models.IntegerField  # 모집중인 인원
    tempNumberOfMembers = models.IntegerField  # 현재 모집된 인원

    dueDate = models.DateTimeField  # 마감일

    head_image = models.ImageField(upload_to='recruit-post/images/%Y/%m/%d/', blank=True)
    attached_file = models.FileField(upload_to='recruit-post/files/%Y/%m/%d/', blank=True)

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    # post와 one to many relationship으로 연결 (
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)  # 유저가 삭제되면, post가 의미가 없어지기 때문에 cascade

    # null, blank --> null은 DB 속성 중 null이 가능한지, blank는 request롤 입력시 빈칸이 가능한지.
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return f'[{self.pk}] {self.title} :: {self.author}'

    def get_absolute_url(self):
        return f'/recruit-post/{self.pk}'

    def get_file_name(self):
        return os.path.basename(self.attached_file.name)

    def get_content_markdown(self):
        return markdown(self.content)


class Comment(models.Model):
    post = models.ForeignKey(RecruitPost, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author}::{self.content}'

    def get_absolute_url(self):
        return f'{self.post.get_absolute_url()}#comment-{self.pk}'
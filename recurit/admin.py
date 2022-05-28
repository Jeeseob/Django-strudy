from django.contrib import admin

# 현재 디렉토리의 하위 디렉토리인 models에서 Post객체 import
from .models import RecruitPost, Category, Tag, Comment
from markdownx.admin import MarkdownxModelAdmin


# 카테고리 이름을 기반으로 slug을 만들어주는 코드
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


# admin.site.register(Post)
admin.site.register(RecruitPost)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(RecruitPost, MarkdownxModelAdmin)
admin.site.register(Comment)

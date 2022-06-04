from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404

# CBV를 사용하기 위함.
from django.views.generic import ListView, DetailView, CreateView, UpdateView

# url패턴에서 실행하는 함수
from recruit.models import RecruitPost, MemberJoin, Category, Tag

# 로그인 방문자 접근
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CommentForm


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = RecruitPost
    fields = ['title', 'number_of_member', 'hook_message', 'content', 'head_image', 'due_date', 'category', 'tags']

    template_name = "recruit/recruitpost_form_update.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


class PostCreate(LoginRequiredMixin, CreateView):
    model = RecruitPost
    fields = ['title', 'number_of_member', 'hook_message', 'content', 'head_image', 'due_date', 'category', 'tags']

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.author = current_user
            return super(PostCreate, self).form_valid(form)
        else:
            return redirect('/recruit')


class JoinCreate(LoginRequiredMixin, CreateView):
    model = MemberJoin
    fields = ['name', 'phone_number', 'content']

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.author = current_user
            form.instance.recruit_post = RecruitPost.objects.get(pk=self.kwargs['pk'])

            return super(JoinCreate, self).form_valid(form)
        else:
            return redirect('/recruit')


class JoinDetail(DetailView):
    model = MemberJoin

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated and self.request.user == self.get_object().author \
                or self.request.user == RecruitPost.objects.get(pk=self.kwargs['pk']).author:
            context = super(JoinDetail, self).get_context_data()
            context['categories'] = Category.objects.all()
            context['no_category_post_count'] = RecruitPost.objects.filter(category=None).count()

            return context
        else:
            raise PermissionDenied
            #return redirect('/recruit/post/' + str(self.kwargs['pk']))


class JoinList(LoginRequiredMixin, ListView):
    model = MemberJoin  # 모델 객체 설정
    ordering = 'pk'  # 정렬 방식 설정(선착순)

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            context = super(JoinList, self).get_context_data()
            context['memberjoin_list'] = MemberJoin.objects.filter(author=self.request.user)
            context['recruitpost'] = RecruitPost.objects.get(pk=self.kwargs['pk'])
            context['categories'] = Category.objects.all()
            context['no_category_post_count'] = RecruitPost.objects.filter(category=None).count()

            return context

        else:
            raise PermissionDenied
            # return redirect('/recruit/post/'+self.kwargs['pk'])


class MyPageRecruit(LoginRequiredMixin, ListView):
    model = RecruitPost  # 모델 객체 설정
    ordering = 'pk'  # 정렬 방식 설정(선착순)

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            context = super(MyPageRecruit, self).get_context_data()
            context['recruitpost_list'] = RecruitPost.objects.filter(author=self.request.user)
            context['categories'] = Category.objects.all()
            context['no_category_post_count'] = RecruitPost.objects.filter(category=None).count()

            return context

        else:
            raise PermissionDenied

class MyPageJoin(LoginRequiredMixin, ListView):
    model = MemberJoin  # 모델 객체 설정
    ordering = 'pk'  # 정렬 방식 설정(선착순)

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            context = super(MyPageJoin, self).get_context_data()
            context['memberjoin_list'] = MemberJoin.objects.filter(author=self.request.user)
            context['categories'] = Category.objects.all()
            context['no_category_post_count'] = RecruitPost.objects.filter(category=None).count()

            return context

        else:
            raise PermissionDenied


def my_page(request):
    context = {
        'categories': Category.objects.all(),
        'no_category_post_count': RecruitPost.objects.filter(category=None).count(),
    }
    return render(
        request,
        'recruit/mypage.html',
        context
    )

# class based views (CBV)
class PostList(ListView):
    model = RecruitPost  # 모델 객체 설정
    ordering = '-pk'  # 정렬 방식 설정(pk 역순)

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = RecruitPost.objects.filter(category=None).count()
        return context


class PostDetail(DetailView):
    model = RecruitPost

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = RecruitPost.objects.filter(category=None).count()
        context['comment_form'] = CommentForm

        return context


class CategoryPostList(ListView):
    model = RecruitPost
    ordering = '-pk'

    def get_context_data(self, **kwargs):
        context = super(CategoryPostList, self).get_context_data()
        if self.kwargs['slug'] == 'no-category':
            context['recruitpost_list'] = RecruitPost.objects.filter(category__slug=None)
            context['category'] = '미분류'
        else:
            context['recruitpost_list'] = RecruitPost.objects.filter(category__slug=self.kwargs['slug'])
            context['category'] = Category.objects.get(slug=self.kwargs['slug'])

        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = RecruitPost.objects.filter(category=None).count()

        return context

def show_tag_posts(request, slug):
    tag = Tag.objects.get(slug=slug)
    recruitpost_list = tag.recruitpost_set.all()

    context = {
        'categories': Category.objects.all(),
        'no_category_post_count': RecruitPost.objects.filter(category=None).count(),
        'tag': tag,
        'recruitpost_list': recruitpost_list
    }

    return render(
        request,
        'recruit/recruitpost_list.html',
        context
    )


def show_search_posts(request, search):
    allTags = Tag.objects.all()

    # Tag가 존재하는지 확인
    slugs = []

    for i in allTags:
        if search in i.slug:
            slugs.append(i.slug)

    recruitpost_list = []
    for slug in slugs:
        tag = Tag.objects.get(slug=slug)
        recruitpost_list += tag.recruitpost_set.all()

    context = {
        'categories': Category.objects.all(),
        'no_category_post_count': RecruitPost.objects.filter(category=None).count(),
        'search': search,
        'recruitpost_list': recruitpost_list
    }

    return render(
        request,
        'recruit/recruitpost_list.html',
        context
    )


def new_comment(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(RecruitPost, pk=pk)

        if request.method == "POST":
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()

                return redirect(comment.get_absolute_url())
        else:
            return redirect(post.get_absolute_url())

    else:
        raise PermissionDenied

# 템플릿 이름을 강제하는 방법. -> 하지만, name convention에 익숙해진 사람들에게 혼선을 줄 수 있어, 지정한 대로 하는 것이 생산성이 높다.
# template_name = 'blog/index.html'
# Create your views here.

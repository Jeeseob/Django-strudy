from django.shortcuts import render
from recruit.models import RecruitPost
from recruit.models import Category
# Create your views here.

def landing(request):
    return render(
        request,
        'index.html',
        {
            'recent_posts': RecruitPost.objects.order_by('-pk')[:3],
            'categories': Category.objects.all(),
            'no_category_post_count': RecruitPost.objects.filter(category=None).count(),
        }
    )
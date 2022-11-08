from django.shortcuts import render, redirect
from .models import Post, Category, Tag
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Create your views here.
class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff


    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_superuser or current_user.is_staff):
            form.instance.author = current_user
            return super(PostCreate, self).form_valid(form)
        else:
            return redirect('/blog/')

    # 템플릿 : 모델명_form.html
    # 아래 함수는 CreateView와 관계없이 sidebar을 보기 위한 함수
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostCreate, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count  # category가 없는 것들
        return context

class PostList(ListView):
    model = Post
    ordering = '-pk'


    #category때문에 넣어준 함수 : 추가하고싶은 요소
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count    # category가 없는 것들
        return context

    # 템플릿 모델명_list.html : post_list.html
    # post_list.html파일은 현재 blog디렉토리에 있는 index.html과 같다. 이름만 다르게 한 것.
    # 파라미터 모델명_list : post_list
class PostDetail(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetail,self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count
        return context


def category_page(request, slug):
    if slug == 'no_category':
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else :
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)
    return render(request,'blog/post_list.html', {
        'category' : category,
        'post_list' : post_list,
        'categories' : Category.objects.all(),
        'no_category_post_count' : Post.objects.filter(category=None).count
    })


def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()
    return render(request, 'blog/post_list.html', {
        'tag': tag,
        'post_list': post_list,
        'categories': Category.objects.all(),
        'no_category_post_count': Post.objects.filter(category=None).count
    })


    # 템플릿 모델명_detail.html : post_detail.html
    # 파라미터 모델명 : post

#def index(request):
#    posts = Post.objects.all().order_by('-pk')

#    return render(request, 'blog/index.html', {'posts' : posts})

#def single_post_page(request, pk):
#    post = Post.objects.get(pk=pk)

#    return render(request, 'blog\single_post_page.html', {'post':post})
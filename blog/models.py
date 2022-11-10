from django.db import models
from django.contrib.auth.models import User
import os

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self): #IP주소/blog/tag/slug/
        return f'/blog/tag/{self.slug}/'

# Category는 admin해줘야함. admin에서 category볼 수 있도록 + views설정도, 설정주의 sidebar? post_set.all() <-ex
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
    def __str__(self):
        return self.name

    # slug에 맞게 카테고리 배열됨
    def get_absolute_url(self):
        return f'/blog/category/{self.slug}'

    # admin에 뜨는 이름 지어줄 때
    class Meta:
        verbose_name_plural = 'Categories'



class Post(models.Model):
    title = models.CharField(max_length=30)
    hook_text = models.CharField(max_length=100, blank=True)  #CharField와 다르게 TextField는 길이 제한 없음.
    content = models.TextField()

    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)    # _media가 생략된 것...?
    # %Y 2022, %y 22
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 추후 author 작성  - 다대일 관계를 표현하는 foreignkey
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)  # models.CASCADE는 사용자가 지워지면 작성한 글도 지워짐

    #카테고리 다대일 설정. admin.py도 설정해줘야함.
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, null=True, blank=True)

    def __str__(self):
        return f'[{self.pk}]{self.title}:: {self.author} : {self.created_at}'

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'


    #다운로드 될 파일 이름 설정
    def get_file_name(self):
        return os.path.basename(self.file_upload.name)

    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]
        # get_file_name() => 결과는 파일 이름.확장명
        # split(.)을 하면 a.txt -> a txt
        # b.docx -> b docx
        # c.xlsx -> c xlsx  로 나뉘게 된다.
        # a.b.c.txt -> a b c txt 로 나뉠 수 있는 예외가 생김
        # 이것때문에 []이 인덱스 번호는 1이 아닌 -1로 표현한다.
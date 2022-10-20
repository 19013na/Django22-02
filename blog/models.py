from django.db import models
from django.contrib.auth.models import User
import os

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=30)
    hook_text = models.TextField(max_length=100, blank=True)  #CharField와 다르게 TextField는 길이 제한 없음.
    content = models.TextField()

    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)    # _media가 생략된 것...?
    # %Y 2022, %y 22
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 추후 author 작성
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'[{self.pk}]{self.title}:: {self.author} : {self.created_at}'

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'

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
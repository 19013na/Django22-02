from django.urls import path
from . import views

urlpatterns = [ #IP주소/blog
    path('', views.PostList.as_view()),
    path('<int:pk>/', views.PostDetail.as_view())

    #path('', views.index), #IP주소/blog
    #path('<int:pk>/', views.single_post_page)  #<---- 09/29수업. 함수를 사용하지 않고 클래스를 이용하겠다.

]
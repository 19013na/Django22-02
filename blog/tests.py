from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post, Category
from django.contrib.auth.models import User

#1. pip install beautifulsoup4 *confirm : pip list

# Create your tests here.
class TestView(TestCase):   #class 만듦. class 이름은 시작 대문자 , view부분을 검사하는 것

    def setUp(self):
        self.client = Client()
        self.user_kim = User.objects.create_user(username="kim", password="somepassword")   #user관련 test
        self.user_lee = User.objects.create_user(username="lee", password="somepassword")   #그리고 2. post가 있는 경우로 가서 author추가

        #Category검사하려고 Category만들어줌.
        self.category_com = Category.objects.create(name="computer", slug="computer")
        self.category_cul = Category.objects.create(name="culture", slug="culture")

        #Category검사하려고 post를 미리 만듦.
        self.post_001 = Post.objects.create(title="첫번째 포스트", content="첫번째 포스트입니다.",author = self.user_kim,
                                            category=self.category_com)
        self.post_002 = Post.objects.create(title="두번째 포스트", content="두번째 포스트입니다.",author = self.user_lee,
                                            category=self.category_cul)
        self.post_003 = Post.objects.create(title="세번째 포스트", content="세번째 포스트입니다.",
                                       author = self.user_lee)

    #별도의 nav에 대한 함수이므로 Test가 이름 앞에 붙으면 안된다.
    def nav_test(self, soup):
        navbar = soup.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('AboutMe', navbar.text)

        # a태그가 Home으로 되어있냐
        home_btn = navbar.find('a', text="Home")
        # 홈버튼에서 href로 되어있는 값하고 슬래시 url값이 같은가.
        self.assertEqual(home_btn.attrs['href'],"/")
        blog_btn = navbar.find('a', text="Blog")
        self.assertEqual(blog_btn.attrs['href'], "/blog/")
        about_btn = navbar.find('a', text="AboutMe")
        self.assertEqual(about_btn.attrs['href'], "/about_me/")

    def category_test(self, soup):
        # sidebar.html에서 category부분을 category-card로 아이디 설정
        category_card = soup.find('div', id='category-card')
        self.assertIn('Categories', category_card.text)
        self.assertIn(f'{self.category_com} ({self.category_com.post_set.count()})', category_card.text)
        self.assertIn(f'{self.category_cul} ({self.category_cul.post_set.count()})', category_card.text)
        #필드명말고도 추가적으로 다른 정보가 들어가는 경우 f를 넣어줘야한다.
        self.assertIn(f'미분류 (1)', category_card.text)

    def test_post_list(self):                       #0
        response = self.client.get('/blog/')        #0
        #0. response 결과가 정상적인지
        self.assertEqual(response.status_code, 200) #0. url가져올때마다 test해줘야함.
        # /blog/가 정상적으로 작동하는가, 200이 정상 화면 출력 (오류는 404)

        #0. soup는 그냥 변수이름임. 바꿀 수 있음.
        soup = BeautifulSoup(response.content, 'html.parser') # 0. response의 content를 가져오겠다. + 분석까지 하겠다. html로 파서

        #0. title이 정상적으로 보이는지
        self.assertEqual(soup.title.text, 'Blog')   #1

        #0. navbar가 정상적으로 보이는지
        #navbar = soup.nav                      #1 모듈화를 해주고 나서 navbar가 post_list랑 detail에서랑 통일됨.
        #self.assertIn('Blog', navbar.text)     #1 함수로 만들어서 사용
        #self.assertIn('AboutMe', navbar.text)  #1
        self.nav_test(soup)     #함수를 호출하는 형식으로 만들어줌.
        self.category_test(soup)    #Category검사

        self.assertEqual(Post.objects.count(), 3)

        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        main_area = soup.find('div', id="main-area")
        self.assertIn(self.post_001.title, main_area.text)
        self.assertIn(self.post_002.title, main_area.text)
        self.assertIn(self.post_001.author.username.upper(), main_area.text)
        self.assertIn(self.post_002.author.username.upper(), main_area.text)
        self.assertNotIn('아무 게시물이 없습니다.', main_area.text)

        # Post가 정상적으로 보이는지 테스트한다.
        # 1-1. 맨 처음엔 Post가 하나도 없어야해서 이전에 테스트로 생성한 post 모두 지워줌.
        Post.objects.all().delete()

        # 1-2. 포스트가 하나도 없다면 post가 정상적으로 보이는가
        self.assertEqual(Post.objects.count(), 0)

        # 1-3. blog의 포스트 목록 페이지를 가져온다.
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        # 1-4. id가 main-area인 div태그를 찾을거다. main-area는 base.html에 있음.
        main_area = soup.find('div', id="main-area")
        self.assertIn('아무 게시물이 없습니다.', main_area.text)  # 1. 저말이 main_area에 포함되어있는가.

        # 1-5. Post가 2개 있는 경우 - Category 검사때문에 위로 올림...
        #post_001 = Post.objects.create(title="첫번째 포스트", content="첫번째 포스트입니다.",     #2
        #                              author = self.user_kim)
        #post_002 = Post.objects.create(title="두번째 포스트", content="두번째 포스트입니다.",     #2
        #                               author = self.user_lee)
        #self.assertEqual(Post.objects.count(), 2)
        # 2-1. 아래 3줄은 포스트 목록페이지를 새로고침했을 때,
        #response = self.client.get('/blog/')
        #self.assertEqual(response.status_code, 200)
        #soup = BeautifulSoup(response.content, 'html.parser')
        #2-2. manin area에 포스트가 2개 존재한다.
        #main_area = soup.find('div', id="main-area")
        #self.assertIn(self.post_001.title, main_area.text)
        #self.assertIn(self.post_002.title, main_area.text)
        # (+) user확인
        # self.assertIn(post_001.author.username.upper(), main_area.text)
        # self.assertIn(post_002.author.username.upper(), main_area.text)
        #2-3. '아직 게시물이 없습니다'문구는 더 이상 나타나지 않아야한다.
        #self.assertNotIn('아무 게시물이 없습니다.', main_area.text)   # notin이다! 있으면 안된다.


    def test_post_detail(self):
        # 1-1. 처음 시작할 때는 아무런 페이지 없이 시작. 페이지 하나 이상 있어야 들어갈 수 있음.
        #post_001 = Post.objects.create(title="첫번째 포스트", content="첫번째 포스트입니다.",
        #                               author=self.user_kim)
        #1-2. 바로 위에 post_001로 포스트를 만듦. 그게 잘 작동하는가 검사
        self.assertEqual(self.post_001.get_absolute_url(), '/blog/1/')

        #1-3. post_001의 내용을 가져옴. 그리고 정상적으로 작동하는지 테스트
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)                 #이게 정상적으로 작동하는가.
        soup = BeautifulSoup(response.content, 'html.parser')

        #1-4. navbar가 잘 돌아가는지 확인, post_detail과 post_list의 navbar가 동일해서 위에 함수로 만들어줌.
        #navbar = soup.nav
        #self.assertIn('Blog', navbar.text)
        #self.assertIn('AboutMe', navbar.text)
        self.nav_test(soup)

        # 1-5. soup.title에 post_001 title이 있는지 검사
        self.assertIn(self.post_001.title, soup.title.text)

        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('div', id='post-area')
        self.assertIn(self.post_001.title, post_area.text)
        self.assertIn(self.post_001.content, post_area.text)
        # (+) user테스트
        self.assertIn(self.post_001.author.username.upper(), post_area.text)
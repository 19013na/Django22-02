from django.contrib import admin
from .models import Post, Category

# Register your models here.
#post목록이 admin에서 보일 수 있도록 한다.
admin.site.register(Post)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}
# slug는 name과 같은 값을 가지는데, 자동설정될 수 있도록 미리 설정해둔다.

#카테고리 목록이 admin에서 보일 수 있도록한다.
admin.site.register(Category, CategoryAdmin)

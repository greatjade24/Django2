from django.contrib import admin
from board.models import Board

# Register your models here.
class BoardAdmin(admin.ModelAdmin):
    list_display=('id','제목','작성자','조회수')

admin.site.register(Board, BoardAdmin)
from django.contrib import admin

# Register your models here.

from newspaperapp.models import newsArticle, userInfo, newsCategory, Comment

class newsArticleAdmin(admin.ModelAdmin):
    list_display = ('headline', 'text', 'category')
    #list_editable = ('category')

admin.site.register(newsArticle, newsArticleAdmin)
admin.site.register(userInfo)
admin.site.register(newsCategory)
admin.site.register(Comment)

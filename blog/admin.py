from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe

from .models import *

from ckeditor_uploader.widgets import CKEditorUploadingWidget


class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'


class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('id', 'title', 'slug', 'categories', 'created_at', 'views', 'get_photo', 'is_published')
    list_display_links = ('id', 'title')
    list_filter = ('categories', 'is_published')
    list_editable = ('is_published',)
    fields = ('title', 'slug', 'content', 'photo', 'get_photo', 'categories', 'tags', 'views', 'created_at', 'is_published')
    readonly_fields = ('get_photo', 'views', 'created_at')
    search_fields = ('title', 'content')
    save_on_top = True
    save_as = True

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="75">')

    get_photo.short_description = 'IMG'


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


class CommentAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ('id', 'post', 'name', 'created_at')
    readonly_fields = ('created_at',)


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment, CommentAdmin)
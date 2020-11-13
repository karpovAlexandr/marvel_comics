from django.contrib import admin

from marvel.models import Comics, Profile, Creators, Characters, Stories


@admin.register(Stories)
class StoriesAdmin(admin.ModelAdmin):
    fields = ('name', 'type',)
    list_display = ('id', 'name', 'type',)
    list_display_links = ('id', 'name', 'type',)


@admin.register(Characters)
class CharactersAdmin(admin.ModelAdmin):
    fields = ('name',)
    list_display = ('id', 'name',)
    list_display_links = ('id', 'name',)


@admin.register(Creators)
class CreatorsAdmin(admin.ModelAdmin):
    fields = ('name', 'role',)
    list_display = ('id', 'name', 'role',)
    list_display_links = ('id', 'name', 'role',)


@admin.register(Comics)
class ComicsAdmin(admin.ModelAdmin):
    fields = ('comics_id', 'title', 'variant_description',)
    list_display = ('comics_id', 'title', 'variant_description',)
    list_display_links = ('comics_id', 'title', 'variant_description',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display = ('id',)
    list_display_links = ('id',)

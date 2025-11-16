from django.contrib import admin
from .models import PersonalInfo, Education, WorkExperience, Project, HobbyPost

@admin.register(PersonalInfo)
class PersonalInfoAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'headline', 'email', 'location')

admin.site.register(Education)
admin.site.register(WorkExperience)
admin.site.register(Project)

@admin.register(HobbyPost)
class HobbyPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'person', 'created_at', 'is_published')
    list_filter = ('category', 'is_published', 'created_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
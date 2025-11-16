from django.db import models

class PersonalInfo(models.Model):
    full_name = models.CharField(max_length=120)
    headline = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=120, blank=True)
    photo_url = models.URLField(blank=True)

    def __str__(self):
        return self.full_name

class Education(models.Model):
    person = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE, related_name='educations')
    school = models.CharField(max_length=200)
    degree = models.CharField(max_length=200, blank=True)
    field = models.CharField(max_length=200, blank=True)
    start_year = models.IntegerField(null=True, blank=True)
    end_year = models.IntegerField(null=True, blank=True)
    details = models.TextField(blank=True)

    def __str__(self):
        return f"{self.school} - {self.degree}"

class WorkExperience(models.Model):
    person = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE, related_name='experiences')
    company = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.company} - {self.role}"

class Project(models.Model):
    person = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=200)
    url = models.URLField(blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

class HobbyPost(models.Model):
    CATEGORY_CHOICES = [
        ('poem', 'Poem'),
        ('movie', 'Movie Review'),
        ('anime', 'Anime Review'),
        ('blog', 'Blog / Reflection'),
        ('other', 'Other'),
    ]

    person = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE, related_name='hobby_posts')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='blog')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

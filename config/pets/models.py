from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils import timezone

class Pet(models.Model):
    name = models.CharField(max_length=45)
    size_choice = (
        ('Small', 'Small (1-10 kg)'),
        ('Medium', 'Medium (11-26 kg)'),
        ('Large', 'Large (27-45 kg)'),
        ('Extra-Large', 'Extra-Large (46+ kg)')
    )
    size = models.CharField(max_length=40, blank=True, null=True, choices=size_choice)
    breed = models.CharField(max_length=50)
    gender_choice = (
        ('Male', 'Male'),
        ('Female', 'Female')
        )
    gender = models.CharField(max_length=30, blank=True, null=True, choices=gender_choice)
    age = models.IntegerField()
    characteristics = models.TextField()
    overall_health = models.TextField()
    children_choice = (
        ('children < 5', 'children under 5 years old'),
        ('children < 12', 'children under 12 years old'),
        ('all age children ', 'children of all ages'),
        ('no children ', 'can not handle the stress of children'),
    )
    good_in_home_with = models.CharField(max_length=50, blank=True, null=True, choices=children_choice)
    date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=100, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name + '-' + str(self.size) + '-' + self.breed + '-' + str(self.gender)+ '-' + str(self.age))
        return super().save(*args, **kwargs)

    banner = models.ImageField(default="fallback.PNG", blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    approved = models.BooleanField('Approved', default=False)
    rejected = models.BooleanField('Rejected', default=False)
    def __str__(self):
        return self.name

class Application(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    applicant_email = models.EmailField()
    message = models.TextField()
    objects = models.Manager()
    def __str__(self):
        return f"Application for {self.pet.name} by {self.applicant_email}"
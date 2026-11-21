from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return self.user.username

    @property
    def total_hours(self):
        return sum(c.hours for c in self.user.contributions.filter(status='Confirmed'))

    @property
    def total_contributions(self):
        return self.user.contributions.filter(status='Confirmed').count()

class Contribution(models.Model):
    CATEGORY_CHOICES = [
        ('Cleanup', 'Cleanup'),
        ('Teaching', 'Teaching'),
        ('Health', 'Health'),
        ('Environment', 'Environment'),
        ('Other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contributions')
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    location = models.CharField(max_length=100, blank=True)
    date = models.DateField()
    hours = models.DecimalField(max_digits=5, decimal_places=1)
    photo = models.ImageField(upload_to='contributions/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.user.username}"

class Confirmation(models.Model):
    contribution = models.OneToOneField(Contribution, on_delete=models.CASCADE, related_name='confirmation')
    confirmed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(blank=True)
    confirmed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Confirmed: {self.contribution.title}"
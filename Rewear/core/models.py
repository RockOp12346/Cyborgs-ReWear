from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

User = get_user_model()

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    points = models.IntegerField(default=0)
    profile_img = models.ImageField(upload_to='profile_images', default='default_profile.png')
    location = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Item(models.Model):
    CONDITION_CHOICES = [
        ('NEW', 'New with tags'),
        ('LIKE_NEW', 'Like new'),
        ('GOOD', 'Good'),
        ('FAIR', 'Fair'),
    ]
    
    CATEGORY_CHOICES = [
        ('TOPS', 'Tops'),
        ('BOTTOMS', 'Bottoms'),
        ('DRESSES', 'Dresses'),
        ('OUTERWEAR', 'Outerwear'),
        
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending Approval'),
        ('ACTIVE', 'Active'),
        ('SWAPPED', 'Swapped'),
        ('REMOVED', 'Removed'),
    ]

    title = models.CharField(max_length=200)
    is_available = models.BooleanField(default=True)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    size = models.CharField(max_length=10)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    points_required = models.IntegerField(validators=[MinValueValidator(0)])
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.CharField(max_length=200, blank=True)

    @property
    def tag_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]

    def __str__(self):
        return self.title

class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='item_images/')
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.item.title}"

class Swap(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requested_swaps')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='swap_requests')
    is_points_swap = models.BooleanField(default=False)
    offered_item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, blank=True, related_name='offered_in_swaps')
    points_offered = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Swap request for {self.item.title} by {self.requester.username}"
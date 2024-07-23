from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    bio = models.TextField(max_length=500,blank=True)
    profile_picture = models.ImageField(upload_to="profile_picture/",blank=True)

    def __str__(self) -> str:
        return f"Profile {self.id}"

def create_profile(sender,instance,created,**kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()

post_save.connect(create_profile,sender=User)
    

class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts/')
    caption = models.TextField(blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User,related_name='likes')
    def __str__(self) -> str:
        return f'Post By {self.user.username}'
    
class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    text =  models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'Comment {self.text[0:30]}'

class Follow(models.Model):
    follower = models.ForeignKey(User,on_delete=models.CASCADE,related_name='following')
    following = models.ForeignKey(User,on_delete=models.CASCADE,related_name='followers')
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Follow by {self.following}"
    
class Like(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='like')
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post','user')

    def __str__(self) -> str:
        return f"{self.user.username} likes {self.post}"
    
# class Stream(models.Model):
#     following = models.ForeignKey(User,on_delete=models.CASCADE,related_name='stream_followers')
#     user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='stream_user')
#     post = models.ForeignKey(Post,on_delete=models.CASCADE)
#     date = models.DateTimeField()

#     def add_post(sender,instance,*args,**kwargs):
#         post = instance
#         user = post.user
#         followers = Follow.objects.all().filter(following=user)
#         for follower in followers:
#             stream = Stream(post=post,user=follower.follower,date=create)



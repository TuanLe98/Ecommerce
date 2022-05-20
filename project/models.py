from django.db import models
from users.models import Profile
import uuid
import datetime

# Create your models here.

class Project(models.Model):
    owner = models.ForeignKey(Profile,on_delete=models.CASCADE,blank=True,null=True)
    title = models.CharField(max_length=200,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    tags = models.ManyToManyField('Tag',blank=True)
    image = models.ImageField(null=True,blank=True,default="user-default.png")
    vote_total = models.IntegerField(default=0,null=True,blank=True)
    vote_ratio = models.IntegerField(default=0,null=True,blank=True)
    demo_link = models.CharField(max_length=2000,null=True,blank=True)
    source_link = models.CharField(max_length=3000,null=True,blank=True)
    time = models.DateTimeField(auto_now_add=True,null=True)
    id = models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False,unique=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = [
            '-vote_ratio','-vote_total','title'
        ]

    @property
    def reviewer(self):
        queryset = self.review_set.all().values_list('owner__id',flat=True)
        return queryset

    @property
    def getVoteCount(self):
        reviews = self.review_set.all()
        upVotes = reviews.filter(value='yes').count()
        totalVotes = reviews.count()

        ratio = (upVotes / totalVotes) * 100
        self.vote_total = totalVotes
        self.vote_ratio = ratio

        self.save()

class Review(models.Model):
    VOTE_TYPE = (
        ('yes','Yes'),
        ('no','No')
    )

    owner = models.ForeignKey(Profile,on_delete=models.CASCADE,null=True)
    project = models.ForeignKey(Project,on_delete=models.CASCADE,null=True)
    body = models.TextField(blank=True,null=True)
    value = models.CharField(max_length=200,choices=VOTE_TYPE)
    time = models.DateTimeField(auto_now_add=True,null=True)
    id = models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False,unique=True)

    def __str__(self):
        return self.value

    class Meta:
        unique_together = [['owner','project']]

class Tag(models.Model):
    name = models.CharField(max_length=200)
    time = models.DateTimeField(auto_now_add=True,null=True)
    id = models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False,unique=True)

    def __str__(self):
        return self.name


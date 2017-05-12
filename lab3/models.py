# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=64, primary_key=True)
    password = models.CharField(max_length=64)
    birthday = models.DateField(blank=True, null=True)
    name = models.CharField(max_length=16)
    address = models.CharField(max_length=128, blank=True, null=True)

    def __unicode__(self):
        return self.name


class Level(models.Model):
    name = models.CharField(max_length=16, unique=True)

    def __unicode__(self):
        return self.name


class Education(models.Model):
    user = models.ForeignKey(User, db_index=True)
    level = models.ForeignKey(Level)
    start_date = models.DateField()
    end_date = models.DateField()

    def __unicode__(self):
        return self.user.name + u"的" + self.level.name + u"教育经历"


class Work(models.Model):
    user = models.ForeignKey(User)
    place = models.CharField(max_length=128)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    job = models.CharField(max_length=32)

    def __unicode__(self):
        return self.user.name + u'的' + self.place + u"教育经历"


class FriendGroup(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=32)

    def __unicode__(self):
        return self.user.name + u'的' + self.name + u'好友分组'


class FriendsRelation(models.Model):
    friend = models.ForeignKey(User)
    group = models.ForeignKey(FriendGroup)

    def __unicode__(self):
        return self.group.user.name + u'的在' + self.group.name + u'好友组里的' + self.friend.name


class Diary(models.Model):
    user = models.ForeignKey(User)
    update_time = models.DateTimeField()
    title = models.CharField(max_length=32)
    content = models.TextField()


class ReplyToDiary(models.Model):
    user = models.ForeignKey(User)
    diary = models.ForeignKey(Diary)
    content = models.CharField(max_length=128)
    date_time = models.DateTimeField()


class ReplyToReply(models.Model):
    user = models.ForeignKey(User)
    reply = models.ForeignKey(ReplyToDiary)
    content = models.CharField(max_length=128)
    date_time = models.DateTimeField()


class Share(models.Model):
    user = models.ForeignKey(User)
    diary = models.ForeignKey(Diary)
    date_time = models.DateTimeField()
    content = models.CharField(max_length=128)




from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models


# from core.models import User


# Create your models here.
class Mail(models.Model):
    ACCEPTED = 'A'
    NOT_ACCEPTED = 'N'
    PENDING = 'P'
    ACCEPTED_CHOICES = (
        (ACCEPTED, 'accepted'),
        (NOT_ACCEPTED, 'not accepted'),
        (PENDING, 'pending'),
    )
    TRANSCRIPT = 'T'
    ATTACHMENT = 'A'
    TYPE_CHOICES = (
        (TRANSCRIPT, 'transcript'),
        (ATTACHMENT, 'attachment'),
    )
    subject = models.CharField(max_length=255, verbose_name='عنوان')
    description = models.TextField(verbose_name='متن')
    reason = models.CharField(max_length=255, verbose_name='بابت')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='ساختن')
    attachment = models.FileField(upload_to='file', verbose_name='پیسوست',null=True,blank=True)
    owner = models.ForeignKey('core.User', on_delete=models.SET_NULL, null=True, related_name='user_mails',
                              verbose_name='صاحب نامه')
    hide_mail = models.ManyToManyField('core.User', related_name='hidden_mail', verbose_name='نامه های مخفی شده')
    is_accepted = models.CharField(choices=ACCEPTED_CHOICES, default=PENDING, max_length=1, verbose_name='نوع')
    type = models.CharField(choices=TYPE_CHOICES, default=ATTACHMENT, verbose_name='نوع')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='اپدیت')
    user = models.ForeignKey('core.User', on_delete=models.SET_NULL, null=True, related_name='users_mail',
                             verbose_name='چه کسی')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    recurring_meeting = GenericForeignKey('content_type', 'object_id')


class Messages(models.Model):
    user = models.ForeignKey('core.User', on_delete=models.SET_NULL, null=True, verbose_name='کاربر',
                             related_name='user_massage')
    description = models.TextField(verbose_name='متن')
    attachment = models.FileField(upload_to='file')
    is_accepted = models.BooleanField()
    mail = models.ForeignKey(Mail, on_delete=models.PROTECT, verbose_name='نامه', related_name='mail_massage')
    unread = models.ManyToManyField('core.User', related_name='user_unread', verbose_name='خوانده نشده')
    meta_data = models.JSONField()


class Financial(models.Model):
    meeting = GenericRelation(Mail)
    origin_card_number = models.CharField(max_length=16, verbose_name='شماره کارت مبدا')
    destination_card_number = models.CharField(max_length=16, verbose_name='شماره کارت مقصد')
    amount = models.PositiveIntegerField()

    # class Meta:
    #     proxy = True


class Marriage(models.Model):
    meeting = GenericRelation(Mail)
    picture_women_id = models.ImageField(upload_to='images', verbose_name='عکس',null=True,blank=True)
    women_name = models.CharField(max_length=255, verbose_name='نام همسر')
    date_marriage = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ازدواج')

    # class Meta:
    #     proxy = True

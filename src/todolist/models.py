from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Work(models.Model):
    name = models.CharField(max_length=50, verbose_name="목록 이름")
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateField(auto_now_add=True)
    modify_date = models.DateField(auto_now=True)
    done = models.BooleanField(default=False, verbose_name="완료 시 선택해주세요")
    description = models.CharField(max_length=50, blank=True, verbose_name="내용")
    deadline = models.DateField(blank=True, null=True, verbose_name="마감 기한")

    def job_done(self):
        return self.done

    job_done.admin_order_field = 'done'
    job_done.boolean = True

    WORK_PRIORITY = (
        ('1', '낮음'),
        ('2', '중간'),
        ('3', '높음'),
    )
    priority = models.CharField(max_length=1, choices=WORK_PRIORITY, default='1', verbose_name="우선 순위")

    class Meta:
        ordering = ['done', '-priority', 'deadline']

    def __str__(self):
        return self.name


class Card(models.Model):
    name = models.CharField(max_length=50, verbose_name="할 일 제목")
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateField(auto_now_add=True)
    modify_date = models.DateField(auto_now=True)
    done = models.BooleanField(default=False, verbose_name="완료 시 선택해주세요")
    description = models.CharField(max_length=50, blank=True, verbose_name="내용")
    work = models.ForeignKey(Work, on_delete=models.CASCADE)
    deadline = models.DateField(blank=True, null=True, verbose_name="마감 기한")

    def job_done(self):
        return self.done

    job_done.admin_order_field = 'done'
    job_done.boolean = True

    CARD_PRIORITY = (
        ('1', '낮음'),
        ('2', '중간'),
        ('3', '높음'),
    )
    priority = models.CharField(max_length=1, choices=CARD_PRIORITY, default='1', verbose_name="우선 순위")

    class Meta:
        ordering = ['done', '-priority', 'deadline']

    def __str__(self):
        return self.name

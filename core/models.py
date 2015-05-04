import random
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.contrib.auth.models import Group, User


def set_staff(sender, instance, **kwargs):
    instance.is_staff = True
pre_save.connect(set_staff, sender=User)

def set_group(sender, instance, **kwargs):
    if kwargs['created']:
        instance.groups.add(Group.objects.get(name="Site Users"))
        instance.save()
post_save.connect(set_group, sender=User)


class QuizAnswer(models.Model):
    question = models.ForeignKey('QuizQuestion')
    text = models.CharField(max_length=256)
    correct = models.BooleanField(default=False)

    def __unicode__(self):
        return self.text[:16]


class QuizQuestion(models.Model):
    quiz = models.ForeignKey('Quiz')
    question = models.CharField(max_length=128)

    @property
    def answers(self):
        return QuizAnswer.objects.filter(question__id=self.id)

    def __unicode__(self):
        return self.question[:16]


class Quiz(models.Model):
    author = models.ForeignKey(User, editable=False)
    title = models.CharField(max_length=32)
    description = models.TextField()

    def get_absolute_url(self):
        return reverse('quiz_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name_plural = "Quizzes"

    @property
    def questions(self):
        return QuizQuestion.objects.filter(quiz__id=self.id)

    def __unicode__(self):
        return self.title

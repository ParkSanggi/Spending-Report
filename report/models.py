from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Day(models.Model):
    DAY_OF_MONTH = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10),
                    (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20),
                    (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28), (29, 29), (30, 30),
                    (31, 31))
    m_day = models.PositiveSmallIntegerField(default=1, choices=DAY_OF_MONTH)

    class Meta:
        ordering = ['m_day']

    def __str__(self):
        return str(self.m_day) + "일"

    def get_absolute_url(self):
        return reverse('report:detail', args=[self.m_day])

class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Event(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='events')
    f_day = models.ForeignKey(Day, on_delete=models.SET_NULL, null=True, related_name='events')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='events')
    description = models.CharField(max_length=50)
    expense = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category.name + str(self.expense)
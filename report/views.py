from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
import calendar

from .models import Day, Category, Event
from .forms import EventForm
from django.utils.safestring import mark_safe

class MayCalendar(calendar.HTMLCalendar):

    user = None

    def formatday(self, day, weekday):

        user = self.user
        t_expense = self.trans_expense(day)
        m_expense = self.meal_expense(day)
        e_expense = self.etc_expense(day)
        total_expense = self.total_expense(day)

        if day == 0:
            return '<td class="%s">&nbsp;</td>' % self.cssclass_noday
        else:
            a = 10000
            test = "{:,}".format(a)
            return '<td class="%s"><a id="day" href="/detail/%d">%d</a>' \
                   '<div id="food">%s</div>' \
                   '<div id="trans">%s</div>' \
                   '<div id="etc">%s</div>' \
                   '<div>%s</div></td>' \
                   % (self.cssclasses[weekday], day, day, m_expense, t_expense, e_expense, total_expense)

    def formatmonthname(self, theyear, themonth, withyear=True):
        """
        Return a month name as a table row.
        """
        if withyear:
            s = '%s %s' % (calendar.month_name[themonth], theyear)
        else:
            s = '%s' % calendar.month_name[themonth]
        return '<tr><th colspan="7" class="%s" id="title">%s</th></tr>' % (
            self.cssclass_month_head, s)

    def total_expense(self, day):
        event_list = Event.objects.filter(author=self.user, f_day=day)
        t_expense = 0
        for event in event_list:
            t_expense += event.expense

        if not event_list:
            t_expense = '&nbsp;'
        return t_expense

    def meal_expense(self, day):
        event_list = Event.objects.filter(f_day=day, category_id=1, author=self.user)
        meal_expense = 0
        for event in event_list:
            meal_expense += event.expense

        if not event_list:
            meal_expense = '&nbsp;'

        return str(meal_expense)

    def trans_expense(self, day):
        event_list = Event.objects.filter(f_day=day, category_id=2, author=self.user)
        trans_expense = 0
        for event in event_list:
            trans_expense += event.expense

        if not event_list:
            print(f'----------------------------{event_list}]')
            trans_expense = '&nbsp;'

        return str(trans_expense)

    def etc_expense(self, day):
        event_list = Event.objects.filter(f_day=day, category_id=3, author=self.user)
        etc_expense = 0
        for event in event_list:
            etc_expense += event.expense

        if not event_list:
            etc_expense = '&nbsp;'

        return str(etc_expense)

def mayCalendar(request):
    mayCal = MayCalendar(calendar.SUNDAY)

    user = request.user
    if user.id == None:
        user = None
    mayCal.user = user

    total_meal = calculate(user, 1)
    total_trans = calculate(user, 2)
    total_etc = calculate(user, 3)

    cal = mayCal.formatmonth(2019,5)

    context = {'object_list': mark_safe(cal),
               'total_meal':total_meal,
               'total_trans': total_trans,
               'total_etc' : total_etc,
               }
    return render(request, 'report/calendar.html', context )

@login_required
def event_create(request, day_number):
    day_info = Day.objects.get(m_day=day_number)
    event_form = EventForm(request.POST)
    event_form.instance.author_id = request.user.id
    event_form.instance.f_day = day_info

    if event_form.is_valid():
        event = event_form.save()

    return redirect(day_info)

@login_required
def event_update(request, event_id):
    event = Event.objects.get(pk=event_id)
    day_info = Day.objects.get(m_day=event.f_day.m_day)

    if request.method == "POST":
        event_form = EventForm(request.POST, instance=event)
        if event_form.is_valid():
            event_form.save()
            return redirect(day_info)
    else:
        event_form = EventForm(instance=event)

    return render(request, 'report/event_update.html', {'event_form': event_form})

@login_required
def event_delete(request, event_id):
    event = Event.objects.get(pk=event_id)
    day_info = Day.objects.get(m_day=event.f_day.m_day)

    if request.method == "POST":
        event.delete()
        return redirect(day_info)
    else:
        return render(request, 'report/event_delete.html', {'event': event})

@login_required
def day_detail(request, day_number):

    if not Day.objects.filter(m_day=day_number):
        day_info = Day()
        day_info.m_day = day_number
        day_info.save()

    day_info = Day.objects.get(m_day=day_number)

    events = Event.objects.filter(author=request.user, f_day=day_info)

    event_form = EventForm()
    return render(request, 'report/day_detail.html', {'day_info': day_info,
                                                   'event_form': event_form,
                                                   'events': events})




def calculate(user, category):

    total = 0
    event_list = Event.objects.filter(author=user, category_id=category)
    for event in event_list:
        total += event.expense

    return total

# def max(user):
#     days = Day.objects.all()
#
#     expense_list = []
#     for day in days:
#         event_list = Event.objects.filter(author=user, f_day=day)
#         total = 0
#         for event in event_list:
#             total += event.expense
#             expense_list.append(total)
#
#     day_number = expense_list.index(max(expense_list))





# def calcul2(user, category):
#
#     def total_expense(self, day):
#         event_list = Event.objects.filter(author=self.user, f_day=day)
#         t_expense = 0
#         for event in event_list:
#             t_expense += event.expense


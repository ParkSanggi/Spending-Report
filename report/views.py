from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
import calendar

from .models import Day, Category, Event
from .forms import EventForm
from django.utils.safestring import mark_safe

class MayCalendar(calendar.HTMLCalendar):

    def formatday(self, day, weekday):

        if day == 0:
            return '<td class="%s">&nbsp;</td>' % self.cssclass_noday
        else:
            a = 10000
            test = "{:,}".format(a)
            return '<td class="%s"><a id="day" href="/detail/%d">%d</a>' \
                   '<div id="food">식비 %s</div>' \
                   '<div id="trans">&nbsp;</div>' \
                   '<div id="etc">기타 10000</div>' \
                   '<div>4</div></td>' \
                   % (self.cssclasses[weekday], day, day, test)

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

def mayCalendar(request):
    mayCal = MayCalendar(calendar.SUNDAY)
    cal = mayCal.formatmonth(2019,5)
    return render(request, 'report/calendar.html', {'object_list': mark_safe(cal)})

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
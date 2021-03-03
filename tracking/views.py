import datetime
import logging
import os
from datetime import timedelta
from shutil import rmtree

from bokeh import palettes
from bokeh.io import output_file, save
from bokeh.models import HoverTool, ColumnDataSource, Legend
from bokeh.plotting import figure
from django import forms
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import render
from django.utils import timezone
from django.utils.timezone import now

from tracking.models import Visitor, Pageview, VisitSummary
from tracking.settings import TRACK_PAGEVIEWS
from . import utils

log = logging.getLogger(__file__)

# tracking wants to accept more formats than default, here they are
input_formats = [
    '%Y-%m-%d %H:%M:%S',  # '2006-10-25 14:30:59'
    '%Y-%m-%d %H:%M',  # '2006-10-25 14:30'
    '%Y-%m-%d',  # '2006-10-25'
    '%Y-%m',  # '2006-10'
    '%Y',  # '2006'
]


class DashboardForm(forms.Form):
    start = forms.DateTimeField(required=False, input_formats=input_formats)
    end = forms.DateTimeField(required=False, input_formats=input_formats)


@permission_required('tracking.visitor_log')
def dashboard(request):
    "Counts, aggregations and more!"
    end_time = now()
    start_time = end_time - timedelta(days=7)
    defaults = {'start': start_time, 'end': end_time}

    form = DashboardForm(data=request.GET or defaults)
    if form.is_valid():
        start_time = form.cleaned_data['start']
        end_time = form.cleaned_data['end']

    # determine when tracking began
    try:
        obj = Visitor.objects.order_by('start_time')[0]
        track_start_time = obj.start_time
    except (IndexError, Visitor.DoesNotExist):
        track_start_time = now()

    # If the start_date is before tracking began, warn about incomplete data
    warn_incomplete = (start_time < track_start_time)

    # queries take `date` objects (for now)
    user_stats = Visitor.objects.user_stats(start_time, end_time)
    visitor_stats = Visitor.objects.stats(start_time, end_time)
    if TRACK_PAGEVIEWS:
        pageview_stats = Pageview.objects.stats(start_time, end_time)
    else:
        pageview_stats = None

    # get the last 100 page visits
    page_visits = Pageview.objects.all().order_by("-view_time")
    if len(page_visits) > 101:
        page_visits = page_visits[:100]

    context = {
        'form': form,
        'track_start_time': track_start_time,
        'warn_incomplete': warn_incomplete,
        'user_stats': user_stats,
        'visitor_stats': visitor_stats,
        'pageview_stats': pageview_stats,
        'page_visits': page_visits,
    }
    context = summarize_data(context)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    target_dir = os.path.join(base_dir, 'templates', 'tracking', 'temp')
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            if "report_temp" in file:
                my_file = "tracking/temp/{}".format(file)

    context["report_path"] = my_file
    return render(request, 'tracking/dashboard.html', context)


@permission_required('tracking.visitor_log')
def user_history(request, user):
    my_user = User.objects.get(pk=user)

    # get the last 100 page visits
    page_visits = Pageview.objects.filter(visitor__user=my_user).order_by("-view_time")

    context = {
        'my_user': my_user,
        'page_visits': page_visits,
    }
    context = summarize_data(context, my_user)
    # print(context)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    target_dir = os.path.join(base_dir, 'templates', 'tracking', 'temp')
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            if "report_temp" in file:
                my_file = "tracking/temp/{}".format(file)

    context["report_path"] = my_file

    return render(request, 'tracking/user_history.html', context)


@permission_required('tracking.visitor_log')
def app_history(request, app):
    page_visits = Pageview.objects.filter(url__icontains=app).order_by("-view_time")
    context = {
        'my_app': app,
        'page_visits': page_visits,
    }
    context = summarize_data(context, None, app)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    target_dir = os.path.join(base_dir, 'templates', 'tracking', 'temp')
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            if "report_temp" in file:
                my_file = "tracking/temp/{}".format(file)

    context["report_path"] = my_file

    return render(request, 'tracking/app_history.html', context)


def summarize_data(context, user=None, app=None):
    # start by chucking all the unsummarized data
    # utils.chunk_pageviews()

    # now build the context variable to pass in
    if not app:
        # get the list of apps
        if not user:
            app_list = [visit["application_name"] for visit in
                        VisitSummary.objects.all().values("application_name").order_by("application_name").distinct()]
        else:
            app_list = [visit["application_name"] for visit in
                        VisitSummary.objects.filter(user=user).values("application_name").order_by("application_name").distinct()]

        app_dict = {}
        final_app_dict = {}
        for app in app_list:
            # create a new file containing data
            if not user:
                result = VisitSummary.objects.filter(application_name=app).values('application_name').order_by(
                    "application_name").distinct().annotate(dsum=Sum('page_visits'))
            else:
                result = VisitSummary.objects.filter(application_name=app, user=user).values('application_name').order_by(
                    "application_name").distinct().annotate(dsum=Sum('page_visits'))
            app_dict[app] = result[0]["dsum"]
        for key, value in sorted(app_dict.items(), key=lambda item: item[1], reverse=True):
            final_app_dict[key] = value
        context["app_dict"] = final_app_dict

        # now for today
        app_dict = {}
        final_app_dict = {}
        for app in app_list:
            # create a new file containing data
            if not user:
                result = VisitSummary.objects.filter(application_name=app, date__year=timezone.now().year, date__month=timezone.now().month,
                                                     date__day=timezone.now().day).values('page_visits').order_by(
                    "page_visits").aggregate(dsum=Sum('page_visits'))
            else:
                result = VisitSummary.objects.filter(application_name=app, user=user, date__year=timezone.now().year,
                                                     date__month=timezone.now().month,
                                                     date__day=timezone.now().day).values('page_visits').order_by(
                    "page_visits").aggregate(dsum=Sum('page_visits'))

            if result["dsum"]:
                app_dict[app] = result["dsum"]

        for key, value in sorted(app_dict.items(), key=lambda item: item[1], reverse=True):
            final_app_dict[key] = value
        context["app_dict_today"] = final_app_dict
        app = None
    else:
        app_list = [app, ]

    if not user and not app:
        # get the list of users
        user_list = [visit["user"] for visit in
                     VisitSummary.objects.all().values("user").order_by("user").distinct()]
        user_dict = {}
        final_user_dict = {}
        for my_user in user_list:
            # create a new file containing data
            result = VisitSummary.objects.filter(user=my_user).values('user').order_by(
                "user").distinct().annotate(dsum=Sum('page_visits'))
            if User.objects.filter(pk=my_user).exists():
                user_dict[User.objects.get(pk=my_user)] = result[0]["dsum"]

        for key, value in sorted(user_dict.items(), key=lambda item: item[1], reverse=True):
            final_user_dict[key] = value

        context["user_dict"] = final_user_dict

        # get the list of users for TODAY
        user_list = [visit["user"] for visit in
                     VisitSummary.objects.all().values("user").order_by("user").distinct()]
        user_dict = {}
        final_user_dict = {}
        for my_user in user_list:
            # create a new file containing data
            result = VisitSummary.objects.filter(user=my_user, date__year=timezone.now().year, date__month=timezone.now().month,
                                                 date__day=timezone.now().day).values('page_visits').order_by(
                "page_visits").distinct().aggregate(dsum=Sum('page_visits'))
            if result["dsum"]:
                user_dict[User.objects.get(pk=my_user)] = result["dsum"]

        for key, value in sorted(user_dict.items(), key=lambda item: item[1], reverse=True):
            final_user_dict[key] = value

        context["user_dict_today"] = final_user_dict

    elif app:
        # get the list of users
        user_list = [visit["user"] for visit in
                     VisitSummary.objects.filter(application_name=app).values("user").order_by("user").distinct()]
        user_dict = {}
        final_user_dict = {}
        for my_user in user_list:
            # create a new file containing data
            result = VisitSummary.objects.filter(user=my_user, application_name=app).values('user').order_by(
                "user").distinct().annotate(dsum=Sum('page_visits'))
            user_dict[User.objects.get(pk=my_user)] = result[0]["dsum"]

        for key, value in sorted(user_dict.items(), key=lambda item: item[1], reverse=True):
            final_user_dict[key] = value

        context["user_dict"] = final_user_dict

    generate_page_visit_report(app_list, user=user, app=app)

    return context


def generate_page_visit_report(app_list, user=None, app=None):
    # start assigning files and by cleaning the temp dir
    base_dir = os.path.dirname(os.path.abspath(__file__))
    target_dir = os.path.join(base_dir, 'templates', 'tracking', 'temp')
    target_file = os.path.join(target_dir, 'report_temp_{}.html'.format(timezone.now().strftime("%H%M%S")))
    # target_file = os.path.join(target_dir, 'report_temp.html')

    calc_total = False if app else True

    try:
        rmtree(target_dir)
    except:
        print("no such dir.")
    os.mkdir(target_dir)

    # output to static HTML file
    output_file(target_file)

    p = figure(
        tools="pan,box_zoom,wheel_zoom,reset,save",
        x_axis_label='Date',
        y_axis_label='Pageviews',
        plot_width=800, plot_height=500,
        x_axis_type="datetime",
        toolbar_location="above",
    )

    # generate color palette
    if len(app_list) <= 2:
        colors = palettes.Set1[3][:len(app_list)]
    elif len(app_list) <= 9:
        colors = palettes.Set1[len(app_list)]
    else:
        # if the app list is too big, let's just take the apps of interest...
        app_list = [
            "project-planning",
            "whalesdb",
            "csas",
            "grais",
            "hermorrhage",
            "diets",
            "inventory",
            # "cruises",
            "travel",
            "ihub",
        ]
        colors = palettes.Set1[len(app_list)]

    # get a list of days
    if not user and not app:
        date_list = [datetime.datetime(date["date"].year, date["date"].month, date["date"].day, 0, 0) for date in VisitSummary.objects.all().values("date").order_by("date").distinct()]
    elif user:
        date_list = [datetime.datetime(date["date"].year, date["date"].month, date["date"].day, 0, 0) for date in VisitSummary.objects.filter(user=user).values("date").order_by("date").distinct()]
    elif app:
        date_list = [datetime.datetime(date["date"].year, date["date"].month, date["date"].day, 0, 0) for date in
                     VisitSummary.objects.filter(application_name=app).values("date").order_by("date").distinct()]
    # prime counter variable
    i = 0
    LEGEND = []
    for app in app_list:
        # create a new file containing data
        if not user:
            qs = VisitSummary.objects.filter(application_name=app).values('date').order_by("date").distinct().annotate(
                dsum=Sum('page_visits'))
        else:
            qs = VisitSummary.objects.filter(application_name=app, user=user).values('date').order_by("date").distinct().annotate(
                dsum=Sum('page_visits'))
        dates = [datetime.datetime(i["date"].year, i["date"].month, i["date"].day, 0, 0) for i in qs]
        counts = [i["dsum"] for i in qs]
        source = ColumnDataSource(data=dict(dates=dates, counts=counts, apps=[app for i in range(0, len(dates))]))
        r0 = p.line('dates', 'counts', line_color=colors[i], line_width=2, source=source)
        r1 = p.circle('dates', 'counts', fill_color=colors[i], line_color=colors[i], size=4, source=source)
        LEGEND.append((app, [r0, r1]))
        i += 1

    legend = Legend(items=LEGEND, location="center")
    p.add_layout(legend, 'right')
    TOOLTIPS = [
        ("Application", "@apps"),
        ("Date", "@dates{%F}"),
        ("Visits", "@counts"),
    ]
    p.add_tools(HoverTool(
        tooltips=TOOLTIPS,
        formatters={
            '@dates': 'datetime',  # use 'datetime' formatter for 'date' field
        },
    ))

    # if calc_total:
    #     total_count = []
    #     for date in date_list:
    #         # create a new file containing data
    #         if not user:
    #             result = VisitSummary.objects.filter(date=date).values('date').order_by("date").distinct().annotate(dsum=Sum('page_visits'))
    #         else:
    #             result = VisitSummary.objects.filter(date=date, user=user).values('date').order_by("date").distinct().annotate(
    #                 dsum=Sum('page_visits'))
    #         total_count.append(result[0]["dsum"])
    #
    #     p.line(date_list, total_count, legend_label="total", line_color='black', line_width=1, line_dash=[6, 3])
    #     p.circle(date_list, total_count, legend_label="total", fill_color='black', line_color="black", size=1)
    #     p.legend.location = "top_left"

    save(p)

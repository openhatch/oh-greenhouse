from collections import defaultdict, OrderedDict
from datetime import timedelta
import re

from django.contrib import messages, comments
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.admin.models import LogEntry, ADDITION
from django.contrib.contenttypes.models import ContentType
from django.contrib.comments import Comment
from django.contrib.comments.signals import comment_was_posted
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.dispatch import receiver
from django.utils import timezone
from django.db.models import Q, Max, Min, Count

from distro_info import UbuntuDistroInfo
from generic_aggregation import generic_annotate

from greenhouse.decorators import group_perm_required
from greenhouse.models import Activity, Person, UserProfile
from greenhouse.forms import NotesForm, EditContrib


def months(months):
    return timezone.now() - timedelta(days=months*30)


def group(type):
    NUM_UPLOADS_EXPERIENCED = 40
    filtered = Person.objects.filter(control_group=False).filter(
        exclude=False).filter(authoritative_person=None)
    base = filtered.annotate(latest=Max('activities__time')).annotate(
        earliest=Min('activities__time')).annotate(total=Count('activities'))
    active = base.filter(latest__gte=months(4))
    types = {
        'first_timers': base,
        'experienced': active.filter(total__gte=NUM_UPLOADS_EXPERIENCED),
        'inactive': base.filter(total__gte=5).filter(
            latest__gt=months(12)).filter(latest__lt=months(2)),
        'potential': active.filter(total__gte=NUM_UPLOADS_EXPERIENCED
                        ).filter(earliest__lte=months(6)),
        'recent': base.filter(latest__gte=months(2)),
        }
    return types[type]


def suggestions(email):
    person = Person.objects.get(email=email, authoritative_person=None)
    earliest_action = person.activities.order_by('-time')[0].time
    latest_action = person.activities.latest('time').time
    total_uploads = person.activities.count()
    if not person.exclude and earliest_action > months(3):
        return 'This new contributor has not been contacted, \
        you should contact him/her, \
        <a href="https://wiki.debian.org/GreeetingForNewContributors" \
        target="_blank">click here for sample email templates</a>'
    if not person.exclude and latest_action > months(4) and total_uploads > 40:
        return 'Suggest a new package for this person to work on'
    if latest_action > months(12) and latest_action < months(2):
        return 'This person is inactive'
    if (not person.exclude and latest_action > months(12) and
            total_uploads > 40 and earliest_action <= months(6)):
        return 'This person should apply for Debian Developer status'
    else:
        return 'This person does not fall under any of the categories'


@group_perm_required()
def person_detail(request, email):
    person = get_object_or_404(Person, email=email, authoritative_person=None)
    contributors = get_list_or_404(Person, authoritative_person=None)
    activities = Activity.objects.filter(person=person)
    recent_uploads = activities.order_by('-time')[0:10]
    ppu_candidates = get_ppu_candidates(activities)
    if request.method == 'POST':
        if 'save_notes' in request.POST:
            notes_form = NotesForm(request.POST)
            if notes_form.is_valid():
                person.notes = notes_form.cleaned_data['notes']
                person.save()
                change_message = "Updated %s's whiteboard." % person.name
                log_action(person, change_message, request.user.pk)
                messages.success(request, 'Change successfully saved...')
                return HttpResponseRedirect('#')
    else:
        notes_form = NotesForm(initial={'notes': person.notes})

    return render(request, 'greenhouse/person.html', {'person': person,
                                           'recent_uploads': recent_uploads,
                                           'ppu_candidates': ppu_candidates,
                                           'notes_form': notes_form,
                                           'contributor_list': contributors,
                                           'suggestion': suggestions(email),
                                           })


def get_ppu_candidates(uploads):
    """
    Takes an Activity object filtered by email_changer and returns
    a list of package that were uploaded by a contributor more than
    five times.
    """
    packages = uploads.values_list('subproject', flat=True)
    ppu_candidates = []
    appearances = defaultdict(int)
    for curr in packages:
        appearances[curr] += 1
    for pkg in appearances:
        if appearances[pkg] > 5:
            ppu_candidates += [pkg]
    return ppu_candidates


def get_uploads_per_release(email):
    """
    Takes an email and returns an ordered dict of uploads per release.
    """
    uploads_per_release = OrderedDict([])
    person = get_object_or_404(Person, email=email, authoritative_person=None)
    for d in UbuntuDistroInfo().all:
        release_uploads = len(Activity.objects.filter(
            person=person).filter(release__icontains=d))
        if uploads_per_release or release_uploads > 0:
            uploads_per_release[d] = release_uploads
    return uploads_per_release


@group_perm_required()
def edit_person(request, email):
    person = get_object_or_404(Person, email=email)
    if request.method == 'POST':
        person_form = EditContrib(request.POST)
        if person_form.is_valid():
            new_email = person_form.cleaned_data['email']
            person.email = person_form.cleaned_data['email']
            person.email = new_email
            person.save()
            if email is not new_email:
                activities = Activity.objects.filter(email_changer=email)
                activities.update(person__email=new_email)
            change_message = "Updated %s's details." % person.name
            log_action(person, change_message, request.user.pk)
            messages.success(request, 'Change successfully saved...')
            return HttpResponseRedirect('/contributors/{}'.format(new_email))
    else:
        person_form = EditContrib(initial={'email': email,
                                           'email': person.email})
    return render(request, 'greenhouse/edit_person.html', {'person': person,
                                                'person_form': person_form})


def contacted(request, email):
    if request.POST:
        p = Person.objects.get(email=email)
        p.contacted = not p.contacted
        p.save()
        return HttpResponseRedirect('/contributors/potential_devs')


def log_action(object, change_message, user):
    LogEntry.objects.log_action(
        user_id=user,
        content_type_id=ContentType.objects.get_for_model(object).pk,
        object_id=object.pk,
        object_repr=object.email,
        change_message=change_message,
        action_flag=ADDITION
    )


@group_perm_required()
def user_profile(request, user):
    profile = User.objects.get(username=user).profile
    actions = LogEntry.objects.filter(user_id=profile.user_id)
    edited_contribs = actions.order_by('object_repr').values_list(
        "object_repr", flat=True).distinct()
    return render(request, 'greenhouse/user_profile.html',
                  {'profile': profile,
                   'edited_contribs': edited_contribs})


def site_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully...')
    return HttpResponseRedirect('/')


def access_denied(request, redirect):
    messages.error(request, """
        You do not have the correct permissions to view that page...
        """)
    return HttpResponseRedirect(redirect)


def index(request):
    return render(request, 'greenhouse/index.html', dashboard(request))


def dashboard(request):
    MAX_PPL_IN_VIEW = 5
    first_timers = []
    experienced = []
    inactive = []
    contacted_filter = set()

    first_timers_qs = group('first_timers').select_related(
        'contacts').order_by('-latest')
    experienced_qs = group('experienced').select_related(
        'contacts').order_by('-latest')
    inactive_qs = group('inactive').select_related(
        'contacts').order_by('-latest')
    actions = LogEntry.objects.filter(user_id=request.user.id)
    contacted_qs = Comment.objects.for_model(Person).order_by('submit_date')

    for p in first_timers_qs:
        if len(first_timers) < MAX_PPL_IN_VIEW and not p.contacts.all():
            first_timers.append(p)
    for p in experienced_qs:
        if p.contacts.all(): 
            recent_c = p.contacts.all().reverse()[0].submit_date
        else:
            recent_c = None
        # The query is to get the time the person did their 40th upload and 
        # if they were contacted since
        time_40th = Activity.objects.filter(person__email=p.email).order_by("time")[39].time
        if len(experienced) < MAX_PPL_IN_VIEW and (recent_c is None or recent_c < time_40th):
            experienced.append(p)
    for p in inactive_qs:
        if p.contacts.all():
            recent_c = p.contacts.all().reverse()[0].submit_date
        else:
            recent_c = None
        if len(inactive) < MAX_PPL_IN_VIEW and (recent_c is None or 
            recent_c < Activity.objects.prefetch_related('person'
            ).filter(person__email=p.email).latest('time').time):
            inactive.append(p)
    for c in contacted_qs:
        if len(contacted_filter) < MAX_PPL_IN_VIEW:
            contacted_filter.add(c.object_pk)
    query = Q()
    for object_pk in contacted_filter:
        query |= Q(id=object_pk)
    contacted = Person.objects.filter(query) if query else []
    return {'first_timers': first_timers,
            'experienced': experienced,
            'inactive': inactive,
            'contacted': contacted,
            'actions': actions,
            }


@receiver(comment_was_posted)
def on_contact_saved(sender, comment=None, request=None, **kwargs):
    person = Person.objects.get(pk=comment.object_pk)
    change_message = "Recorded a contact with %s." % person.name
    log_action(person, change_message, comment.user.pk)
    messages.success(request, 'Change successfully saved...')


def delete_comment(request, email, comment_id):
    if request.POST:
        comment = get_object_or_404(comments.get_model(), id=comment_id)
        comment.delete()
        msg = "Successfully deleted contact"
        messages.success(request, msg)
        return HttpResponseRedirect(reverse('person_detail', args=(email,)))


def unify_identities(request):
    if request.POST:
        merge_from_email = request.POST["merge_from"]
        merge_into_data = request.POST["merge_into"]
        merge_into_email = re.search(r"<(.*)>", merge_into_data).groups()[0]
        merge_from = Person.objects.get(email=merge_from_email,
                                        authoritative_person=None)
        merge_into = Person.objects.get(email=merge_into_email,
                                        authoritative=None)
        merge_from.merge(merge_into)
        msg = ' '.join(["Successful unification of", merge_from_email,
                        "into", merge_into_email])
        messages.success(request, msg)
        return HttpResponseRedirect(reverse('person_detail',
                                            args=(merge_into_email,)))

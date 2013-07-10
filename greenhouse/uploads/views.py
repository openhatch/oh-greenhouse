from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from collections import defaultdict
from datetime import timedelta
from distro_info import UbuntuDistroInfo
from collections import OrderedDict
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.admin.models import LogEntry, ADDITION
from django.contrib.contenttypes.models import ContentType

from uploads.decorators import group_perm_required
from uploads.models import Uploads, People, UserProfile
from django.contrib.auth.models import User
from uploads.forms import NotesForm, EditContrib

from django.dispatch import receiver
from django.contrib.comments.signals import comment_was_posted


@group_perm_required()
def first_timers(request):
    output = []
    for p in People.objects.all().prefetch_related("first_upload"
                                ).prefetch_related("last_upload"):
        if p.total_uploads < 5:
            color = "lt5"
        if p.total_uploads >= 5 and p.total_uploads < 10:
            color = "gt5"
        if p.total_uploads >= 10 and p.total_uploads < 20:
            color = "gt10"
        if p.total_uploads >= 20 and p.total_uploads < 50:
            color = "gt20"
        if p.total_uploads >= 50:
            color = "gt50"
        ul_info = {'p': p,
                   'color': color}
        output.append(ul_info)
    return render(request, 'first_timers.html', {'output': output})


@group_perm_required()
def person_detail(request, email):
    person = get_object_or_404(People, email=email)
    uploads = Uploads.objects.filter(email_changer=email)
    recent_uploads = uploads.order_by('timestamp').reverse()[0:10]
    #uploads_per_release = get_uploads_per_release(email)
    ppu_candidates = get_ppu_candidates(uploads)
    if request.method == 'POST':
        if 'save_notes' in request.POST:
            notes_form = NotesForm(request.POST)
            #contacted = BooleanForm(initial={'checkbox': person.contacted})
            if notes_form.is_valid():
                person.notes = notes_form.cleaned_data['notes']
                person.save()
                change_message = "Updated %s's whiteboard." % person.name
                log_action(person, change_message, request.user.pk)
                messages.success(request, 'Change successfully saved...')
                return HttpResponseRedirect('#')
    else:
        notes_form = NotesForm(initial={'notes': person.notes})
    return render(request, 'person.html', {'person': person,
                                           'recent_uploads': recent_uploads,
                                           'ppu_candidates': ppu_candidates,
                                           'notes_form': notes_form,
                                           })
#                                           'uploads_per_release':
#                                                uploads_per_release})


def get_ppu_candidates(uploads):
    """
    Takes an Uploads object filtered by email_changer and returns
    a list of package that were uploaded by a contributor more than
    five times.
    """
    packages = uploads.values_list('package', flat=True)
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
    for d in UbuntuDistroInfo().all:
        release_uploads = len(Uploads.objects.filter(
            email_changer=email).filter(release__icontains=d))
        if uploads_per_release or release_uploads > 0:
            uploads_per_release[d] = release_uploads
    return uploads_per_release


@group_perm_required()
def edit_person(request, email):
    person = get_object_or_404(People, email=email)
    if request.method == 'POST':
        person_form = EditContrib(request.POST)
        if person_form.is_valid():
            new_email = person_form.cleaned_data['email']
            person.email = person_form.cleaned_data['email']
            person.email = new_email
            person.save()
            if email is not new_email:
                uploads = Uploads.objects.filter(email_changer=email)
                uploads.update(email_changer=new_email)
            change_message = "Updated %s's details." % person.name
            log_action(person, change_message, request.user.pk)
            messages.success(request, 'Change successfully saved...')
            return HttpResponseRedirect('/contributors/{}'.format(new_email))
    else:
        person_form = EditContrib(initial={'email': email,
                                           'email': person.email})
    return render(request, 'edit_person.html', {'person': person,
                                                'person_form': person_form})


@group_perm_required()
def recent_contributors(request):
    recent_contributors = []
    cutoff_date = timezone.now() - timedelta(days=2 * 30)
    for p in People.objects.all().prefetch_related("last_upload"):
        if p.last_upload.timestamp > cutoff_date:
            recent_contributors += [p]
    return render(request, 'recent_contributors.html',
                  {'recent_contributors': recent_contributors})


@group_perm_required()
def lost_contributors(request):
    lost_contributors = []
    one_year = timezone.now() - timedelta(days=365)
    two_months = timezone.now() - timedelta(days=2 * 30)
    for p in People.objects.all().prefetch_related('last_upload'):
        ul_date = p.last_upload.timestamp
        if  ul_date > one_year and ul_date < two_months:
            lost_contributors += [p]
    return render(request, 'lost_contributors.html',
                  {'lost_contributors': lost_contributors})


@group_perm_required()
def potential_devs(request):
    potential_devs = []
    cutoff_upload = {}
    six_months = timezone.now() - timedelta(days=6 * 30)
    for p in People.objects.filter(ubuntu_dev=False
                          ).filter(total_uploads__gte=40
                          ).filter(is_active=True
                          ).prefetch_related("first_upload"
                          ).prefetch_related("last_upload"
                          ).filter(first_upload__timestamp__lte=six_months):
            uploads = Uploads.objects.filter(email_changer=p.email)
            #p.fortieth = uploads.order_by("timestamp")[39].timestamp
            potential_devs += [p]
    return render(request, 'potential_devs.html',
                  {'potential_devs': potential_devs,
                  'cutoff_upload': cutoff_upload})
    
def contacted(request, email):
    if request.POST:
        p = People.objects.get(email=email)
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
    edited_contribs = actions.order_by('object_repr'
                            ).values_list("object_repr",
                                          flat=True).distinct()
    return render(request, 'user_profile.html', {'profile': profile,
                                                 'actions': actions,
                                                 'edited_contribs':
                                                      edited_contribs})


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
    return render(request, 'index.html', dashboard())


def dashboard():
    first_timers = []
    experienced = []
    inactive = []
    three_months = timezone.now() - timedelta(days=3 * 30)
    two_months = timezone.now() - timedelta(days=2 * 30)
    six_months = timezone.now() - timedelta(days=6 * 30)
    one_year = timezone.now() - timedelta(days=365)
    people = People.objects.all().prefetch_related("first_upload"
                                ).prefetch_related("last_upload"
                                ).select_related('contacts'
                                ).order_by('last_upload__timestamp').reverse()
    first_timers_qs = people.filter(first_upload__timestamp__gte=three_months)
    experienced_qs = people.filter(ubuntu_dev=False
                          ).filter(total_uploads__gte=40
                          ).filter(is_active=True)
    inactive_qs = people.filter(last_upload__timestamp__gt=one_year
                       ).filter(last_upload__timestamp__lt=two_months
                       ).filter(total_uploads__gte=5)
    for p in first_timers_qs:
        if (len(first_timers) < 20 and not p.contacts.all()):
            first_timers.append(p)
    for p in experienced_qs:
        if p.contacts.all():
            recent_c = p.contacts.all().reverse()[0].submit_date
        else:
            recent_c = None
        if (len(experienced) < 20 and (recent_c is None or
            recent_c < Uploads.objects.filter(email_changer=p.email
                                     ).order_by("timestamp"
                                     )[39].timestamp)):
            experienced.append(p)
    for p in inactive_qs:
        if p.contacts.all():
            recent_c = p.contacts.all().reverse()[0].submit_date
        else:
            recent_c = None
        if len(inactive) < 20 and (recent_c is None or
            recent_c < p.last_upload.timestamp):
                inactive.append(p)
    return {'first_timers': first_timers,
            'experienced': experienced,
            'inactive': inactive}


@receiver(comment_was_posted)
def on_contact_saved(sender, comment=None, request=None, **kwargs):
    person = People.objects.get(pk=comment.object_pk)
    change_message = "Recorded a contact with %s." % person.name
    log_action(person, change_message, comment.user.pk)
    messages.success(request, 'Change successfully saved...')
    

        
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import UpdateView, TemplateView, CreateView

from pegasus_app.forms import PhoneNumberCheckConfigForm, ScheduleDayForm, ScheduleDayFormset
from pegasus_app.models import ScheduleDay, PhoneNumberCheckConfig


class PhoneNumberCheckConfigCreateView(CreateView):
    model = PhoneNumberCheckConfig
    template_name = 'phone_create.html'
    form_class = PhoneNumberCheckConfigForm
    object = None

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        weekday_formset = ScheduleDayFormset()
        return self.render_to_response(
                  self.get_context_data(phone_form=form,
                                        weekday_formset=weekday_formset,
                                        )
                                     )

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        assignment_question_form = AssignmentQuestionFormSet(self.request.POST)
        if form.is_valid() and assignment_question_form.is_valid():
            return self.form_valid(form, assignment_question_form)
        else:
            return self.form_invalid(form, assignment_question_form)

    def form_valid(self, form, assignment_question_form):
        """
        Called if all forms are valid. Creates Assignment instance along with the
        associated AssignmentQuestion instances then redirects to success url
        Args:
            form: Assignment Form
            assignment_question_form: Assignment Question Form

        Returns: an HttpResponse to success url

        """
        self.object = form.save(commit=False)
        # pre-processing for Assignment instance here...
        self.object.save()

        # saving AssignmentQuestion Instances
        assignment_questions = assignment_question_form.save(commit=False)
        for aq in assignment_questions:
            #  change the AssignmentQuestion instance values here
            #  aq.some_field = some_value
            aq.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, assignment_question_form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.

        Args:
            form: Assignment Form
            assignment_question_form: Assignment Question Form
        """
        return self.render_to_response(
                 self.get_context_data(form=form,
                                       assignment_question_form=assignment_question_form
                                       )
        )


def get_schedule_day_form(phone_config, weekday):
    schedule_day = ScheduleDay.objects.filter(phone_config=phone_config,day=weekday).first()

    return ScheduleDayForm(instance=schedule_day, prefix=weekday)


def validate_and_save_schedule_day_form(payload, phone_config, weekday):
    schedule_day_form = ScheduleDayForm(payload, prefix=weekday)
    if schedule_day_form.is_valid():
        ScheduleDay.objects.update_or_create(
            phone_config=phone_config,
            day=weekday,
            defaults=schedule_day_form.cleaned_data
        )
    return schedule_day_form


def schedule_form_handler(request, phone_config, weekday):
    if request.method == 'GET':
        schedule_day = ScheduleDay.objects.filter(phone_config=phone_config, day=weekday).first()
        schedule_day_form = ScheduleDayForm(instance=schedule_day, prefix=weekday)
    elif request.method == 'POST':
        # import ipdb; ipdb.set_trace()
        schedule_day_form = ScheduleDayForm(request.POST, prefix=weekday)
        if schedule_day_form.is_valid():
            if schedule_day_form.cleaned_data['is_active']:
                ScheduleDay.objects.update_or_create(
                    phone_config=phone_config,
                    day=weekday,
                    defaults=schedule_day_form.cleaned_data
                )
            # else:
            #     ScheduleDay.objects.update_or_create(
            #         phone_config=phone_config,
            #         day=weekday,
            #         defaults={
            #             'open_time': None,
            #             'close_time': None,
            #         }
            #     )
    return schedule_day_form


def change_config_number(request, id):
    phone_config = PhoneNumberCheckConfig.objects.get(id=id)
    if request.method == 'GET':
        schedule_day_formset = ScheduleDayFormset(phone_config=phone_config,)

        #
        # schedule_monday_form = get_schedule_day_form(phone_config, ScheduleDay.ScheduleDayType.MONDAY)
        # schedule_tuesday_form = get_schedule_day_form(phone_config, ScheduleDay.ScheduleDayType.TUESDAY)
        # schedule_wednesday_form = get_schedule_day_form(phone_config, ScheduleDay.ScheduleDayType.WEDNESDAY)
        # schedule_thursday_form = ScheduleDayForm(instance=schedule_thursday, prefix='thursday')
        # schedule_friday_form = ScheduleDayForm(instance=schedule_friday, prefix='friday')
        # schedule_saturday_form = ScheduleDayForm(instance=schedule_saturday, prefix='saturday')
        # schedule_sunday_form = ScheduleDayForm(instance=schedule_sunday, prefix='sunday')

    elif request.method == 'POST':

        phone_config_form = PhoneNumberCheckConfigForm(request.POST)
        if phone_config_form.is_valid():
            PhoneNumberCheckConfig.objects.update_or_create(id=id, defaults={
                'ima_name': phone_config_form.cleaned_data['ima_name'],
                'phone': phone_config_form.cleaned_data['phone'],
                'failure_threshold': phone_config_form.cleaned_data['failure_threshold'],
                'test_frequency': phone_config_form.cleaned_data['test_frequency']
            })

        # schedule_monday_form = validate_and_save_schedule_day_form(
        #     request.POST, phone_config, ScheduleDay.ScheduleDayType.MONDAY
        # )
        # ...

    context = {
        'phone_config_form': phone_config_form,
        'schedule_day_formset': schedule_day_formset
        # 'schedule_tuesday_form': schedule_form_handler(request, phone_config, ScheduleDay.ScheduleDayType.TUESDAY),
        # 'schedule_wednesday_form': schedule_form_handler(request, phone_config, ScheduleDay.ScheduleDayType.WEDNESDAY),
        # 'schedule_thursday_form': schedule_form_handler(request, phone_config, ScheduleDay.ScheduleDayType.THURSDAY),
        # 'schedule_friday_form': schedule_form_handler(request, phone_config, ScheduleDay.ScheduleDayType.FRIDAY),
        # 'schedule_saturday_form': schedule_form_handler(request, phone_config, ScheduleDay.ScheduleDayType.SATURDAY),
        # 'schedule_sunday_form': schedule_form_handler(request, phone_config, ScheduleDay.ScheduleDayType.SUNDAY)

    }

    return render(request, 'pegasus_app/change_number.html', context)


def home_page(request):
    phone_config_form = PhoneNumberCheckConfigForm()
    phone = PhoneNumberCheckConfig.objects.values('phone')
    schedule_formset = ScheduleDayFormset()
    if request.method == 'POST':
        # import ipdb; ipdb.set_trace()
        phone_config_form = PhoneNumberCheckConfigForm(request.POST)
        schedule_formset = ScheduleDayFormset(request.POST)
        if phone_config_form.is_valid():
            phone_config = phone_config_form.save(commit=False)
            phone_config.user_plan = request.user.plan
            phone_config.save()
            for form in schedule_formset:
                if form.is_valid():
                    form.cleaned_data['phone_config'] = phone_config
                    schedule_day = ScheduleDay.objects.create(**form.cleaned_data)


    print(request.POST)

    context = {
        'phone': phone,
        'phone_config_form': phone_config_form,
        'schedule_formset': schedule_formset
    }

    return render(request, 'pegasus_app/main.html', context)


class Phone(TemplateView):
    template_name = "temp.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        phone_number = PhoneNumberCheckConfig.objects.first()
        phone_number_form = PhoneNumberCheckConfigForm(instance=phone_number)
        context['phone_number_form'] = phone_number_form

        schedule_formset = ScheduleDayFormset(instance=phone_number)
        context['schedule_formset'] = schedule_formset

        return context

    def post(self, request, id):
        phone_number = PhoneNumberCheckConfig.objects.get(id=id)
        # import ipdb; ipdb.set_trace()
        phone_number_form = PhoneNumberCheckConfigForm(instance=phone_number, data=request.POST)
        if phone_number_form.is_valid():
            phone_number_form.save()

        formset = ScheduleDayFormset(request.POST, instance=phone_number)
        if formset.is_valid():
            formset.save()

        redirect_url = reverse('phone', args='1')
        return HttpResponseRedirect(redirect_url)

def manage_books(request, author_id):
    author = Author.objects.get(pk=author_id)
    BookInlineFormSet = inlineformset_factory(Author, Book, fields=('title',))
    if request.method == "POST":
        formset = BookInlineFormSet(request.POST, request.FILES, instance=author)
        if formset.is_valid():
            formset.save()
            # Do something. Should generally end with a redirect. For example:
            return HttpResponseRedirect(author.get_absolute_url())
    else:
        formset = BookInlineFormSet(instance=author)
    return render(request, 'manage_books.html', {'formset': formset})

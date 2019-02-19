from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.views.generic.edit import BaseCreateView, BaseUpdateView, BaseDetailView
from django.views.generic import View, ListView, CreateView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.base import ContextMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse


from polls.models import Survey, Response, Product
from users.models import User, Profile
from polls.forms import SurveyForm, ResponseForm

def survey_list(request):
    return render(request, 'polls/survey_list.html')


class IncludeModelCreateUrlMixin:
    """ Adds the model's create URL in the view's context. Used for CRUD views """
    @property
    def _model_name(self):
        """ returns model name as a lower case string"""
        return str(self.model.__name__).lower()

    @property
    def model_url(self):
        """ returns model create url view name """
        return f'polls:create_{self._model_name}'

    def get_context_data(self, **kwargs):
        """ include model's "create URL" in context """
        context = super().get_context_data(**kwargs)
        context['model_create_url'] = self.model_url
        return context


class BaseListCustom(LoginRequiredMixin, IncludeModelCreateUrlMixin, ListView):
    """ Base View Class to list objects with FK to User model"""

    @property
    def _custom_qs(self):
        """ returns model's QS filtered down to the User being viewed """
        return self.model.objects.filter(user=self.request.user)

    def get_queryset(self):
        return self._custom_qs


# Base View classes to implement modal-based CRUD
class JsonResponseMixin:
    """ Mixin that enables responses as JSON that suits the structure in my templates """

    @property
    def partial_table_template(self):
        """
        default template where the data is rendered as a table. default behavior is using the model's name
        as lowercase
        """
        model_name = str(self.model.__name__)
        return f'polls/includes/{model_name.lower()}/partial_table.html'

    def process_valid_form(self, object_list):
        """ Render table with new object created and return in json"""
        data = dict()
        data['form_is_valid'] = True
        data['html_data'] = render_to_string(self.partial_table_template,
                                             context={'object_list': object_list})
        return JsonResponse(data)

    def process_invalid_form(self, context):
        data = dict()
        data['form_is_valid'] = False
        data['html_form'] = render_to_string(self.form_template, context)
        return JsonResponse(data)


class BaseCreateCustom(LoginRequiredMixin, IncludeModelCreateUrlMixin, JsonResponseMixin, BaseCreateView):
    """ Base Class to create objects that have a FK to the User model"""
    form_template = 'polls/includes/partial_create.html'

    def form_valid(self, form):
        """ Render table with new object created and return in json"""
        print('valid form')
        form.instance.user = self.request.user
        form.save()
        object_list = self.model.objects.filter(user=self.request.user)
        return self.process_valid_form(object_list)

    def form_invalid(self, form):
        context = {'form': form}
        return self.process_invalid_form(context)

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        context = {'form': form, 'model_create_url': self.model_url}
        data = dict()
        data['html_form'] = render_to_string(self.form_template, context, request)
        return JsonResponse(data)


class BaseUpdateCustom(LoginRequiredMixin, JsonResponseMixin, BaseUpdateView):
    """ Base Class to update objects that have a FK to the User model"""
    form_template = 'polls/includes/partial_update.html'

    def form_valid(self, form):
        """ Render table with updated object and return in json"""
        form.save()
        object_list = self.model.objects.filter(user=self.object.user)
        return self.process_valid_form(object_list)

    def form_invalid(self, form):
        context = {'form': form}
        return self.process_invalid_form(context)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        form.instance = self.object
        context = {'form': form}
        data = dict()
        data['html_form'] = render_to_string(self.form_template, context, request)
        return JsonResponse(data)


class BaseDeleteCustom(LoginRequiredMixin, JsonResponseMixin, SingleObjectMixin, ContextMixin, View):
    """ Base class to delete objects with FK to User model """
    form_template = 'polls/includes/partial_delete.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        data = dict()
        context = {'object': self.object}
        data['html_form'] = render_to_string(self.form_template, context, request=request)
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        object_list = self.model.objects.filter(user=self.object.user)
        self.object.delete()
        data = dict()
        data['form_is_valid'] = True
        data['html_data'] = render_to_string(self.partial_table_template,
                                             context={'object_list': object_list})
        return JsonResponse(data)

class ListSurvey(BaseListCustom):
    """ For surveyors """
    model = Survey
    template_name = 'polls/survey_list.html'


class ChooseSurvey(LoginRequiredMixin, ListView):
    """ For respondents """
    model = Survey
    template_name = 'polls/choose_survey.html'

class CreateSurvey(BaseCreateCustom):
    model = Survey
    form_class = SurveyForm

    def get_form(self, form_class):
        return form_class(self.request.user, self.request.POST)


class UpdateSurvey(BaseUpdateCustom):
    model = Survey
    form_class = SurveyForm


class DeleteSurvey(BaseDeleteCustom):
    model = Survey
    form_class = SurveyForm

@login_required
def respond_survey(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    response = Response.objects.create(user=request.user, survey=survey)
    form = ResponseForm(request.POST or None, instance=response)
    if request.method == 'POST':
        if form.is_valid():
            print('valid')
            form.save()
            return HttpResponseRedirect(response.survey.get_success_url())
        else:
            print('form invalid')

    context = {'form': form, 'survey': survey}
    return render(request, 'polls/respond_survey.html', context)

@login_required
def thankyou(request, survey_id):
    return render(request, 'polls/thankyou.html')


class ResponseList(LoginRequiredMixin, ListView):
    """ List responses to a survey"""
    model = Response
    template_name = 'response_list.html'

    def get_queryset(self):
        survey_id = self.kwargs['survey_id']
        self.survey = Survey.objects.get(pk=survey_id)
        return self.survey.responses.all()

class ResponseDetail(DetailView):
    model = Response

class ListProduct(BaseListCustom):
    model = Product
    template_name = 'product_list.html'

# Product CRUD
class CreateProduct(BaseCreateCustom):
    model = Product
    fields = ('name', 'description')

class UpdateProduct(BaseUpdateCustom):
    model = Product
    fields = ('name', 'description')

class DeleteProduct(BaseDeleteCustom):
    model = Product

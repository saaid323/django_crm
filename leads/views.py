from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from .models import Lead, Agent, Category
from .forms import LeadForm, CustomUserCreationForm, AssignAgentForm, LeadCategoryForm
from django.views import generic
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from agents.mixins import OrganisorAndLoginRequiredMixin
# Create your views here.


class SignupView(generic.CreateView):
    template_name = 'registration/signup.html'
    form_class = CustomUserCreationForm

    def get_success_url(self) -> str:
        return reverse("login")


class LeadListView(LoginRequiredMixin, generic.ListView):
    template_name = 'leads/lead_list.html'
    context_object_name = 'leads'

    def get_queryset(self):
        user = self.request.user
        
        if user.is_organiser:
            queryset = Lead.objects.filter(organisation=user.userprofile, agent__isnull=False)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation, agent__isnull=False)
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(LeadListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organiser:
            queryset = Lead.objects.filter(organisation=user.userprofile, agent__isnull=True)
            context.update({
                "unassigned_leads": queryset
            })
        return context


class AssignAgentView(LoginRequiredMixin, generic.FormView):
    template_name = 'leads/assign_agent.html'
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({'request': self.request})
        return kwargs

    def get_success_url(self) -> str:
        return reverse("lead_list")
    
    def form_valid(self, form):
        lead = Lead.objects.get(id=self.kwargs['pk'])
        agent = form.cleaned_data['agent']
        lead.agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)
    
class CategoryListView(LoginRequiredMixin, generic.ListView):
    template_name = 'leads/category_list.html'
    context_object_name = 'categorys'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        if user.is_organiser:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
        
        context.update({
            'unassigned_lead_count': queryset.filter(category__isnull=True).count()
        })
        return context

    def get_queryset(self):
        user = self.request.user
        
        if user.is_organiser:
            queryset = Category.objects.filter(organisation=user.userprofile)
        else:
            queryset = Category.objects.filter(organisation=user.agent.organisation)
        return queryset



class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "leads/category_detail.html"
    context_object_name = 'categorys'

    def get_queryset(self):
        user = self.request.user

        if user.is_organiser:
            queryset = Category.objects.filter(organisation=user.userprofile)
        else:
            queryset = Category.objects.filter(organisation=user.agent.organisation)
        return queryset


class LeadCategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'leads/category_update.html'
    form_class = LeadCategoryForm

    def get_queryset(self):
        user = self.request.user
        
        if user.is_organiser:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_success_url(self):
        return reverse('lead_detail', kwargs={"pk": self.get_object().id})



class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'leads/lead_detail.html'
    context_object_name = 'lead'

    def get_queryset(self):
        user = self.request.user
        
        if user.is_organiser:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            queryset = queryset.filter(agent__user=user)
        return queryset


class LeadCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    template_name = 'leads/lead_create.html'
    form_class = LeadForm

    def get_success_url(self) -> str:
        return reverse("lead_list")
    
    def form_valid(self, form):
        send_mail(subject='A lead has been created', message='Go to the site to see the new lead',
                  from_email='test@test.com', recipient_list='test2@test.com')
        return super(LeadCreateView, self).form_valid(form)
    
class LeadUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    template_name = 'leads/lead_update.html'
    form_class = LeadForm

    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
            return Lead.objects.filter(organisation=user.userprofile)

    def get_success_url(self) -> str:
        return reverse("lead_list")
    
class LeadDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    template_name = 'leads/lead_delete.html'

    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
            return Lead.objects.filter(organisation=user.userprofile)


    def get_success_url(self) -> str:
        return reverse("lead_list")

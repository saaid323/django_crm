import random
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from leads.models import Agent
from django.shortcuts import reverse
from .forms import AgentModelForm
from .mixins import OrganisorAndLoginRequiredMixin
from django.core.mail import send_mail
# Create your views here.

class AgentListView(OrganisorAndLoginRequiredMixin, generic.ListView):
    template_name = 'agents/agent_list.html'

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)


class AgentCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    template_name = 'agents/create_agent.html'
    form_class = AgentModelForm
    
    def get_success_url(self) -> str:
        return reverse('agent_list')
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organiser = False
        user.set_password(f"{random.randint(0, 1000)}")
        user.save()
        Agent.objects.create(user=user, organisation=self.request.user.userprofile)
        send_mail(
            subject='You are invite to be an agent',
            message='You were added as an agent on DJCRM. Please Login',
            from_email='admin@test.com',
            recipient_list=[user.email]
        )
        return super(AgentCreateView, self).form_valid(form)


class AgentDetailView(OrganisorAndLoginRequiredMixin, generic.DetailView):
    template_name = 'agents/agent_detail.html'
    

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)



class AgentUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    template_name = 'agents/update_agent.html'
    form_class = AgentModelForm
    
    def get_success_url(self) -> str:
        return reverse('agent_list')
    
    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)
    


class AgentDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    template_name = 'agents/agent_delete.html'
    
    def get_success_url(self) -> str:
        return reverse('agent_list')

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)





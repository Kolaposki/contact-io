from django.shortcuts import render, redirect
from .models import Contacts
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy


# Create your views here.
# The user must be logged in before accessing the contacts they created [ can not view contacts of other users ]
# will redirect to the login page if the user is not authenticated
class HomePageView(LoginRequiredMixin, ListView):
    model = Contacts
    template_name = 'index.html'
    context_object_name = 'contacts'

    """Verify that the current user is authenticated."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, "You need to be logged in before accessing your contacts")
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        contacts = super().get_queryset()  # get all the contacts stored in the db
        return contacts.filter(manager=self.request.user).order_by('date_added')  # filter the contacts based on the logged in user


class DetailPageView(LoginRequiredMixin, DetailView):
    model = Contacts
    template_name = 'detail.html'
    context_object_name = 'contact'


@login_required
def search(request):
    if request.GET:
        search_term = request.GET['search_term']  # get value that was passed in url
        # search_result = Contacts.objects.filter(name__icontains=search_term)  # Case-insensitive containment test.
        # using complex query - Q
        search_result = Contacts.objects.filter(
            Q(name__icontains=search_term) | Q(email__icontains=search_term) | Q(info__icontains=search_term) | Q(
                phone__iexact=search_term)
        )

        context = {"search_term": search_term,
                   "contacts": search_result.filter(manager=request.user)}
        return render(request, 'search.html', context=context)
    else:
        return redirect('home')  # redirect to home page if there's no data in d url


class CreateContactView(LoginRequiredMixin, CreateView):
    model = Contacts
    fields = ['name', 'email', 'phone', 'gender', 'info', 'image']
    template_name = 'create.html'
    context_object_name = 'contact'
    success_url = '/'

    def form_valid(self, form):
        instance = form.save(commit=False)  # get the form but dont save in db yet
        instance.manager = self.request.user  # set the logged in user to be the manager(creator) of the post
        messages.success(self.request, "Contact created successfully")
        instance.save()
        return redirect('home')


class UpdateContactView(LoginRequiredMixin, UpdateView):
    model = Contacts
    fields = ['name', 'email', 'phone', 'gender', 'info', 'image']
    template_name = 'update.html'
    context_object_name = 'contact'

    def form_valid(self, form):
        instance = form.save()
        messages.success(self.request, "Contact succefully updated")
        return redirect('detail', instance.pk)  # redirect to detail page after submission of form


class DeletePageView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Contacts
    template_name = 'delete.html'
    success_url = '/'
    context_object_name = 'contact'
    success_message = "%(name)s Contact was deleted successfully"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()  # get the objects from the db
        messages.success(self.request, self.success_message % obj.__dict__)  # inject the object into the message
        return super(DeletePageView, self).delete(request, *args, **kwargs)


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('home')

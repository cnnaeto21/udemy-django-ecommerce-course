from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import CreateView, FormView, DetailView, View, UpdateView
from django.views.generic.edit import FormMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe 

from ecommerce.mixins import NextUrlMixin, RequestFormAttachMixin
 
from .forms import LoginForm, RegisterForm, GuestForm, ReactivateEmailForm, UserDetailChangeForm 
from .models import GuestEmail, EmailActivation
from .signals import user_logged_in

# @login_required
# def account_home_view(request):
#     return render(request, "accounts/home.html", {})

# class LoginRequiredMixin(object):
#     @method_decorator(login_required)
#     def dispatch(self, request, *args, **kwargs):
#         return super(LoginRequiredMixin, self).dispatch(self, request,*args, **kwargs)


class AccountHomeView(LoginRequiredMixin, DetailView):
    template_name = 'accounts/home.html'
    def get_object(self):
        return self.request.user

class AccountEmailActivateView(FormMixin, View):
    success_url = '/login/'
    form_class = ReactivateEmailForm
    key = None 
    def get(self, request, key=None, *args, **kwargs):
        self.key = key
        if key is not None:
            qs = EmailActivation.objects.filter(key__iexact=key)
            confirm_qs = qs.confirmable()
            if confirm_qs.count() == 1:
                obj = confirm_qs.first()
                obj.activate()
                messages.success(request, "Your emails has been confirmed. Please login")
                return redirect("login")
            else:
                activated_qs = qs.filter(activated=True)
                if activated_qs.exists():
                    reset_link = reverse("password_reset")
                    msg = """
                        Email already confirmed. Do you need to <a href = "{link}">reset your password</a>?
                    """.format(link=reset_link)
                    messages.success(request, mark_safe(msg))
                    return redirect("login")
        context = {'form': self.get_form(), 'key': key}
        return render(request, 'registration/activation-error.html', {})
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    def form_valid(self, form):
        msg = """ Activation Link sent. Please check your email """
        request = self.request
        messages.success(request, msg)
        email = form.cleaned_data.get("email")
        obj = EmailActivation.objects.email_exists(email).first()
        user = obj.user
        new_activation = EmailActivation.objects.create(user=user, email=email)
        new_activation.send_activation()
        return super(AccountEmailActivateView, self).form_valid(form)
    def form_invalid(self, form):
        context = {'form': form, 'key': self.key}
        return render(self.request, 'registration/activation-error.html', context)

# Create your views here.
# def guest_register_view(request):
#     form = GuestForm(request.POST or None)
#     context = {
#         "form": form
#     }
#     print("User logged in")
#     #print(request.user.is_authenticated())
#     next_ = request.GET.get('next')
#     next_post = request.POST.get('next')
#     redirect_path = next_ or next_post or None 
#     if form.is_valid():
#         email = form.cleaned_data.get("email")
#         new_guest_email = GuestEmail.objects.create(email=email)
#         request.session['guest_email_id'] = new_guest_email.id
#         if is_safe_url(redirect_path, request.get_host()):
#             return redirect(redirect_path)
#         else:
#             return redirect("/register/")
#     return redirect("/register/")
class GuestRegisterView(NextUrlMixin, RequestFormAttachMixin, CreateView):
    form_class = GuestForm
    default_next = '/register/'

    def get_success_url():
        self.get_next_url()

    def form_invalid(self, form):
        return redirect(self.default_next)
    # def form_valid(self, form):
    #     request = self.request
    #     email = form.cleaned_data.get("email")
    #     new_guest_email = GuestEmail.objects.create(email=email)
    #     return redirect(self.get_next_url())


class LoginView(NextUrlMixin, RequestFormAttachMixin, FormView):
    form_class = LoginForm
    success_url = '/'
    template_name = 'accounts/login.html'
    defualt_next = "/"

    def get_form_kwargs(self):
        kwargs = super(LoginView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs 

    def get_next_url(self):
        request = self.request
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None 
        if is_safe_url(redirect_path, request.get_host()):
            return redirect_path
        return "/"


    def form_valid(self, form):
        next_path = self.get_next_url()
        return redirect(next_path)


# def login_page(request):
#     form = LoginForm(request.POST or None)
#     context = {
#         "form": form
#     }
#     print("User logged in")
#     next_ = request.GET.get('next')
#     next_post = request.POST.get('next')
#     redirect_path = next_ or next_post or None 
#     if form.is_valid():
#         print(form.cleaned_data)
#         username = form.cleaned_data.get("username")
#         password = form.cleaned_data.get("password")
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             try: 
#                 del request.session['guest_email_id']
#             except:
#                 pass
#             if is_safe_url(redirect_path, request.get_host()):
#                 return redirect(redirect_path)
#             else:
#                 return redirect("/")
#         else:
#             print("Error")
#     return render(request, "accounts/login.html", context)

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = '/login/'

class UserDetailUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserDetailChangeForm 
    template_name = 'accounts/detail-update-view.html'
    def get_object(self):
        return self.request.user
    
    def get_context_data(self, *args, **kwargs):
        context = super(UserDetailUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Change your Account Details'
        return context
    def get_success_url(self):
        return reverse("account:home")



# User = get_user_model()
# def register_page(request):
#     form = RegisterForm(request.POST or None)
#     context = {
#         "form": form
#     }
#     if form.is_valid():
#         form.save()
#     return render(request, "accounts/register.html", context)
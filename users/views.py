from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.views.generic.edit import FormView

from .forms import CreateUserForm

from .services.email_verification_services import complete_email_verification, \
                                                  send_letter_for_email_verification
from .services.registaration_services import create_non_active_user_from_form
from .services.password_reset_services import get_user_by_email, \
                                              send_letter_for_password_reset


class PasswordResetRequestView(FormView):
    form_class = PasswordResetForm
    template_name = 'users/password_reset/password_reset.html'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        user = get_user_by_email(email)
        domain = get_current_site(self.request).domain
        send_letter_for_password_reset(domain, user)
        return redirect('password_reset_done')

    def form_invalid(self, form):
        messages.info(self.request, "Enter valid email")
        return self.render_to_response(self.get_context_data(form=form))


class RegisterView(FormView):
    template_name = 'users/register.html'
    form_class = CreateUserForm

    @never_cache
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('list')
        return super(RegisterView, self).get(request, *args, **kwargs)
    
    def form_valid(self, form):
        user = create_non_active_user_from_form(form)
        send_letter_for_email_verification(get_current_site(self.request).domain,
                                           user)
        return render(self.request, 
                      'users/email_confirm/email_sent.html')

    def form_invalid(self, form):
        for error in form.errors.values():
            print(error)
            messages.info(self.request, error.as_text()[2:])
        return self.render_to_response(self.get_context_data(form=form))
    

def confirm_email_verification_view(request, uidb64, token):
    try:
        complete_email_verification(uidb64, token)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return render(request, 
                      'users/email_confirm/email_unconfirmed.html')
    else:
        return render(request,
                      'users/email_confirm/email_confirmed.html')


def login_page(request):
    if request.user.is_authenticated:   
        return redirect('list')
    if request.method.lower() == 'post':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, 
                            password=password)
        if user:
            login(request, user)
            return redirect('list')
        else:
            messages.info(request, 
                          'Username or password is incorrect')
    return render(request, 'users/login.html')


@login_required
def logout_page(request):
    logout(request)
    return redirect('login')

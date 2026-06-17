from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.views import generic

from .forms import SignUpForm


class SignUpView(generic.View):
    form_class = SignUpForm
    initial = {}
    template_name = 'registration/signup.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to='blog:post_list')
        return super(SignUpView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='blog:post_list')

        return render(request, self.template_name, {'form': form})

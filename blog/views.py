from django.shortcuts import render, redirect


def index(request):
    return render(request, 'blog/index.html', context={'site': 'mysite.com'})


def contact(request):
    return redirect('blog:about')

from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from .forms import ContactForm


def home_page(request):
    context = {
        "title": "Hello World!",
        "content": "Welcome to the homepage",
    }
    if request.user.is_authenticated():
        context["premium_content"] = "Dope"
    return render(request, "home_page.html", context)

def about_page(request):
    context = {
        "title":"About",
        "content":"Welcome to the about page "
    }
    return render(request, "home_page.html", context)

def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        "title":"Contact",
        "content":"Welcome to the contact page",
        "form": contact_form,
        #"brand": "new Brand Name"  
    }
    if contact_form.is_valid():
        print(contact_form.cleaned_data)
        if request.is_ajax():
            return JsonResponse({"message": "Thank you"})
    

    if contact_form.errors:
        errors = contact_form.errors.as_json()
        if request.is_ajax():
            return HttpResponse(errors, status=400, content_type='application/json')
    # if request.method == "POST":
    #     #print(request.POST)
    #     print(request.POST.get("fullname"))
    #     print(request.POST.get("email"))
    #     print(request.POST.get("content"))
    return render(request, "contact/view.html", context)

def profile_page(request):
    context = {
        "title":"User Name",
        "content":"Profile"
    }
    return render(request, "home_page.html", context)

def home_page_old(request):
    html_ = """
    <!doctype html>
    <html lang="en">
        <head>
            <!-- Required meta tags -->
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

            <!-- Bootstrap CSS -->
            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css" integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk" crossorigin="anonymous">

            <title>Hello, world!</title>
        </head>
        <body>
            <div class = "text-center">
                <h1>Hello, world!</h1>
            </div>

            <!-- Optional JavaScript -->
            <!-- jQuery first, then Popper.js, then Bootstrap JS -->
            <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
            <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
            <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.min.js" integrity="sha384-OgVRvuATP1z7JjHLkuOU7Xw704+h835Lr+6QL9UvYjZE3Ipu6Tp75j7Bh/kR0JKI" crossorigin="anonymous"></script>
        </body>
    </html>
    """
    return HttpResponse(html_)
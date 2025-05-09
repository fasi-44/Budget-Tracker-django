from django.shortcuts import render, redirect

def root_view(request):
    # return HttpResponse("This is a different message!")
    # return render(request, "welcome.html")  # Render a template
    return redirect("/api/")  # Redirect to your API
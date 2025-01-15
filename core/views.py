from django.shortcuts import render

# Create your views here.


def chat(request):
    if not request.session.session_key:
        request.session.create()
    print("hello from chat")
    return render(request, 'chat.html')

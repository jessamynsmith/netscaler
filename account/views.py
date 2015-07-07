from django.shortcuts import redirect
from django.contrib.auth import logout

# Create your views here.

def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return redirect('/')
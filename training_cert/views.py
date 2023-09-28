from django.shortcuts import redirect, render
from django.contrib import messages

from .forms import Training_Cert_Form ,Cert_Number_form
from .models import Training_Cert 

# Create your views here.

def Training_Cert_View (request):
    form = Training_Cert_Form
    if request.method == 'POST':
        form = Training_Cert_Form(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('training_cert_view')
    context = {
        'form': form,
    }

    return render(request, 'training_cert/register_cert.html', context)


def Cert_list (request):
    all_cert = Training_Cert.objects.all()
    context = {
        'all_cert': all_cert,
    }

    return render(request, 'training_cert/cert_list.html', context)


def validate_cert (request):
    form = Cert_Number_form()
    if request.method == 'POST':
        form = Cert_Number_form( request.POST )
        if form.is_valid():
            cert_number = form.cleaned_data['cert_number']

            try:
                cert_info = Training_Cert.objects.get( cert_number = cert_number  )

                messages.success(request, f"Cert Is Valid ... { cert_info.cert_bearer_first_name } { cert_info.cert_bearer_last_name } attend the { cert_info.traning_platform } training.")
            
            except Training_Cert.DoesNotExist:
                messages.info(request, f"the following certificate is not valid or not found on our kroon and kiosk record")
                return redirect('validate_cert')
   

    context = {
        'form': form,
    }

    return render(request, 'training_cert/cert_validate.html', context)
            


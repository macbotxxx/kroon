import datetime
from datetime import datetime, timezone

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django.template.loader import get_template
import pytz
utc=pytz.UTC
from config.utils import render_to_pdf
import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
# from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

from transactions.models import Transactions
from .models import Mask_Statement_Of_Account
from subscriptions.models import Merchant_Subcribers



def statement_of_account_view (request, id):
    """
    statment of account pdf
    """
    total = 0
    mask_id = Mask_Statement_Of_Account.objects.get(masked_id = id )
    # created_date__gte=start_date, created_date__lte=end_date,
    statement_account = Transactions.objects.filter( user = mask_id.user)
    user = mask_id.user

    credit = Transactions.objects.select_related("user").filter(user= mask_id.user, recipient = mask_id.user, currency = "KC", status = "successful")

    for i in credit:
        total += i.credited_kroon_amount
    total_credit = total

    qs = Transactions.objects.select_related("user").filter(user= mask_id.user, benefactor = mask_id.user , currency = "KC", status = "successful")
    for i in qs:
        total += i.debited_kroon_amount
       
    total_debitted = total


    context = {
        'statement_account': statement_account,
        'user': user,
        'total_credit':total_credit,
        'total_debitted':total_debitted,
    }

    return render(request, 'statement_of_account/statment.html', context )


def test_view (request):
    """
    statment of account pdf
    """
    current_time = datetime.now()
    # check_otp_duration = utc.localize(check_otp.duration)
    current_time = utc.localize(current_time) 
    plans = Merchant_Subcribers.objects.filter( active = True )
    for i in plans:
        if i.end_date < current_time:
            i.active = False
            i.save()
            return JsonResponse ('this transaction has no pending', safe =False)
        else:
            pass

    return render(request, 'statement_of_account/mk.html' )





def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    result = finders.find(uri)
    if result:
            if not isinstance(result, (list, tuple)):
                    result = [result]
            result = list(os.path.realpath(path) for path in result)
            path=result[0]
    else:
            sUrl = settings.STATIC_URL        # Typically /static/
            sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
            mUrl = settings.MEDIA_URL         # Typically /media/
            mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

            if uri.startswith(mUrl):
                    path = os.path.join(mRoot, uri.replace(mUrl, ""))
            elif uri.startswith(sUrl):
                    path = os.path.join(sRoot, uri.replace(sUrl, ""))
            else:
                    return uri

    # make sure that file exists
    if not os.path.isfile(path):
            raise Exception(
                    'media URI must start with %s or %s' % (sUrl, mUrl)
            )
    return path


def render_pdf_view(request):
    template_path = 'statement_of_account/mk.html'
    context = {'myvar': 'this is your template context'}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response, link_callback=link_callback)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
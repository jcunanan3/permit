from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from permit import settings


from django.contrib.auth.decorators import login_required, permission_required
from permit_app.forms import EmailUserCreationForm, PermitCreationForm, PermitApprovalForm
from django.core.mail import EmailMultiAlternatives
from permit_app.models import Permit, PermitUser
# from django.core.context_processors import csrf
from django.template import RequestContext
from django.contrib.auth.decorators import user_passes_test
import requests
import json
import stripe

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = EmailUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = EmailUserCreationForm()
    return render(request, "registration/register.html", {
        'form': form,
    })

@login_required
def profile(request):
    if not request.user.is_authenticated():
        return redirect("login")
    return render(request,'profile.html')

def home(request):
    return render(request,'home.html')

def about(request):
    return render(request,'about.html')

@login_required
def permit_application(request):
    if request.method == "POST":
        form = PermitCreationForm(request.POST)
        if form.is_valid():
            permit_form = form.save(commit=False)
            if permit_form:
                permit_form.user = request.user
                permit_form.save()
                # email staff
                staff_text = "There is a permit from {} awaiting approval.".format(request.user)
                staff_users = PermitUser.objects.all().filter(MTA_staff=True)
                for i in staff_users:
                    msg = EmailMultiAlternatives("New permit", staff_text, settings.DEFAULT_FROM_EMAIL, [i.email])
                    msg.send()
                return redirect("/profile")
    else:
        form = PermitCreationForm()
        data = {'form': form}
    return render(request, "permit_application.html",data)


def staff_check(user):
    return user.MTA_staff

# @login_required
@user_passes_test(staff_check)
def view_permits(request):
    permits = Permit.objects.order_by("-date")
    # response_array = []
    # for i in permits:
    #     location = i.street_address+",San Francisco,CA"
    #     response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address='+location+'&key=AIzaSyBukXf80UEFP8KYbO4GGC729nHJCMdU-30')
    #     response = response.json()
    #     response_array.append(response)
    return render_to_response("view_permits.html", {'permits':permits})


@login_required
def view_permit(request, permit_id):
    permit = Permit.objects.get(id=permit_id)
    data = {"permit": permit}
    return render_to_response("view_permit.html",data)

@login_required
@user_passes_test(staff_check)
def edit_permit(request, permit_id):

    permit = Permit.objects.get(id=permit_id)
    if request.method == "POST":
        form = PermitApprovalForm(request.POST, instance=permit)
        if form.is_valid():
            if form.save():
                # return redirect("/view_permits/{}".format(permit_id))

                if permit.approved:
                    html_content2 = "approved"
                else:
                    html_content2 = "rejected"
                html_content = '<p>Your permit for {} on date {} was {}. Staff comments:<p>{}'.format(permit.street_address,permit.date,html_content2,permit.MTA_comments)
                response_text = "Your permit was {}".format(html_content2)
                msg = EmailMultiAlternatives("Parking permit application", response_text, settings.DEFAULT_FROM_EMAIL, [permit.user.email])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                return redirect("/view_permits")
    else:
        form = PermitApprovalForm(instance=permit)
    data = {"permit": permit, "form":form}
    #use RequestContext to support csrf token
    return render_to_response("edit_permit.html",RequestContext(request, data))

def logout(request):
    logout(request,"logged_out.html")
    return

def test(request):
    staff_users = PermitUser.objects.all().filter(MTA_staff=True)
    return render_to_response("test.html", {'staff_users': staff_users})

def view_map(request):

    return render(request,'view_map.html',)


def view_map_info(request):
    permits = Permit.objects.order_by("-date")
    response_array = []
    for i in permits:
        location=i.street_address+",San Francisco,CA"
        response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address='+location+'&key=AIzaSyBukXf80UEFP8KYbO4GGC729nHJCMdU-30')
        response=response.json()
        response_array.append(response)
    return HttpResponse(json.dumps(response_array), content_type='application/json')

@csrf_exempt
def charge(request):
        # Set your secret key: remember to change this to your live secret key in production
    # See your keys here https://dashboard.stripe.com/account
    stripe.api_key = "sk_test_BQokikJOvBiI2HlWgH4olfQ2"

    # Get the credit card details submitted by the form
    token = request.POST['stripeToken']

    # Create a Customer
    customer = stripe.Customer.create(
        card=token,
        description="payinguser@example.com"
    )

    # Charge the Customer instead of the card
    stripe.Charge.create(
        amount=16300, # in cents
        currency="usd",
        customer=customer.id
    )
    return render(request, 'charge.html')







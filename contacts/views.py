from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import Contact


def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(
                listing_id=listing_id, user_id=user_id)
            if has_contacted:
                messages.error(
                    request, 'You have already expressed your interest for this listing')
                return redirect('/listings/'+listing_id)

        contact = Contact(listing=listing, listing_id=listing_id, name=name, email=email,
                          phone=phone, message=message, user_id=user_id)

        contact.save()

        # Sending email
        # send_mail(
        #     'Property listing inquiry on SVN Real Estate',
        #     'New inquiry alert, sign in to see details',
        #     'contact@svnre.com',
        #     [realtor_email, 'contact@svnre.com'],
        #     fail_silently=False
        # )

        messages.success(
            request, 'Your inquiry has been posted, the realtor will get back to you asap')
        return redirect('/listings/'+listing_id)

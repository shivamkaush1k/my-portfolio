from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from django.http import HttpResponseRedirect,HttpResponse
from .forms import ContactForm

def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Honeypot check (redirect if FILLED)
            if form.cleaned_data.get("honeypot"):
                return redirect("contacts:contacts")  # Bot detected
            
            try:
                with transaction.atomic():
                    contact = form.save(commit=False)
                    contact.ip_address = request.META.get("REMOTE_ADDR")
                    contact.sent_at = timezone.now()
                    contact.save()
                    
                    # Send email
                    send_mail(
                        subject=f"Portfolio: {contact.subject or 'New Contact'}",
                        message=f"Name: {contact.name}\nEmail: {contact.email}\n\nMessage:\n{contact.message}",
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[getattr(settings, 'CONTACT_EMAIL', 'shivamkashik.1004@gmail.com')],
                        fail_silently=False,
                    )
                    
                    messages.success(request, "Message sent successfully! 🚀")
                    return redirect("contacts:contacts")
                
            except BadHeaderError:
                messages.error(request, "Invalid header found.")
            except Exception as e:
                messages.error(request, f"Error sending email: {str(e)}")
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = ContactForm()

    return render(request, "contacts/contact.html", {"form": form})

# Privacy redirects - ALL SOCIAL LINKS
def contact_linkedin(request):
    """LinkedIn redirect"""
    return HttpResponseRedirect('https://www.linkedin.com/in/shi1vamkaush1k/')

def contact_github(request):
    """GitHub redirect"""
    return HttpResponseRedirect('https://github.com/shivamkaush1k')

def contact_instagram(request):
    """Instagram redirect"""
    return HttpResponseRedirect('https://www.instagram.com/sadaa_shivam/')

def contact_x(request):
    """X redirect"""
    return HttpResponseRedirect('')

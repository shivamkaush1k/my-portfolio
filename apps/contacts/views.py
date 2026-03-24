from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.db import transaction
from django.http import JsonResponse, HttpResponseRedirect
from .forms import ContactForm


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        
        if form.is_valid():
            # Honeypot check
            if form.cleaned_data.get("honeypot"):
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'message': 'Spam detected'}, status=400)
                return redirect("contacts:contact")
            
            try:
                # Save to DB
                with transaction.atomic():
                    contact = form.save(commit=False)
                    contact.ip_address = request.META.get("REMOTE_ADDR")
                    contact.save()

                # Send email
                subject = contact.subject or "New Contact Form"
                full_message = f"""
New Portfolio Contact Form Submission

👤 Name: {contact.name}
📧 Email: {contact.email}
🎯 Subject: {subject}

💬 Message:
{contact.message}

---
🌐 IP: {contact.ip_address}
📅 Sent: {contact.sent_at}
                """
                
                send_mail(
                    subject=f"Portfolio: {subject}",
                    message=full_message.strip(),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CONTACT_EMAIL],
                    fail_silently=False,
                )

                # Response
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True, 
                        'message': 'Message sent successfully! 🚀'
                    })
                
                messages.success(request, "Message sent successfully! 🚀")
                return redirect("contacts:contact")

            except BadHeaderError:
                error_msg = "Invalid email header detected"
            except Exception as e:
                error_msg = f"Message saved but email delivery failed"
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': error_msg}, status=500)
            
            messages.error(request, error_msg)
        
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False, 
                    'message': 'Please fix the form errors',
                    'errors': form.errors
                }, status=400)
            
            messages.error(request, "Please fix the errors below.")
    
    else:
        form = ContactForm()
    
    return render(request, "contacts/contact.html", {"form": form})


# Social redirects
def contact_linkedin(request):
    return HttpResponseRedirect("https://www.linkedin.com/in/shivamkaush1k/")

def contact_github(request):
    return HttpResponseRedirect("https://github.com/shivamkaush1k")

def contact_instagram(request):
    return HttpResponseRedirect("https://www.instagram.com/sadaa_shivam/")

def contact_x(request):
    return HttpResponseRedirect("https://x.com/shivamkaush1k")

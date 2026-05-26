from django.shortcuts import redirect, render
from django.contrib import messages
from django.views import View

from polls.models import DateDecision

def get_client_ip(request):
    """Helper function to grab the voter's IP address."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

class LandingPageView(View):
    template_name = 'polls/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        decision = request.POST.get('decision')
        feedback = request.POST.get('feedback', '').strip()
        ip = get_client_ip(request)

        # Basic validation
        if decision in ['YES', 'NO']:
            DateDecision.objects.create(
                decision=decision,
                feedback=feedback,
                voter_ip=ip
            )
            messages.success(request, "Your verdict has been recorded into the ether.")
            return redirect('landing_page') 
            
        return render(request, self.template_name)
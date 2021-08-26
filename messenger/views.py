from django.shortcuts import get_object_or_404, render, redirect
from accounts.models import Profile
from django.contrib.auth.decorators import login_required
from .forms import ChatMessage, ChatMessageForm
from django.db.models import Q
# Create your views here.
# homepage - all users - recent messages
# conversation - create - redirect back to same page

@login_required
def index(request):
    profiles = Profile.objects.exclude(user=request.user)
    return render(request, 'messenger/homepage.html', {'profiles': profiles})
    
@login_required
def conversation(request, profile_id):
    if request.user.profile.id == profile_id:
        return redirect('message_homepage')

    receiver_profile = get_object_or_404(Profile, id=profile_id)
    messages = ChatMessage.objects.filter(
        Q(receiver=receiver_profile, sender=request.user.profile)|
        Q(sender=receiver_profile, receiver=request.user.profile)
    )
    form = ChatMessageForm()
    if request.method == 'POST':
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user.profile
            message.receiver = receiver_profile
            message.save()
            return redirect('conversation', receiver_profile.id)
    return render(request, 'messenger/conversation.html', {'form':form, 'chat_messages':messages})
    
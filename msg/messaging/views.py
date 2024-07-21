from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm
from .models import Message, User
from django.http import JsonResponse
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.conf import settings
from django.utils.http import http_date
from django.contrib.auth.decorators import login_required
import os
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Max, Case, When
from .models import Message

from django.http import JsonResponse
from django.core.serializers import serialize

def user_messages(request):
    user = request.user

    # Annotate the latest message timestamp for sent and received messages
    sent_messages = Message.objects.filter(sender=user).values('receiver_id').annotate(latest_timestamp=Max('timestamp'))
    received_messages = Message.objects.filter(receiver=user).values('sender_id').annotate(latest_timestamp=Max('timestamp'))

    # Combine both sent and received messages to find the latest interaction per user
    combined_messages = list(sent_messages) + list(received_messages)

    # Get the maximum timestamp per user
    user_interactions = {}
    for msg in combined_messages:
        user_id = msg.get('receiver_id') or msg.get('sender_id')
        timestamp = msg['latest_timestamp']
        if user_id not in user_interactions or timestamp > user_interactions[user_id]:
            user_interactions[user_id] = timestamp

    # Sort user ids by the latest interaction timestamp
    sorted_user_ids = sorted(user_interactions.keys(), key=lambda x: user_interactions[x], reverse=True)

    # Get the sorted user queryset
    preserved_order = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(sorted_user_ids)])
    users = User.objects.filter(id__in=sorted_user_ids).select_related('profile').order_by(preserved_order)

    # Serialize the users queryset
    users_data = list(users.values('username', 'profile__profile_photo'))

    return JsonResponse(users_data, safe=False)

@login_required
def home(request):

    return render(request, 'messaging/home.html')
def user_login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(request,username=username,password=password)
        print(user,password)
        if user is not None:
            login(request, user)
            return redirect('/messaging')
        else:
            messages.info(request,'username or password is incorrect')

    return render(request, 'messaging/login.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            user=form.cleaned_data.get('username')
            messages.success(request,'the user '+user+ ' is registered')
            return redirect('/messaging/login')
    else:
        form=RegistrationForm()

    return render(request, 'messaging/register.html', {'form': form})

def chat(request):
    return render(request,'messaging/chat.html')
@login_required
def profile(request):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
            return redirect('profile')
    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'p_form': p_form,
    }

    return render(request, 'messaging/profile.html', context)

def logout_view(request):
    logout(request)
    messages.success(request,'the user is logged out')
    return redirect('/messaging/login/')  # Redirects to the login page


@login_required
def protected_media(request, file_path):
    # Ensure the file path is safe and within MEDIA_ROOT
    file_path = os.path.join(settings.MEDIA_ROOT, file_path)
    if not os.path.isfile(file_path):
        raise Http404("File does not exist")

    # Serve the file
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read())
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = f'attachment; filename={os.path.basename(file_path)}'
        response['Last-Modified'] = http_date(os.path.getmtime(file_path))
        return response
@login_required()
def fetch_user_list(request):
    query = request.GET.get('search', '')
    if query:
        users = User.objects.exclude(username=request.user.username).filter(username__icontains=query).values(
            'username')
    else:
        return []
    user_list = list(users)
    return JsonResponse(user_list, safe=False)
@login_required
def MessageView(request, username):
    try:
        other_user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    current_user = request.user

    # Ensure that current_user is authorized to see messages with other_user
    # if not (Message.objects.filter(
    #         (Q(sender=current_user) & Q(receiver=other_user)) |
    #         (Q(sender=other_user) & Q(receiver=current_user))
    # ).exists()):
    #     return JsonResponse({'error': 'Unauthorized'}, status=403)

    messages = Message.objects.filter(
        (Q(sender=current_user) & Q(receiver=other_user)) |
        (Q(sender=other_user) & Q(receiver=current_user))
    ).order_by('timestamp').values(
        'sender__username',
        'receiver__username',
        'content',
        'media_file',
        'media_image',
        'timestamp',
        'is_read'
    )

    # Update media fields to return URLs
    for message in messages:
        if message['media_file']:
            message['media_file'] = request.build_absolute_uri(f'/media/{message["media_file"]}')
        if message['media_image']:
            message['media_image'] = request.build_absolute_uri(f'/messaging/media/{message["media_image"]}')

    data = list(messages)
    return JsonResponse(data, safe=False)
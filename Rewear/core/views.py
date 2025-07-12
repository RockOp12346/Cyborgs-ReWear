from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Profile, Item, ItemImage, Swap

# Create your views here.

def home(request):
    featured_items = Item.objects.filter(status='ACTIVE').order_by('-created_at')[:9]
    return render(request, "home.html", {'featured_items': featured_items})

def dashboard(request):
    # Product listing with search and filters
    search = request.GET.get('search', '')
    category = request.GET.get('category', '')
    status = request.GET.get('status', '')
    items = Item.objects.all()
    if search:
        items = items.filter(name__icontains=search)
    if category:
        items = items.filter(category=category)
    if status:
        items = items.filter(status=status)
    categories = Item.objects.values_list('category', flat=True).distinct()
    # Add image_url fallback for template
    for item in items:
        if item.images.exists():
            item.image_url = item.images.first().image.url
        else:
            item.image_url = '/static/images/placeholder.svg'
    return render(request, "core/browse_products.html", {
        'items': items,
        'categories': categories,
    })

def signup(request):
    if request.method == "POST":
        firstname = request.POST['firstname']
        lastname = request.POST['lastname'] 
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Already Exists')
                return redirect('signup/') 
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Already Taken')
                return redirect('signup/')
            else:
                user = User.objects.create_user(username=username, email=email, password=password, first_name=firstname, last_name=lastname)
                user.save()

                # log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)


                # create a profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('/')

        else:
            messages.info(request, 'Password Does Not Match')
            return redirect('signup/')
        
    else:
        return render(request, 'signup.html')

def signin(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('login/')
    else:
        return render(request, 'signin.html')
    
@login_required(login_url='login/')
def logout(request):
    auth.logout(request)
    return redirect('/')

# Item detail view
@login_required(login_url='login/')
def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    is_owner = item.owner == request.user
    return render(request, 'core/item_detail.html', {'item': item, 'is_owner': is_owner})

# Item create view
@login_required(login_url='login/')
def item_create(request):
    from .forms import ItemForm
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.owner = request.user
            item.save()
            return redirect('item_detail', pk=item.pk)
    else:
        form = ItemForm()
    return render(request, 'core/item_form.html', {'form': form})

# Item edit view
@login_required(login_url='login/')
def item_edit(request, pk):
    from .forms import ItemForm
    item = get_object_or_404(Item, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('core:item_detail', pk=item.pk)
    else:
        form = ItemForm(instance=item)
    return render(request, 'core/item_form.html', {'form': form, 'item': item})

# Swap request view
@login_required(login_url='login/')
def swap_request(request, pk):
    item = get_object_or_404(Item, pk=pk)
    my_listings = Item.objects.filter(owner=request.user)
    if request.method == 'POST':
        request_type = request.POST.get('request_type')
        offered_item_id = request.POST.get('offered_item')
        if request_type == 'swap' and offered_item_id:
            offered_item = get_object_or_404(Item, pk=offered_item_id, owner=request.user)
            Swap.objects.create(
                requester=request.user,
                item=item,
                offered_item=offered_item,
                is_points_swap=False,
                status='PENDING'
            )
            messages.success(request, 'Swap request submitted!')
        elif request_type == 'points':
            Swap.objects.create(
                requester=request.user,
                item=item,
                is_points_swap=True,
                points_offered=item.points_required,
                status='PENDING'
            )
            messages.success(request, 'Points redemption request submitted!')
        else:
            messages.error(request, 'Please select a valid option.')
        return redirect('core:item_detail', pk=item.pk)
    return render(request, 'core/swap_request.html', {
        'item': item,
        'my_listings': my_listings,
    })

# Profile view
@login_required(login_url='login/')
def profile(request):
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=user, id_user=user.id)
    my_listings = Item.objects.filter(owner=user)
    completed_swaps = Swap.objects.filter(requester=user, status__in=['COMPLETED', 'ACCEPTED'])
    completed_requests = Swap.objects.filter(item__owner=request.user, status='COMPLETED')
    ongoing_swaps = Swap.objects.filter(requester=user).exclude(status='COMPLETED')
    print(ongoing_swaps)
    return render(request, 'core/user_profile.html', {
    'profile': profile,
    'my_listings': my_listings,
    'completed_swaps': completed_swaps,
    'ongoing_swaps': ongoing_swaps,
    'completed_requests': completed_requests,
})

# Profile edit view
@login_required(login_url='login/')
def profile_edit(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    if request.method == 'POST':
        first_name = request.POST.get('first_name', user.first_name)
        last_name = request.POST.get('last_name', user.last_name)
        email = request.POST.get('email', user.email)
        location = request.POST.get('location', profile.location)
        bio = request.POST.get('bio', profile.bio)
        profile_img = request.FILES.get('profile_img')

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()

        profile.location = location
        profile.bio = bio
        if profile_img:
            profile.profile_img = profile_img
        profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('core:profile')
    return render(request, 'core/profile_settings.html', {'profile': profile})


@login_required(login_url='login/')
def incoming_swaps(request):
    # Show swaps for items owned by the current user
    swap_requests = Swap.objects.filter(item__owner=request.user).order_by('-created_at')
    if request.method == 'POST':
        swap_id = request.POST.get('swap_id')
        action = request.POST.get('action')
        swap = get_object_or_404(Swap, pk=swap_id, item__owner=request.user)
        if action == 'accept':
            swap.status = 'ACCEPTED'
            swap.save()
            messages.success(request, 'Swap request accepted!')
        elif action == 'complete':
            swap.status = 'COMPLETED'
            swap.save()
            # Mark item as unavailable
            swap.item.is_available = False
            swap.item.save()
            messages.success(request, 'Swap marked as completed!')
        elif action == 'reject':
            swap.status = 'REJECTED'
            swap.save()
            messages.success(request, 'Swap request rejected!')

        return redirect('core:incoming_swaps')
    return render(request, 'core/incoming_swaps.html', {
        'swap_requests': swap_requests,
    })


# Admin items view
@login_required(login_url='login/')
def admin_items(request):
    # Stats
    total_users = Profile.objects.count()
    active_listings = Item.objects.filter(status='ACTIVE').count()
    pending_approvals = Item.objects.filter(status='PENDING').count()

    # Recent Activity: last 10 items (can be filtered/ordered as needed)
    recent_items = Item.objects.select_related('owner').prefetch_related('images').order_by('-created_at')[:10]

    # Prepare data for table
    activity_rows = []
    for item in recent_items:
        activity_rows.append({
            'title': item.title,
            'user': item.owner.username,
            'date': item.created_at.strftime('%Y-%m-%d'),
            'status': item.status.lower(),
            'description': item.description,
            'photo': item.images.first().image.url if item.images.exists() else '/static/images/placeholder.svg',
            'size': item.size,
            'category': item.get_category_display(),
            'points': item.points_required,
        })

    context = {
        'total_users': total_users,
        'active_listings': active_listings,
        'pending_approvals': pending_approvals,
        'activity_rows': activity_rows,
    }
    return render(request, 'core/admin_pg.html', context)
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib import messages
import datetime
from realestate import settings
from django.utils import timezone
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import generic
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.urls import reverse

# DRF imports
from rest_framework import generics
from .serializers import *
from rest_framework import viewsets
from rest_framework.permissions import *
from rest_framework.authentication import TokenAuthentication, BasicAuthentication


# REST API VIEWS
class PropertyViewSet(viewsets.ModelViewSet):
    """
        PropertyViewSet to preform CRUD operations on properties in REST API
        It is Used with router in urls
    """
    queryset = Property.objects.filter(active=True)
    serializer_class = PropertySerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserApiView(generics.RetrieveUpdateAPIView):
    """UserApiView to view requesting user profile in REST API"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication, TokenAuthentication, ]

    def get_object(self):
        return self.request.user


class RegisterApiView(generics.CreateAPIView):
    """RegisterApiView to register users in REST API"""
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny, ]


class CategoryViewSet(viewsets.ModelViewSet):
    """CategoryViewSet to perform CRUD operations on Category in REST API
     It can be assessed only by the Admin"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]


########################################################################################
########################################################################################
########################################################################################

# HTTP REQUESTS/RESPONSE VIEWS
def homepage(request):

    property = Property.objects.filter(active=True)
    latest_property = Property.objects.filter(
        active=True).order_by('-date_posted')[0:4]

    context = {'property': property, 'latest_property': latest_property}
    return render(request, 'homepage.html', context)


class PropertyList(generic.ListView):
    queryset = Property.objects.filter(active=True).order_by('-date_posted')
    template_name = 'property_list.html'
    paginate_by = 6


class PropertyDetail(generic.DetailView):
    model = Property
    template_name = 'property_detail.html'


@login_required
def property_upload(request):
    property_queryset = Property.objects.all()
    new_property = None
    form = PropertyForm()
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        images = request.FILES.getlist('images[]')
        if form.is_valid():
            new_property = form.save(commit=False)
            new_property.owner = request.user
            new_property.save()

            for i in images:
                test = PropertyImage(property=new_property, image=i)
                test.save()
            # PropertyImage.objects.create(property=property,image=i)
            messages.success(request, 'Property has been added successfully')
            messages.info(
                request, 'An Admin will review your property and activate it ')
            return redirect('home')

    context = {'form': form, 'new_property': new_property,
               'property_queryset': property_queryset}

    return render(request, 'property_form.html', context)


class PropertyDelete(generic.DeleteView):
    model = Property
    template_name = 'property_delete.html'
    # success_url = 'home'

    def get_success_url(self):
        messages.success(
            self.request, "Property has been deleted successfully")
        return reverse("profile", self.request.user)


def search(request):
    keyword = request.GET.get('search_keyword')
    type = request.GET.get('property_type')
    price = request.GET.get('price')
    if keyword != '':
        property = Property.objects.filter(
            title__icontains=keyword, active=True)
        if type != '':
            property = Property.objects.filter(
                title__icontains=keyword, property_type=type, active=True)
            if price != '':
                property = Property.objects.filter(
                    title__icontains=keyword, property_type=type, price__lte=price, active=True)
    elif keyword == '' and type != '':
        property = Property.objects.filter(property_type=type, active=True)
        if price != '':
            property = Property.objects.filter(
                property_type=type, price__lte=price, active=True)
    elif keyword == '' and type == '' and price != '':
        property = Property.objects.filter(price__lte=price, active=True)
    else:
        property = Property.objects.none()

    return render(request, 'search_result.html', {'property': property})


def profile(request, username):
    user = User.objects.get(username=username)
    now = timezone.now()
    last_seen = user.online.last_activity
    online = None
    user_property = Property.objects.filter(
        owner=user, active=True).order_by('-date_posted')
    if now > last_seen + datetime.timedelta(seconds=settings.USER_ONLINE_TIMEOUT):
        online = False

    else:
        online = True

    page = Paginator(user_property, 6)
    page_number = request.GET.get('page')
    page_obj = page.get_page(page_number)

    context = {'user': user, 'now': now,
               'online': online, 'user_property': user_property, 'page_obj': page_obj}

    return render(request, 'profile.html', context)


@login_required
def profile_update(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileForm(
            request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your Profile has been updated")
            return redirect('profile', request.user.username)

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)

    context = {'user_form': user_form, 'profile_form': profile_form}

    return render(request, 'profile_update.html', context)


def contact_email(request):
    sender_email = request.POST.get("sender_email")
    subject = f'New contact {sender_email}: {request.POST.get("subject")}'
    message = request.POST.get("message")
    to_email = request.POST.get("owner_email")
    msg = None
    if subject and message and to_email:
        msg = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [
                           to_email], reply_to=[sender_email])
        msg.send()
        messages.success(request, "Your messages has been sent")

    else:
        messages.error(request, "Make sure all fields are entered and valid.")
    return redirect('home')

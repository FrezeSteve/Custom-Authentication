from accounts.models import DeviceTracker
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.text import slugify
import random
import string

User = get_user_model()


def custom_set_cookie(request, response):
    if not request.get_signed_cookie('custom_session_id', default=None):
        if not (request.session and request.session.get('session_key')):
            request.session.save()
        value = request.session.session_key
        max_age = 60 * 60 * 60 * 24 * 30
        response.set_signed_cookie(
            "custom_session_id", value=value, max_age=max_age, expires=None, path='/'
            , domain=None, secure=None, httponly=True, samesite='Strict'
        )


# def custom_set_cookie_for_user(response, session_id):
#     max_age = 60 * 60 * 60 * 24 * 30
#     response.set_signed_cookie(
#         "custom_session_id", value=session_id, max_age=max_age, expires=None, path='/'
#         , domain=None, secure=None, httponly=True, samesite='Strict'
#     )

def get_create_device_tracker(request):
    session_id = request.get_signed_cookie('custom_session_id', default=None)
    # get or create anonymous user
    device = DeviceTracker.objects.filter(
        device_id=session_id
    )
    if not device.exists():
        device = DeviceTracker.objects.create(
            device_id=session_id
        )
    else:
        device = device.first()
    device.last_used = timezone.now()
    device.save()
    return device


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance
    has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=4)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def store_device_to_user(request, device):
    logged_in_user = User.objects.filter(id=request.user.id).first()
    if logged_in_user:  # avoid errors if user is not found
        logged_in_user.device.add(device)
        logged_in_user.save()

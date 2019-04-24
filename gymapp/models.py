from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.db.models.signals import pre_save, m2m_changed
from django.contrib.auth.models import User
from django.conf import settings 
from django.db import models
from django.conf import settings




def validate_only_one_instance(obj):
    model = obj.__class__
    if (model.objects.count() > 0 and
            obj.id != model.objects.get().id):
        raise ValidationError("Can only create 1 %s instance" % model.__name__)


class Organization(models.Model):
    name = models.CharField(max_length=200)
    slogan = models.CharField(null=True, blank=True, max_length=200)
    logo = models.ImageField(upload_to='organizationdetails')
    about = models.TextField()
    address = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    mobile = models.CharField(max_length=20)
    favicon = models.ImageField(upload_to='organizationdetails')
    facebook = models.URLField()
    twitter = models.URLField(null=True, blank=True)
    youtube = models.URLField(null=True, blank=True)
    map_location = models.CharField(max_length=50)
    mission = models.TextField(null=True, blank=True)
    vision = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    def clean(self):
        validate_only_one_instance(self)


DAY = (
    ('sunday', 'sunday'),
    ('monday', 'monday'),
    ('tuesday', 'tuesday'),
    ('wednesday', 'wednesday'),
    ('thursday', 'thursday'),
    ('friday', 'friday'),
    ('saturday', 'saturday'),
)

VerificationStatus = (
    ('verified', 'verified'),
    ('pending', 'pending'),
    ('cancelled', 'cancelled'),

)
POSITION = (
    ('Header ad', 'Header ad'),
    ('Banner ad', 'Banner ad'),
    ('Side ad1', 'Side ad1'),
    ('Side ad2', 'Side ad2'),
    ('Inner ad1', 'Inner ad1'),
    ('Inner ad2', 'Inner ad2'),

)


class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_by = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, null=True, blank=True)

    class Meta:
        abstract = True


class Message(TimeStamp):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.name



class Admin(models.Model):
    user = models.OneToOneField(User,on_delete=models.PROTECT, null=True, blank=True)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=200)
    email = models.EmailField()
    about = models.TextField(blank=True, null=True)
    image = models.ImageField(
        upload_to='admin/', default="/default.jpg", blank=True, null=True)

class Client(models.Model):
    user = models.OneToOneField(User,on_delete=models.PROTECT, null=True, blank=True)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=200)
    email = models.EmailField()
    about = models.TextField(blank=True, null=True)
    image = models.ImageField(
        upload_to='client/', default="/default.jpg", blank=True, null=True)



class Trainer(TimeStamp):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, null=True, blank=True)
    email = models.EmailField()
    image = models.ImageField(upload_to='trainer/')
    speciality = models.CharField(max_length=512)
    details = models.TextField(max_length=512)
    experience = models.PositiveIntegerField()

    def __str__(self):
        return self.name + " (" + self.speciality + ")"

    @property
    def title(self):
        return self.name


class Product_Category(TimeStamp):
    product_name = models.CharField(max_length=100)

    def __str__(self):
        return self.product_name


class Product(TimeStamp):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, null=True, blank=True)
    image1 = models.ImageField(upload_to='product/', null=True, blank=True)
    image2 = models.ImageField(upload_to='product/',null=True, blank=True)
    image3 = models.ImageField(upload_to='product/',null=True, blank=True)
    image4 = models.ImageField(upload_to='product/',null=True, blank=True)
    details = models.TextField(max_length=512)
    price = models.FloatField(max_length= 200)
    product_category = models.ForeignKey(Product_Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="product_category")


class Subscriber(TimeStamp):
    email = models.EmailField(max_length=200)

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['-id']


class Blog(TimeStamp):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, null=True, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='blogs/')
    email = models.ManyToManyField(Subscriber)

    def __str__(self):
        return self.title


class Event(TimeStamp):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    image = models.ImageField(upload_to='events/')
    detail = models.TextField()
    date = models.DateTimeField()
    venue = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Facility(TimeStamp):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    image = models.ImageField(upload_to='facility/')
    detail = models.TextField()

    def __str__(self):
        return self.title


class ImageGallery(TimeStamp):
    image = models.ImageField(upload_to='gallery/')
    title = models.CharField(max_length=250, null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.image.url

    class Meta:
        ordering = ['-id']


class Notice(TimeStamp):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, null=True, blank=True)
    detail = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-id']


class PageDropdown(TimeStamp):
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.title


class Page(TimeStamp):
    title = models.ForeignKey(
        PageDropdown, on_delete=models.CASCADE, related_name="pages")
    slug = models.SlugField(unique=True, null=True, blank=True)
    image = models.ImageField(upload_to='pages')
    content = models.TextField()

    def __str__(self):
        return self.slug


class PopUp(TimeStamp):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='popup/')
    message = models.TextField()
    show = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-id']


class Order(TimeStamp):
    quantity = models.PositiveIntegerField()
    product = models.ForeignKey(Product, on_delete=models.PROTECT, null=True, blank = True)


class Client(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.PROTECT, null=True, blank=True)
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='orders',null=True, blank=True)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    date = models.DateField(null=True, blank=True)
    image = models.ImageField(
        upload_to='user/', blank=True, null=True)


class Service(TimeStamp):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    image = models.ImageField(upload_to='services/')
    detail = models.TextField()

    def __str__(self):
        return self.title


class Schedule(TimeStamp):
    trainer = models.ForeignKey(
        Trainer, on_delete=models.CASCADE, related_name='schedules')
    day = models.CharField(max_length=20, choices=DAY)
    arrival = models.TimeField(max_length=30)
    departure = models.TimeField(max_length=30)
    details = models.CharField(max_length=512)

    def __str__(self):
        return self.doctor.name


class Slider(TimeStamp):
    title = models.CharField(max_length=200)
    about = models.CharField(max_length=200)
    image = models.ImageField(upload_to='sliders/')

    def __str__(self):
        return self.title


class Testimonial(TimeStamp):
    written_by = models.CharField(max_length=200)
    relation = models.CharField(max_length=100)
    testimonial = models.TextField(max_length=400)
    image = models.ImageField(upload_to='testimonials/')

    def __str__(self):
        return self.written_by

    class Meta:
        ordering = ['-id']


class VideoGallery(TimeStamp):
    title = models.CharField(max_length=200)
    video_link = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-id']

User = settings.AUTH_USER_MODEL


class CartManager(models.Manager):
    def new_or_get(self, request):
        cart_id = request.session.get('cart_id', None)
        print(cart_id,11111111111111111)
        qs = self.get_queryset().filter(id=cart_id)

        if qs.count() == 1:
            new_obj = False
            cart_obj = qs.first()
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = Cart.objects.new(user=request.user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id
        return cart_obj, new_obj

    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)


# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank=True)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    objects = CartManager()

    def __str__(self):
        return str(self.id)


def pre_save_cart_receiver(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        products = instance.products.all()
        total = 0
        for x in products:
            total += x.price
        instance.total = total
        instance.save()


m2m_changed.connect(pre_save_cart_receiver, sender=Cart.products.through)


def all_pre_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(all_pre_save, sender=Notice)
pre_save.connect(all_pre_save, sender=Page)
pre_save.connect(all_pre_save, sender=Trainer)
pre_save.connect(all_pre_save, sender=Service)
pre_save.connect(all_pre_save, sender=Blog)
pre_save.connect(all_pre_save, sender=Event)
pre_save.connect(all_pre_save, sender=Facility)
pre_save.connect(all_pre_save, sender=ImageGallery)
pre_save.connect(all_pre_save, sender=PageDropdown)


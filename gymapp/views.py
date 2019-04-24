from django.views.generic import *
from .models import *
from .forms import *
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.core.mail import send_mail
from django.urls import reverse, reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from urllib.parse import urlparse, parse_qs
from django.http import Http404
from django.http import HttpResponse
from django.contrib.auth.models import User, Group
from django.http import HttpResponseRedirect
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.db.models import signals
from django.core.exceptions import ValidationError
from django.contrib import messages
from urllib.parse import urlparse
# CLIENT VIEWS
# CLIENT VIEWS
# CLIENT VIEWS
# CLIENT VIEWS


class ClientMixin(object):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['organization'] = Organization.objects.get(id=1)
        context['clienttestimoniallist'] = Testimonial.objects.all()
        context['clientproductlist'] = Product.objects.all()
        context['clienttrainerlist'] = Trainer.objects.all()
        context['clienteventlist'] = Event.objects.all()
        context['clientloginform'] = ClientLoginForm
        context['clientcreateform'] = ClientRegistrationForm
        # context['clientappointmentform'] = ClientAppointmentForm
        context['clientsubscriberform'] = ClientSubscriberForm
        context['clientschedulelist'] = Schedule.objects.all()
        context['clientpagedropdown'] = PageDropdown.objects.all()
        print(self.request.session.get('cart_id'))
        if self.request.session.get('cart_id'):
            context['cart'] = Cart.objects.get(id = self.request.session.get('cart_id'))
        return context


class ClientPageNotFoundView(ClientMixin, TemplateView):
    template_name = "clienttemplates/404.html"


class ClientHomeView(ClientMixin, SuccessMessageMixin, TemplateView):
    template_name = "clienttemplates/clienthome.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clientservicelist'] = Service.objects.all()
        context['clientsliderlist'] = Slider.objects.all()
        context['clientpopup'] = PopUp.objects.first()
        return context


class ClientAboutView(ClientMixin, TemplateView):
    template_name = "clienttemplates/clientabout.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clienttrainerlist'] = Trainer.objects.all()
        context['testimoniallist'] = Testimonial.objects.all()
        return context


class ClientContactCreateView(ClientMixin, SuccessMessageMixin, CreateView):
    template_name = "clienttemplates/clientcontact.html"
    form_class = ClientContactForm
    success_url = '/'
    success_message = 'We will be in contact with you soon'


# class ClientAppointmentCreateView(ClientMixin, SuccessMessageMixin, CreateView):
#     template_name = "clienttemplates/clientbase.html"
#     form_class = ClientAppointmentForm
#     success_url = reverse_lazy("gymapp:clienthome")
#     success_message = 'Your Appointment is Booked.'

#     def form_valid(self, form):
#         if self.request.POST.get('selects'):
#             form.instance.doctor = Doctor.objects.get(
#                 slug=self.request.POST.get('selects'))

#         return super().form_valid(form)


class ClientSubscriberCreateView(ClientMixin, SuccessMessageMixin, CreateView):
    template_name = "clienttemplates/clienthome.html"
    form_class = ClientSubscriberForm
    success_url = reverse_lazy("gymapp:clienthome")
    success_message = 'You have been Subscribed'

    def form_valid(self, form):
        # self.object = form.save()
        subject = 'Registration Confirmation'
        message = 'Thank you for registering.'
        email_from = 'settings.EMAIL_HOST_USER'
        recipient_list = [form.instance.email]
        send_mail(subject, message, email_from,
                  recipient_list, fail_silently=False)
        return super().form_valid(form)


class ClientTrainerListView(ClientMixin, ListView):
    template_name = "clienttemplates/clienttrainerlist.html"
    model = Trainer
    context_object_name = 'clienttrainerlist'


class ClientProductListView(ClientMixin, ListView):
    template_name = "clienttemplates/clientproductlist.html"
    model = Product
    context_object_name = 'clientproductlist'


class ClientProductDetailView(ClientMixin, DetailView):
    template_name = "clienttemplates/clientproductdetail.html"
    model = Product
    context_object_name = 'clientproductdetail'


class ClientCartTotalView(ClientMixin, DetailView):
    template_name = "clienttemplates/clientcarttotal.html"
    model = Cart
    context_object_name = 'clientcarttotal'

    def get_object(self,*args,**kwargs):
        cart = Cart.objects.get(id = self.kwargs.get('pk'))
        cart.user = self.request.user
        cart.save()

        qs = Cart.objects.get(id = self.kwargs.get('pk'))
        return qs


class ClientScheduleListView(ClientMixin, ListView):
    template_name = "clienttemplates/clientschedulelist.html"
    model = Schedule
    context_object_name = 'clientschedulelist'


class SearchResultView(ClientMixin, TemplateView):
    template_name = 'clienttemplates/clientsearchresult.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        if query:
            lookup = Q(title__icontains=query)
            slist = Blog.objects.filter(lookup)
            context["slist"] = slist
        return context


class ClientTrainerDetailView(ClientMixin, DetailView):
    template_name = "clienttemplates/clienttrainerdetail.html"
    model = Trainer
    context_object_name = 'clienttrainerdetail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clienttrainerlist'] = Trainer.objects.all()
        context['sundayschedules'] = Schedule.objects.filter(
            trainer__slug=self.kwargs['slug'], day="sunday")
        context['mondayschedules'] = Schedule.objects.filter(
            trainer__slug=self.kwargs['slug'], day="monday")
        context['tuesdayschedules'] = Schedule.objects.filter(
            trainer__slug=self.kwargs['slug'], day="tuesday")
        context['wednesdayschedules'] = Schedule.objects.filter(
            trainer__slug=self.kwargs['slug'], day="wednesday")
        context['thursdayschedules'] = Schedule.objects.filter(
            trainer__slug=self.kwargs['slug'], day="thursday")
        context['fridayschedules'] = Schedule.objects.filter(
            trainer__slug=self.kwargs['slug'], day="friday")
        context['saturdayschedules'] = Schedule.objects.filter(
            trainer__slug=self.kwargs['slug'], day="saturday")
        return context


class ClientScheduleDetailView(ClientMixin, DetailView):
    template_name = "clienttemplates/clientscheduledetail.html"
    model = Schedule
    context_object_name = 'clientscheduledetail'


class ClientPageDetailView(ClientMixin, DetailView):
    template_name = "clienttemplates/clientpagedetail.html"
    model = Page
    context_object_name = 'clientpagedetail'


class ClientServiceListView(ClientMixin, ListView):
    template_name = "clienttemplates/clientservicelist.html"
    paginate_by = 3
    model = Service
    context_object_name = 'clientservicelist'


class ClientServiceDetailView(ClientMixin, DetailView):
    template_name = "clienttemplates/clientservicedetail.html"
    model = Service
    context_object_name = 'clientservicedetail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clientservicelist'] = Service.objects.all()
        return context


class TestimonialListView(ClientMixin, ListView):
    template_name = "clienttemplates/clientabout.html"
    model = Testimonial
    context_object_name = 'testimoniallist'


# class SliderListView(ClientMixin, ListView):
#     template_name = "clienttemplates/clienthome.html"
#     model = Slider
#     context_object_name = 'clientsliderlist'


class ClientFacilityListView(ClientMixin, ListView):
    template_name = "clienttemplates/clientfacilitylist.html"
    model = Facility
    paginate_by = 3
    context_object_name = 'clientfacilitylist'


class ClientFacilityDetailView(ClientMixin, DetailView):
    template_name = "clienttemplates/clientfacilitydetail.html"
    model = Facility
    context_object_name = 'clientfacilitydetail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clientfacilitylist'] = Facility.objects.all()
        return context


class ClientNoticeListView(ClientMixin, ListView):
    template_name = "clienttemplates/clientnoticelist.html"
    model = Notice
    context_object_name = 'clientnoticelist'


class ClientNoticeDetailView(ClientMixin, DetailView):
    template_name = "clienttemplates/clientnoticedetail.html"
    model = Notice
    context_object_name = 'clientnoticedetail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clientnoticelist'] = Notice.objects.all()
        return context


class ClientEventListView(ClientMixin, ListView):
    template_name = "clienttemplates/clienteventlist.html"
    model = Event
    context_object_name = 'clienteventlist'


class ClientEventDetailView(ClientMixin, DetailView):
    template_name = "clienttemplates/clienteventdetail.html"
    model = Event
    context_object_name = 'clienteventdetail'


class ClientImageListView(ClientMixin, ListView):
    template_name = "clienttemplates/clientimagelist.html"
    model = ImageGallery
    context_object_name = 'clientimagelist'


class ClientVideoListView(ClientMixin, ListView):
    template_name = "clienttemplates/clientvideolist.html"
    model = VideoGallery
    context_object_name = 'clientvideolist'


class ClientBlogListView(ClientMixin, ListView):
    template_name = "clienttemplates/clientbloglist.html"
    model = Blog
    paginate_by = 3
    context_object_name = 'clientbloglist'


class ClientBlogDetailView(ClientMixin, DetailView):
    template_name = "clienttemplates/clientblogdetail.html"
    model = Blog
    context_object_name = 'clientblogdetail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clientbloglist'] = Blog.objects.all()
        return context



class ClientLoginView(FormView):
    template_name = 'clienttemplates/clienthome.html'
    success_url = reverse_lazy("gymapp:clienthome")
    form_class = ClientLoginForm  

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            if Admin.objects.filter(user=user).exists():
                messages.success(self.request,'You were successfully logged in.')
                return redirect('gymapp:clientabout')
            elif Client.objects.filter(user=user).exists():
                messages.success(self.request,'You were successfully logged in.')
                return redirect('gymapp:clienthome')
        else:
            return redirect('gymapp:clienthome')
        return super().form_valid(form)

    def get_success_url(self, *args, **kwargs):
        self.next_url = self.request.POST.get('next')
        if self.next_url is not None:
            return self.next_url
        else:
            return self.success_url



# class ClientLoginView(SuccessMessageMixin,FormView):
#     template_name = 'clienttemplates/clienthome.html'
#     form_class = ClientLoginForm
#     success_url = reverse_lazy("gymapp:clienthome")
#     success_message = 'Logged in successfully'

    # def get_context_data(self,*args,**kwargs):
    #     context = super().get_context_data(*args,**kwargs)
    #     print(111111111111111111111,context)
    #     return context

#     # def get(self, request):
#     #     if request.user.is_authenticated:
#     #         return render(self.request, 'clienttemplates/home.html')
#     #     return super().get(request)

#     def form_valid(self, form):
#         username = form.cleaned_data['username']
#         password = form.cleaned_data['password']
#         user = authenticate(username=username,
#                             password=password)

#         # if user is not None and user.is_staff:
#         if user and not user.is_staff:
#             login(self.request, user)
#             print("--------------------------------------")
#         else:
#             return render(self.request, self.template_name, {
#                 'form': form,
#                 'errors': "Please correct username or password"})
#             print("##############################################")

#         return super().form_valid(form)

#     def dispatch(self,*args,**kwargs):
#         if self.request.user.is_authenticated:
#             return redirect('gymapp:clienthome')
#         return super().dispatch(*args,**kwargs)

#     def get_success_url(self, *args, **kwargs):
#         self.next_url = self.request.POST.get('next')
#         if self.next_url is not None:
#             return self.next_url
#         else:
#             return self.success_url


class ClientLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('gymapp:clienthome')


class ClientRegistrationView(CreateView):
    template_name = 'clienttemplates/clienthome.html'
    form_class = ClientRegistrationForm
    success_url = reverse_lazy('gymapp:clienthome')
    success_message = "Client created successfully"

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        user = User.objects.create_user(username, password)
        group = Group.objects.get(name="Client")
        group.user_set.add(user)
        user.set_password(password)
        user.save()
        print(user)
        return super().form_valid(form)


def cart_detail_api_view(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    products = [{
        "name": x.name,
        "price": x.name
    } for x in cart_obj.products.all()]  #[object,object,object]
    return JsonResponse({"products": products})


def cart_update(request):
    product_id = request.POST.get('product')
    print(product_id)
    if product_id is not None:
        product_obj = Product.objects.get(id=product_id)
        print(product_obj)
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
            product_added = False
        else:
            cart_obj.products.add(product_obj)
            product_added = True
        # return redirect(product_obj.get_absolute_url())
        request.session['cart_items'] = cart_obj.products.count()


        if request.is_ajax():
            print("ajax request")
            data = {
                "added": product_added,
                "cart_item_count": cart_obj.products.count()
            }
            return JsonResponse(data)
    return redirect("gymapp:clientproductlist")




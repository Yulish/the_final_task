from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.views import View
from django.contrib import messages
from django.contrib.auth import get_user_model, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, get_object_or_404, redirect, resolve_url, reverse
from django.core.mail import send_mail
from django.core.files.storage import default_storage
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseForbidden
from django.utils.decorators import method_decorator
from urllib.parse import urlparse, parse_qs
from .models import Poster, Category, Response, EmailVerification
from .filters import PosterFilter, ResponseFilter
from .forms import ProfileForm, Add_Change_Form, ResponseAcceptForm, ResponseForm
from datetime import datetime, timezone
import os

User = get_user_model()


class ProfileView(LoginRequiredMixin, View):

    def get(self, request, pk):
        user = get_object_or_404(User, id=pk)
        return render(request, 'profile.html', {'profile_user': user})


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    form_class = ProfileForm
    model = User
    template_name = 'profile_update.html'

    def get_form_class(self):
        return ProfileForm

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('profile', args=[pk]))
        else:
            return render(request, 'profile_update.html', {'form': form, 'user': user})

class PosterList(ListView):
    model = Poster
    queryset = Poster.objects.order_by('-poster_origin')
    template_name = 'poster.html'
    context_object_name = 'poster'

    paginate_by = 5
    items = list(range(1, len(Poster.objects.all()) + 1))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        user_id = self.request.GET.get('user_id')
        if user_id:
            filtered_posters = Poster.objects.filter(user__id=user_id)
            paginator = Paginator(filtered_posters, self.paginate_by)
            page_number = self.request.GET.get('page', 1)
            page_obj = paginator.get_page(page_number)
            context['page_obj'] = page_obj
            context['paginator'] = paginator
            context['is_paginated'] = True
        else:
            pass
        my_posters = Poster.objects.filter(user=user)
        context['my_posters'] = my_posters
        context['time_now'] = datetime.now(timezone.utc)
        context['categories'] = Category.objects.all()
        context['next_category'] = None
        context['filterset'] = self.filterset
        category_id = self.request.GET.get('category_id')
        page_obj = context.get('page_obj')
        if page_obj:
            for poster in page_obj:
                poster.responses_list = Response.objects.filter(poster=poster)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PosterFilter(self.request.GET, queryset)
        category_id = self.request.GET.get('category_id')
        if category_id:
            queryset = queryset.filter(categories__id=category_id)

        user_id = self.request.GET.get('user_id')
        if user_id:
            queryset = queryset.filter(user__id=user_id)
        return self.filterset.qs.order_by('-poster_origin')


class PosterCategory(PosterList):
    model = Poster
    template_name = 'category.html'
    context_object_name = 'category'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Poster.objects.filter(categories=self.category).order_by('-poster_origin')
        return queryset


class PosterDetail(LoginRequiredMixin, DetailView):
    model = Poster
    template_name = 'id.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        poster = self.get_object()
        context['active_responses'] = Response.objects.filter(poster=poster, status=False)
        context['accepted_responses'] = Response.objects.filter(poster=poster, status=True)
        return context

    def get_queryset(self):
        return Poster.objects.filter(user=self.request.user).order_by('-poster_origin')

    def get_object(self):
        return get_object_or_404(Poster, pk=self.kwargs['pk'])



class PosterAdd(LoginRequiredMixin, CreateView):

    model = Poster
    form_class = Add_Change_Form
    template_name = 'create.html'
    success_url = reverse_lazy('posters')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)



class PosterChange(LoginRequiredMixin, UpdateView):
    model = Poster
    form_class = Add_Change_Form
    template_name = 'poster_update.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('poster_detail', kwargs={'pk': self.kwargs['pk']})



class PosterDelete(LoginRequiredMixin, DeleteView):
    model = Poster
    template_name = 'poster_delete.html'

    def get_success_url(self):
        user_id = self.request.GET.get('user_id')
        url = reverse('posters')
        if user_id:
            url += f'?user_id={user_id}'
        return url


class ResponseCreate(LoginRequiredMixin, CreateView):
    model = Response
    template_name = 'response.html'
    form_class = ResponseForm

    def get_success_url(self):
        return reverse('poster_detail', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        poster = get_object_or_404(Poster, pk=self.kwargs['pk'])
        context['poster'] = poster
        return context

    def form_valid(self, form):
        poster = get_object_or_404(Poster, pk=self.kwargs['pk']) # Получаем постер по pk из URL
        form.instance.poster = poster # Связываем отклик с постером
        form.instance.sender = self.request.user # Связываем с пользователем
        form.instance.receiver = poster.user
        return super().form_valid(form)



class ResponseAccept(LoginRequiredMixin, UpdateView):
    model = Response
    form_class = ResponseAcceptForm
    template_name = 'response_accept.html'
    success_url = reverse_lazy('poster_detail')

    def get_queryset(self):
        return super().get_queryset().filter(poster__user=self.request.user) # Только отклики на постеры текущего пользователя

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        response = get_object_or_404(Response, pk=self.kwargs['pk'])
        context['response'] = response  #  в шаблон для отображения
        context['poster'] = response.poster
        return context

    def form_valid(self, form):
        response = get_object_or_404(Response, pk=self.kwargs['pk'])
        form.instance.status = True
        self.success_url = reverse_lazy('responses', kwargs={'pk': self.request.user.pk})
        return super().form_valid(form)


class ResponseList(ListView):
    model = Response
    queryset = Response.objects.order_by('-response_origin')
    template_name = 'my_responses.html'
    context_object_name = 'responses'
    paginate_by = 5
    items = list(range(1, len(Response.objects.all()) + 1))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        accepted_count = Response.objects.filter(receiver=user, status=True).count()
        context['accepted_count'] = accepted_count
        context['time_now'] = datetime.now(timezone.utc)
        context['filterset'] = self.filterset
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(receiver=self.request.user)
        self.filterset = ResponseFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs.order_by('-response_origin')


class ResponseDetail(DetailView):
    model = Response
    template_name = 'response_detail.html'
    context_object_name = 'response_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        response = self.get_object()
        poster = response.poster
        context['poster'] = poster
        context['accepted_responses'] = Response.objects.filter(poster=poster, status=True)
        context['pending_responses'] = Response.objects.filter(poster=poster, status=False)
        context['responses'] = Response.objects.filter(poster=poster).distinct()
        context['accepted_count'] = Response.objects.filter(poster=poster, status=True).count()
        return context

    def get_queryset(self):
        return Response.objects.filter(receiver=self.request.user)  # user видит только свои отклики

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.receiver != self.request.user:
            return get_object_or_404(Response, pk=self.kwargs['pk'], receiver=self.request.user)
        return obj



class AcceptedResponses(ListView):
    model = Response
    template_name = 'accepted_responses.html'
    context_object_name = 'accepted_responses'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        return Response.objects.filter(receiver=user, status=True).order_by('-response_origin')


class ResponseDelete(DeleteView):
    model = Response
    template_name = 'response_delete.html'

    def get_success_url(self):
        return reverse_lazy('responses', kwargs={'pk': self.request.user.pk})

class StartView(TemplateView):
    template_name = 'account/login.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'Добро пожаловать!'
        return context

def my_logout(request):
    template_name = 'account/logout.html'
    logout(request)
    return redirect('account_login')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Пользователь с таким email уже существует.')
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_active = False
        user.save()

        verification = EmailVerification.objects.create(user=user)
        verification.generate_code()

        subject = 'Ваш код подтверждения'
        message = f'Ваш код: {verification.code}'
        from_email = 'ishmakova1@yandex.ru'
        recipient_list = [email]

        send_mail(subject, message, from_email, recipient_list)
        messages.success(request, 'Код отправлен на ваш email. Проверьте почту.')
        return redirect('verify_code', user_id=user.id)

    return render(request, 'register.html')

def verify_code_view(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        code = request.POST.get('code')
        verification = EmailVerification.objects.get(user=user)
        if verification.code == code:
            user.is_active = True
            user.save()
            verification.delete()
            messages.success(request, 'Регистрация завершена! Теперь войдите.')
            return redirect('profile', pk=user.id)

        else:
            messages.error(request, 'Неверный код.')
        return redirect('register')
    return render(request, 'verify_code.html', {'user_id': user_id})



# для отмены ограничения по добавлению медиа
def custom_upload(request):
    upload_file = request.FILES.get('upload')
    if not upload_file:
        return JsonResponse({'uploaded': 0, 'error': {'message': 'No file uploaded'}})

    filename = upload_file.name
    upload_path = os.path.join('uploads', filename)

    saved_path = default_storage.save(upload_path, upload_file)
    url = default_storage.url(saved_path)

    return JsonResponse({'uploaded': 1, 'fileName': filename, 'url': url})
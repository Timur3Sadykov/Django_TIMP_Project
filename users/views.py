from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserOurRegistration, UserUpdateForm
from django.contrib import messages
from .models import GreenHouse, TController, LController, WController
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.core.mail import send_mail
from decimal import Decimal
from django.utils import timezone, dateformat
from django.http import HttpResponse
import matplotlib.pyplot as plt
from datetime import date, datetime

def Connection(request):
    if request.method == "GET":
        UID = request.GET.get('UID')
        tc = TController.objects.get(UUID=UID)
        tc.t = Decimal(request.GET.get('t'))
        tc.old = tc.old + '; ' + dateformat.format(timezone.now(), 'Y-m-d H:i:s') + ': ' + request.GET.get('t')
        tc.save()
        if tc.t < tc.tmin or tc.t > tc.tmax:
            mail = (f'Опасная температура: {tc.t} градусов в теплице {tc.house}')
            send_mail('Теплица', mail, 'sadykov.tf98@gmail.com', [tc.house.owner.email], fail_silently=False)
        return JsonResponse({'name': tc.name, 'vstart': tc.vstart, 'vstop': tc.vstop,
        'hstart': tc.hstart, 'hstop': tc.hstop, 'tmin': tc.tmin, 'tmax': tc.tmax, 'refresh': tc.refresh})

    return JsonResponse({'Status': 'NO'})

def FirstConnection(request):
    if request.method == "GET":
        tc = TController.objects.filter(status=False).first()
        #tc = TController.objects.last()
        if tc.status == False:
            tc.status = True
            tc.t = Decimal(request.GET.get('t'))
            tc.old = dateformat.format(timezone.now(), 'Y-m-d H:i:s') + ': ' + request.GET.get('t')
            tc.save()
            return JsonResponse({'UUID': tc.UUID, 'name': tc.name, 'vstart': tc.vstart, 'vstop': tc.vstop,
            'hstart': tc.hstart, 'hstop': tc.hstop, 'tmin': tc.tmin, 'tmax': tc.tmax, 'refresh': tc.refresh})

    return JsonResponse({'Status': 'NO'})

def ControllerDetail(request, pk):
    tc = TController.objects.get(UUID=pk)
    list = []
    list1 = []
    x = dict(e.split(': ') for e in tc.old.split('; '))
    for key, value in x.items():
        date = key
        val = value
        list.append(date)
        list1.append(val)
    plt.plot(list, list1)
    plt.show()
    return redirect('house-detail', tc.house.pk)

class DeleteTControllerView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = TController
    success_url = '/house'

    def test_func(self):
        house = self.get_object().house
        if self.request.user == house.owner:
            return True
        return False

class UpdateTControllerView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = TController
    fields = ['name', 'vstart', 'vstop', 'hstart', 'hstop', 'tmin', 'tmax', 'refresh']

    def form_valid(self, form):
        #form.instance.house = GreenHouse.objects.filter(pk=self.kwargs['pk']).first()
        return super().form_valid(form)

    def test_func(self):
        house = self.get_object().house
        if self.request.user == house.owner:
            return True
        return False

class CreateTControllerView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = TController
    fields = ['name', 'vstart', 'vstop', 'hstart', 'hstop', 'tmin', 'tmax', 'refresh']

    def form_valid(self, form):
        form.instance.house = GreenHouse.objects.filter(pk=self.kwargs['pk']).first()
        return super().form_valid(form)

    def test_func(self):
        house = GreenHouse.objects.filter(pk=self.kwargs['pk']).first()
        if self.request.user == house.owner:
            return True
        return False

def LConnection(request):
    d = 0
    if request.method == "GET":
        UID = request.GET.get('UID')
        lc = LController.objects.get(UUID=UID)
        lc.light = int(request.GET.get('light'))
        lc.old = lc.old + '; ' + dateformat.format(timezone.now(), 'Y-m-d H:i:s') + ': ' + request.GET.get('light')
        lc.save()
        now = timezone.now().time()
        if now > lc.LightDayStart and now < lc.LightDayStop and lc.light < 70:
            d = datetime.combine(date.today(), lc.LightDayStop) - datetime.combine(date.today(), now)
            d = d.total_seconds()
        return JsonResponse({'name': lc.name, 'time': d, 'refresh': lc.refresh})

    return JsonResponse({'Status': 'NO'})

def LFirstConnection(request):
    d = 0
    if request.method == "GET":
        lc = LController.objects.last()
        if lc.status == False:
            lc.status = True
            lc.light = int(request.GET.get('light'))
            lc.old = dateformat.format(timezone.now(), 'Y-m-d H:i:s') + ': ' + request.GET.get('light')
            lc.save()
            now = timezone.now().time()
            if now > lc.LightDayStart and now < lc.LightDayStop and lc.light < 70:
                d = datetime.combine(date.today(), lc.LightDayStop) - datetime.combine(date.today(), now)
                d = d.total_seconds()
            return JsonResponse({'UUID': lc.UUID, 'name': lc.name, 'time': d, 'refresh': lc.refresh})

    return JsonResponse({'Status': 'NO'})

def LControllerDetail(request, pk):
    lc = LController.objects.get(UUID=pk)
    list = []
    list1 = []
    x = dict(e.split(': ') for e in lc.old.split('; '))
    for key, value in x.items():
        date = key
        val = value
        list.append(date)
        list1.append(val)
    plt.plot(list, list1)
    plt.show()
    return redirect('house-detail', lc.house.pk)

class DeleteLControllerView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = LController
    success_url = '/house'
    template_name = "users/TController_confirm_delete.html"

    def test_func(self):
        house = self.get_object().house
        if self.request.user == house.owner:
            return True
        return False

class UpdateLControllerView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = LController
    fields = ['name', 'LightDayStart', 'LightDayStop', 'refresh']
    template_name = "users/TController_form.html"

    def form_valid(self, form):
        #form.instance.house = GreenHouse.objects.filter(pk=self.kwargs['pk']).first()
        return super().form_valid(form)

    def test_func(self):
        house = self.get_object().house
        if self.request.user == house.owner:
            return True
        return False

class CreateLControllerView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = LController
    fields = ['name', 'LightDayStart', 'LightDayStop', 'refresh']
    template_name = "users/TController_form.html"

    def form_valid(self, form):
        form.instance.house = GreenHouse.objects.filter(pk=self.kwargs['pk']).first()
        return super().form_valid(form)

    def test_func(self):
        house = GreenHouse.objects.filter(pk=self.kwargs['pk']).first()
        if self.request.user == house.owner:
            return True
        return False

def WConnection(request):
    if request.method == "GET":
        UID = request.GET.get('UID')
        lc = WController.objects.get(UUID=UID)
        lc.water = int(request.GET.get('water'))
        lc.old = lc.old + '; ' + dateformat.format(timezone.now(), 'Y-m-d H:i:s') + ': ' + request.GET.get('water')
        lc.save()
        return JsonResponse({'name': lc.name, 'start': lc.WaterStart, 'stop': lc.WaterStop, 'refresh': lc.refresh})

    return JsonResponse({'Status': 'NO'})

def WFirstConnection(request):
    if request.method == "GET":
        lc = WController.objects.last()
        if lc.status == False:
            lc.status = True
            lc.water = int(request.GET.get('water'))
            lc.old = dateformat.format(timezone.now(), 'Y-m-d H:i:s') + ': ' + request.GET.get('water')
            lc.save()
            return JsonResponse({'UUID': lc.UUID, 'name': lc.name, 'start': lc.WaterStart, 'stop': lc.WaterStop, 'refresh': lc.refresh})

    return JsonResponse({'Status': 'NO'})

def WControllerDetail(request, pk):
    lc = WController.objects.get(UUID=pk)
    list = []
    list1 = []
    x = dict(e.split(': ') for e in lc.old.split('; '))
    for key, value in x.items():
        date = key
        val = value
        list.append(date)
        list1.append(val)
    plt.plot(list, list1)
    plt.show()
    return redirect('house-detail', lc.house.pk)

class DeleteWControllerView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = WController
    success_url = '/house'
    template_name = "users/TController_confirm_delete.html"

    def test_func(self):
        house = self.get_object().house
        if self.request.user == house.owner:
            return True
        return False

class UpdateWControllerView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = WController
    fields = ['name', 'WaterStart', 'WaterStop', 'refresh']
    template_name = "users/TController_form.html"

    def form_valid(self, form):
        #form.instance.house = GreenHouse.objects.filter(pk=self.kwargs['pk']).first()
        return super().form_valid(form)

    def test_func(self):
        house = self.get_object().house
        if self.request.user == house.owner:
            return True
        return False

class CreateWControllerView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = WController
    fields = ['name', 'WaterStart', 'WaterStop', 'refresh']
    template_name = "users/TController_form.html"

    def form_valid(self, form):
        form.instance.house = GreenHouse.objects.filter(pk=self.kwargs['pk']).first()
        return super().form_valid(form)

    def test_func(self):
        house = GreenHouse.objects.filter(pk=self.kwargs['pk']).first()
        if self.request.user == house.owner:
            return True
        return False

class ShowHouseView(LoginRequiredMixin, ListView):
    model = GreenHouse
    template_name = "users/house.html"
    context_object_name = 'house'
    # ordering = ['-date']

    def get_queryset(self):
        return GreenHouse.objects.filter(owner = self.request.user).order_by('date')

    def get_context_data(self, **kwards):
        ctx = super(ShowHouseView, self).get_context_data(**kwards)
#        ctx.update({
#            'TController': TController.objects.all,
#        })
        ctx['title'] = 'Личный кабинет'
        return ctx

class HouseDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = GreenHouse

    def get_context_data(self, **kwards):
        ctx = super(HouseDetailView, self).get_context_data(**kwards)
        ctx.update({
            'TController': TController.objects.all,
            'LController': LController.objects.all,
            'WController': WController.objects.all,
        })
        ctx['title'] = GreenHouse.objects.filter(pk=self.kwargs['pk']).first()
        return ctx

    def test_func(self):
        house = GreenHouse.objects.filter(pk=self.kwargs['pk']).first()
        if self.request.user == house.owner:
            return True
        return False

class CreateHouseView(LoginRequiredMixin, CreateView):
    model = GreenHouse
    fields = ['name']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class UpdateHouseView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = GreenHouse
    fields = ['name']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        house = self.get_object()
        if self.request.user == house.owner:
            return True
        return False

class DeleteHouseView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = GreenHouse
    success_url = '/house'

    def test_func(self):
        house = self.get_object()
        if self.request.user == house.owner:
            return True
        return False

def register(request):
    if request.method == "POST":
        form = UserOurRegistration(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккауент {username} был создан. Введите имя пользователя и пароль для авторизации')
            return redirect('user')
    else:
        form = UserOurRegistration()
    return render(request, 'users/registration.html', {'form': form, 'title':'Регистрация'})

@login_required
def profile(request):
    if request.method == "POST":
        update_user = UserUpdateForm(request.POST, instance=request.user)

        if update_user.is_valid():
            update_user.save()
            messages.success(request, f'Аккауент {username} был успешно изменен')
            return redirect('profile')

    else:
        update_user = UserUpdateForm(instance=request.user)

    data = {
        'update_user': update_user
    }

    return render(request, 'users/profile.html', data)

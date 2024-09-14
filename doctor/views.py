from datetime import datetime
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django import forms
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Doctor, Visit
from .forms import BookingForm
from django.utils import timezone
from .models import Doctor

class DoctorListView(LoginRequiredMixin,ListView):
    model = Doctor
    template_name = 'doctor/forms/doctorList.html'
    
    def get_queryset(self):
        return Doctor.objects.filter(
            is_active = True).values(
                'user__full_name', 'specialty__spec_name'
            )
    
    
class DoctorSearchView(LoginRequiredMixin,ListView):
    model = Doctor
    template_name = 'doctor/forms/doctorSearch.html'
    
    def get_queryset(self):
        search_item = self.request.GET.get('search_item', '')
        if search_item:
            return Doctor.objects.filter(
                Q(specialty__icontains=search_item) | 
                Q(user__full_name__icontains=search_item )
            ).filter(is_active=True).values(
                'user__full_name', 'specialty__spec_name' ,'availability'
            )


class BookingForm(forms.Form):
    date = forms.DateField()
    time = forms.TimeField()


@login_required
def book_visit(request, doctor_id):
    doctor = get_object_or_404(Doctor, doctor_id=doctor_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            time = form.cleaned_data['time']
            datetime_combined = timezone.make_aware(datetime.combine(date, time))
            available_slots = doctor.get_available_slots(date)
            if time in available_slots:
                visit = Visit.objects.create(
                    doctor=doctor,
                    user=request.user,
                    date_time=datetime_combined
                )
                doctor.availability[date].remove(time.strftime('%H:%M'))
                doctor.save()

                return HttpResponse("Appointment booked successfully! Please proceed to payment.")
            else:
                return HttpResponse("Selected time is not available.", status=400)
    else:
        form = BookingForm()

    context = {
        'doctor': doctor,
        'form': form,
        'available_slots': doctor.get_available_slots(request.GET.get('date'))
    }
    return render(request, 'doctor/book_appointment.html', context)




def doctor_detail(request, doctor_id):
    doctor = get_object_or_404(Doctor, doctor_id=doctor_id)
    context = {
        'doctor': doctor,
        'available_slots': doctor.get_available_slots(datetime.now().strftime('%A').lower())
    }
    return render(request, 'doctor/doctor_detail.html', context)

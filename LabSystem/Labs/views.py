from collections import Counter
from django import contrib
import django
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from datetime import datetime, timedelta
from .models import *


def index(request):
    testers = Tester.objects.all().count()
    patients = Patient.objects.all().count()
    samples = Specimen.objects.all().count()
    vaccinations = Vaccination.objects.all().count()

    today_date = datetime.today()
    monthly_model = Specimen.objects.filter(
        date_taken__month=today_date.month, results='Positive').values_list("date_taken")
    monthly_count_rep = Counter([rep[0] for rep in monthly_model])
    monthly_amount_rep = {}

    for rep in monthly_count_rep:
        monthly_amount_rep[rep] = 0

    for month in monthly_model:
        for rep in monthly_amount_rep:
            if month[0] == rep:
                monthly_amount_rep[rep] += 1

    label = list(monthly_amount_rep.keys())
    data = list(monthly_amount_rep.values())

    monthly_model2 = Specimen.objects.filter(
        date_taken__month=today_date.month, results='Negative').values_list("date_taken")
    monthly_count_rep2 = Counter([rep[0] for rep in monthly_model2])
    monthly_amount_rep2 = {}

    for rep2 in monthly_count_rep2:
        monthly_amount_rep2[rep2] = 0

    for month in monthly_model2:
        for rep2 in monthly_amount_rep2:
            if month[0] == rep2:
                monthly_amount_rep2[rep2] += 1
    data2 = list(monthly_amount_rep2.values())

    # compute infection per county

    county_model = Specimen.objects.filter(
        date_taken__month=today_date.month, results='Positive').values_list("patient__county")
    county_count_rep = Counter([rep[0] for rep in county_model])
    county_amount_rep = {}

    for rep in county_count_rep:
        county_amount_rep[rep] = 0

    for month in county_model:
        for rep in county_amount_rep:
            if month[0] == rep:
                county_amount_rep[rep] += 1

    label3 = list(county_amount_rep.keys())
    data3 = list(county_amount_rep.values())

    context = {
        'label': label,
        'data': data,
        'data2': data2,
        'label3': label3,
        'data3': data3,
        'testers': testers,
        'patients': patients,
        'samples': samples,
        'vaccinations': vaccinations
    }
    return render(request, 'Labs/dashboard.html', context)


def register_tester(request):

    if request.method == 'GET':
        return render(request, 'Labs/register_tester.html')

    if request.method == 'POST':
        form = RegisterTester(request.POST or None, request.FILES)

        if form.is_valid():
            first_name = form.data['first_name']
            last_name = form.data['last_name']
            gender = form.data['gender']
            id_number = form.data['id_number']
            contact = form.data['contact']
            email = form.data['email']
            profession = form.data['profession']
            avatar = request.FILES['avatar']

            try:
                from PIL import Image
                Image.open(avatar)
            except:
                from django.contrib import messages
                messages.warning(request, 'Sorry your image is invalid')
                return redirect('Labs:index')

            Tester.objects.create(
                user=request.user,
                first_name=first_name.capitalize(),
                last_name=last_name.capitalize(),
                gender=gender,
                id_number=id_number,
                contact=contact,
                email=email,
                profession=profession,
                avatar=avatar,
            )
            from django.contrib import messages
            messages.success(request, 'Tester created Successfully.')
            return redirect('Labs:index')
        else:
            print(form.errors)
            from django.contrib import messages
            messages.warning(
                request, 'An error occurred. Try again later or contact the administrator.')
            return redirect('Labs:index')


def tester_list(request):

    all_testers = Tester.objects.filter(user=request.user)
    context = {
        'all_testers': all_testers,
    }
    return render(request, 'Labs/tester_list.html', context)


def tenant_details(request, pk):
    tester = Tester.objects.get(id=pk)
    context = {
        'tester': tester
    }
    return render(request, 'Labs/tester_details.html', context)


def delete_tester(request, pk):
    tester = Tester.objects.get(id=pk)

    tester.delete()
    messages.success(request, 'Tester record deleted successfully')
    return redirect('Labs:index')


def register_patient(request):

    if request.method == 'GET':
        return render(request, 'Labs/register_patient.html')

    if request.method == 'POST':
        form = RegisterPatient(request.POST or None)

        if form.is_valid():

            first_name = form.data['first_name']
            last_name = form.data['last_name']
            gender = form.data['gender']
            id_number = form.data['id_number']
            contact = form.data['contact']
            email = form.data['email']
            region = form.data['region']
            county = form.data['county']
            user = request.user
            location = form.data['location']

            all_patients = Patient.objects.all()

            for patient in all_patients:
                if id_number != '' and patient.id_number == id_number:
                    from django.contrib import messages
                    messages.warning(
                        request, 'Sorry, Patient with this Id Number is already Registered.')
                    return redirect('Labs:register_patient')

            Patient.objects.create(
                user=user,
                first_name=first_name.capitalize(),
                last_name=last_name.capitalize(),
                gender=gender,
                id_number=id_number,
                contact=contact,
                email=email,
                region=region,
                county=county,
                location=location,
            )
            from django.contrib import messages
            messages.success(request, 'Patient created Successfully.')
            return redirect('Labs:index')
        else:
            print(form.errors)
            from django.contrib import messages
            messages.warning(
                request, 'An error occurred. Try again later or contact the administrator.')
            return redirect('Labs:index')


def patient_list(request):
    all_patients = Patient.objects.filter(user=request.user)
    context = {
        'all_patients': all_patients,
    }
    return render(request, 'Labs/patient_list.html', context)


def patients_details(request, pk):
    patient = Patient.objects.get(id=pk)

    previous_testings = Specimen.objects.filter(patient=patient)
    previous_vaccinations = Vaccination.objects.filter(patient=patient)
    context = {
        'patient': patient,
        'previous_testings': previous_testings,
        'previous_vaccinations': previous_vaccinations,
    }
    return render(request, 'Labs/patient_details.html', context)


def delete_patient(request, pk):
    patient = Patient.objects.get(id=pk)
    patient.delete()
    messages.success(request, 'The patient was deleted successfully.')
    return redirect('Labs:index')


def register_sample(request):

    if request.method == 'GET':
        form = RegisterSample(request.POST or None)
        context = {
            'form': form
        }
        return render(request, 'Labs/register_sample.html', context)

    if request.method == 'POST':
        form = RegisterSample(request.POST or None)

        if form.is_valid():
            patient = form.data['patient']
            patient = Patient.objects.get(id=patient)
            ref_code = form.data['ref_code']

            all_samples = Specimen.objects.all()

            for sample in all_samples:
                if ref_code != '' and sample.Ref_code == ref_code:
                    from django.contrib import messages
                    messages.warning(
                        request, 'Sorry, Sample with this ID is already Registered.')
                    return redirect('Labs:register_sample')

            Specimen.objects.create(
                user=request.user,
                patient=patient,
                Ref_code=ref_code,
            )
            from django.contrib import messages
            messages.success(request, 'Sample created Successfully.')
            return redirect('Labs:index')
        else:
            print(form.errors)
            from django.contrib import messages
            messages.warning(
                request, 'An error occurred. Try again later or contact the administrator.')
            return redirect('Labs:index')


def sample_list(request):
    unprocessed_samples = Specimen.objects.filter(
        processed=False, user=request.user)
    processed_samples = Specimen.objects.filter(
        processed=True, user=request.user)

    context = {
        'unprocessed_samples': unprocessed_samples,
        'processed_samples': processed_samples,

    }
    return render(request, 'Labs/sample_list.html', context)


def update_sample_result(request, pk):
    sample = Specimen.objects.get(id=pk)

    result = request.POST.get('result')

    sample.results = result
    sample.processed = True
    sample.save()
    sample.patient.last_status = result
    sample.patient.save()

    messages.success(request, 'Sample status updated Successfully.')

    return redirect('Labs:sample_list')


def register_vaccination(request):

    if request.method == 'GET':
        form = RegisterVaccination(request.POST or None)
        context = {
            'form': form
        }
        return render(request, 'Labs/register_vaccination.html', context)

    if request.method == 'POST':
        form = RegisterVaccination(request.POST or None)

        if form.is_valid():
            patient = form.data['patient']
            patient = Patient.objects.get(id=patient)
            print(patient)
            fos = form.data['fos']

            if patient.last_status == 'Positive':
                from django.contrib import messages
                messages.warning(
                    request, 'Sorry, You cannot be Vaccinated if your last status was positive or if you were not tested at all.')
                return redirect('Labs:register_vaccination')
            elif patient.last_status == 'Negative':
                previous_vaccinations = Vaccination.objects.filter(
                    patient=patient)
                vaccinationcount = previous_vaccinations.count()

                if vaccinationcount >= 2:
                    from django.contrib import messages
                    messages.warning(
                        request, 'Sorry, This patient has already been vaccinated Twice.')
                    return redirect('Labs:register_vaccination')

                elif vaccinationcount == 1:
                    if fos == 'First':
                        from django.contrib import messages
                        messages.warning(
                            request, 'You cannot administor the First Vaccination Twice.')
                        return redirect('Labs:register_vaccination')

                    else:
                        Vaccination.objects.create(
                            user=request.user,
                            patient=patient,
                            first_or_second=fos,
                        )
                        from django.contrib import messages
                        messages.success(
                            request, 'Vaccine administration created Successfully.')
                        return redirect('Labs:index')

                elif vaccinationcount == 0:
                    if fos == 'Second':
                        from django.contrib import messages
                        messages.warning(
                            request, 'You cannot administor the 2nd Vaccination before the first one.')
                        return redirect('Labs:register_vaccination')
                    else:
                        Vaccination.objects.create(
                            user=request.user,
                            patient=patient,
                            first_or_second=fos,
                        )
                        from django.contrib import messages
                        messages.success(
                            request, 'Vaccine administration created Successfully.')
                        return redirect('Labs:index')
            else:
                from django.contrib import messages
                messages.warning(
                    request, 'Sorry, You cannot access a Vaccine if your are not tested.')
                return redirect('Labs:register_vaccination')

        else:
            print(form.errors)
            from django.contrib import messages
            messages.warning(
                request, 'An error occurred. Try again later or contact the administrator.')
            return redirect('Labs:index')


def vaccination_list(request):
    all_vaccinations = Vaccination.objects.filter(
        user=request.user).order_by('-date_of_administration')
    context = {
        'all_vaccinations': all_vaccinations,
    }
    return render(request, 'Labs/vaccination_list.html', context)


def infection_per_county(request):
    # today_date = datetime.today()
    county_model = Specimen.objects.filter(
        results='Positive').values_list("patient__county")
    county_count_rep = Counter([rep[0] for rep in county_model])
    county_amount_rep = {}

    for rep in county_count_rep:
        county_amount_rep[rep] = 0

    for month in county_model:
        for rep in county_amount_rep:
            if month[0] == rep:
                county_amount_rep[rep] += 1

    label3 = list(county_amount_rep.keys())
    data3 = list(county_amount_rep.values())

    context = {
        'label3': label3,
        'data3': data3
    }

    return render(request, 'Labs/infection_per_county.html', context)


def infection_per_county_detail(request, county):

    county_model = Specimen.objects.filter(
        patient__county=county).values_list("results")
    county_count_rep = Counter([rep[0] for rep in county_model])
    county_amount_rep = {}

    for rep in county_count_rep:
        county_amount_rep[rep] = 0

    for month in county_model:
        for rep in county_amount_rep:
            if month[0] == rep:
                county_amount_rep[rep] += 1

    label3 = list(county_amount_rep.keys())
    data3 = list(county_amount_rep.values())

    positive = Specimen.objects.filter(
        patient__county=county, results='Positive').count()
    negative = Specimen.objects.filter(
        patient__county=county, results='Negative').count()
    total = positive + negative

    infection_rate = (positive / total) * 100

    female = Specimen.objects.filter(
        patient__county=county, results='Positive', patient__gender='Female').count()
    male = Specimen.objects.filter(
        patient__county=county, results='Positive', patient__gender='Male').count()

    positive_cases = Specimen.objects.filter(
        patient__county=county, results='Positive')
    negative_cases = Specimen.objects.filter(
        patient__county=county, results='Negative  ')

    context = {
        'county': county,
        'label3': label3,
        'data3': data3,
        'positive': positive,
        'negative': negative,
        'total': total,
        'infection_rate': infection_rate,
        'female': female,
        'male': male,
        'positive_cases': positive_cases,
        'negative_cases': negative_cases,


    }
    return render(request, 'Labs/infection_per_county_detail.html', context)


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(
                    request, 'Logged in Successfully as ' + request.user.username)
                return redirect('Labs:index')
            else:
                messages.warning(request, 'Account not activated')
                return render(request, 'Labs/login.html')
        else:
            messages.warning(request, 'Invalid Username or Password!')
            return render(request, 'Labs/login.html')
    return render(request, 'Labs/login.html')


def logout_user(request):
    logout(request)
    form = UserLogForm(request.POST or None)
    context = {
        'form': form
    }
    messages.success(request, 'Successfully Logged out.')
    return redirect('Labs:login_user')


def register(request):
    if request.method == 'POST':
        form = UserLogForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            Location = request.POST.get('Location')
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    LabCenter.objects.create(
                        user=request.user,
                        lab_name=username,
                        location=Location,
                        remaining_testing_kits=0,
                        remaining_vaccines=0,
                    )

                    return redirect('Labs:index')
        context = {
            'form': form,
        }
        messages.warning(request, 'Error. Username already Taken Try another.')
        return render(request, 'Labs/register.html', context)
    else:
        form = UserLogForm(request.POST or None)
        context = {
            'form': form,
        }
        return render(request, 'Labs/register.html', context)
# # user registration function
# def register(request):
#     if request.method == 'POST':
#         form = UserLogForm(request.POST or None)
#         if form.is_valid():
#             user = form.save(commit=False)
#             username = form.data['lab_center_name']
#             password = request.POST.get('password')
#             location = request.POST.get('Location')

#             print(username)
#             print(password)
#             print(location)
#             user.set_password(password)
#             user.save()
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)

#                     LabCenter.objects.create(
#                         user=request.user,
#                         lab_name=username,
#                         location=location,
#                         remaining_testing_kits=0,
#                         remaining_vaccines=0,
#                     )

#                     return redirect('Labs:index')
#         context = {
#             'form': form,
#         }
#         print(form.errors)
#         messages.warning(request, 'Error. Username already Taken Try another.')
#         return render(request, 'Labs/register.html', context)
#     else:
#         form = UserLogForm(request.POST or None)
#         form2 = LabCenterForm(request.POST or None)
#         context = {
#             'form': form,
#             'form2': form2,
#         }
#         return render(request, 'Labs/register.html', context)

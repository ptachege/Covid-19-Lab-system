from django.db import models
from django.contrib.auth.models import User


class LabCenter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    lab_name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    remaining_testing_kits = models.IntegerField(default=0)
    remaining_vaccines = models.IntegerField(default=0)


professionChoice = (
    ('Doctor', 'Doctor'),
    ('Nurse', 'Nurse'),
    ('Regular', 'Regular'),
)


class Tester(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    id_number = models.CharField(max_length=10)
    contact = models.CharField(max_length=10)
    email = models.CharField(max_length=100)
    profession = models.CharField(max_length=100, choices=professionChoice)
    avatar = models.ImageField()

    class Meta:
        verbose_name = 'Tester'
        verbose_name_plural = 'Testers'

    def __str__(self):
        return self.first_name


class Patient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    id_number = models.CharField(max_length=10, blank=True, null=True)
    contact = models.CharField(max_length=10)
    email = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    county = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    last_status = models.CharField(max_length=20, null=True, blank=True)

    class Meta:

        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'

    def __str__(self):
        return self.first_name + ' ' + self.last_name


resultStatus = (
    ('Positive', 'Positive'),
    ('Negative', 'Negative')
)


class Specimen(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    Ref_code = models.CharField(max_length=10000, blank=True, null=True)
    date_taken = models.DateField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    results = models.CharField(max_length=20, choices=resultStatus, blank=True, null=True)

    class Meta:

        verbose_name = 'Specimen'
        verbose_name_plural = 'Specimens'

    def __str__(self):
        return str(self.Ref_code)


FirstSecondChoice = (
    ('First', 'First'),
    ('Second', 'Second')
)


class Vaccination(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date_of_administration = models.DateTimeField(auto_now_add=True)
    first_or_second = models.CharField(
        max_length=20, choices=FirstSecondChoice, blank=True, null=True)

    class Meta:

        verbose_name = 'Vaccination'
        verbose_name_plural = 'Vaccinations'

    def __str__(self):
        return str(self.pk)


class VaccinationKitSupply(models.Model):
    delivery_sn_no = models.CharField(max_length=1000)
    number_of_kits = models.IntegerField(default=0)
    date_of_delivery = models.DateField()

    class Meta:

        verbose_name = 'VaccinationKit'
        verbose_name_plural = 'VaccinationKits'

    def __str__(self):
        return self.delivery_sn_no
    
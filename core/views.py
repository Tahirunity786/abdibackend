from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from core.models import Contact
from django.contrib import messages
from core.models import Beds, Bed_Reservation
from core_account.utiles import send_mail_to_admin
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model
from core.models import Appointment
from django.db.models import Q
User = get_user_model()


@login_required(login_url="/hospitrack/user/login")
def bed_reservation(request):
    beds = Beds.objects.all().order_by("-id")
    beds_count = Beds.objects.count()
    data = {
        "beds":beds,
        "beds_count":beds_count,
    }
    return render(request, 'core/bed-reservation.html', data)

@login_required(login_url="/hospitrack/user/login")
def doctor_appointment(request):
    doc = User.objects.filter(account_type="Doctor", medical_verified=True).order_by("-id")
    doc_count = User.objects.filter(account_type="Doctor", medical_verified=True).count()

    data = {
        "doctors":doc,
        "doctorscount":doc_count
    }
    return render(request, 'core/doctor-appointment.html', data)

@login_required(login_url="/hospitrack/user/login")
def about_us(request):

    return render(request, 'core/about-us.html')

@login_required(login_url="/hospitrack/user/login")
def contact_us(request):
    if request.method == "POST":
        full_name = request.POST.get('fullname')
        email = request.POST.get('email')
        phone_no = request.POST.get('phno')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        if not (full_name and email and subject and message):
            messages.error(request, 'Please fill in all required fields.')
            return redirect('Profile')

        try:
            Contact.objects.create(
                user=request.user,
                full_name=full_name,
                email=email,
                phone_no=phone_no,
                subject=subject,
                message=message,
                status="Pending"
            )
            messages.success(request, 'Thank you for reaching out. Our team looks forward to connecting with you soon.')
            return redirect('Profile')
        except Exception as e:
            messages.error(request, f'An error occurred: {e}')
            return redirect('Profile')

    return render(request, 'core/contact.html')


@login_required(login_url="/hospitrack/user/login")
def freq_ask_questions(request):

    return render(request, 'core/freq-q-ans.html')

def bed_viewer(request):
    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.body)
            bed_id = data.get('bed_id')
            bed = Beds.objects.get(id=bed_id)
            response_data = {
                'id': bed.id,
                'bedno': bed.bed_no,
                'description': bed.description,
            }
            return JsonResponse(data=response_data)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON format in request body.'}, status=400)
        except Beds.DoesNotExist:
            return JsonResponse({'error': 'Bed not found.'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)

def bed_reservation_agent(request, id):
    if request.method == 'POST':
        user = request.user
        reason = request.POST.get("reason")

        # Check if the user has already reserved a bed
        if Bed_Reservation.objects.filter(user=user).exists():
            messages.error(request, 'You have already reserved a bed.')
            return redirect("BEDRESERVATION")

        # Get the bed object or return a 404 if it doesn't exist
        bed = get_object_or_404(Beds, id=id)

        # Check if the bed is already reserved
        if bed.reservation:
            messages.error(request, 'This bed is already reserved.')
            return redirect("BEDRESERVATION")

        # Create the bed reservation
        reservation = Bed_Reservation.objects.create(
            user=user,
            bed=bed,
            tell_us_why=reason,
            status="Pending"
        )

        # Update the bed reservation status
        bed.reservation = reservation
        bed.save()

        # Send email to admin
        subject = f"Bed Reservation Request by {user.get_full_name()}"
        message = f"Hi HospiTrack Team!\n\nMy name is {user.get_full_name()}.\n\nI want to reserve bed number {bed.bed_no}.\n\nMy reason is: {reason}\n\nYours sincerely,\n{user.get_full_name()}"
        # send_mail_to_admin(subject, message)

        messages.success(request, 'Bed reservation successful.')
        return redirect('BEDRESERVATION')

    # Handle GET requests or other HTTP methods
    return redirect('BEDRESERVATION')

def appointment_agent(request, doc_id):
    if request.method == "POST":
        try:
            doctor = User.objects.get(id=doc_id)
            
        except User.DoesNotExist:
            messages.error(request, 'Doctor does not exist.')
            return redirect("DOCTORAPPOINTMENTS")
        
        if doctor.exceed_quota > 5:
            
            messages.error(request, "The doctor has too many appointments with other patient. Please wait for an appointment.")
            return redirect("DOCTORAPPOINTMENTS")
        
        full_name = request.POST.get("fullname")
        mobile_no = request.POST.get("phno")
        appday = request.POST.get("appday")
        reason = request.POST.get("reason")
        if full_name and mobile_no and appday and reason:
            Appointment.objects.create(user=request.user, doctor_user=doctor,status="Pending", full_name=full_name, reason=reason, scheduled_day=appday, phone_no=mobile_no)
            doctor.exceed_quota += 1  # Increment quota
            doctor.save()
            messages.success(request, "Your appointment request has been submitted successfully. The doctor will contact you soon.")
            return redirect("DOCTORAPPOINTMENTS")
        else:
            messages.error(request, "Please fill out all fields.")
            return redirect("DOCTORAPPOINTMENTS")

    else:
        messages.error(request, "Invalid request.")
        return redirect("DOCTORAPPOINTMENTS")
    
def doc_user_info(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)

        user_id = data.get('user_id')
        doc_user = User.objects.get(id = user_id, account_type="Doctor")
        
        data={
            'id': doc_user.id,
            "firstname":doc_user.first_name,
            "lastname":doc_user.last_name,
            "exprience":doc_user.experience,
            "Education":doc_user.education_background,
            "Certification":doc_user.certifications,
            
        }
        # Process contact_id as needed
        return JsonResponse(data=data)
    else:
        messages.error(request, "Invalid request")
        return JsonResponse({'error': 'Invalid request.'}, status=400)

def appointment_gainer(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)

        app_id = data.get('app_id')
       
        appointment_user = Appointment.objects.get(id = app_id)
        
        data={
            'id': appointment_user.id,
            'reason':appointment_user.reason
            
        }
        # Process contact_id as needed
        return JsonResponse(data=data)
    else:
        messages.error(request, "Invalid request")
        return JsonResponse({'error': 'Invalid request.'}, status=400)

def accept_appointment(request, id):
    try:
        appointment = Appointment.objects.get(id=id)
    except Appointment.DoesNotExist:
        messages.error(request, "The appointment does not exist.")
        return redirect("Profile")
    
    appointment.status = "Ok"
    appointment.save()

    messages.success(request, "The appointment has been successfully accepted.")
    return redirect("Profile")

def declined_appointment(request, id):
    try:
        appointment = Appointment.objects.get(id=id)
    except Appointment.DoesNotExist:
        messages.error(request, "The appointment does not exist.")
        return redirect("Profile")
    
    appointment.status = "Decline"
    appointment.save()

    messages.success(request, "The appointment declined from you.")
    return redirect("Profile")


@require_POST
def search_beds(request):
    import json
    
    # Retrieve JSON data from the request body
    data = json.loads(request.body.decode('utf-8'))
    selected_rooms = data.get('rooms', [])  # Retrieve selected rooms from JSON data
    show_available = data.get('show_available', False)  # Retrieve the state of "Show Available Beds" checkbox
    
    # Query all beds
    beds = Beds.objects.all()
    
    # If "Show Available Beds" checkbox is checked, filter only available beds
    if show_available:
        # Filter beds that have no reservation or have a reservation with status "Decline"
        beds = beds.filter(Q(reservation__isnull=True) | Q(reservation__status="Decline"))
        beds_data = [{"id": bed.id, 'room_no': bed.room_no, 'bed_no': bed.bed_no, 'description': bed.description, "status": bed.reservation.status if bed.reservation else None} for bed in beds]
        return JsonResponse({'beds': beds_data})

    # Filter beds based on selected rooms
    if selected_rooms:
        beds = beds.filter(room_no__in=selected_rooms)
    
    # Serialize the queryset to JSON
    beds_data = [{"id": bed.id, 'room_no': bed.room_no, 'bed_no': bed.bed_no, 'description': bed.description, "status": bed.reservation.status if bed.reservation else None} for bed in beds]
    return JsonResponse({'beds': beds_data})


@require_POST
def search_input_beds(request):
    import json
    
    # Retrieve JSON data from the request body
    data = json.loads(request.body.decode('utf-8'))
    query = data.get('query', '')  # Retrieve search query from JSON data
    
    # Query beds matching the search query
    beds = Beds.objects.filter(Q(room_no__icontains=query) | Q(bed_no__icontains=query) | Q(description__icontains=query))
    
    # Serialize the queryset to JSON
    beds_data = [{"id": bed.id, 'room_no': bed.room_no, 'bed_no': bed.bed_no, 'description': bed.description, "status": bed.reservation.status if bed.reservation else None} for bed in beds]
    
    # Return the JSON response
    return JsonResponse({'beds': beds_data})


@require_POST
def search_doctor(request):
    import json
    
    # Retrieve JSON data from the request body
    data = json.loads(request.body.decode('utf-8'))
    specialities = data.get('specialities', [])  # Retrieve selected specialties from JSON data
    show_available = data.get('show_availabledocs', False)  # Retrieve the state of "Show Available Doctors" checkbox
    
    # Query all users (doctors)
    doctors = User.objects.filter(account_type="Doctor", medical_verified=True)
    
    # If "Show Available Doctors" checkbox is checked, filter only available doctors
    if show_available:
        # Filter doctors that are available
        available_doctors = doctors.filter(available_toggler=True)
        
        # Serialize the queryset to JSON for available doctors
        doctors_data = [{"id": i.id, 'firstname': i.first_name, 'lastname': i.last_name, "speciality": i.speciality} for i in available_doctors]
    else:
        # Filter doctors based on selected specialties
        if specialities:
            
            specialty_doctors = doctors.filter(speciality__in=specialities)
        else:
            specialty_doctors = doctors  # Use all doctors if no specialties are selected
    
        # Serialize the queryset to JSON for specialty doctors
        doctors_data = [{"id": i.id, 'firstname': i.first_name, 'lastname': i.last_name, "speciality": i.speciality} for i in specialty_doctors]
    
    return JsonResponse({'doctors': doctors_data})


@require_POST
def search_input_doctor(request):
    import json
    
    # Retrieve JSON data from the request body
    data = json.loads(request.body.decode('utf-8'))
    query = data.get('query', '')  # Retrieve search query from JSON data
    
    # Query beds matching the search query
    user = User.objects.filter(
        Q(first_name__icontains=query) |
        Q(last_name__icontains=query) |
        Q(speciality__icontains=query),
        Q(account_type="Doctor") & Q(medical_verified=True)
    ).order_by("-id")
  
    if query == '':
        user = User.objects.filter(account_type="Doctor", medical_verified=True)
    
    # Serialize the queryset to JSON
    doctors_data = [{"id": i.id, 'firstname': i.first_name, 'lastname': i.last_name, "speciality":i.speciality} for i in user]
    
    # print(doctors_data)
    # Return the JSON response
    return JsonResponse({'doctors': doctors_data})

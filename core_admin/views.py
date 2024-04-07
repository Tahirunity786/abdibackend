from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from core.models import Bed_Reservation, Appointment, Contact, Beds
from django.contrib import messages
from core_admin.admin_utiles import a_to_u
User = get_user_model()

@login_required(login_url="/hospitrack/user/login")
def admin_index(request):
    user = User.objects.filter(account_type="Patient").count()
    user_d = User.objects.filter(account_type="Doctor").count()
    bed_reservation = Beds.objects.all().order_by("-id")[:10]
    appointments = Appointment.objects.all().order_by("-id")[:10]
    data = {
        "user_data_p":user,
        "user_data_d":user_d,
        "bed_reservation":bed_reservation,
        "appointments":appointments,
    }
    return render(request, 'super_controller/index.html', data)

@login_required(login_url="/hospitrack/user/login")
def admin_appointments(request):
    app = Appointment.objects.all()

    data ={
        "app":app
    }
    return render(request, 'super_controller/Appointments.html', data)

@login_required(login_url="/hospitrack/user/login")
def admin_doctors(request):

    doctors = User.objects.filter(account_type="Doctor").order_by("-id")
    data ={
        "doctors":doctors
    }
    return render(request, 'super_controller/Doctors.html', data)

@login_required(login_url="/hospitrack/user/login")
def admin_userprofile(request):
    return render(request, 'super_controller/profile.html')

@login_required(login_url="/hospitrack/user/login")
def admin_user_management(request):

    doctor = User.objects.filter(account_type="Doctor").order_by("-id")
    patient = User.objects.filter(account_type="Patient").order_by("-id")
    admin = User.objects.filter(account_type="Admin").order_by("-id")

    data = {
        "doctor":doctor,
        "patient":patient,
        "admin":admin,
    }

    return render(request, 'super_controller/Users.html',data )

@login_required(login_url="/hospitrack/user/login")
def admin_bed_reservations(request):
    beds = Beds.objects.all().order_by("-id")

    data = {
        "beds":beds
    }
    return render(request, 'super_controller/bed-reservement.html', data)

@login_required(login_url="/hospitrack/user/login")
def admin_contacts(request):
    contact = Contact.objects.all().order_by('-id')
    data = {
        "contact":contact
    }
    return render(request, 'super_controller/contact.html', data)


@login_required(login_url="/hospitrack/user/login")
def add_bed(request):
    beds = Beds.objects.all().order_by("-id")

    data = {
        "beds":beds
    }
    return render(request, 'super_controller/Add-bed.html', data)

def contact_viewer(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)

        contact_id = data.get('contact_id')
        contact = Contact.objects.get(id = contact_id)
        data={
            'id': contact.id,
            "ticket":contact.contact_ticket,
            "email":contact.email,
            "phone_no":contact.phone_no,
            "subject":contact.subject,
            "message":contact.message,
        }
        # Process contact_id as needed
        return JsonResponse(data=data)
    else:
        messages.error(request, "Invalid request")
        return JsonResponse({'error': 'Invalid request.'}, status=400)



def contact_sender(request, id):
    if request.method == 'POST':
        message = request.POST.get('ans')
        if request.user.is_authenticated and message:
            contact = Contact.objects.get(id=id)
            # Mail creation
            subject = f"Response to Ticket# {contact.contact_ticket}: Thank you for contacting us"
            msg = f"Dear {contact.user.first_name} {contact.user.first_name},\n\nThank you for reaching out to us. My name is {request.user.get_full_name()}, and I'm here to assist you with your query.\n\nYour message: {contact.message}\n\nSolution: {message}\n\nSincerely,\n{request.user.get_full_name()}"
           
            if a_to_u(subject, msg, contact):
                messages.success(request, "Your response has been sent successfully.")
                contact.status = "Solved"
                contact.save()
            else:
                messages.error(request, "Failed to send the response email.")
            return redirect("contacts")
        else:
            messages.error(request, "User not authenticated or message is empty")
            return redirect("contacts")
    else:
        messages.error(request, "Invalid request method")
        return redirect("contacts")
    
def decline_contact(request, id):
    
    try:
        contact = Contact.objects.get(id=id)
    except:
        messages.error(request, "Contact not exist")
        return redirect('contacts')
    
    contact.status = "Declined"
    contact.save()
    messages.success(request, "Declined successfully.")
    return redirect('contacts')


def Register_Doctor(request, slug):
    if request.method == "POST" and slug == "Doctor":
        try:
            # Retrieve data from POST request
            first_name = request.POST.get('firstname')
            last_name = request.POST.get('lastname')
            email = request.POST.get('email')
            phone_no = request.POST.get('phno')
            license_number = request.POST.get('licensenumber')
            speciality = request.POST.get('sp')
            cv_file = request.FILES.get('cvfile')
            password = request.POST.get('pass')
         
            # Create user object
            user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                mobile_number=phone_no,
                doctor_cv=cv_file,
                license_number=license_number,
                medical_verified=True,
                speciality=speciality
            )

            # Set password
            user.set_password(password)

            # Assign account type and save user
            user.account_type = slug
            user.save()

            # Redirect to doctors page after successful registration
            return redirect("doctors")

        except Exception as e:
            # Handle any errors that may occur during user registration
            messages.error(request, f"Failed to register user: {e}")

    # Redirect to appropriate page if method is not POST or slug is not Doctor
    return redirect("doctors")  # Assuming there's a doctors page to redirect to

def verify_doc(request, id, acc_type):
    try:
        user = User.objects.get(id=id, account_type=acc_type)
    except User.DoesNotExist:
        messages.error(request, "User does not exist")
        return redirect("doctors")
    except Exception as e:
        messages.error(request, f"Failed to verify user: {e}")
        return redirect("doctors")

    # Update user's medical verification status
    try:
        user.medical_verified = True
        user.save()
        messages.success(request, "Successfully verified user's medical status")
    except Exception as e:
        messages.error(request, f"Failed to update user's medical status: {e}")

    return redirect("doctors")


def add_bed_post(request):
    # Retrieve data from POST request
    if request.method == "POST":

        room_no = request.POST.get("rno")
        bed_no = request.POST.get("bno")
        description = request.POST.get("desc")
   
        # Check if all required fields are provided
        if room_no and bed_no and description:
            try:
                # Create a new Bed object with the provided data
                Beds.objects.create(room_no=room_no, bed_no=bed_no, description=description)
                # Provide success message
                messages.success(request, "Bed added successfully.")
            except Exception as e:
                # Provide error message if something goes wrong during bed creation
                messages.error(request, f"Failed to add bed: {e}")
        else:
            # Provide error message if any required field is missing
            messages.error(request, "Please provide all required information.")
    
        # Redirect back to the beds page regardless of success or failure
        return redirect("beds")
    else:
        messages.error(request, "Invalid request")
        return redirect("beds")

def del_bed(request, id):
    try:
        # Attempt to retrieve the bed object
        bed = Beds.objects.get(id=id)
    except Beds.DoesNotExist:
        # Handle the case where the bed with the specified ID does not exist
        messages.error(request, "No bed found with the specified ID.")
        return redirect("beds")

    try:
        # Delete the bed object
        bed.delete()
        # Provide a success message upon successful deletion
        messages.success(request, "Bed data deleted successfully.")
    except Exception as e:
        # Handle any exceptions that might occur during deletion
        messages.error(request, f"Failed to delete bed data: {e}")

    # Redirect back to the beds page, regardless of success or failure
    return redirect("beds")


def decline_bed_request(request, id):
    try:
        bed = get_object_or_404(Beds, id=id)
    except Beds.DoesNotExist:
        messages.error(request, "Bed does not exist.")
        return redirect('reservation')

    if bed.reservation:
        bed.reservation.status = "Decline"
        bed.reservation.save()
        messages.success(request, "Bed reservation declined successfully.")
    else:
        messages.error(request, "No reservation found for this bed.")

    return redirect('reservation')


def accept_bed_request(request, id):
    try:
        bed = get_object_or_404(Beds, id=id)
    except Beds.DoesNotExist:
        messages.error(request, "Bed does not exist.")
        return redirect('reservation')

    if bed.reservation:
        bed.reservation.status = "Reserve"
        bed.reservation.save()  # Save the reservation object after updating the status
        messages.success(request, "Bed reservation accepted successfully.")
    else:
        messages.error(request, "No reservation found for this bed.")

    return redirect('reservation')

def bed_viewer(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)

        bed_id = data.get('bed_id')
        bed = Beds.objects.get(id = bed_id)
        data={
            'id': bed.id,
            "bedno":bed.bed_no,
            "reason":bed.reservation.tell_us_why,
            
        }
        # Process contact_id as needed
        return JsonResponse(data=data)
    else:
        messages.error(request, "Invalid request")
        return JsonResponse({'error': 'Invalid request.'}, status=400)

def del_user(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        messages.error(request, "User does not exist.")
        return redirect("user")  # Assuming "user_list" is the correct URL name for user list view
    
    user.delete()

    messages.success(request, "User deleted successfully.")
    return redirect("user")  # Assuming "user_list" is the correct URL name for user list view


def admin_profile_update(request):
    try:
        
        if request.method == "POST" and request.user.is_authenticated == True:
            user = request.user
            profile = request.FILES.get('pic')
            first_name = request.POST.get("firstname")
            last_name = request.POST.get("lastname")
            email = request.POST.get("email")
            username = request.POST.get("username")
            birthday = request.POST.get("birthday")
            gender = request.POST.get("gender")
            phno = request.POST.get("phno")
         
            try:
                user = User.objects.get(email=user)
            except User.DoesNotExist:
                messages.error(request, "User not found.")
                return redirect("Profile")
                
     
            if phno:
                user.mobile_number = phno
     
            if profile:
                user.profile = profile
            if gender:
                user.gender = gender
            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name
            if email:
                user.email = email
            if username:
                user.username = username
            if birthday:
               
                user.date_of_birth = birthday
                
            user.save()
            messages.success(request, "Profile Updated.")
            return redirect("profile")
        else:
            # Handle cases where the request method is not POST or user is not authenticated
            messages.error(request, "Invalid request.")
            return redirect("profile")
    except Exception as e:
      
        messages.error(request, f"Error {e}")
        return redirect("profile")

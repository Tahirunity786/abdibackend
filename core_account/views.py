from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model
from django.contrib import messages
from core_account.models import Special_code
from django.http import JsonResponse
from core.models import Contact, Appointment, Bed_Reservation, Beds
from django.db.models import Q
User = get_user_model()

# Create your views here.
def Login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        try:
            user_state = User.objects.get(email = email)
        except User.DoesNotExist:
            messages.error(request, "User not exist")

            return redirect("Login")
        
        user = authenticate(request, username=user_state.email, password=password)
        
        if user is not None:
            if user_state.account_type == "Patient":
                login(request, user)
                return redirect('home')
            elif user_state.account_type == "Doctor" and user_state.medical_verified == True:
                login(request, user)
                return redirect('home')
            elif user_state.account_type == "Admin":
                login(request, user)
                return redirect('dashboard')
            else:
                return redirect('Login')
        else:
            messages.error(request, "Credentials not matched!")
            return redirect('Login')
          
    if request.method == "GET":
        return render(request, 'core_account/login.html')


def Register_api(request, slug):
    if request.method == "POST":
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        phone_no = request.POST.get('phno')
        email = request.POST.get('email')
        check_box = request.POST.get('chkbx')
        password = request.POST.get('pass')
        confirm_password = request.POST.get('rpass')
        
        
        if not (first_name and last_name and phone_no and email and password and confirm_password):
            messages.error(request, "Please fill in all required fields!")
            return redirect('Register')

        if password != confirm_password:
          
            messages.error(request, "Passwords do not match!")
            return redirect("Register")

        if check_box != "on":
            messages.error(request, "Please accept our terms & conditions!")
            return redirect('Register')

        if slug == "Patient":
            user = User.objects.create(first_name=first_name, last_name=last_name, email=email, mobile_number=phone_no)
        
        elif slug == "Doctor":
            license_number = request.POST.get('licensenumber')
            spc = request.POST.get('spc')
            cv_file = request.FILES.get('cvfile')
            if not (license_number and cv_file and spc):
                messages.error(request, "Please provide license number and CV!")
                return redirect('Register')
            user = User.objects.create(first_name=first_name, last_name=last_name, speciality=spc, email=email, mobile_number=phone_no, doctor_cv=cv_file, license_number=license_number)

        elif slug == "Admin":
            special_code = request.POST.get('specialcode')
        
            latest_special_code = Special_code.objects.latest('created_at')
        
            if not special_code or latest_special_code.code != special_code:  # Compare special codes
                messages.error(request, "Invalid special code. Please try again!")
                return redirect('Register')
            user = User.objects.create(first_name=first_name, last_name=last_name, email=email, mobile_number=phone_no)
        
        else:
            messages.error(request, "Invalid user type!")
            return redirect('Register')

        user.set_password(password)
        user.account_type = slug
        user.save()
        success_message = f'Please <b><a href="/hospitrack/user/login">Login</a></b> to continue! Account type {slug}'
        messages.success(request, mark_safe(success_message))
        return redirect('Register')

    else:
        messages.error(request, "Invalid request method!")
        return redirect('Register')
    


def Register(request):

    return render(request, 'core_account/signup.html')

def Profile(request):

    if request.method == "GET":
    
        user = request.user
        print(user)
        if user:
            try:
                contacts = Contact.objects.filter(user=user).order_by("-id")
                appointments = Appointment.objects.filter(user=user).order_by("-id")
                doctor_appoints = Appointment.objects.filter(doctor_user=user.id).order_by("-id")
                done_appoints = Appointment.objects.filter(
                    Q(doctor_user=user.id, status="Ok") | Q(doctor_user=user.id, status="Declined")
                ).order_by("-id")
                bed_reservements = Bed_Reservation.objects.filter(user=user).order_by("-id")
                user_data = User.objects.get(email = user)
                bed_reservation = Beds.objects.filter(reservation__user=user).order_by("-id")
                
                doc_app= Appointment.objects.filter(user=user.id).order_by("-id")

            except Exception as e:
                return redirect("Profile")
            
            data = {
                "user_data": user_data, 
                "contacts": contacts, 
                "appointments": appointments, 
                "reservements": bed_reservements, 
                "docappoint": doctor_appoints, 
                "done_appoints": done_appoints, 
                "bed_reservation": bed_reservation, 
                "doc_app": doc_app, 
            }
        else:
          
            messages.error(request, "User not found")
            return redirect("Profile")
        return render(request, 'core_account/Account.html', data)

def profile_update(request):
    try:
        
        if request.method == "POST" and request.user.is_authenticated == True:
            user = request.user
           
            first_name = request.POST.get("firstname")
            last_name = request.POST.get("lastname")
            email = request.POST.get("email")
            username = request.POST.get("username")
            birthday = request.POST.get("birthday")
            education = request.POST.get("edu")
            account_certificate = request.POST.get("ac")
            experience = request.POST.get("exp")
           
            try:
                user = User.objects.get(email=user)
            except User.DoesNotExist:
                messages.error(request, "User not found.")
                return redirect("Profile")
                
     
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

            # For doctor user
            if user.account_type == "Doctor" and education:
                user.education_background = education
            if user.account_type == "Doctor" and account_certificate:
                user.certifications = account_certificate
            if user.account_type == "Doctor" and experience:
                user.experience = experience

            user.save()
            messages.success(request, "Profile Updated.")
            return redirect("Profile")
        else:
            # Handle cases where the request method is not POST or user is not authenticated
            messages.error(request, "Invalid request.")
            return redirect("Profile")
    except Exception as e:
     
        messages.error(request, f"Error {e}")
        return redirect("Profile")

def reset_password(request):
    try:
        if request.method == "POST" and request.user.is_authenticated:
            user = request.user
            current_password = request.POST.get("prepass")
            new_password = request.POST.get("newpass")
            confirm_password = request.POST.get("confirmpass")

            # Ensure new and confirm passwords match
            if new_password != confirm_password:
              
                messages.error(request, "New password and confirm password do not match.")
                return redirect("Profile")
            
            # Check if current password matches the user's actual password
            if not user.check_password(current_password):
               
                messages.error(request, "Incorrect current password.")
                return redirect("Profile")
            
            # Update the user's password
            user.set_password(new_password)
            user.save()
            logout(request)
            messages.success(request, "Password updated successfully.")
            return redirect("Login")
        else:
            # Handle cases where the request method is not POST or user is not authenticated
            
            messages.error(request, "Invalid request.")
            return redirect("Profile")
    except Exception as e:
        # Log the error for debugging purposes
    
        messages.error(request, f"Error occurred: {e}")
        return redirect("Profile")


def pic_updater(request):
    try:
        
        if request.method == "POST" and request.user.is_authenticated == True:
            user = request.user
            profile = request.FILES['pic']
            try:
                user = User.objects.get(email=user)
            except User.DoesNotExist:
                messages.error(request, "User not found.")
                return redirect("Profile")
            if profile:
                user.profile = profile

                user.save()

                messages.success(request, "Profile picture updated.")
                return redirect("Profile")
            else:
                messages.error(request, "Picture not uploaded")
                return redirect("Profile")
            
        else:
            messages.error(request, "Invalid request")
            return redirect("Profile")
    except Exception as e:
        messages.error(request, f"Error occurred: {e}")
        return redirect("Profile")



def Logout(request):
    logout(request)
    return redirect("Login")
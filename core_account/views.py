from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model
from django.contrib import messages
from core_account.models import Special_code
User = get_user_model()

# Create your views here.
def Login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user_state = User.objects.get(email = email)
        except User.DoesNotExist as e:
            return redirect("Login")
        
        user = authenticate(request, username=user_state.email, password=password)
        if user is not None:
            if user_state.account_type == "Patient":
                login(request, user)
                return redirect('home')
            elif user_state.account_type == "Doctor":
                login(request, user)
                return redirect('home')
            elif user_state.account_type == "Admin":
                login(request, user)
                return redirect('ControlRoom')
            else:
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
            return redirect('Register')

        if check_box != "on":
            messages.error(request, "Please accept our terms & conditions!")
            return redirect('Register')

        if slug == "Patient":
            user = User.objects.create(first_name=first_name, last_name=last_name, email=email, mobile_number=phone_no)
        
        elif slug == "Doctor":
            license_number = request.POST.get('licensenumber')
            cv_file = request.FILES.get('cvfile')
            if not (license_number and cv_file):
                messages.error(request, "Please provide license number and CV!")
                return redirect('Register')
            user = User.objects.create(first_name=first_name, last_name=last_name, email=email, mobile_number=phone_no, doctor_cv=cv_file, license_number=license_number)

        elif slug == "Admin":
            special_code = request.POST.get('specialcode')
            latest_special_code = Special_code.objects.latest('created_at')
            if not special_code or latest_special_code != special_code:
                messages.error(request, "Invalid special code. Please try again!")
                return redirect('Register')
            user = User.objects.create(first_name=first_name, last_name=last_name, email=email, mobile_number=phone_no)
        
        else:
            messages.error(request, "Invalid user type!")
            return redirect('Register')

        user.set_password(password)
        user.account_type = slug
        user.save()
        success_message = 'Please <b><a href="/core/public/u/logout">Login</a></b> to continue!'
        messages.success(request, mark_safe(success_message))
        return redirect('Register')

    else:
        messages.error(request, "Invalid request method!")
        return redirect('Register')
    


def Register(request):

    return render(request, 'core_account/signup.html')

def Profile(request):

    return render(request, 'core_account/Account.html')

def Logout(request):
    logout(request)
    return redirect("Login")
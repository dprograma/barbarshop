from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . models import User
from . import sendmail
from .forms import UserForm, MyUserCreationForm

# Create your views here.


def loginUser(request):
    page = 'Login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist.')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    context = {'page': page}
    return render(request, 'shop/login_register.html', context)


def registerUser(request):
    page = "Sign Up"
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid:
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            # Send email notification
            to = user.email
            subject = 'Account Creation for Barbarshop'
            emailMsg = f'''<div style="background: #eee;padding: 10px;">
                            <div style="max-width: 500px;margin: 0px auto;font-family: sans-serif;text-align: center;background: #fff;border-radius: 5px;overflow: hidden;">
                                <div style="width: 100%;background: #fc9700;">
                                    <h1 style="color: #fff;text-decoration: none;margin: 0px;padding: 10px 0px;">Barbarshop</h1>
                                </div>
                                <div style="color: #000;padding: 10px;margin-top: 10px;">
                                    Hello {user.username}, <br/>Thank you for registering with us at Barbarshop. Please login to your dashboard with your email and password
                                    <div style="padding: 10px;margin: 10px 0px;color: #000;background: #eee;border-radius: 5px;">
                                    Account Confirmation:
                                        <div style="font-size: 35px; color: #000;font-weight: 700;">
                                            Confirmed
                                        </div>
                                    </div>
                                </div>
                                <div style="color: #000; padding-bottom: 10px;">
                                    However, if this registration process was not initiated by you, kindly ignore this mail.
                                    <br />
                                    If you have encounter any problem while creating your account, feel free to <a href="http://localhost:8000/contact" style="text-decoration: none; color: #bf5794;">contact us</a>
                                </div>
                            </div>
                        </div>'''
            alt = '''Hello user, Thank you for registering with us at Barbarshop. Please login to your dashboard with your email and dashboard. <br />  However, if this registration process was not initiated by you, kindly ignore this mail.'''
            sendmail.SendMail(to, subject, emailMsg, alt)
            messages.success(f"You account was created successfully. An email has been sent to {user.email} to confirm your account.")
            # end email notification
            # return redirect('home')
        else:
            messages.error("Something went wrong during registration.")
    context = {'form': form, 'page': page}
    return render(request, 'shop/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def home(request):
    context = {}
    return render(request, 'shop/home.html', context)


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid:
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'shop/update_user.html', {'form: form'})


@login_required(login_url='login')
def userProfile(request, pk):
    user = User.objects.get(id=pk)
    context = {'user': user}
    return render(request, 'shop/profile.html', context)


@login_required(login_url='login')
def bookAppointment(request):
    context = {}
    return render(request, 'shop/appointment.html', context)

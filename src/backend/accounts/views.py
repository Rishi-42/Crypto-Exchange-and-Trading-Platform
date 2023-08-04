from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
import random
# for verification email
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


def register(request):
    """
    As the data is received form the form,
    the data is validated using method is_valid() and 
    the valid datas are stores into the database
    similarly a verification mail is send to the user
    """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split('@')[0]
            user = Account.objects.create_user(
                first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.save() # store the object into the database
            # USER activation
            current_site = get_current_site(request)
            mail_subject = "Please activate your account"
            message = render_to_string('account/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)), #encoding the user pk(id)
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            return redirect('/account/login/?command=verification&email='+email)
    else:
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'account/customer_register.html', context)


def login(request):
    """
    The user credentials is authenticated
    if the user credentials are correct the user is 
    redirected to the verification page
    """
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('two_auth')
        else:
            messages.error(request, 'Invalid email or password')
            return render(request, 'account/login.html')
    return render(request, 'account/login.html')



def activate(request, uidb64, token):
    """
    To activate the user status a 
    email is send to the user as the 
    user clicks the link send via email 
    then this class activates the users account
    """
    try:
        uid = urlsafe_base64_decode(uidb64).decode() #decoding the encoded user pk(id)
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(
            request, "Congratulations! Your account is activated.")
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')


def forgotpassword(request):
    """
    To reset the passworduser need to
    provide their registered email and a 
    reset link is send via their email
    """
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            # reset password
            current_site = get_current_site(request)
            mail_subject = "Reset Password"
            message = render_to_string('account/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)), #encoding the user pk(id)
                'token': default_token_generator.make_token(user), # generate token
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            messages.success(
                request, 'Password reset email has been send to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Invalid email')
            return render(request, 'account/forgotpassword.html')
    return render(request, 'account/forgotpassword.html')



"""
Similar to the user activation the link is 
validated and the user is provided with a form
to reset their password
"""
def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetpassword')
    else:
        messages.error(request, 'Invalid reset password link')
        return redirect('forgotpassword')


def resetpassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST.get('confirm_password', False)
        if password == confirm_password:
            uid = request.session['uid']
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successfully')
            return redirect('login')
        else:
            messages.error(request, 'Password not matched')
            return redirect('resetpassword')
    return render(request, 'account/resetpassword.html')


"""
Sends the user eight digits of random number
via email if the number is valid then the user
can login into the application."""
@login_required(login_url='login')
def two_auth(request):
    current_user = request.user
    email = current_user.email
    if request.method == 'POST':
        number = request.POST['number']
        if number == request.session.get('verification_code'):
            # Clear the verification code from the session
            request.session['verification_code'] = None
            return redirect('market_data_view')
        else:
            messages.error(request, 'Invalid verification code')
            return render(request, 'account/two_auth.html')
    # Generate a new verification code if not already set in the session
    if not request.session.get('verification_code'):
        verification_code = str(random.randint(10000000, 99999999))
        request.session['verification_code'] = verification_code
        mail_subject = "Verify your login"
        message = render_to_string('account/two_auth_email.html', {
            'user': current_user,
            'verification_code': verification_code,
        })
        to_email = email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()
    return render(request, 'account/two_auth.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, "Successfully logged out!")
    return render(request, 'account/login.html')

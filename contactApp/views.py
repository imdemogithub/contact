from django.shortcuts import redirect, render
from django.http import JsonResponse
from .models import *
from random import randint
from django.core.mail import send_mail
from django.conf import settings
from .paytm_checksum import generate_checksum, verify_checksum
from django.views.decorators.csrf import csrf_exempt

default_dict = {
    'style_pages': ['login_page', 'register_page', 'otp_page', 'profile_page'],
    'msg': '',
}

# create otp
def create_otp(request):
    otp = randint(1000, 9999)
    request.session['otp'] = otp

    send_otp(request)

    print("OTP is: ", otp)

    return redirect(otp_page)

# send otp
def send_otp(request):
    email_to_list = [request.session['email'],]
    
    subject = 'OTP for Contact Manager Registration'

    email_from = settings.EMAIL_HOST_USER

    message = f"Your One Time Password for verification is: {request.session['otp']}"

    send_mail(subject, message, email_from, email_to_list)

    msg_system('seccess', 'OTP', f'OTP has sent to {request.session["email"]}')

# verify otp
@csrf_exempt
def verify_otp(request):
    otp = request.session['otp']
    
    if int(request.POST['otp']) == otp:
        print("otp verified.")

        master = Master.objects.get(Email=request.session['email'])
        master.IsActive = True
        master.save()

        msg_system('seccess', 'Verified', f'OTP verified successfully.')
        
        del request.session['email']
        del request.session['otp']

        # return redirect(login_page)
        return JsonResponse({'url': 'login_page', })
    else:
        msg_system('warning', 'Invalid OTP', f'You entered invalid OTP.')
    
    # return redirect(otp_page)
    return JsonResponse({'url': 'otp_page', })

# msg system
def msg_system(type, title, text):
    default_dict['msg'] = {}
    default_dict['msg']['type'] = type
    default_dict['msg']['title'] = title
    default_dict['msg']['text'] = text

# first page
def index(request):
    default_dict['current_page'] = 'register_page'
    return render(request, 'register_page.html', default_dict)

# Register Page
def register_page(request):
    default_dict['current_page'] = 'register_page'
    return render(request, 'register_page.html', default_dict)

# OTP Page
def otp_page(request):
    default_dict['current_page'] = 'otp_page'
    return render(request, 'otp_page.html', default_dict)

# Login Page
def login_page(request):
    default_dict['current_page'] = 'login_page'
    return render(request, 'login_page.html', default_dict)

# Register Functionality
@csrf_exempt
def register(request):
    print(request.POST)

    if request.method == 'POST':
        email = request.POST['email']
        pwd = request.POST['password']
        c_pwd = request.POST['confirm_password']

        
        try:
            if pwd == c_pwd:
                m = Master.objects.create(
                    Email = email,
                    Password = pwd
                )
                UserProfile.objects.create(Master=m)

                request.session['email'] = email

                # create and sending otp
                create_otp(request)
                
                # msg_system('seccess', 'updated', 'Account created successfully.')
                return JsonResponse({'url': 'otp_page', })
                # return redirect(otp_page)
            else:
                msg_system('warning', 'Password', 'Both password are not same.')
                return JsonResponse({'url': 'error_url', })
        except Exception as err:
            msg_system('warning', 'Email', f'{email} is already exists.')
        
        return redirect(register_page)
    else:
        print('----error---')
        return redirect(register_page)

# Login Functionality
@csrf_exempt
def login(request):
    
    if request.method == 'POST':
        email = request.POST['email']
        pwd = request.POST['password']

        try:
            master = Master.objects.get(Email=email)
            if master.Password == pwd:
                request.session['email'] = email
                # return redirect(profile_page)
                return JsonResponse({'url': 'profile_page', })
            else:
                msg_system('warning', 'Incorrect', 'Please enter correct password')

                # return redirect(login_page)
                return JsonResponse({'url': 'login_page', })
        except Master.DoesNotExist as err:
            print(err)
            msg_system('warning', 'Email', f'{email} does not exist.')

            return JsonResponse({'url': 'login_page', })
    else:
        return JsonResponse({'url': 'login_page', })

# create option dictionary
def create_options(choices, key_name):
    options = []
    for cat in choices:
        options.append(
            {
                'option_code': cat[0],
                'option_text': cat[1],
            }
        )
    print(options)
    default_dict[key_name] = options

# Serialize Model Object
def serialize(obj):
    d = {}
    for k in obj.__dict__:
        # print('type of k: ', k, type(obj.__dict__[k]))
        if not k.startswith('_'):
            val = obj.__dict__[k]
            
            d.update({k: val})

            if type(val) != int:
                if '/' in val:
                    print('/ in val: ', settings.MEDIA_URL + obj.__dict__[k])
                    d.update({k: settings.MEDIA_URL + obj.__dict__[k]})
    return d

# Load Profile Data
def profile_data(request):
    if 'email' in request.session:
        master = Master.objects.get(Email=request.session['email'])
        user = UserProfile.objects.get(Master=master)

        # Load All Contacts
        contacts = Contact.objects.filter(
            UserProfile = user
        )

        # print('user serialized: ', serialize(user))

        # print("media: ",settings.MEDIA_URL)

        user = serialize(user)
        # user['ProfileImage'] = settings.MEDIA_URL + user['ProfileImage']

        default_dict['user'] = user
        default_dict['contacts'] = [serialize(contact) for contact in contacts]
        # print('contacts: ', default_dict['contacts'])
        default_dict['total_contacts'] = len(contacts)
    else:
        return redirect(login_page)

    return JsonResponse(default_dict)
    
# Profile Page
def profile_page(request):
    
    create_options(categories, 'contact_categories')
    create_options(countries, 'countries')

    default_dict['current_page'] = 'profile_page'

    profile_data(request)
    return render(request, 'profile_page.html', default_dict)

# Profile Update
@csrf_exempt
def profile_update(request):
    print("POST DATA:: ", request.POST)
    master = Master.objects.get(Email=request.session['email'])
    user = UserProfile.objects.get(Master=master)

    user.FullName = request.POST['full_name']
    user.Mobile = request.POST['mobile']
    user.Country = request.POST['country']
    user.Pincode = request.POST['pincode']
    user.Address = request.POST['address']

    user.save()

    msg_system('success', 'Updated', 'Profile updated successfully.')

    return redirect(profile_page)

# profile image upload
@csrf_exempt
def profile_image_upload(request):
    master = Master.objects.get(Email=request.session['email'])
    user = UserProfile.objects.get(Master = master)

    print("data: ", request.POST)
    print("files: ", request.FILES)
    
    if 'user_profile_image' in request.FILES:
        image_file = request.FILES['user_profile_image']

    user.ProfileImage = image_file
    user.save()

    msg_system('success', 'Image Changed', 'Your profile photo uploaded successfully.')

    return redirect(profile_page)

# password update
@csrf_exempt
def password_update(request):
    master = Master.objects.get(Email=request.session['email'])
    old_pwd = request.POST['old_password']
    new_pwd = request.POST['new_password']
    if old_pwd == master.Password:
        master.Password = new_pwd
        master.save()
        msg_system('success', 'Changed', 'Password changed successfully.')
    else:
        msg_system('warning', 'Password', 'Old password is incorrect.')
        
    return redirect(profile_page)

# Add New Contact
@csrf_exempt
def add_contact(request):
    print('request data: ', request.POST)

    master = Master.objects.get(Email=request.session['email'])
    user = UserProfile.objects.get(Master=master)

    new_contact = Contact.objects.create(
        UserProfile = user,
        Category = request.POST['category'],
        FullName = request.POST['contact_fullname'],
        Email = request.POST['contact_email'],
        Mobile = request.POST['contact_mobile'],
        Country = request.POST['contact_country'],
        Pincode = request.POST['contact_pincode'],
        Address = request.POST['contact_address'],
    )

    if 'contact_image' in request.FILES:
        new_contact.ContactImage = request.FILES['contact_image']
        new_contact.save()

    msg_system('success', 'Added', 'New contact has been added.')

    return redirect(profile_page)

# Contact Update
@csrf_exempt
def contact_update(request, pk):
    print("POST DATA:: ", request.POST)
    master = Master.objects.get(Email=request.session['email'])
    user = UserProfile.objects.get(Master=master)
    contact = Contact.objects.get(UserProfile=user, pk=pk)

    contact.Category = request.POST['category']
    contact.FullName = request.POST['contact_fullname']
    contact.Email = request.POST['contact_email']
    contact.Mobile = request.POST['contact_mobile']
    contact.Country = request.POST['contact_country']
    contact.Pincode = request.POST['contact_pincode']
    contact.Address = request.POST['contact_address']

    if 'contact_image' in request.FILES:
        contact.ContactImage = request.FILES['contact_image']

    contact.save()

    msg_system('success', 'Updated', 'Contact updated successfully.')

    return redirect(profile_page)

# Contact Delete
def contact_delete(request, pk):
    master = Master.objects.get(Email=request.session['email'])
    user = UserProfile.objects.get(Master=master)
    Contact.objects.get(UserProfile=user, pk=pk).delete()

    msg_system('success', 'Deleted', 'Contact deleted successfully.')

    return redirect(profile_page)

# Payment Function
def initiate_payment(request):
    try:
        amount = int(request.POST['pricing_amount'])
        master = Master.objects.get(Email=request.session['email'])
        user = UserProfile.objects.get(Master=master)
        
    except:
        msg_system('danger', 'Error', 'Wrong Accound Details or amount.')
        return redirect(profile_page)

    transaction = Transaction.objects.create(made_by=user, amount=amount)
    transaction.save()
    merchant_key = settings.PAYTM_SECRET_KEY

    params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(transaction.order_id)),
        ('CUST_ID', str(transaction.made_by.Master.Email)),
        ('TXN_AMOUNT', str(transaction.amount)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        # ('EMAIL', request.user.email),
        # ('MOBILE_N0', '9911223388'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
        # ('PAYMENT_MODE_ONLY', 'NO'),
    )

    paytm_params = dict(params)
    checksum = generate_checksum(paytm_params, merchant_key)

    transaction.checksum = checksum
    transaction.save()

    paytm_params['CHECKSUMHASH'] = checksum
    print('SENT: ', checksum)
    return render(request, 'redirect.html', context=paytm_params)

# Callback Function
@csrf_exempt
def callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'callback.html', context=received_data)
        return render(request, 'callback.html', context=received_data)

# Logout
def logout(request):
    if 'email' in request.session:
        del request.session['email']

    return redirect(index)
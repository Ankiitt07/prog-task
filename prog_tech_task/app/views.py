import os
import qrcode
from django.shortcuts import render, redirect
from django.shortcuts import render
from django.contrib.sessions.models import Session
from django.http import JsonResponse
from app.models import *
from django.core.files.base import ContentFile                  
from io import BytesIO
from django.contrib import messages

# Create your views here.
def signup(request):
    return render(request, 'signup.html')

def login(request):
    return render(request, 'login.html')

def logout(request):
    del request.session['isUserLogin']
    del request.session['user_id']
    del request.session['user_name']
    return redirect('/login/')

def images_upload(request):
    if request.session._session:
        if not request.session['isUserLogin']:
            return redirect('/login/')
        else:
            user_id = request.session['user_id']
            data = UserImages.objects.filter(user = user_id).order_by('-img_id').first()
            if data:
                last_data = {
                    "img_type":data.img_type
                }
                return render(request, 'images_upload.html', {'data': last_data})
            else:
                data = {
                    "img_type" : "portrait"
                }
                return render(request, 'images_upload.html', {'data': data})
            

def add_user(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        mobile = request.POST['mobile']
        user_data = UserProfile.objects.all()
        user_mobile = user_data.filter(user_mobile = mobile)
        user_email = user_data.filter(user_email = email)

        if user_email:
            messages.error(request, 'Email already exists. Please use a different email.')
        elif user_mobile:
            messages.error(request, 'Mobile number already exists. Please use a different number.')
        else:
            user_model = UserProfile()
            user_model.user_name = name
            user_model.user_email = email
            user_model.user_mobile = mobile
            user_model.user_password = password
            user_model.save()

            request.session['isUserLogin'] = True
            request.session['user_id'] = user_model.user_id
            request.session['user_name'] = user_model.user_name

            messages.success(request, 'User added successfully.')
            return redirect('/images_upload/')
    return render(request, 'signup.html')

def authentication(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user_data = UserProfile.objects.filter(user_email = email, user_password = password)
        if user_data:
            user_info = UserProfile.objects.get(user_email = email, user_password = password)
            request.session['isUserLogin'] = True
            request.session['user_id'] = user_info.user_id
            request.session['user_name'] = user_info.user_name

            return redirect('/images_upload/')
        else:
            messages.error(request, 'Invalid Email or Password. Please enter correct credential')
    return render(request, 'login.html')


def upload_image(request):
    if request.session._session:
        if not request.session['isUserLogin']:
            return redirect('/login/')
        else:
            if request.method == 'POST':
                image_type = request.POST['imageType']
                image_file = request.FILES.get('image')
                original_image_name = image_file.name
                image_name = original_image_name.replace(' ', '_')
                user_id = request.session['user_id']

                # Save image information to the database
                user_img_model = UserImages()
                user_img_model.user_id = user_id
                user_img_model.img_name = image_name
                user_img_model.img_type = image_type
                user_img_model.image = image_file
                user_img_model.save()

                # Generate QR code for the image link
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(request.build_absolute_uri(user_img_model.image.url))
                qr.make(fit=True)
                qr_img = qr.make_image(fill_color="black", back_color="white")

                # Save QR code image to BytesIO
                qr_code_buffer = BytesIO()
                qr_img.save(qr_code_buffer, format='PNG')

                # Save the QR code image to the qr_code field in the model
                user_img_model.qr_code.save(f'{user_img_model.img_id}_qrcode.png', ContentFile(qr_code_buffer.getvalue()), save=True)

                return redirect('/gallery/')


def uploaded_images(request):
    return render(request, 'gallery.html')

def gallery(request):
    if request.session._session:
        if not request.session['isUserLogin']:
            return redirect('/login/')
        else:
            user_id = request.session['user_id']
            image_type = UserImages.objects.filter(user=user_id).first()
            portrait_images = list(UserImages.objects.filter(img_type='portrait', user=user_id).order_by('img_id'))
            landscape_images = list(UserImages.objects.filter(img_type='landscape', user=user_id).order_by('img_id'))
            processed_records = []

            def get_next_images(count, img_list):
                images = []
                for _ in range(count):
                    if img_list:
                        images.append(img_list.pop(0))
                return images

            while portrait_images or landscape_images:
                portrait_pair = get_next_images(2, portrait_images)
                landscape = get_next_images(1, landscape_images)
                if image_type.img_type == "portrait":
                    if portrait_pair:
                        if len(portrait_pair) == 2:
                            processed_records.append({'record1': portrait_pair[0], 'record2': portrait_pair[1]})
                        else:
                            processed_records.append({'record1': portrait_pair[0], 'record2': None})
                    if landscape:
                        processed_records.append({'landscape': landscape[0]})
                elif image_type.img_type == "landscape":
                    if landscape:
                        processed_records.append({'landscape': landscape[0]})
                    if portrait_pair:
                        if len(portrait_pair) == 2:
                            processed_records.append({'record1': portrait_pair[0], 'record2': portrait_pair[1]})
                        else:
                            processed_records.append({'record1': portrait_pair[0], 'record2': None})

            context = {'processed_records': processed_records}
            return render(request, 'gallery.html', context)


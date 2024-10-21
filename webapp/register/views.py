from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password  # Updated import
import re
from datetime import date
from .models import RegisterUser  # Adjust the import based on your project structure

def register_view(request):
    if request.method == 'POST':
        # Extract form data from POST request
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        date_of_birth = request.POST.get('date_of_birth', '').strip()

        # Initialize error messages list
        errors = []

        # Validate first name (capitalize automatically)
        if not first_name or not last_name:
            errors.append("First and last name are required.")
        else:
            first_name = first_name.capitalize()
            last_name = last_name.capitalize()

        # Validate phone number (must be 11 digits)
        if len(phone_number) != 11 or not phone_number.isdigit():
            errors.append("Phone number must be 11 digits.")

        # Validate email (must be a valid email format)
        if not re.match(r"^[a-zA-Z0-9._%+-]+@(gmail\.com|yahoo\.com|outlook\.com)$", email):
            errors.append("Email must be a valid Gmail, Yahoo, or Outlook address.")

        # Validate password (must meet complexity requirements)
        if len(password) < 8:
            errors.append("Password must be at least 8 characters long.")
        elif (not re.search(r"[A-Z]", password) or
              not re.search(r"[a-z]", password) or
              not re.search(r"[0-9]", password) or
              not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)):
            errors.append("Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character.")

        # Validate date of birth (must be at least 18 years old)
        try:
            dob = date.fromisoformat(date_of_birth)  # Assuming format is YYYY-MM-DD
            age = date.today().year - dob.year - ((date.today().month, date.today().day) < (dob.month, dob.day))
            if age < 18:
                errors.append("You must be at least 18 years old.")
        except ValueError:
            errors.append("Invalid date format. Please use YYYY-MM-DD.")

        # If there are errors, display them; otherwise, proceed to save
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'register/register.html', {
                'first_name': first_name,
                'last_name': last_name,
                'phone_number': phone_number,
                'email': email,
                'date_of_birth': date_of_birth
            })

        # Save the user data to the database
        user = RegisterUser(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=email,
            password=make_password(password),  # Hash the password
            date_of_birth=date_of_birth  # Store as is; consider changing to DateField if needed
        )
        user.save()

        messages.success(request, 'Registration successful!')
        return redirect('login')  # Redirect to login or wherever appropriate after registration

    else:
        # Display empty form if it's a GET request
        return render(request, 'register/register.html')

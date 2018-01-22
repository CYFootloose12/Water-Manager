from django import forms

from django.contrib.auth.models import User
from django.core.validators import validate_email, RegexValidator
from models import *

MAX_UPLOAD_SIZE = 2500000

LOCATION_CHOICES = (
    ('Boston, MA','Boston, MA'),
    ('New York, NY','New York, NY'),
    ('Miami, FL','Miami, FL'),
    ('Boston, MA','Houston, TX'),
    )

class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=20)
    last_name  = forms.CharField(max_length=20)
    email      = forms.CharField(max_length = 40,
                                 validators = [validate_email])
    username   = forms.CharField(max_length = 20)
    password1  = forms.CharField(max_length = 200, 
                                 label='Password', 
                                 widget = forms.PasswordInput())
    password2  = forms.CharField(max_length = 200, 
                                 label='Confirm password',  
                                 widget = forms.PasswordInput())


    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.

    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(RegistrationForm, self).clean()

        # Confirms that the two password fields match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        # We must return the cleaned data we got from our parent.
        return cleaned_data


    # Customizes form validation for the username field.
    def clean_username(self):
        # Confirms that the username is not already present in the
        # User model database.
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")

        # We must return the cleaned data we got from the cleaned_data
        # dictionary
        return username

    # Customizes form validation for the first_name field.
    def clean_first_name(self):
        #Confirms that the first name does not have any numbers in it
        first_name = self.cleaned_data.get('first_name')
        if (first_name.isalpha()):
            return first_name
        else:
            raise forms.ValidationError("Provide a first name with only lettters")

    # Customizes form validation for the last_name field.
    def clean_last_name(self):
        #Confirms that the last name does not have any numbers in it
        last_name = self.cleaned_data.get('last_name')
        if (last_name.isalpha()):
            return last_name
        else:
            raise forms.ValidationError("Provide a last name with only lettters")

    def clean_zip_code(self):
        zip_code = self.cleaned_data.get('zip_code')
        if (zip_code.isdigit() == False):
            raise forms.ValidationError("Provide a zip code with only numbers.")
        elif (len(zip_code) != 5):
            raise forms.ValidationError("Your zip code must have five digits.")
        else:
            return zip_code


class EditForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        exclude = (
            'user',
        )
    # Customizes form validation for the first_name field.
    def clean_first_name(self):
        #Confirms that the first name does not have any numbers in it
        first_name = self.cleaned_data.get('first_name')
        if (first_name.isalpha()):
            return first_name
        else:
            raise forms.ValidationError("Provide a first name with only lettters")

    # Customizes form validation for the last_name field.
    def clean_last_name(self):
        #Confirms that the last name does not have any numbers in it
        last_name = self.cleaned_data.get('last_name')
        if (last_name.isalpha()):
            return last_name
        else:
            raise forms.ValidationError("Provide a last name with only lettters")

    def clean_zip_code(self):
        zip_code = self.cleaned_data.get('zip_code')
        if (zip_code.isdigit() == False):
            raise forms.ValidationError("Provide a zip code with only numbers.")
        elif (len(zip_code) != 5):
            raise forms.ValidationError("Your zip code must have five digits.")
        else:
            return zip_code

class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        exclude = (
            'watering_times',
            'userInfo',
            )

    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(PlantForm, self).clean()
        # Confirms that the two password fields matchd
        # We must return the cleaned data we got from our parent.
        return cleaned_data

    def clean_name(self):
        #Confirms that the first name does not have any numbers in it
        name = self.cleaned_data.get('name')
        if (name.isalpha()):
            return name
        else:
            raise forms.ValidationError("Provide a name with only lettters")

    def clean_zip_code(self):
        zip_code = self.cleaned_data.get('zip_code')
        if (zip_code.isdigit() == False):
            raise forms.ValidationError("Provide a zip code with only numbers.")
        elif (len(zip_code) != 5):
            raise forms.ValidationError("Your zip code must have five digits.")
        else:
            return zip_code

    def clean_type(self):
        type = self.cleaned_data.get('type')
        possibleTypesOfPlants = ['Aloe Vera', 'Cactus', 'Daisy', 'Fern', 'Garden Sage', 
        'Lavendar', 'Mint', 'Orchid', 'Oregano', 'Petunia', 'Rose', 'Rosemary', 'Snake Plant', 'Spider Plant', 'Sunflower', 'Violet']
        if ((type in possibleTypesOfPlants) == False):
            raise forms.ValidationError("We do not recognize this plant type. Please click a plant type below.")
        return type

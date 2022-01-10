import re
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.template.response import TemplateResponse
from django.shortcuts import redirect, render
from django.db.models import Sum
from django.urls import reverse
from django.views import View

from .serializers import *
from .models import *

import pdb

class SignupView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return TemplateResponse(request, 
                                    'signup.html', 
                                    {'messages' : 'Already logged in'}
                                    )

        return TemplateResponse(request, 'signup.html')

    def post(self, request):
        user_data=dict()
        
        for key, val in request.POST.items():
            user_data[key] = request.POST.get(key)
        try:
            serializer = NewUserSerializer(data=user_data)
            if serializer.is_valid():
                serializer.save()
                return TemplateResponse(request, 
                                        'login.html', 
                                        {'messages' : 'Signup successful! Please proceed and login'}
                                        )
            else:
                return TemplateResponse(request, 
                                        'signup.html', 
                                        {'messages' : 'Incorrect identification format.'}
                                        )

        except Exception as exp:
            return TemplateResponse(request, 
                                    'signup.html', 
                                    {'messages' : 'Signup failed.'}
                                    )


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('usr:entry'))
        
        return TemplateResponse(request, 'login.html')
    
    def post(self, request):
        try:
            user = authenticate(request, 
                                username=request.POST['email'],
                                password=request.POST['password']) 

            if user is not None:
                login(request, user)
                return redirect('usr:entry')
            else:
                return TemplateResponse(request, 
                                        'login.html', 
                                        {'messages':'Login failed.'}
                                        )

        except Exception as exp:
            return TemplateResponse(request, 
                                    'login.html', 
                                    {'messages' : str(exp)}
                                    )

class Signout(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            return redirect('usr:login')
        else:
            HttpResponse('user not logged in')


class EntryView(View):
    def get(self, request):
        if request.user.is_authenticated:
            entries = EntryModel.objects.filter(owner=request.user.username,
                                                pre_delete=False)
            tot_exp = entries.aggregate(Sum('amount')).get('amount__sum', 0.00)
            return render(request, 
                        'entry.html', 
                        {'ent' : entries, 
                        'tot_exp': tot_exp}
                        )
            
        else:
            return redirect('usr:login')
        
    def post(self, request):
        try:
            if request.user.is_authenticated:
                serializer=EntrySerializer(data=request.POST)
                
                if serializer.is_valid(raise_exception=True):
                    serializer.save(owner=request.user)
                return redirect(reverse('usr:entry'))
            else:
                return TemplateResponse(request, 
                                        'entry.html', 
                                        {'messages' : 'User is not logged in.'}
                                        )

        except Exception as exp:
            return TemplateResponse(request, 
                                    'entry.html', 
                                    {'messages' : 'error.'}
                                    )


class Deleteds(View):
    def get(self, request):
        if request.user.is_authenticated:
            deleteds = EntryModel.objects.filter(owner=request.user.username).filter(pre_delete=True)
            return render(request, 
                        'entry_deleted.html', 
                        {'ent': deleteds}
                        )

        else:
            return redirect('usr:login')



@login_required()
def entry_get(request, entry_id):
    entries = EntryModel.objects.get(id=entry_id)
    entries.date = entries.date.strftime('%Y-%m-%d')
    return TemplateResponse(request, 
                            'entry_edit.html', 
                            {'ent' : entries}
                            )

@login_required()
def entry_delete(request, entry_id):
    entry = EntryModel.objects.get(pk=entry_id)
    
    if request.user.username == entry.owner:
        if entry.pre_delete == True:
            entry.delete()  
        else:
            entry.pre_delete = True
            entry.save()
        return redirect(reverse('usr:entry'))

    else:
        return TemplateResponse(request, 
                                'entry.html', 
                                {'messages' : 'Unauthorized.'}
                                )

@login_required()
def entry_revert(request, entry_id):
    entry = EntryModel.objects.get(pk=entry_id)
    if request.user.username == entry.owner:
        if entry.pre_delete == True:
            entry.pre_delete = False
            entry.save()
        return redirect(reverse('usr:entry'))

    else:
        return TemplateResponse(request, 
                                'entry.html', 
                                {'messages' : 'Unauthorized.'}
                                )

@login_required()
def entry_put(request, entry_id):
    try:
        if request.method =='POST':
            entry = EntryModel.objects.get(id=entry_id)
            if request.user.username == entry.owner:
                serializer=EntrySerializer(entry, data=request.POST)
                
                if serializer.is_valid(raise_exception=True):
                    serializer.save(owner=request.user.username)
                    return redirect(reverse('usr:entry'))

                return HttpResponse('wrong format')

            return TemplateResponse(request, 
                                    'entry.html', 
                                    {'messages' : 'Unauthorized.'}
                                    )

    except Exception as exp:
        return HttpResponse(f'error: {exp}')

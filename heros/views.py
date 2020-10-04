from django.shortcuts import render, redirect
import json
import requests
import random

# IMPORT INTERNAL ARRAYS FOR HERO ATTRIBUTES
from .hobbies import hobbies
from .cliche import cliche_list
from .rejects import rejects
from .responses import responses

# IMPORT MAIL LIBRARIES
from .second_response import second_response
from django.contrib.auth.models import User
from django.core.mail import send_mail,send_mass_mail

# USER AUTH DECORATOR
from django.contrib.auth.decorators import login_required

# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# HOMEPAGE (IF LOGGED IN) HANDLE USER GENDER CHOICE

@login_required
def homeView(request):
    
    # CREATE LIST COPY OR ORIGINAL LIST WILL REBUILD ITSELF AFTER ITERATION
    the_cliche_list=cliche_list.copy()
    gender='Female'
    dictin={}
    final_list=[]
    heros=0
    my_hobbies=[]

    # PULL DATA FROM HEROAPI

    if request.method=='POST':
		
	    gender= request.POST['gender']

    while heros < 12:
        
        number=random.randint(1,730)
        hobbies_num=random.randint(3,7)   
        

        # API KEY REMOVED FOR REPO
        url= "https://superheroapi.com/api/YOUR API KEY HERE/"+str(number)+"/image"
        urla = "https://superheroapi.com/api/YOUR API KEY HERE/"+str(number) +"/appearance"

        api_request = requests.get(url)
        apihero = json.loads(api_request.content)

        print (apihero['id'])
        
        api_requesta = requests.get(urla)
        apiheroappear = json.loads(api_requesta.content)

        if apiheroappear['gender']==gender and apihero['name']not in rejects:

            for x in range(hobbies_num):
                my_hobbies.append(random.choice(hobbies))

            name=apihero['name']
            url=apihero['url']
            height = apiheroappear['height'][0]
            weight = apiheroappear['weight'][0]
            eyecolor = apiheroappear['eye-color']
            hero_id=apihero['id']
            one_liner = random.choice(the_cliche_list)
            hero_hobbies=my_hobbies.copy()
            

            pos=the_cliche_list.index(one_liner)
            print(pos)
            del the_cliche_list[pos]

            # HANDLE NULL RESPONSES FROM API
            if height=='-':
                height='undisclosed'
            if weight=='- lb':
                weight='undisclosed'
            if eyecolor=='-':
                eyecolor='undisclosed'

            # ADD ATTRIBUTES TO HERO'S DICTIONARY OF ATTRIBUTES
            dictin.update({'url': url})
            dictin.update({'height': height})
            dictin.update({'weight': weight})  
            dictin.update({'name':name}) 
            dictin.update({'eyecolor': eyecolor})
            dictin.update({'one_liner':one_liner})
            dictin.update({'hero_hobbies': hero_hobbies})
            dictin.update({'hero_id':hero_id})

            final_list.append(dictin.copy()) 

            heros += 1
            my_hobbies.clear()
            print(the_cliche_list)
            

        elif apiheroappear['gender'] != gender:
            continue     
        
    return render(request, 'home.html', {'final_list': final_list,'number':number})

# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# HANDLE HERO ARRAYS

def introView(request):
    
    fem_dictin={}
    male_dictin = {}
    male_list=[]
    fem_list=[]
    fem_heros=0
    male_heros=0

# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# RENDER FEMALE 'HEROS'

    while fem_heros < 1:
        
        number=random.randint(1,730)
        # API KEY REMOVED FOR REPO
        url= "https://superheroapi.com/api/YOUR API KEY HERE/"+str(number)+"/image"
        urla = "https://superheroapi.com/api/YOUR API KEY HERE/"+str(number) +"/appearance"

        api_request = requests.get(url)
        apihero = json.loads(api_request.content)
        
        api_requesta = requests.get(urla)
        apiheroappear = json.loads(api_requesta.content)

       

        if apiheroappear['gender']=='Female' and apihero['name']not in rejects:

            female_name=apihero['name']
            female_url=apihero['url']
           
            fem_dictin.update({'female_url': female_url})
            fem_dictin.update({'female_name':female_name}) 

            fem_list.append(fem_dictin.copy()) 

            fem_heros += 1            

        elif apiheroappear['gender'] != 'Female':
            continue 

# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# RENDER MALE 'HEROS'

    while male_heros < 1:

        number = random.randint(1, 730)

        # API KEY REMOVED FOR REPO
        url = "https://superheroapi.com/api/YOUR API KEY HERE/" + \
            str(number)+"/image"
        urla = "https://superheroapi.com/api/YOUR API KEY HERE/" + \
            str(number) + "/appearance"

        api_request = requests.get(url)
        apihero = json.loads(api_request.content)

        api_requesta = requests.get(urla)
        apiheroappear = json.loads(api_requesta.content)

        if apiheroappear['gender'] == 'Male' and apihero['name']not in rejects:

            male_name = apihero['name']
            male_url = apihero['url']

            male_dictin.update({'male_url': male_url})
            male_dictin.update({'male_name': male_name})

            male_list.append(male_dictin.copy())

            male_heros += 1

        elif apiheroappear['gender'] != 'Male':
            continue        
        
    return render(request, 'intro.html', {'male_list': male_list,'fem_list':fem_list})


# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# HANDLE USER MESSAGES

@login_required
def sendMessage(request):
    if request.method=='POST':
	    hero_name_send= request.POST['hero_name']

    # API KEY REMOVED FOR REPO
    url= "https://superheroapi.com/api/YOUR API KEY HERE/"+str(hero_name_send)+"/image"

    api_request = requests.get(url)
    apihero = json.loads(api_request.content)

    hero_name=apihero['name']
    	    
    return render(request, 'message.html', {'hero_name': hero_name, 'hero_name_send': hero_name_send})


# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# HANDLE MESSAGES REPLY

@login_required
def messageSent(request):
    user=request.user.get_username()
    email = request.user.email

    if request.method == 'POST':
	    hero_name_send = request.POST['hero_name_send']
    your_message = request.POST['your_message']
    your_subject = request.POST['your_subject']

    # API KEY REMOVED FOR REPO
    url = "https://superheroapi.com/api/YOUR API KEY HERE/" + \
        str(hero_name_send)+"/image"
    api_request = requests.get(url)
    apihero = json.loads(api_request.content)

    hero_name = apihero['name']

    message_name = "Hello "+user+", this is "+hero_name+" from hero dating app"
    message = "Hey "+user + "! \n" + \
        random.choice(responses) + "...... \n" + \
        random.choice(second_response)+"......"+"\n\n"+"-"+hero_name

    message1 = (your_subject + " " +hero_name, your_message, email, ['herodatesite@gmail.com'])
    message2 = (message_name, message, 'ADDRESSREMOVEDFORGIT@gmail.com', [email])
    send_mass_mail((message1, message2), fail_silently=False)


    return render(request, 'message_sent.html', {'hero_name': hero_name})

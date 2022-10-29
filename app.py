from email.mime import image
import json
import profile
from re import template
from turtle import Shape
import bs4 as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import yaml
import requests
import urllib
import os
import cairosvg
import numpy as np
from PIL import Image, ImageDraw
# open config.yaml
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# create images folder if not exists
if not os.path.exists('images'):
    os.makedirs('images')



url = config['linkedin_profile']['url']

profileinfo = {
    'phone': config['info']['phone'],
    'email': config['info']['email'],
    'location': config['info']['location'],
    'discord': config['info']['discord'],
    'instant': config['info']['instant'],
    'website': config['info']['website'],
    'headline': config['info']['headline'],
}

themes = config['themes'][0]['path']

broswer = webdriver.Chrome(
    executable_path='./chromedriver_win32/chromedriver.exe')

broswer.get(url)


# get all html code from the page
html = broswer.page_source

broswer.quit()

soup = bs.BeautifulSoup(html, 'html.parser')

# get the name of the person
name = soup.find(
    'h1', class_='top-card-layout__title font-sans text-lg papabear:text-xl font-bold leading-open text-color-text mb-0').text.strip()
about = soup.find(
    'div', class_='core-section-container__content break-words').text.strip()

# find all li profile-section-card  experience-item
experience__list = soup.find_all('ul', class_='experience__list')
experience__list = soup.find_all(
    'li', class_='profile-section-card experience-item')

jobs = []

for job in experience__list:
    currentjob = {}
    currentjob['title'] = job.find(
        'h3', class_='profile-section-card__title').text.strip()
    currentjob['subtitle'] = job.find(
        'h4', class_='profile-section-card__subtitle').text.strip()
    range = job.find(
        'p', class_='experience-item__duration experience-item__meta-item').text.strip().split(' ')
    index = range[3].find('Present')
    if index != -1:
        number = range[3].replace('Present', '')
        range[3] = 'Present ' + number
    else:
        # remove first 4 characters from string
        year = range[4][0:4]
        number = range[4][4:]
        range[4] = year + ' ' + number
    # join the list
    currentjob['range'] = ' '.join(range)
    currentjob['location'] = job.find(
        'p', class_='experience-item__location experience-item__meta-item').text.strip()
    if (job.find('p', class_='show-more-less-text__text--more')) != None:
        currentjob['description'] = job.find(
            'p', class_='show-more-less-text__text--more').text.strip()
    else:
        currentjob['description'] = job.find(
            'p', class_='show-more-less-text__text--less').text.strip()
    currentjob['image'] = job.find('img')['data-delayed-url']
    jobs.append(currentjob)

edus = []

educations = soup.find_all(
    'li', class_='profile-section-card education__list-item')
for education in educations:
    edu = {}
    edu['school'] = education.find(
        'h3', class_='profile-section-card__title').text.strip()
    degrees = education.find_all(
        'span', class_='education__item education__item--degree-info')
    degreetext = ''
    for degree in degrees:
        degreetext += degree.text.strip() + ' '
    edu['degree'] = degreetext

    edu['range'] = education.find(
        'p', class_='education__item education__item--duration').text.strip()
    if education.find('p', class_='education__item education__item--activities-and-societies') != None:
        edu['activities'] = education.find(
            'p', class_='education__item education__item--activities-and-societies').text.strip()

    try:
        edu['description'] = education.find(
            'div', class_='show-more-less-text').text.strip()
    except:
        edu['description'] = ''

    edu['image'] = education.find('img')['data-delayed-url']

    edus.append(edu)

certs = []

certifications = soup.find_all('ul', class_='certifications__list')[0]
certifications = certifications.find_all('li', class_='profile-section-card')

for certification in certifications:
    cert = {}
    cert['title'] = certification.find(
        'h3', class_='profile-section-card__title').text.strip()
    cert['image'] = certification.find('img')['data-delayed-url']
    cert['subtitle'] = certification.find(
        'h4', class_='profile-section-card__subtitle').text.strip()
    cert['range'] = certification.find(
        'span', class_='certifications__start-date').text.strip()
    try:
        cert['credentialid'] = certification.find(
            'div', class_='certifications__credential-id').text.strip()
    except:
        cert['credentialid'] = ''
    try:
        cert['link'] = certification.find(
            'a', class_='certifications__button')['href']
    except:
        cert['link'] = ''

    certs.append(cert)

pubs = []
publications = soup.find_all('ul', class_='publications__list')[0]

publications = publications.find_all(
    'li', class_='profile-section-card personal-project')

for publication in publications:
    pub = {}
    pub['title'] = publication.find(
        'h3', class_='profile-section-card__title').text.strip()
    pub['subtitle'] = publication.find(
        'h4', class_='profile-section-card__subtitle').text.strip().replace('\n', '')
    # remove unnecessary spaces with a line
    pub['subtitle'] = ' '.join(pub['subtitle'].split())

    try:
        pub['description'] = publication.find(
            'p', class_='show-more-less-text__text--more').text.strip()
    except:
        try:
            pub['description'] = publication.find(
                'p', class_='show-more-less-text__text--less').text.strip()
        except:
            pub['description'] = ''

    try:
        pub['link'] = publication.find(
            'a', class_='personal-project__button')['href']
    except:
        pub['link'] = ''
    pubs.append(pub)


import qrcode
img = qrcode.make(profileinfo['website'])
img.save('images/qrcode.png')



# save the data in a json file
data = {
    'name': name,
    'about': about,
    'jobs': jobs,
    'education': edus,
    'certifications': certs,
    'publications': pubs,
    'profile_info': profileinfo,
    'linkedin_url': url,
    'qrcode': 'images/qrcode.png',
}




# save all images in images folder with extension as downloaded

global imageindex
imageindex = 0
def downloadImages(arr):    
    global imageindex
    for a in arr:
        try:            
            imageurl = a['image']
            #download image
            image = requests.get(imageurl) 
            # check if image is a jpeg or svg
            if image.headers['Content-Type'] == 'image/jpeg':
                with open('images/' + str(imageindex) + '.jpg', 'wb') as f:
                    f.write(image.content)                
                    a['image'] = 'images/' + str(imageindex) + '.jpg'
            else:                
                with open('images/' + str(imageindex) + '.svg', 'wb') as f:
                    f.write(image.content)
                #convert svg using cairosvg
                cairosvg.svg2png(url='images/' + str(imageindex) + '.svg', write_to='images/' + str(imageindex) + '.png')
                a['image'] = 'images/' + str(imageindex) + '.png'
                                                                      
            imageindex += 1
        except:
            pass

profilephoto = soup.find('div', class_='top-card__profile-image-container top-card-layout__entity-image-container flex top-card__profile-image-container--cvw-fix')
profilephoto = profilephoto.find('img')['src']
profilephoto = requests.get(profilephoto)
with open('images/profilephoto.jpg', 'wb') as f:
    f.write(profilephoto.content)

# Open the input image as numpy array, convert to RGB
img=Image.open("images/profilephoto.jpg").convert("RGB")
npImage=np.array(img)
h,w=img.size

# Create same size alpha layer with circle
alpha = Image.new('L', img.size,0)
draw = ImageDraw.Draw(alpha)
draw.pieslice([0,0,h,w],0,360,fill=255)

# Convert alpha Image to numpy array
npAlpha=np.array(alpha)

# Add alpha layer to RGB
npImage=np.dstack((npImage,npAlpha))

# Save with alpha
Image.fromarray(npImage).save('images/profilephoto.png')

data['profile_photo'] = 'images/profilephoto.png'




downloadImages(jobs)
downloadImages(edus)
downloadImages(certs)
downloadImages(pubs)

        
with open('data.json', 'w') as outfile:
    json.dump(data, outfile)
  


from docx.shared import Cm
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Cm, Inches, Mm, Emu



template = DocxTemplate(themes)

data['qrcode'] = InlineImage(template, 'images/qrcode.png', width=Mm(30.27))

# set all InlineImages
def setInlineImages(arr):
    for a in arr:
        try:
            a['image'] = InlineImage(template, a['image'], width=Mm(15.19))
        except:
            pass

setInlineImages(jobs)
setInlineImages(edus)
setInlineImages(certs)
setInlineImages(pubs)

#set profile photo as InlineImage circle
data['profile_photo'] = InlineImage(template, 'images/profilephoto.png', width=Mm(25.82), height=Mm(25.82))

template.render(data)

template.save('cv.docx')
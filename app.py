from docx.shared import Mm
from docxtpl import DocxTemplate, InlineImage
import qrcode
import re
import json
from re import template
import bs4 as bs
import yaml
import requests
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

themes = config['themes'][0]['path']

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

# if scrape.html exists
if os.path.exists('scrape.html'):
    # open scrape.html
    with open('scrape.html', 'r', encoding="utf8") as f:
        html = f.read()
    soup = bs.BeautifulSoup(html, 'html.parser')
else:
    # kill script
    def kill():
        print('Follow the instructions in the README.md file, scrape.html not found!')
        exit()
    kill()

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


def cleanText(text):
    text = text.replace('\n', '')
    text = ' '.join(text.split())
    text = re.sub('<[^<]+?>', '', text)
    return text


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
            'p', class_='show-more-less-text__text--more').text.strip().replace('\n', '')

    else:
        currentjob['description'] = job.find(
            'p', class_='show-more-less-text__text--less').text.strip().replace('\n', '')
    currentjob['image'] = job.find('img')['src']
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
        edu['description'] = edu['description']
    except:
        edu['description'] = ''

    edu['image'] = education.find('img')['src']

    edus.append(edu)

certs = []

certifications = soup.find_all('ul', class_='certifications__list')[0]
certifications = certifications.find_all('li', class_='profile-section-card')

for certification in certifications:
    cert = {}
    cert['title'] = certification.find(
        'h3', class_='profile-section-card__title').text.strip()
    cert['image'] = certification.find('img')['src']
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
        'h4', class_='profile-section-card__subtitle').text.strip()
    try:
        pub['description'] = publication.find(
            'p', class_='show-more-less-text__text--more').text.strip()
        # remove line breaks
        pub['description'] = cleanText(pub['description'])
    except:
        try:
            pub['description'] = publication.find(
                'p', class_='show-more-less-text__text--less').text.strip()
            pub['description'] = cleanText(pub['description'])
        except:
            pub['description'] = ''

    try:
        pub['link'] = publication.find(
            'a', class_='personal-project__button')['href']
    except:
        pub['link'] = ''
    pubs.append(pub)


img = qrcode.make(profileinfo['website'])
img.save('images/qrcode.png')


# save the data in a json file
data = {
    'name': cleanText(name),
    'about': cleanText(about),
    'jobs': jobs,
    'education': edus,
    'certifications': certs,
    'publications': pubs,
    'profile_info': profileinfo,
    'linkedin_url': url,
    'qrcode': 'images/qrcode.png',
}

# clean education
for edu in data['education']:
    edu['school'] = cleanText(edu['school'])
    edu['degree'] = cleanText(edu['degree'])
    edu['range'] = cleanText(edu['range'])
    try:
        edu['activities'] = cleanText(edu['activities'])
    except:
        pass
    edu['description'] = cleanText(edu['description'])

# clean jobs
for job in data['jobs']:
    job['title'] = cleanText(job['title'])
    job['subtitle'] = cleanText(job['subtitle'])
    job['range'] = cleanText(job['range'])
    job['location'] = cleanText(job['location'])
    job['description'] = cleanText(job['description'])

# clean certifications
for cert in data['certifications']:
    cert['title'] = cleanText(cert['title'])
    cert['subtitle'] = cleanText(cert['subtitle'])
    cert['range'] = cleanText(cert['range'])
    cert['credentialid'] = cleanText(cert['credentialid'])

# clean publications
for pub in data['publications']:
    pub['title'] = cleanText(pub['title'])
    pub['subtitle'] = cleanText(pub['subtitle'])
    pub['description'] = cleanText(pub['description'])


# save all images in images folder with extension as downloaded

global imageindex
imageindex = 0


def downloadImages(arr):
    global imageindex
    for a in arr:
        try:
            imageurl = a['image']
            # download image
            image = requests.get(imageurl)
            # check if image is a jpeg or svg
            if image.headers['Content-Type'] == 'image/jpeg':
                with open('images/' + str(imageindex) + '.jpg', 'wb') as f:
                    f.write(image.content)
                    a['image'] = 'images/' + str(imageindex) + '.jpg'
            else:
                with open('images/' + str(imageindex) + '.svg', 'wb') as f:
                    f.write(image.content)
                # convert svg using cairosvg
                cairosvg.svg2png(url='images/' + str(imageindex) +
                                 '.svg', write_to='images/' + str(imageindex) + '.png')
                a['image'] = 'images/' + str(imageindex) + '.png'

            imageindex += 1
        except:
            pass


profilephoto = soup.find(
    'div', class_='top-card__profile-image-container top-card-layout__entity-image-container flex top-card__profile-image-container--cvw-fix')
profilephoto = profilephoto.find('img')['src']
profilephoto = requests.get(profilephoto)
with open('images/profilephoto.jpg', 'wb') as f:
    f.write(profilephoto.content)

# Open the input image as numpy array, convert to RGB
img = Image.open("images/profilephoto.jpg").convert("RGB")
npImage = np.array(img)
h, w = img.size

# Create same size alpha layer with circle
alpha = Image.new('L', img.size, 0)
draw = ImageDraw.Draw(alpha)
draw.pieslice([0, 0, h, w], 0, 360, fill=255)

# Convert alpha Image to numpy array
npAlpha = np.array(alpha)

# Add alpha layer to RGB
npImage = np.dstack((npImage, npAlpha))

# Save with alpha
Image.fromarray(npImage).save('images/profilephoto.png')

data['profile_photo'] = 'images/profilephoto.png'


downloadImages(jobs)
downloadImages(edus)
downloadImages(certs)
downloadImages(pubs)


with open('data.json', 'w') as outfile:
    json.dump(data, outfile)


# for all text remove line breaks and remove extra spaces
template = DocxTemplate(themes)

data['qrcode'] = InlineImage(template, 'images/qrcode.png', width=Mm(20))

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

# set profile photo as InlineImage circle
data['profile_photo'] = InlineImage(
    template, 'images/profilephoto.png', width=Mm(25.82), height=Mm(25.82))

template.render(data)

template.save('cv.docx')
print('Check out cv.docx!')

import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import cv2 
import pytesseract
from datetime import datetime, date, timedelta

#Image chargée
img_correct = cv2.imread('Etiquette_sourire_info.PNG')
img_bug = cv2.imread('Etiquette_sourire_info_bug.PNG')

#Chemin de Tesseract
# pytesseract.pytesseract.tesseract_cmd = r'.`\Tesseract\tesseract.exe'

#Config de tesseract
custom_config = '--oem 1 --psm 7'

#Titre
st.title('TEST ETIQUETAGE')
#Affiche l'image chargée
st.image([img_correct, img_bug], width = 300)

type_image = st.radio("Quelle image tester",('Avec la date', 'Sans la date'))

#Si on appuie le bouton
if type_image == 'Avec la date' :
    img = img_correct
elif type_image == 'Sans la date':
    img = img_bug

if st.button('Test Libellé'):
    cropped_img = img[50:75, 0:300]
    cropped_img = cv2.resize(cropped_img, (3*cropped_img.shape[1],3*cropped_img.shape[0] ), interpolation = cv2.INTER_AREA)
    result = pytesseract.image_to_string(cropped_img, config=custom_config).split("\n")[0]
    st.write(result)
else:
    st.write('')

if st.button('Test n° Lot'):
    cropped_img = img[210:240, 200:350]
    cropped_img = cv2.resize(cropped_img, (2*cropped_img.shape[1],2*cropped_img.shape[0] ), interpolation = cv2.INTER_AREA)
    result = pytesseract.image_to_string(cropped_img, config=custom_config).split('\n')[0]
    st.write(result.split(' ')[1])
else:
    st.write('')

if st.button('Test Date'):
    cropped_img = img[210:250, 50:160]
    cropped_img = cv2.resize(cropped_img, (2*cropped_img.shape[1],2*cropped_img.shape[0] ), interpolation = cv2.INTER_AREA)
    result = pytesseract.image_to_string(cropped_img, config=custom_config).split('\n')[0]
    #result = "zz"
    try :
        date_time_result = datetime.strptime(result, '%d-%m-%Y').date()
        st.write(result)
        today = date.today()
        delta = today-date_time_result
        if delta > timedelta(days=15) : 
            st.write("Aujourd'hui : {dateAjd},  DLC du produit : {dateDLC} | date limite de consommation expirée".format(dateAjd = today, dateDLC = date_time_result))
        else :
            st.write("Aujourd'hui : {dateAjd},  DLC du produit : {dateDLC} | date limite de consommation valable".format(dateAjd = today, dateDLC = date_time_result))
    except ValueError :
        st.write("Date eronnée ou non détectée : {resultat}".format(resultat = result))
else:
    st.write('')

add_selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone")
)

st.sidebar.image(img_correct)


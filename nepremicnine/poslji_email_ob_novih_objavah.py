import bs4
import os
import json
import requests
import smtplib

# Pozor! Da lahko kodo zaženemo, je potrebno inštalirati zunanje (nestandardne) knjižnice. To se naredi tako, da se
# odpre terminal, in zažene naslednji ukaz:
# pip3 install -r nepremicnine/requirements.txt


def dobi_html_kodo(url):
    #S pomočjo knjižnice requests tako dobimo HTML kodo na neki spletni strani.
    html_koda = requests.get(url).text
    return html_koda


def najdi_vse_povezave_nepremicnin_v_html_kodi(html_koda):
    # Iz HTML kode s pomočjo knjižnice bs4 preberemo vse data-href atribute h2 tagov, ki se nahajajo znotraj div-ov
    # z class="oglas_container". Do tega, kje se željeni podatki nahajajo, pridemo tako, da uporabimo Preglej/Inspect
    # znotraj brskalnika in preberemo HTML izvorno kodo spletne strani.
    stran = bs4.BeautifulSoup(html_koda, 'html.parser')
    vse_nepremicnine = []
    for o in stran.find_all("div", {"class": "oglas_container"}):
        link = o.h2["data-href"]
        print("Na strani sem našel to povezavo do nepremičnine: " + link)

        vse_nepremicnine.append("https://www.nepremicnine.net" + link)
    return vse_nepremicnine


def preberi_ze_videne_povezave_nepremicnin():
    # Preberimo že videne nepremičnine.
    if os.path.exists("podatki.txt"):
        with open("podatki.txt") as f:
            ze_videne_nepremicnine = json.loads(f.read())
        return ze_videne_nepremicnine
    else:
        # Ce datoteka ne obstaja, vrni prazen seznam.
        return []


def filtriraj_nove_nepremicnine(vse_nepremicnine, ze_videne_nepremicnine):
    # Vrni samo nove nepremičnine, ki še niso videne.
    nove_nepremicnine = []
    for nepremicnina in vse_nepremicnine:
        if nepremicnina not in ze_videne_nepremicnine:
            nove_nepremicnine.append(nepremicnina)
    return nove_nepremicnine


def shrani_vse_nepremicnine(ze_videne_nepremicnine, nove_nepremicnine):
    # Shrani že videne + nove nepremičnine nazaj v isto datoteko.
    with open("podatki.txt", "w") as f:
        f.write(json.dumps(ze_videne_nepremicnine + nove_nepremicnine))


def poslji_email(nove_nepremicnine):
    # Pošlji email z Gmail računa.
    # Za pošiljanje emaila je potrebno vnesti podatke.
    # Zato, da je možno pošiljati z Gmaila, je potrebno odpreti stran https://myaccount.google.com/u/2/lesssecureapps?pageId=none
    # v brskalniku in označiti "Allow less secure apps".
    email_posiljatelja = ""
    gmail_geslo = ""
    email_prejemnika = ""


    telo_emaila = "Nove nepremičnine so:\n"
    for nepremicnina in nove_nepremicnine:
        telo_emaila += nepremicnina + "\n"

    # Naredi prazno vrstico, za lepši izpis.
    print()

    print("Pošiljam email s tem telesom:")
    print(telo_emaila)

    if email_posiljatelja == "" or gmail_geslo == "" or email_prejemnika == "":
        print("Ne morem poslati emaila. Prosim vnesi email pošiljatelja (podprt samo Gmail), njegovo Gmail geslo, ter "
              "email prejemnika.")
        return


    message = "Subject: Nove nepremičnine 2\n\n" + telo_emaila
    s = smtplib.SMTP("smtp.gmail.com", 587)
    s.starttls()

    s.login(email_posiljatelja, gmail_geslo)
    s.sendmail(email_posiljatelja, email_prejemnika, message.encode("UTF-8"))

    print("Uspešno poslal email. Preveri, ali se nahaja v spamu.")


# Za uporabo tega programa odpri nepremicnine.net, prikaži rezultate, nastavi filtre, in skopiraj povezavo v to
# spremenljivko.
url_iskanja = "https://www.nepremicnine.net/oglasi-prodaja/ljubljana-okolica/kamnik/stanovanje/2-sobno/"

html_koda = dobi_html_kodo(url_iskanja)
vse_nepremicnine = najdi_vse_povezave_nepremicnin_v_html_kodi(html_koda)
ze_videne_nepremicnine = preberi_ze_videne_povezave_nepremicnin()

nove_nepremicnine = filtriraj_nove_nepremicnine(vse_nepremicnine, ze_videne_nepremicnine)

if len(nove_nepremicnine) > 0:
    shrani_vse_nepremicnine(ze_videne_nepremicnine, nove_nepremicnine)

    poslji_email(nove_nepremicnine)
else:
    print("Ni novih nepremicnin.")

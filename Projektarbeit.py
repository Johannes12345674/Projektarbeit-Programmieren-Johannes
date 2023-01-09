from turtle import title
import streamlit as st
import pandas as pd
import os
import json 
from PIL import Image
import toml
import numpy as np
import altair as alt



# #Streamlit über anaconda Starten:
# Terminal öffnen
# mit "dir" werden Ordner angezeigt
# mit "cd" Ordner auswählen und Enter drücken 
# dann wieder mit "dir" Ordner anzeigen lassen.
# bis in Ordner navigieren in dem die Phyten Datei abgespeichert ist und dann 
# streamlit run "Dateiname.py" und Enter drücken.

# # Redis Starten:
# auf Anaconda ein Terminal öffnen:
# "redis-server" eingeben.


#Redis Verbindung
from base64 import decode
import redis

host = "localhost"
port = "6379"

r = redis.Redis(
    host = host,
    port = port,
    decode_responses=True   #mit dem decode befehl wird das b' vor der Ausgabe im Terminal weggelassen
)



sections= st.sidebar.radio("Kategorien", ("Gebäudeautomation", "Wetterdaten", "Heizung", "Lichtsteuerung", "Personenkontrolle", "Lüftung"))
if sections== "Gebäudeautomation":
    st.title("Gebäudeautomation")
    st.header("Hilfestellung")
    st.write("Hier haben sie eine schöne Übersicht für zu Ihrer Gebäudeautomation.")
    st.write("Sie können Sich links in den Kategorieren die verschiedenen Daten ihres Gebäudes genauer Betrachten.")

elif sections== "Wetterdaten":
    st.title("Wetterdaten")
    st.header("Temperaturunterschiede Jena")
    #Diagramm 1
    df = pd.read_csv("C:\Users\johan\Desktop\jena_climate_2009_2016.csv")
    df = df.iloc[:30,:]
  
    chart = alt.Chart(df).mark_line().encode(
        x=alt.X('Date Time'),
        y=alt.Y('T (degC)'),
        color=alt.Color("name:N")
        ).properties(title="Temperaturverlauf Jena 2009")
    st.altair_chart(chart, use_container_width=True)
    #Diagramm 2
    df1 = pd.read_csv("C:\Users\johan\Desktop\jena_climate_2009_2016.csv")
    df1 = df1.iloc[368300:368330,:]

    chart = alt.Chart(df1).mark_line().encode(
        x=alt.X('Date Time'),
        y=alt.Y('T (degC)'),
        color=alt.Color("name:N")
        ).properties(title="Temperaturverlauf Jena 2016")
    st.altair_chart(chart, use_container_width=True)
    
    st.write("Im vergleich zum Jahr 2009 ist es im Jahr 2016 deutlich wärmer. Daraus kann man schliessen das sich die Erde Erwärmt.")

   
    

elif sections== "Heizung":
    st.title("Heizung")
    #1. Knopf erstellen

    if not os.path.isfile("EIN"):
        with open("EIN", "w")as f:
            json.dump({"clicks":0},f)
    with open ("EIN")as f:

        counter = json.load(f)["clicks"]

    if st.button("EIN"):
        counter +=1
        st.success("Es Heizt", icon="✅")

    st.write(f"Die Heizung ist Eingeschaltet: {counter}")

    #2. Knopf erstellen

    if not os.path.isfile("AUS"):

        with open("AUS", "w")as f:

            json.dump({"clicks":0},f)

    with open ("AUS")as f:

        counter = json.load(f)["clicks"]

    if st.button("AUS"):

        counter +=1
        st.error("ES Heizt nicht", icon="✖")

    st.write(f"Die Heizung ist Ausgeschaltet: {counter}")
    

    st.header("Momentanwerte")
    Temp={
    "Aussentemp": 18,
    "innentemp": 22,
    "Vorlauftemp": 25,
    "rücklauftemp":20}

    Temperaturen = pd.DataFrame(Temp.items(),columns=["Temp","Grad"])

    st.bar_chart(data=Temperaturen,x="Temp", y="Grad")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Aussentemp", "18 °C", "1.2 °C")
    col2.metric("Innentemp", "22 °C", "0.8 °C")
    col3.metric("Vorlauftemp", "25 °C", "3 °C")
    col4.metric("Rücklauftemp", "20 °C", "-1.2 °C")


elif sections== "Lichtsteuerung":
    st.title("Lichtsteuerung")
    st.header("Wohnen")
    #1. Knopf erstellen

    if not os.path.isfile("EIN"):
        with open("EIN", "w")as f:
            json.dump({"clicks":0},f)
    with open ("EIN")as f:

        counter = json.load(f)["clicks"]

    if st.button("EIN"):
        counter +=1
        st.success("Die Lampe Leuchtet", icon="✅")
        st.image("https://i.pinimg.com/564x/8c/74/5f/8c745fb5e3063ae7af70c2522951f190.jpg")

    st.write(f"Die Lampe ist Eingeschaltet: {counter}")

    #2. Knopf erstellen

    if not os.path.isfile("AUS"):

        with open("AUS", "w")as f:

            json.dump({"clicks":0},f)

    with open ("AUS")as f:

        counter = json.load(f)["clicks"]

    if st.button("AUS"):

        counter +=1
        st.error("Die Lampe Leuchtet nicht", icon="✖")

    st.write(f"Die Lampe ist Ausgeschaltet: {counter}")


elif sections== "Personenkontrolle":
    st.title("Personenkontrolle")
    #Redis 
    st.header("Personen-Zähl-System")
    
    if st.button("Sensor-Eingang"):
        r.incrby("Besucher",1)



    if st.button("Sensor-Ausgang"):
        r.incrby("Besucher",-1)

    st.header("Wie viele Personen sind im Gebäude")
    if st.button(label="Abfrage",help="hier drücken"):
        Anzahl = r.get ("Besucher")
        st.write("Momentan sind:",Anzahl,"Personen im Gebäude")

   

elif sections== "Lüftung":

    st.title("Lüftung")

    if not os.path.isfile("EIN"):
        with open("EIN", "w")as f:
            json.dump({"clicks":0},f)
    with open ("EIN")as f:

        counter = json.load(f)["clicks"]

    if st.button("EIN"):
        counter +=1
        st.success("Die Lüftung wird eingeschaltet", icon="✅")
        
        
    

#2. Knopf erstellen

    if not os.path.isfile("AUS"):

        with open("AUS", "w")as f:

            json.dump({"clicks":0},f)

    with open ("AUS")as f:

        counter = json.load(f)["clicks"]

    if st.button("AUS"):

        counter +=1
        st.error("Die Lüftung wird abgeschaltet", icon="✖")
    Stufe = st.select_slider(
        'Wähle eine Lüftungsstufe',
        options=['Stufe 1', 'Stufe 2', 'Stufe 3', 'Stufe 4', 'Stufe 5'])
    st.write('Die Lüftung ist auf', Stufe)

    
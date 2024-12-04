import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Page configuration
st.set_page_config(page_title="Two-Page Dashboard", layout="wide")

# Navigation menu
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Page 1: Info & Tables", "Page 2: Interactive Graph"])

df = pd.read_excel('sloterdijk_master.xlsx')
profielen = pd.read_excel('profielen_RWS.xlsx')
jaarverbruik = pd.read_csv('table__84651NED.csv').loc[lambda d: d.Perioden == '2020*'][["Vrachtauto's en trekkers gewicht", 'Gemiddeld jaarkilometrage Totaal gemiddeld jaarkilometrage (aantal\xa0km)']]
jaarverbruik.columns = ['type','kms/jaar']
jaarverbruik['kms/jaar'] = jaarverbruik['kms/jaar'].astype(str).str.replace('.','').astype(int)
jaarverbruik = pd.concat([jaarverbruik, pd.DataFrame({'type' : 'bestelbus','kms/jaar' : 18000}, index = [0])], ignore_index = True)
jaarverbruik.set_index('type', inplace = True)

verbruik_cat1 = df.groupby('categorie1').jaarverbruik.sum()

df_values = pd.DataFrame({'type' : ['Aantal trucks','Aantal bestelwagens'],'Aantal':[df['trucks'].sum(),df['bestelbussen'].sum()]})

st.sidebar.write('Totale aantallen voertuigen')
df_values = st.sidebar.data_editor(df_values)

# Page 1: Text, Images, and Tables
if page == "Page 1: Info & Tables":
    st.title("Welkom op het dashboard van Sloterdijk Poort Noord")
    
	#kolommen maken voor pagina
    cols = st.columns(3)

	#afbeeldingen en getallen voertuigen toevoegen
    icon_bestelwagen = "https://raw.githubusercontent.com/isamuu/dashboard/main/Icons%20dashboard/db%20bestelwagen.jpg"
    aantal_bestelwagen = int(df["bestelbussen"].sum())
    icon_bestelwagen_html = f'''<img src="{icon_bestelwagen}" width="150" style="display: block; margin: auto;">
    <p style="text-align: center; font-size: 24px;">{aantal_bestelwagen} Bestelwagens</p>'''

    icon_truck = "https://raw.githubusercontent.com/isamuu/dashboard/main/Icons%20dashboard/db%20truck.jpg"
    aantal_truck = int(df["trucks"].sum())
    icon_truck_html = f'''<img src="{icon_truck}" width="150" style="display: block; margin: auto;">
    <p style="text-align: center; font-size: 24px;">{aantal_truck} Trucks</p>'''
    
    icon_bedrijf = "https://raw.githubusercontent.com/isamuu/dashboard/main/Icons%20dashboard/db%20bedrijf.jpg"
    aantal_bedrijf = len(df['bedrijfsnaam'].unique())
    icon_bedrijf_html = f'''<img src="{icon_bedrijf}" width="150" style="display: block; margin: auto;">
    <p style="text-align: center; font-size: 24px;">{aantal_bedrijf} Bedrijven</p>'''
 
 # Display content in the first column
    cols[0].markdown(icon_bedrijf_html, unsafe_allow_html=True)
    cols[1].markdown(icon_truck_html, unsafe_allow_html=True)
    cols[2].markdown(icon_bestelwagen_html, unsafe_allow_html=True)

    st.title('Dataset')
    st.write("Hieronder staat de dataset achter het dashboard. Deze is verzameld door studenten logistiek en waar nodig aangevuld met sectorspecifieke getallen van het CBS.")

    st.write(df[['bedrijfsnaam','categorie1','categorie2','trucks','bestelbussen','jaarverbruik']].rename(columns = {'categorie1' : 'hoofdcategorie', 'categorie2' : 'subcategorie','jaarverbruik' : 'jaarverbruik (kWh)'}))
	
    st.write('Daarnaast zijn de volgende jaar kilometrages gebruikt voor de trucks en bestelbussen:')
	
    st.write(jaarverbruik.reset_index())


# Page 2: Interactive Stacked Area Graph
elif page == "Page 2: Interactive Graph":
    st.title("Inzicht in de bronnen en piekmomenten van de elektriciteitsvraag")
	
    cols2 = st.columns(2)
	
    resolution = cols2[0].radio("Select Time Resolution", ["Hourly", "Daily", "Monthly"])
    smart = cols2[1].radio("Select charging strategy", ["Normaal", "Smart charging"])
	
    if smart == "Normaal":
        drop_cols = ['truck_smart','bestel_smart']
    elif smart == "Smart charging":
        drop_cols = ['truck','bestel']

    verbruik_uur_mobiliteit = pd.DataFrame({'truck' : profielen['LADEN NORMAAL']*df_values.set_index('type').loc['Aantal trucks']['Aantal'] * 1.2 * jaarverbruik['kms/jaar'].loc['Gewicht volle wagen:10 000 tot 20 000 kg'] ,
                                      'truck_smart' : profielen['LADEN SMART']*df_values.set_index('type').loc['Aantal trucks']['Aantal'] * 1.2 * jaarverbruik['kms/jaar'].loc['Gewicht volle wagen:10 000 tot 20 000 kg'],
                                      'bestel' : profielen['LADEN NORMAAL']*df_values.set_index('type').loc['Aantal bestelwagens']['Aantal'] * 0.3 * jaarverbruik['kms/jaar'].loc['bestelbus'],
                                      'bestel_smart' : profielen['LADEN SMART']*df_values.set_index('type').loc['Aantal bestelwagens']['Aantal'] * 0.3 * jaarverbruik['kms/jaar'].loc['bestelbus'],
									  'datetime' : profielen['datetime']}).set_index('datetime')
    # Resolution selection
	
    verbruik_15min_panden = pd.DataFrame({'INDUSTRIE pand' : profielen['INDUSTRIE']*verbruik_cat1['INDUSTRIE'],
                                    'KANTOOR_ONDERWIJS pand' : profielen['KANTOOR_ONDERWIJS']*verbruik_cat1['KANTOOR/ONDERWIJS'],
                                    'LOGISTIEK pand' : profielen['LOGISTIEK']*verbruik_cat1['LOGISTIEK'],
                                    'OVERIG pand' : profielen['OVERIG']*verbruik_cat1['OVERIG'],
									'datetime' : profielen['datetime']}).set_index('datetime')
    verbruik_uur_panden = verbruik_15min_panden.resample('1h').sum()
    verbruik_uur_totaal = pd.concat([verbruik_uur_panden, verbruik_uur_mobiliteit], axis=1)	

    if resolution == "Hourly":
        time_series_data = verbruik_uur_totaal.drop(drop_cols, axis = 1).loc['2023-01-01':'2023-01-07'].reset_index().melt(id_vars = 'datetime', var_name = 'bron', value_name = 'Vermogen')
    elif resolution == "Daily":
        time_series_data = verbruik_uur_totaal.drop(drop_cols, axis = 1).loc['2023-01'].resample('1d').max().reset_index().melt(id_vars = 'datetime', var_name = 'bron', value_name = 'Vermogen')
    elif resolution == "Monthly":
        time_series_data = verbruik_uur_totaal.drop(drop_cols, axis = 1).resample('1M').max().reset_index().melt(id_vars = 'datetime', var_name = 'bron', value_name = 'Vermogen')


    # Plot stacked area chart
    fig = px.area(
        time_series_data, x="datetime", y="Vermogen", color="bron",
        title=f"Stacked Area Chart ({resolution} Resolution)"
    )
    st.plotly_chart(fig, use_container_width=True)

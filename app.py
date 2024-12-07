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
df['etruck_extra'] = 0
df['etruck_extra'] = np.where(df['bedrijfsnaam'].str.contains('Sligro'),30,df['etruck_extra'])
df['etruck_extra'] = np.where(df['bedrijfsnaam'].str.contains('Post NL SCB'),4,df['etruck_extra'])

profielen = pd.read_excel('profielen_RWS.xlsx')
jaarverbruik = pd.read_csv('table__84651NED.csv').loc[lambda d: d.Perioden == '2020*'][["Vrachtauto's en trekkers gewicht", 'Gemiddeld jaarkilometrage Totaal gemiddeld jaarkilometrage (aantal\xa0km)']]
jaarverbruik.columns = ['type','kms/jaar']
jaarverbruik['kms/jaar'] = jaarverbruik['kms/jaar'].astype(str).str.replace('.','').astype(int)
jaarverbruik = pd.concat([jaarverbruik, pd.DataFrame({'type' : 'bestelbus','kms/jaar' : 18000}, index = [0])], ignore_index = True)
jaarverbruik.set_index('type', inplace = True)

verbruik_cat1 = df.groupby('categorie1').jaarverbruik.sum()

df_values = pd.DataFrame({'Jaar' : [2024,2030,2035,2050],
'Aantal trucks' : [df['trucks'].sum(), (df['trucks'].sum() - int(0.16*df['trucks'].sum())), (df['trucks'].sum() - int(0.42*df['trucks'].sum())), (df['trucks'].sum() - int(0.75*df['trucks'].sum()))],
'Aantal bestelwagens' : [df['bestelbussen'].sum(),(df['bestelbussen'].sum() - int(0.20*df['bestelbussen'].sum())),(df['bestelbussen'].sum() - int(0.50*df['bestelbussen'].sum())),(df['bestelbussen'].sum() - (1.0*df['bestelbussen'].sum()))],
'Aantal e-trucks' : [df['etrucks'].sum(), (df['etrucks'].sum() + df['etruck_extra'].sum() + int(0.16*df['trucks'].sum())), (df['etrucks'].sum() + df['etruck_extra'].sum() + int(0.42*df['trucks'].sum())), (df['etrucks'].sum() + df['etruck_extra'].sum() + (0.75*df['trucks'].sum()))],
'Aantal e-bestelwagens': [df['ebestel'].sum(),(df['ebestel'].sum() + int(0.20*df['bestelbussen'].sum())),(df['ebestel'].sum() + int(0.50*df['bestelbussen'].sum())),(df['ebestel'].sum() + int(1.0*df['bestelbussen'].sum()))]})

st.sidebar.write('Totale aantallen voertuigen')
df_values = st.sidebar.data_editor(df_values)

# Page 1: Text, Images, and Tables
if page == "Page 1: Info & Tables":
    st.title("Welkom op het dashboard van Sloterdijk Poort Noord")
    
	#kolommen maken voor pagina
    cols = st.columns(3)

	#afbeeldingen en getallen voertuigen toevoegen
    icon_bestelwagen = "https://raw.githubusercontent.com/isamuu/dashboard/main/Icons%20dashboard/db%20bestelwagen.jpg"
    aantal_bestelwagen = int(df["bestelbussen"].sum() + df["ebestel"].sum())
    icon_bestelwagen_html = f'''<img src="{icon_bestelwagen}" width="150" style="display: block; margin: auto;">
    <p style="text-align: center; font-size: 24px;">{aantal_bestelwagen} Bestelwagens</p>'''

    icon_truck = "https://raw.githubusercontent.com/isamuu/dashboard/main/Icons%20dashboard/db%20truck.jpg"
    aantal_truck = int(df["trucks"].sum() + df["etrucks"].sum())
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
	
    st.write("## De ontwikkeling van de energievraag over de tijd")
	
    df_tijd = df[['bedrijfsnaam','trucks','bestelbussen','etrucks','ebestel','etruck_extra', 'jaarkilometrage_truck','jaarkilometrage_bestel']]
    df_tijd['2024_etrucks'] = df_tijd['etrucks'] * df_tijd['jaarkilometrage_truck'] * 1.2
    df_tijd['2030_etrucks'] = (df_tijd['etrucks'] + df_tijd['etruck_extra'] + (0.16*df_tijd['trucks'])) * df_tijd['jaarkilometrage_truck'] * 1.2
    df_tijd['2035_etrucks'] = (df_tijd['etrucks'] + df_tijd['etruck_extra'] + (0.42*df_tijd['trucks'])) * df_tijd['jaarkilometrage_truck'] * 1.2
    df_tijd['2050_etrucks'] = (df_tijd['etrucks'] + df_tijd['etruck_extra'] + (0.75*df_tijd['trucks'])) * df_tijd['jaarkilometrage_truck'] * 1.2
    df_tijd['2024_ebestel'] = df_tijd['ebestel'] * df_tijd['jaarkilometrage_bestel'] * 0.4
    df_tijd['2030_ebestel'] = (df_tijd['ebestel'] + (0.20*df_tijd['bestelbussen'])) * df_tijd['jaarkilometrage_bestel'] * 0.4
    df_tijd['2035_ebestel'] = (df_tijd['ebestel'] + (0.50*df_tijd['bestelbussen'])) * df_tijd['jaarkilometrage_bestel'] * 0.4
    df_tijd['2050_ebestel'] = (df_tijd['ebestel'] + (1*df_tijd['bestelbussen'])) * df_tijd['jaarkilometrage_bestel'] * 0.4
    
    df_tijd_truck = df_tijd[['2024_etrucks','2030_etrucks','2035_etrucks','2050_etrucks']].melt(var_name = 'var',value_name = 'energie')
    df_tijd_bestel = df_tijd[['2024_ebestel','2030_ebestel','2035_ebestel','2050_ebestel']].melt(var_name = 'var',value_name = 'energie')
    df_tijd_mobi = pd.concat([df_tijd_truck,df_tijd_bestel], ignore_index = True).groupby('var')['energie'].sum().reset_index()
    
    df_tijd_mobi['jaar'] = df_tijd_mobi['var'].apply(lambda x: x.split('_')[0])
    df_tijd_mobi['bron'] = df_tijd_mobi['var'].apply(lambda x: x.split('_')[1])
    df_tijd_mobi = df_tijd_mobi.drop('var', axis = 1)
	
    df_tijd_pand = df[['bedrijfsnaam','jaarverbruik']].rename(columns = {'bedrijfsnaam' : 'bron', 'jaarverbruik' : 'energie'}).assign(jaar = "[2024,2030,2035,2050]")
    df_tijd_pand['jaar'] = df_tijd_pand['jaar'].apply(lambda x: eval(x))
    df_tijd_pand = df_tijd_pand.explode(column = 'jaar')

    st.write(f"Totaal aantal e-trucks in 2050 = {int(df_tijd['etrucks'].sum() + df_tijd['etruck_extra'].sum() + (0.75*df_tijd['trucks'].sum()))}")
	
    df_tijd_totaal = pd.concat([df_tijd_pand[['energie','jaar','bron']], df_tijd_mobi], ignore_index = True)
	
    # Plot stacked area chart
    fig = px.area(
        df_tijd_totaal, x="jaar", y="energie", color="bron",
        title=f"Stacked Area Chart over time"
    )
    st.plotly_chart(fig, use_container_width=True)

	
    cols2 = st.columns(3)
	
    resolution = cols2[0].radio("Selecteer tijdsresolutie", ["Hourly", "Daily", "Monthly"])
    smart = cols2[1].radio("Selecteer laadstrategie", ["Normaal", "Smart charging"])
    year = cols2[2].radio("Selecteer jaar", [2024, 2030, 2035, 2050])
	
    if smart == "Normaal":
        drop_cols = ['truck_smart','bestel_smart']
    elif smart == "Smart charging":
        drop_cols = ['truck','bestel']
	

    verbruik_uur_mobiliteit = pd.DataFrame({'truck' : profielen['LADEN NORMAAL']* df_values.set_index('Jaar').loc[year]['Aantal e-trucks'] * 1.2 * jaarverbruik['kms/jaar'].loc['Gewicht volle wagen:10 000 tot 20 000 kg'] ,
                                      'truck_smart' : profielen['LADEN SMART']*df_values.set_index('Jaar').loc[year]['Aantal e-trucks'] * 1.2 * jaarverbruik['kms/jaar'].loc['Gewicht volle wagen:10 000 tot 20 000 kg'],
                                      'bestel' : profielen['LADEN NORMAAL']*df_values.set_index('Jaar').loc[year]['Aantal e-bestelwagens'] * 0.4 * jaarverbruik['kms/jaar'].loc['bestelbus'],
                                      'bestel_smart' : profielen['LADEN SMART']*df_values.set_index('Jaar').loc[year]['Aantal e-bestelwagens'] * 0.4 * jaarverbruik['kms/jaar'].loc['bestelbus'],
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
	
	

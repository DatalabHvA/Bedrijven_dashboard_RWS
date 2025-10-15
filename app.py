import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import timedelta

# Page configuration
st.set_page_config(page_title="Two-Page Dashboard", layout="wide")

# Navigation menu
st.sidebar.title("Navigatie")
page = st.sidebar.radio("Ga naar", ["Pagina 1: Info & Tabellen", "Pagina 2: Interactieve Grafiek"])

#terrein_keuze = st.sidebar.radio("Selecteer terrein", ["Sloterdijk Poort Noord", "Dutch Fresh Port"])

verbruik_etruck = 1.26
verbruik_ebakwagen = 0.9
verbruik_ebestel = 0.4

#if terrein_keuze == "Sloterdijk Poort Noord":
#    df = pd.read_excel('data_template Sloterdijk Poort Noord.xlsx').dropna(subset = 'bedrijfsnaam')
#elif terrein_keuze == "Dutch Fresh Port":
#    df = pd.read_excel('data_template DFP V2.xlsx').dropna(subset = 'bedrijfsnaam')
df = pd.read_excel('data_template_Sloterdijk_Poort_Noord_v2.xlsx').dropna(subset = 'bedrijfsnaam')

df['etrucks_2025'] = df['etrucks']
df['etrucks_2030'] = (df['etrucks'] + df['etrucks_uitbreiding_2030'] + (0.16*df['fossiel trucks']))
df['etrucks_2035'] = (df['etrucks'] + df['etrucks_uitbreiding_2030'] + df['etrucks_uitbreiding_2035']+ (0.42*df['fossiel trucks']))
df['etrucks_2050'] = (df['etrucks'] + df['etrucks_uitbreiding_2030'] + df['etrucks_uitbreiding_2035']+ df['etrucks_uitbreiding_2040']+ (0.75*df['fossiel trucks']))
df['ebakwagens_2025'] = df['ebakwagens']
df['ebakwagens_2030'] = (df['ebakwagens'] + df['ebakwagens_uitbreiding_2030'] + (0.16*df['fossiel bakwagens']))
df['ebakwagens_2035'] = (df['ebakwagens'] + df['ebakwagens_uitbreiding_2030'] + df['ebakwagens_uitbreiding_2035']+ (0.42*df['fossiel bakwagens']))
df['ebakwagens_2050'] = (df['ebakwagens'] + df['ebakwagens_uitbreiding_2030'] + df['ebakwagens_uitbreiding_2035']+ df['ebakwagens_uitbreiding_2040']+ (0.75*df['fossiel bakwagens']))
df['ebestel_2025'] = df['ebestel']
df['ebestel_2030'] = (df['ebestel'] + df['ebestelbussen_uitbreiding_2030'] + (0.20*df['fossiel bestelbussen']))
df['ebestel_2035'] = (df['ebestel'] + df['ebestelbussen_uitbreiding_2030'] + df['ebestelbussen_uitbreiding_2035']+ (0.50*df['fossiel bestelbussen']))
df['ebestel_2050'] = (df['ebestel'] + df['ebestelbussen_uitbreiding_2030'] + df['ebestelbussen_uitbreiding_2035']+ df['ebestelbussen_uitbreiding_2040']+ (1*df['fossiel bestelbussen']))

df['etrucks_2025_verbruik'] = df['etrucks'] * df['jaarkilometrage_truck'] * verbruik_etruck
df['etrucks_2030_verbruik'] = df['etrucks_2030'] * df['jaarkilometrage_truck'] * verbruik_etruck
df['etrucks_2035_verbruik'] = df['etrucks_2035'] * df['jaarkilometrage_truck'] * verbruik_etruck
df['etrucks_2050_verbruik'] = df['etrucks_2050'] * df['jaarkilometrage_truck'] * verbruik_etruck
df['ebakwagens_2025_verbruik'] = df['ebakwagens'] * df['jaarkilometrage_bakwagen'] * verbruik_ebakwagen
df['ebakwagens_2030_verbruik'] = df['ebakwagens_2030'] * df['jaarkilometrage_bakwagen'] * verbruik_ebakwagen
df['ebakwagens_2035_verbruik'] = df['ebakwagens_2035'] * df['jaarkilometrage_bakwagen'] * verbruik_ebakwagen
df['ebakwagens_2050_verbruik'] = df['ebakwagens_2050'] * df['jaarkilometrage_bakwagen'] * verbruik_ebakwagen  
df['ebestel_2025_verbruik'] = df['ebestel'] * df['jaarkilometrage_bestel'] * verbruik_ebestel
df['ebestel_2030_verbruik'] = df['ebestel_2030'] * df['jaarkilometrage_bestel'] * verbruik_ebestel
df['ebestel_2035_verbruik'] = df['ebestel_2035'] * df['jaarkilometrage_bestel'] * verbruik_ebestel
df['ebestel_2050_verbruik'] = df['ebestel_2050'] * df['jaarkilometrage_bestel'] * verbruik_ebestel

profielen = pd.read_excel('profielen_RWS_v2.xlsx')
profielen['datetime'] = pd.to_datetime(profielen['datetime'])
profielen.set_index('datetime', inplace = True)


jaarverbruik = pd.read_csv('table__84651NED.csv').loc[lambda d: d.Perioden == '2020*'][["Vrachtauto's en trekkers gewicht", 'Gemiddeld jaarkilometrage Totaal gemiddeld jaarkilometrage (aantal\xa0km)']]
jaarverbruik.columns = ['type','kms/jaar']
jaarverbruik['kms/jaar'] = jaarverbruik['kms/jaar'].astype(str).str.replace('.','').astype(int)
jaarverbruik = pd.concat([jaarverbruik, pd.DataFrame({'type' : 'bestelbus','kms/jaar' : 18000}, index = [0])], ignore_index = True)
jaarverbruik.set_index('type', inplace = True)

verbruik_cat1 = df.groupby('categorie1')['jaarverbruik pand'].sum()


# Page 1: Text, Images, and Tables
if page == "Page 1: Info & Tables":
    st.title("Welkom op het dashboard van Sloterijk Poort Noord")
    
	#kolommen maken voor pagina
    cols = st.columns(4)

	#afbeeldingen en getallen voertuigen toevoegen
    icon_bestelwagen = "https://raw.githubusercontent.com/isamuu/dashboard/main/Icons%20dashboard/db%20bestelwagen.jpg"
    aantal_bestelwagen = int(df["fossiel bestelbussen"].sum() + df["ebestel"].sum())
    icon_bestelwagen_html = f'''<img src="{icon_bestelwagen}" width="150" style="display: block; margin: auto;">
    <p style="text-align: center; font-size: 24px;">{aantal_bestelwagen} Bestelwagens</p>'''

    icon_bakwagen = "https://raw.githubusercontent.com/isamuu/dashboard/main/Icons%20dashboard/db%20bakwagen.jpg"
    aantal_bakwagens = int(df["fossiel bakwagens"].sum() + df["ebakwagens"].sum())
    icon_bakwagen_html = f'''<img src="{icon_bakwagen}" width="150" style="display: block; margin: auto;">
    <p style="text-align: center; font-size: 24px;">{aantal_bakwagens} Bakwagens</p>'''

    icon_truck = "https://raw.githubusercontent.com/isamuu/dashboard/main/Icons%20dashboard/db%20truck.jpg"
    aantal_truck = int(df["fossiel trucks"].sum() + df["etrucks"].sum())
    icon_truck_html = f'''<img src="{icon_truck}" width="150" style="display: block; margin: auto;">
    <p style="text-align: center; font-size: 24px;">{aantal_truck} Trucks</p>'''
    
    icon_bedrijf = "https://raw.githubusercontent.com/isamuu/dashboard/main/Icons%20dashboard/db%20bedrijf.jpg"
    aantal_bedrijf = len(df['bedrijfsnaam'].unique())
    icon_bedrijf_html = f'''<img src="{icon_bedrijf}" width="150" style="display: block; margin: auto;">
    <p style="text-align: center; font-size: 24px;">{aantal_bedrijf} Bedrijven</p>'''
 
 # Display content in the first column
    cols[0].markdown(icon_bedrijf_html, unsafe_allow_html=True)
    cols[1].markdown(icon_truck_html, unsafe_allow_html=True)
    cols[2].markdown(icon_bakwagen_html, unsafe_allow_html=True)
    cols[3].markdown(icon_bestelwagen_html, unsafe_allow_html=True)

    st.header('Dataset')
    st.write("Hieronder staat de dataset achter het dashboard. Deze is verzameld door studenten logistiek en waar nodig aangevuld met sectorspecifieke getallen van het CBS.")

    st.write((df[['bedrijfsnaam','categorie1','categorie2','fossiel trucks', 'fossiel bakwagens','fossiel bestelbussen','etrucks','ebakwagens','ebestel','jaarverbruik pand']].
              rename(columns = {'categorie1' : 'hoofdcategorie', 'categorie2' : 'subcategorie','jaarverbruik pand' : 'jaarverbruik pand (kWh)'}).
              assign(**{'jaarverbruik pand (kWh)' : lambda d: d['jaarverbruik pand (kWh)'].astype(int)})))
	
    st.header('Hierbij zijn de volgende aannames gedaan:')
    st.write('Voor onbekende jaarkilometrages zijn de CBS gemiddelden uit 2020 ingevuld (https://opendata.cbs.nl/#/CBS/nl/dataset/84651NED/table en https://www.cbs.nl/nl-nl/visualisaties/verkeer-en-vervoer/verkeer/verkeersprestaties-bestelautos).')
    st.write(f'Voor het verbruik van de verschillende transportvormen zijn de volgende waardes gebruikt: {verbruik_ebestel}kWu/km voor bestelbussen, {verbruik_ebakwagen}kWu/km voor bakwagens en {verbruik_etruck}kWu/km voor trucks.')
    st.write('In het geval van onbekend jaarverbuik van de panden is een sector gemiddelde per m2 (https://www.cbs.nl/nl-nl/cijfers/detail/83374NED) ingevuld keer het pandoppervlak zoals bekend in de BAG. Wanneer verschillende bedrijven een pand delen is de bijdrage gelijk verdeeld over de deelnemende partijen.')
    st.write('Het totale jaarverbruik voor de panden is vertaald naar een vermogen op ieder uur van de dag door middel van gemiddelde verbruiksprofielen van Liander (https://www.liander.nl/over-ons/open-data - Verbruiksprofielen grootverbruikaansluitingen elektriciteit). Voor de bijdrage van elektrisch transport zijn profielen gebruikt aangeleverd door de bedrijven, waarbij missende waardes zijn ingevuld met de gemiddelde dagprofielen vanuit het ZEC laadmodel (https://laadmodel-zec.streamlit.app/).') 
    st.write('De gebruikte profielen zijn in onderstaande figuur gevisualiseerd.')
    
    # Time slider
    min_time = profielen.index.min().date()
    max_time = profielen.index.max().date()
    time_range = st.slider(
        "Select Time Window",
        min_value=min_time,
        max_value=max_time,
        value=(pd.to_datetime('2023-01-01').date(),pd.to_datetime('2023-01-14').date()),
        format="YYYY-MM-DD",
    )

    # Column selector
    available_categories = profielen.columns[1:]
    selected_category = st.selectbox(
        "Select Categories to Display",
        options=available_categories    )
    
    fig_profielen = px.line(
        profielen.loc[time_range[0]:time_range[1]].reset_index(), x="datetime", y=selected_category)
    st.plotly_chart(fig_profielen, use_container_width=True)
	




# Page 2: Interactive Stacked Area Graph
elif page == "Page 2: Interactive Graph":
    st.title("Inzicht in de bronnen en piekmomenten van de elektriciteitsvraag")
	
    df_values = pd.DataFrame({'Jaar' : [2025,2030,2035,2050],
        'Aantal fossiele trucks' : [df['fossiel trucks'].sum(), 
                                    int(df['fossiel trucks'].sum() - int(0.16*df['fossiel trucks'].sum())), 
                                    int(df['fossiel trucks'].sum() - int(0.42*df['fossiel trucks'].sum())), 
                                    int(df['fossiel trucks'].sum() - int(0.75*df['fossiel trucks'].sum()))],
        'Aantal fossiele bakwagens' : [df['fossiel bakwagens'].sum(),
                                       int(df['fossiel bakwagens'].sum() - int(0.16*df['fossiel bakwagens'].sum())),
                                       int(df['fossiel bakwagens'].sum() - int(0.42*df['fossiel bakwagens'].sum())),
                                       int(df['fossiel bakwagens'].sum() - (0.75*df['fossiel bakwagens'].sum()))],
        'Aantal fossiele bestelwagens' : [df['fossiel bestelbussen'].sum(),
                                          int(df['fossiel bestelbussen'].sum() - int(0.20*df['fossiel bestelbussen'].sum())),
                                          int(df['fossiel bestelbussen'].sum() - int(0.50*df['fossiel bestelbussen'].sum())),
                                          int(df['fossiel bestelbussen'].sum() - (1.0*df['fossiel bestelbussen'].sum()))],
        'Aantal e-trucks' : [df['etrucks'].sum(), 
                             int(df['etrucks_2030'].sum()), 
                             int(df['etrucks_2035'].sum()), 
                             int(df['etrucks_2050'].sum())],
        'Aantal e-bakwagens' : [df['ebakwagens'].sum(), 
                                int(df['ebakwagens_2030'].sum()), 
                                int(df['ebakwagens_2035'].sum()), 
                                int(df['ebakwagens_2050'].sum())], 
        'Aantal e-bestelbussen' : [df['ebestel'].sum(), 
                                  int(df['ebestel_2030'].sum()), 
                                  int(df['ebestel_2035'].sum()), 
                                  int(df['ebestel_2050'].sum())]})

    st.write('Totale aantallen voertuigen')
    df_values = st.data_editor(df_values)
	
    st.write("## De ontwikkeling van de energievraag over de tijd")
	
    df_tijd_truck = df[['etrucks_2025_verbruik','etrucks_2030_verbruik','etrucks_2035_verbruik','etrucks_2050_verbruik']].melt(var_name = 'var',value_name = 'energie')
    df_tijd_bakwagen = df[['ebakwagens_2025_verbruik','ebakwagens_2030_verbruik','ebakwagens_2035_verbruik','ebakwagens_2050_verbruik']].melt(var_name = 'var',value_name = 'energie')
    df_tijd_bestel = df[['ebestel_2025_verbruik','ebestel_2030_verbruik','ebestel_2035_verbruik','ebestel_2050_verbruik']].melt(var_name = 'var',value_name = 'energie')
    df_tijd_mobi = pd.concat([df_tijd_truck,df_tijd_bakwagen,df_tijd_bestel], ignore_index = True).groupby('var')['energie'].sum().reset_index()
    
    df_tijd_mobi['bron'] = (df_tijd_mobi['var'].apply(lambda x: x.split('_')[0]))
    df_tijd_mobi['jaar'] = df_tijd_mobi['var'].apply(lambda x: x.split('_')[1]).astype(int)
    df_tijd_mobi = df_tijd_mobi.drop('var', axis = 1)
	
    df_tijd_pand = df[['bedrijfsnaam','jaarverbruik pand']].rename(columns = {'bedrijfsnaam' : 'bron', 'jaarverbruik pand' : 'energie'}).assign(jaar = "[2025,2030,2035,2050]")
    df_tijd_pand['jaar'] = df_tijd_pand['jaar'].apply(lambda x: eval(x))
    df_tijd_pand = df_tijd_pand.explode(column = 'jaar')

    #st.write(f"Totaal aantal e-trucks in 2050 = {int(df_tijd['etrucks'].sum() + df_tijd['etruck_extra'].sum() + (0.75*df_tijd['trucks'].sum()))}")
	
    df_tijd_totaal = pd.concat([df_tijd_pand[['energie','jaar','bron']], df_tijd_mobi], ignore_index = True)

    cols2 = st.columns(3)
	
    resolution = cols2[0].radio("Selecteer tijdsresolutie", ["Hourly", "Daily", "Monthly","Yearly"])
    smart = cols2[1].radio("Selecteer laadstrategie", ["Normaal", "Smart charging"])
    year = cols2[2].radio("Selecteer jaar", [2025, 2030, 2035, 2050])
	
    if smart == "Normaal":
        drop_cols = ['trucks_smart','bakwagens_smart','bestel_smart']
    elif smart == "Smart charging":
        drop_cols = ['trucks','bakwagens','bestel']

    laden_profielen = df.groupby('laadprofiel')[['etrucks_2025_verbruik','etrucks_2030_verbruik','etrucks_2035_verbruik','etrucks_2050_verbruik','ebakwagens_2025_verbruik','ebakwagens_2030_verbruik','ebakwagens_2035_verbruik','ebakwagens_2050_verbruik','ebestel_2025_verbruik','ebestel_2030_verbruik','ebestel_2035_verbruik','ebestel_2050_verbruik']].sum().reset_index().melt(id_vars='laadprofiel',var_name = 'bron_jaar_verbruik',value_name = 'energie')
    laden_profielen['bron'] = (laden_profielen['bron_jaar_verbruik'].apply(lambda x: x.split('_')[0]))
    laden_profielen['jaar'] = laden_profielen['bron_jaar_verbruik'].apply(lambda x: x.split('_')[1]).astype(int)
    laden_profielen_smart = df.groupby('laadprofiel smart')[['etrucks_2025_verbruik','etrucks_2030_verbruik','etrucks_2035_verbruik','etrucks_2050_verbruik','ebakwagens_2025_verbruik','ebakwagens_2030_verbruik','ebakwagens_2035_verbruik','ebakwagens_2050_verbruik','ebestel_2025_verbruik','ebestel_2030_verbruik','ebestel_2035_verbruik','ebestel_2050_verbruik']].sum().reset_index().rename(columns={'laadprofiel smart' : 'laadprofiel'}).melt(id_vars='laadprofiel',var_name = 'bron_jaar_verbruik',value_name = 'energie')
    laden_profielen_smart['bron'] = (laden_profielen_smart['bron_jaar_verbruik'].apply(lambda x: x.split('_')[0]))
    laden_profielen_smart['jaar'] = laden_profielen_smart['bron_jaar_verbruik'].apply(lambda x: x.split('_')[1]).astype(int)
                          
    def generate_profile(df_profielen, jaar, bron):
        bijdrages = []
        for profiel in df_profielen['laadprofiel'].unique():
            totaal_profiel = float(df_profielen.loc[lambda d: d.laadprofiel == profiel].loc[lambda d: d.jaar == jaar].loc[lambda d: d.bron == bron]['energie'].iloc[0])
            bijdrages.append(pd.DataFrame({profiel : profielen[profiel] * totaal_profiel}))
        return pd.concat(bijdrages, axis = 1).sum(axis = 1)

    verbruik_uur_mobiliteit = pd.DataFrame({'trucks' : generate_profile(laden_profielen, year, 'etrucks'),
                                      'trucks_smart' : generate_profile(laden_profielen_smart, year, 'etrucks'),
                                      'bakwagens' : generate_profile(laden_profielen, year, 'ebakwagens'),
                                      'bakwagens_smart' : generate_profile(laden_profielen_smart, year, 'ebakwagens'),
                                      'bestel' : generate_profile(laden_profielen, year, 'ebestel'),
                                      'bestel_smart' : generate_profile(laden_profielen, year, 'ebestel')},
                                      index = profielen.index)
    # Resolution selection
	
    verbruik_uur_panden = pd.DataFrame({'GOUD pand' : profielen['GOUD_PAND']*verbruik_cat1['GOUD_PAND'],
                                    'INDUSTRIE pand' : profielen['INDUSTRIE']*verbruik_cat1['INDUSTRIE'],
                                    'KANTOOR_ONDERWIJS pand' : profielen['KANTOOR_ONDERWIJS']*verbruik_cat1['KANTOOR/ONDERWIJS'],
                                    'LOGISTIEK pand' : profielen['LOGISTIEK']*verbruik_cat1['LOGISTIEK'],
                                    'OVERIG pand' : profielen['OVERIG']*verbruik_cat1['OVERIG']},
                                    index = profielen.index)
    #verbruik_uur_panden = verbruik_15min_panden.resample('1h').sum()
    verbruik_uur_totaal = pd.concat([verbruik_uur_panden, verbruik_uur_mobiliteit], axis=1)	

    def select_max_row(df_day):
        st.write(df_day)
        i = df_day['row_sum'].idxmax()
        return df_day.iloc[i]
	
    if resolution == "Hourly":
        week_selector = st.select_slider(
            "Select Week",
            options = pd.date_range(pd.to_datetime('2023-01-01'),pd.to_datetime('2023-12-24'),freq = '1d'))

        time_series_data = verbruik_uur_totaal.drop(drop_cols, axis = 1).loc[week_selector:week_selector + timedelta(weeks = 1)].reset_index().melt(id_vars = 'datetime', var_name = 'bron', value_name = 'Vermogen')
        ylabel = 'Vermogen (kW)'
    elif resolution == "Daily":

        month_selector = st.select_slider(
            "Select Month",
            options = pd.date_range(pd.to_datetime('2023-01-01').date(),pd.to_datetime('2023-12-24').date(),freq = '1W'))

        _d = verbruik_uur_totaal.index.floor('1d')
        _idxmax = verbruik_uur_totaal.assign(row_sum = lambda d: d.sum(numeric_only=True, axis=1)).groupby(_d)['row_sum'].idxmax()
        time_series_data = (
         verbruik_uur_totaal.drop(drop_cols, axis = 1).loc[_idxmax, :]
         .set_index(_idxmax.index)
         .loc[month_selector:month_selector + timedelta(weeks = 4)]
         .reset_index()
         ).melt(id_vars = 'datetime', var_name = 'bron', value_name = 'Vermogen')
        ylabel = 'Vermogen (kW)'
        #time_series_data = verbruik_uur_totaal.drop(drop_cols, axis = 1).loc['2023-01'].assign(row_sum = lambda d: d.sum(numeric_only=True, axis=1)).resample('1d').apply(select_max_row).reset_index().melt(id_vars = 'datetime', var_name = 'bron', value_name = 'Vermogen')
    elif resolution == "Monthly":
        _m = pd.DatetimeIndex(pd.Series(verbruik_uur_totaal.index).apply(lambda t: pd.Timestamp(t.year,t.month,1)))
        _idxmax = verbruik_uur_totaal.assign(row_sum = lambda d: d.sum(numeric_only=True, axis=1)).groupby(_m)['row_sum'].idxmax()
        time_series_data = (
         verbruik_uur_totaal.drop(drop_cols, axis = 1).loc[_idxmax, :]
         .set_index(_idxmax.index)
         .reset_index()
         ).melt(id_vars = 'datetime', var_name = 'bron', value_name = 'Vermogen').drop_duplicates()
        ylabel = 'Vermogen (kW)'
        #time_series_data = verbruik_uur_totaal.drop(drop_cols, axis = 1).assign(row_sum = lambda d: d.sum(numeric_only=True, axis=1)).resample('1M').apply(select_max_row).reset_index().melt(id_vars = 'datetime', var_name = 'bron', value_name = 'Vermogen')
    elif resolution == "Yearly":
        time_series_data = df_tijd_totaal.merge(df[['bedrijfsnaam','categorie1']], left_on = 'bron', right_on = 'bedrijfsnaam', how = 'left')
        time_series_data['bron'] = np.where(time_series_data['categorie1'].isna(), time_series_data['bron'], time_series_data['categorie1'])
        time_series_data = time_series_data.groupby(['jaar','bron']).energie.sum().reset_index()
        time_series_data['datetime'] = pd.to_datetime(time_series_data.jaar, format = '%Y')
        time_series_data['Vermogen'] = time_series_data['energie']
        ylabel = 'Energie (kWu)'
        #time_series_data = verbruik_uur_totaal.drop(drop_cols, axis = 1).assign(row_sum = lambda d: d.sum(numeric_only=True, axis=1)).resample('1M').apply(select_max_row).reset_index().melt(id_vars = 'datetime', var_name = 'bron', value_name = 'Vermogen')


    # Plot stacked area chart
    fig = px.area(
        time_series_data, x="datetime", y="Vermogen", color="bron",
        title=f"Energievraag over de tijd ({resolution} Resolution)",
        labels={'Vermogen' : ylabel}
    )
    fig.update_xaxes(
    type="date",
    tickformatstops=[
        dict(dtickrange=[None, 1000*60*60*24], value="%d %b %H:%M"),      # hours
        dict(dtickrange=[1000*60*60*24, 1000*60*60*24*30], value="%d %b"),  # days
        dict(dtickrange=[1000*60*60*24*30, "M12"], value="%b"),      # months
        dict(dtickrange=["M12", None], value="%Y")                   # beyond a year, still just
    ]
	)
    st.plotly_chart(fig, use_container_width=True)
	
    # Plot pie chart - hidden for RWS stakeholder meeting 15-10-2025
    #fig = px.pie(
    #    df_tijd_totaal.loc[lambda d: d.jaar == year],  values="energie", names="bron",
    #    title=f"Verdeling energievraag per bron (kWu)"
    #)
    #fig.update_xaxes(showticklabels=False)
    #st.plotly_chart(fig, use_container_width=True)
	

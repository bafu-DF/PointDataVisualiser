import streamlit as st
import pandas as pd
import ssl
import altair as alt
import numpy as np

# get rid of ssl connection error (certificates)
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

def main():
    # create selection box in sidebar with stations to choose from
    st.sidebar.title('Settings and tools')
    st.sidebar.subheader('Upload file')
    # create main windows layout
    st.title('InSAR Timeseries plotter')

    uploadedFile = st.sidebar.file_uploader("Upload a .csv file", type=".csv")

    source = r'/Users/florian/Downloads/dummyDataset_for_Visualisation.csv'
    if uploadedFile is not None:
        df = pd.read_csv(uploadedFile, sep = ',', na_values=9999)
        # convert date to datetime format
        df['date_abs'] = pd.to_datetime(df['date_abs'])

        # create sidebar
        st.sidebar.subheader('Sidebar')
        #dfCoordinates = pd.DataFrame({'easting': [df['easting_LV03'].iloc[-1]], 'northing': [df['northing_LV03'].iloc[-1]]})

        selectedPoint = st.sidebar.selectbox("Choose point number", np.unique(df['PointNumber']))
        dfPointSelection = df[df['PointNumber'] == selectedPoint]
        dfPointSelection['valuestring'] = str(dfPointSelection['y_obs'].values)
        st.sidebar.subheader('Plot options')
        st.sidebar.markdown('Define plot options such as a specified date range or the point size for all plots in this '
                            'section.')
        start_date = st.sidebar.date_input('Enter start date', min(df['date_abs']) - pd.Timedelta(days=5))
        end_date = st.sidebar.date_input('Enter end date', max(df['date_abs'])+ pd.Timedelta(days=5))
        markerSize = st.sidebar.slider(
            'Set marker size',
            10, 200, (60))

        # create plots
        st.subheader('InSAR Time Series')
        scatter_chart = st.altair_chart(
            alt.Chart(dfPointSelection)
                .mark_circle(size=markerSize, color = 'steelblue')
                .encode(alt.X('date_abs:T', scale=alt.Scale(domain=(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))), title='Time'),
                        alt.Y('y_obs:Q', scale=alt.Scale(zero=False), title='Displacement [mm]'),
                        tooltip=[alt.Tooltip('date_abs', title='Date'), 'valuestring'])
                .configure_axis(
                labelFontSize=12,
                titleFontSize=14
                )
                .properties(
                    width=800,
                    height=400)
                .interactive()
        , use_container_width= True)

    else:
        st.write('Please upload a compatible .csv file.')

    st.sidebar.subheader('Impressum')
    st.sidebar.markdown('This app is **in a developing/prototyping  stage**. For questions and suggestions: '
                        '<a href = "mailto: florian.denzinger@bafu.admin.ch">Contact</a>. ',
                        unsafe_allow_html=True)
    st.sidebar.markdown('Webapp developed by DF, 2021')

    # hide hamburger and footer
    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

if __name__ == "__main__":
    main()


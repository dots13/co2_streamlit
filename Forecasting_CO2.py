import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import gdown
from statsmodels.tsa.arima.model import ARIMAResults
import os
import plotly.graph_objects as go

st.set_page_config(page_title='Predicting CO2 Emissions', page_icon=':earth_africa:', initial_sidebar_state='auto')

# Path to data
script_dir = os.path.dirname(__file__)  # the cwd relative path of the script file
rel_path = "data/WORLD-OWID-Features-Monthly.csv"  # the target file
rel_to_cwd_path = os.path.join(script_dir, rel_path)  # the cwd-relative path of the target file

# Read csv file
df = pd.read_csv(rel_to_cwd_path, index_col='year')
df.drop(['land_use_change_co2'], axis=1, inplace=True)
# select values only after 1920
df = df.loc['1880-01-01':]
df.loc[:'1950-01-01', 'flaring_co2'] = np.nan
df.loc[:'1882-01-01', 'gas_co2'] = 0


@st.cache_resource
def load_pkl(path):
    return ARIMAResults.load(path_to_model)


# https://drive.google.com/drive/folders/1VnXQ4M-5c-7wiZ5krgOSGpp-FXzeeJnY?usp=drive_link
# https://drive.google.com/drive/folders/1ow4duyt0nIOjOcK972U6kLOCf1v1Q-Z-?usp=drive_link
def load_model():
    f_checkpoint = Path(f"models//co2_ARIMA_Model.pkl")
    with st.spinner("Downloading model... this may take awhile! \n Don't stop it!"):
        gdown.download_folder(id='1ow4duyt0nIOjOcK972U6kLOCf1v1Q-Z-', quiet=True, use_cookies=False)


color_palette = {
    'gas_co2': '#85DBF7',
    'flaring_co2': '#FFE760',
    'oil_co2': '#17C07F',
    'cement_co2': '#C7D0D2',
    'co2': '#EB5858',
    'coal_co2': '#6E6E6E',
    'other_industry_co2': '#F54C95',
    'land_use_change_co2': '#549439'
}

features_dic = {
    'Gas': 'gas_co2',
    'Flaring': 'flaring_co2',
    'Oil': 'oil_co2',
    'Cement': 'cement_co2',
    'Co2': 'co2',
    'Coal': 'coal_co2',
    'Other industry': 'other_industry_co2',
}

models_dic = {}
save_dest = Path('models')
save_dest.mkdir(exist_ok=True)

for col in df.columns:
    f_checkpoint = Path(f"models/{col}_ARIMA_Model.pkl")
    if not f_checkpoint.exists():
        load_model()
    else:
        path_to_model = Path(f"models/{col}_ARIMA_Model.pkl")
        modelicka = load_pkl(path_to_model)
        models_dic[col] = modelicka


def main():
    feature_list = ['Gas', 'Flaring', 'Oil', 'Cement', 'Co2', 'Coal', 'Other industry']
    st.title('CO2 Emissions Forecasting App')

    selected_feature_box = st.selectbox(
        "Select your Industry",
        feature_list
    )

    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: start;} </style>',
             unsafe_allow_html=True)

    radio_choose = st.radio("Choose plot option", ("Forecasted Values", "Whole Dataset"))
    # months = st.slider('Select the number of months for prediction:', 1, 120, value=1)

    months = 120
    forecasting_points = pd.date_range(start='2021-01-01', periods=months, freq="1MS")

    fig = go.Figure()
    fig.update_xaxes(showline=True, linewidth=1, linecolor='rgb(96, 103, 117)', gridcolor='rgb(96, 103, 117)')
    fig.update_yaxes(showline=True, linewidth=1, linecolor='rgb(96, 103, 117)', gridcolor='rgb(96, 103, 117)')
    fig.update_layout(paper_bgcolor="#262730", plot_bgcolor="rgb(52, 53, 56)")

    run_button = st.button('Run Forecast')
    predicted_values = False
    if run_button:
        selected_feature = features_dic[selected_feature_box]
        if radio_choose == "Whole Dataset":
            fig.add_trace(go.Scatter(x=df.index,
                                     y=df[selected_feature],
                                     mode='lines',
                                     marker_color=color_palette[selected_feature],
                                     name=selected_feature_box,
                                     )
                          )
            model = models_dic[selected_feature]
            predicted_values = model.forecast(months)
            fig.add_trace(go.Scatter(x=forecasting_points, y=predicted_values,
                                     mode='lines',
                                     marker_color='red',
                                     name='Forecast')
                          )
        else:
            model = models_dic[selected_feature]
            predicted_values = model.forecast(months)
            fig.add_trace(go.Scatter(x=forecasting_points, y=predicted_values,
                                     mode='lines',
                                     marker_color=color_palette[selected_feature],
                                     name=selected_feature,
                                     )
                          )
        # fig.update_yaxes(ticksuffix="$")
        fig.update_layout(title="CO2 Forecasting for 10 years.",
                          yaxis_title='Million tonnes')
        st.plotly_chart(fig, theme=None)

        df_pred = pd.DataFrame(predicted_values).reset_index()
        df_pred.columns = ['date', 'CO2 Million tonnes']
        df_final = pd.DataFrame(df_pred.groupby(df_pred['date'].dt.year)['CO2 Million tonnes'].mean())
        st.dataframe(df_final.T)


if __name__ == '__main__':
    main()
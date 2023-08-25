import streamlit as st
import pandas as pd
import pickle
from pathlib import Path
import gdown
from statsmodels.tsa.arima.model import ARIMAResults
import os
import plotly.graph_objects as go

# Path to data
script_dir = os.path.dirname(__file__)  # the cwd relative path of the script file
rel_path = "data/WORLD-OWID-Features-Monthly.csv"  # the target file
rel_to_cwd_path = os.path.join(script_dir, rel_path)  # the cwd-relative path of the target file

# Read csv file
df = pd.read_csv(rel_to_cwd_path, index_col='year')
#df.drop('country', axis=1, inplace=True)
# select values only after 1920
df = df.loc['1920-01-01':]

models_dic = {}
@st.cache_resource
def load_pkl(path):
    return pickle.load(open(path, "rb"))
def load_model():
    save_dest = Path('models')
    save_dest.mkdir(exist_ok=True)
    f_checkpoint = Path(f"models//co2_ARIMA_Model.pkl")
    if not f_checkpoint.exists():
        with st.spinner("Downloading model... this may take awhile! \n Don't stop it!"):
            gdown.download_folder(id='1VnXQ4M-5c-7wiZ5krgOSGpp-FXzeeJnY', quiet=True, use_cookies=False)
    else:
        for col in df.columns:
            path_to_model = Path(f"models/{col}_ARIMA_Model.pkl")
            modelicka = ARIMAResults.load(path_to_model)
            models_dic[col] = modelicka


color_palette = {
    'gas_co2': '#85DBF7',
    'flaring_co2': '#FFE760',
    'oil_co2': '#17C07F',
    'cement_co2': '#C7D0D2',
    'co2': '#EB5858',
    'coal_co2': '#6E6E6E',
    'other_industry_co2': '#F54C95',
    'land_use_change_co2': '#F54C95'
}

color_palette_forecast = {
    'gas_co2': '#89DFE6',
    'flaring_co2': '#FFE659',
    'oil_co2': '#3EFBB2',
    'cement_co2': '#DFE9EB',
    'co2': '#EF0000',
    'coal_co2': '#927373'
}

def main():
    load_model()
    print(models_dic)
    st.title('CO2 Emissions Forecasting App')
    features = list(df.columns)
    selected_features = st.multiselect(
        'Select your Industry',
        features)

    st.markdown("""
            <style>
                span[data-baseweb="tag"][aria-label="gas_co2, close by backspace"]{
                    background-color: #85DBF7;
                }
                span[data-baseweb="tag"][aria-label="flaring_co2, close by backspace"]{
                    background-color: #FFE760;
                }
                span[data-baseweb="tag"][aria-label="oil_co2, close by backspace"]{
                    background-color: #17C07F;
                }
                span[data-baseweb="tag"][aria-label="cement_co2, close by backspace"]{
                    background-color: #DFE9EB;
                }
                span[data-baseweb="tag"][aria-label="co2, close by backspace"]{
                    background-color: #EF0000;
                }
                span[data-baseweb="tag"][aria-label="coal_co2, close by backspace"]{
                    background-color: #6E6E6E;
                }
            </style>
            """, unsafe_allow_html=True)

    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: start;} </style>',
             unsafe_allow_html=True)

    st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>',
             unsafe_allow_html=True)

    radio_choose = st.radio("Choose plot option", ("Forecasted Values", "Whole Dataset"))


    forecasting_points = pd.date_range(start='2021-01-01', periods=96, freq="1M")

    fig = go.Figure()
    fig.update_xaxes(showline=True, linewidth=1, linecolor='rgb(96, 103, 117)', gridcolor='rgb(96, 103, 117)')
    fig.update_yaxes(showline=True, linewidth=1, linecolor='rgb(96, 103, 117)', gridcolor='rgb(96, 103, 117)')
    fig.update_layout(paper_bgcolor="#262730", plot_bgcolor="rgb(52, 53, 56)")

    run_button = st.button('Run Forecast')
    if run_button:
        for feature in selected_features:
            if radio_choose == "Whole Dataset":
                fig.add_trace(go.Scatter(x=df.index, y=df[feature],
                                         mode='lines',
                                         marker_color=color_palette[feature],
                                         name=feature))
            model = models_dic[feature]
            predicted_values = model.forecast(96)
            fig.add_trace(go.Scatter(x=forecasting_points, y=predicted_values,
                                     mode='lines',
                                     marker_color='red',
                                     name=f"forecast {feature}",
                                     showlegend=False)
                          )

    st.plotly_chart(fig, theme=None)

if __name__ == '__main__':
    main()

import streamlit as st
import pickle
import os

# Path to model
script_dir = os.path.dirname(__file__)  # the cwd relative path of the script file
rel_path_model = "models/cement_co2_ARIMA_Model2.pkl"  # the target file
rel_to_cwd_path_model = os.path.join(script_dir, rel_path_model)

loaded = pickle.load(open(rel_to_cwd_path_model, "rb"))
print(loaded)
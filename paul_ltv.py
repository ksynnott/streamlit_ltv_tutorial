import importlib
import streamlit as st
import pandas as pd
import datetime
import numpy as np
import plotly.express as px
from main import streamlit_LTV_tutorial

CAC = 700.0
client = "Paul O'Donovan"

markdown_vals = """
    <style>
    .main {
    background-color: #2a6d59
    }
    <style>
    """

file = 'data/LTV_PaulOD.csv'

streamlit_LTV_tutorial(file, CAC, markdown_vals, client)
import importlib
import streamlit as st
import pandas as pd
import datetime
import numpy as np
import plotly.express as px
from main import streamlit_LTV_tutorial

CAC = 170.0
client = 'Roy Keane'

markdown_vals = """
    <style>
    .main {
    background-color: #2a6d59
    }
    <style>
    """

file = 'data/LTV_RoyKeane.csv'

streamlit_LTV_tutorial(file, CAC, markdown_vals, client)
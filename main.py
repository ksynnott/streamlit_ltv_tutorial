import imp
import streamlit as st
import pandas as pd
import datetime
import numpy as np
import plotly.express as px

CAC = 170.0

st.markdown(
    """
    <style>
    .main {
    background-color: #fffff0
    }
    <style>
    """,
    unsafe_allow_html=True
)


def streamlit_LTV_tutorial(LTV_file, CAC, markdown_style, client_name):

    st.markdown(
    markdown_style,
    unsafe_allow_html=True
)

    header = st.container()
    dataset = st.container()
    LTV_visualisation = st.container()

    @st.cache
    def get_data(filename):
        LTV_data = pd.read_csv(filename)

        LTV_data['day'] = pd.to_datetime(LTV_data['day'])
        df_firstPurchase = LTV_data.groupby('customer_id').min().reset_index().copy()
        df_firstPurchase.rename(columns={'day':'min_day'}, inplace=True)
        df_firstPurchase.drop(columns=['total_sales', 'sale_kind'], inplace=True)

        LTV_data = LTV_data.merge(df_firstPurchase, on='customer_id', how='left')

        LTV_data['day_diff_days'] = (LTV_data['day'] - LTV_data['min_day'])/np.timedelta64(1, 'D')
        LTV_data['day_diff_weeks'] = (LTV_data['day'] - LTV_data['min_day'])/np.timedelta64(1, 'W')
        LTV_data['day_diff_months'] = (LTV_data['day'] - LTV_data['min_day'])/np.timedelta64(1, 'M')
        LTV_data[['day_diff_days', 'day_diff_weeks', 'day_diff_months']] = LTV_data[['day_diff_days', 'day_diff_weeks', 'day_diff_months']].astype(int)

        LTV_monthly = LTV_data.groupby('day_diff_months').agg({'customer_id' : pd.Series.nunique, 'total_sales' : sum}).reset_index()
        LTV_monthly['total_sales'] =  LTV_monthly['total_sales'].cumsum()
        LTV_monthly['LTV'] = LTV_monthly['total_sales']/LTV_monthly['customer_id'][0]

        return LTV_data, LTV_monthly


    with header:
        st.title('Tracer x eCommerce Data')
        #st.text(f'In this dashboard we look at LTV for {client_name}')


    with dataset:
        #st.header('Tracer x eCommerce Data')
        #st.text('This dataset is from the Shopify x Tracer integration looking at customer orders in Tracer')

        LTV_data, LTV_vis = get_data(LTV_file)
        #st.write(LTV_vis.tail(100))




    with LTV_visualisation:
        st.header('Visualisating LTV')
        st.text('LTV over time. First purchase is at zero months')

        sel_col, disp_col = st.columns(2)

        LTV_month = sel_col.slider('Select the time frame you wish to look at LTV (months)', min_value=int(LTV_vis['day_diff_months'].min()), max_value=int(LTV_vis['day_diff_months'].max()), value=12, step=1)

        LTV_chosen = round(LTV_vis[LTV_vis['day_diff_months'] == LTV_month]['LTV'].values[0],2)

        sel_col.text(f'LTV for a {LTV_month} month period is ${LTV_chosen}')

        
        margin = round(LTV_chosen - CAC,2)
        p_or_l = "profit" if margin > 0 else "loss"

        sel_col.markdown(f'Given that your current combined CAC \${CAC} then over {LTV_month} month you will make ${margin} {p_or_l}')

        LTV_line = LTV_vis.set_index('day_diff_months')['LTV'].copy()

        fig = px.line(LTV_line)

        fig.update_layout(
            showlegend=False,
            width=400,
            height=300,
            margin=dict(l=1, r=1, b=1, t=1),
            font=dict(color="#383635",size=15),
            paper_bgcolor="#fffff0",)

        fig.update_yaxes(title='Lifetime Value')
        fig.update_xaxes(title='Monthly')

        fig.add_hline(y=LTV_chosen, line_dash="dash", line_color="green")

        disp_col.write(fig)




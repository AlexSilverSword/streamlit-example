from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import os

"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""


with st.echo(code_location='below'):
    st.title('Columbus Systems')

    path2= "CWTP NF streamlit.xlsx"
    @st.cache
    def load_data(path2):
        df=pd.read_excel(path2,index_col="Recd Date",parse_dates=True)
        return df

    df=load_data(path2)

    system = df['Systems'].sort_values(ascending=True).drop_duplicates()
    system_choice = st.sidebar.multiselect('Select your system(s):', system)
    # print(system_choice)


    result1 = df[(df["Systems"].isin(system_choice))]

    # result1 = result1.dropna(axis=1, thresh=int(result1.shape[1]*0.95))
    result1 = result1.dropna(axis=1, how="all")
    result1["Recd Date"] = result1.index

    for i in result1.columns[2:]:
        if i != "Recd Date" and i != "Temperature":
            selection = alt.selection_single(on='mouseover', nearest=True)
            # selection = alt.selection_multi(fields=['Origin'])
            chart = alt.Chart(result1).mark_line(point=True).encode(
            x=alt.X("Recd Date"),
            y=alt.Y(i),
            color=alt.Color("Systems:N"),
            tooltip = ["Recd Date",i]
            ).properties(title=i
            ).add_selection(selection)
            st.altair_chart(chart, use_container_width=True)



        st.altair_chart(alt.Chart(pd.DataFrame(data), height=500, width=500)
            .mark_circle(color='#0068c9', opacity=0.5)
            .encode(x='x:Q', y='y:Q'))

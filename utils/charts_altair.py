import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

def test_altair_chart():st.bar_chart(chart_data)

class ALTAIR:
    def __init__(self, dataframe = None, titulo = "Titulo", height = 400):
        self.dataframe = dataframe
        self.titulo = titulo
        self.height = height
    def bar(self, x = "", y = "", horizontal = False, sort = True, mark_text = True):
        if horizontal == True:
                chart = (alt.Chart(self.dataframe).mark_bar()
                    .encode(x = f"{x}:Q", 
                            y=alt.Y(y).sort('-x') if sort == True else y,
                            text = f"{x}:Q", 
                            tooltip=[y, alt.Tooltip(f'{x}:Q', format=',.2f')],
                    )
                    .properties(
                        title=self.titulo,
                        height=self.height
                    )
                )
                if mark_text:
                    chart = chart + chart.mark_text(align='left', dx=1).encode(text=alt.Text(f'{x}:Q', format=',.0f'))
        else:
                chart = (alt.Chart(self.dataframe).mark_bar()
                    .encode(x = alt.X(x).sort('-y')if sort == True else y, 
                            y= y,
                            text = x, 
                            tooltip=[x, alt.Tooltip(f'{y}:Q', format=',.2f')],
                    )
                    .properties(
                        title=self.titulo,
                        height=self.height
                    )
                )
                if mark_text:
                    chart = chart + chart.mark_text(align='left', dx=1).encode(text=alt.Text(f'{y}:Q', format=',.0f'))
                        
        return st.altair_chart(chart, use_container_width=True,theme="streamlit")
    def pie(self, value = "", color = ""):
        chart =alt.Chart(self.dataframe).mark_arc(innerRadius=50).encode(
                    theta=f"{value}:Q",
                    color=f"{color}:N",
                ).properties(
                    title=self.titulo,
                    height=self.height
                )
        return st.altair_chart(chart, use_container_width=True,theme="streamlit")
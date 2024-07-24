import streamlit as st
import numpy as np
import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objs as go

# Add histogram data
x1 = np.random.randn(200) - 2
x2 = np.random.randn(200)
x3 = np.random.randn(200) + 2

# Group data together
hist_data = [x1, x2, x3]

group_labels = ['Group 1', 'Group 2', 'Group 3']

# Create distplot with custom bin_size
def test_plotly_chart():
    fig = ff.create_distplot(
            hist_data, group_labels, bin_size=[.1, .25, .5])

    # Plot!
    st.plotly_chart(fig, use_container_width=True)
    
def create_stack_np(dataframe = pd.DataFrame(), lista = []):
    return np.stack(tuple(dataframe[elemento] for elemento in lista),axis = -1)
    
def pie_(df = pd.DataFrame(),label_col = '', 
             value_col = '',list_or_color = None, dict_color = None,
             title = '', textinfo = 'percent+label+value' , textposition = 'inside',
             height = 300, showlegend = True, color_list = [], textfont_size = 12, hole = 0,
             
             
    ):
        if dict_color != None:
            marker_colors = [dict_color[i]for i in df[label_col]] if type(dict_color) == dict else list_or_color
        elif color_list != None  and dict_color == None:
            marker_colors = color_list
        elif color_list == None  and dict_color == None:
              marker_colors = None#px.colors.qualitative.Plotly 
        figure = go.Figure()
        figure.add_trace(
            go.Pie(labels=df [label_col],values=df[value_col],
                marker_colors = marker_colors,
                #hovertemplate='<br><b>'+label_col+': %{labels}</b><br><b>'+value_col+': %{value:,.2f}</b>'
                hoverlabel=dict(font_size=15),
                hovertemplate = "<b>%{label}</b> <br><b> %{percent}</b></br><b>%{value:,.0f}</b>",
                name='',
                rotation=10,
                )
        )    
        figure.update_layout(title=title,title_font_size = 18)
        figure.update_traces(textposition = textposition, textinfo = textinfo, hole = hole)
        figure.update_traces(hoverinfo='label+percent+value', textfont_size = textfont_size)
        figure.update_layout(height = height,margin = dict(t=60, b=60, l=60, r=60),showlegend = showlegend)
        figure.update_layout(legend=dict(font=dict(size=10)))
        return figure

def line_traces_(df = None, height = 300 , trace = [],colors = [],ejex = [], hover_unified = True,title=""):
    fig = go.Figure()
    if len(ejex)==1:
        ejexx =df[ejex[0]]
    elif len(ejex)==2: 
        ejexx =[df[ejex[0]],df[ejex[1]]]#
    for value,color in zip(trace,colors):
        
        fig.add_trace(go.Scatter(
            x = ejexx,
            y = df[value],
            name = value,
            marker=dict(color=color),
            mode="markers+lines",
            cliponaxis=False,
            #hovertemplate ='<br><b>%{x}</b><br><b>%{y}</b>',
            hoverlabel=dict(font_size=16)
        ))
        if hover_unified == True:
            fig.update_layout(hovermode="x unified")
        else:
            fig.update_traces(hovertemplate ='<br><b>%{x}</b><br><b>%{y}</b>',hoverlabel=dict(font_size=15))
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    fig.update_layout(
        title = title,
        title_font_size = 22,
        height = height,
        #title_text="STOCK VALORIZADO Y NRO ITEMS POR MES Y AÑO",
    )
    fig.update_xaxes(tickfont=dict(size=12),showticklabels = True,)#,showgrid=True, gridwidth=1, gridcolor='black',
    fig.update_yaxes(tickfont=dict(size=12),showticklabels = True)  
    if len(ejex)==1:
        fig.update_layout(yaxis_tickformat = ',',margin = dict(b=60,r=20,t = 70))
    elif len(ejex)==2: 
        fig.update_layout(yaxis_tickformat = ',',margin = dict(b=100,r=20,t = 70))

    return fig

def figure_stock_var_y2(df = None, height = 450 , moneda = 'Soles', title = ""):
    var_numerica = f'Stock Valorizado {moneda}'
    stock_var_df = df.groupby(['Año', 'Mes','Mes_'])[[var_numerica]].sum().sort_values(['Año','Mes_']).reset_index()
    stock_items_df = df.groupby(['Año', 'Mes','Mes_'])[[var_numerica]].count().sort_values(['Año','Mes_']).reset_index()
    stock_items_df = stock_items_df.rename(columns = {var_numerica:'Nro Items'})
    stock_var_items_df = stock_var_df.merge(stock_items_df,how = 'inner',on=["Año","Mes","Mes_"])
    fig = go.Figure()

    fig.add_trace(go.Bar(
    x = [stock_var_items_df['Año'],stock_var_items_df['Mes']],
    y = stock_var_items_df[var_numerica],
    name = "Stock Valorizado",
    cliponaxis=False,
    #marker=dict(color="rgb(29,105,125)"),
    hovertemplate ='<br>'+'Periodo'+': <b>%{x}</b><br>'+var_numerica+': <b>%{y}</b>',hoverlabel=dict(font_size=15,bgcolor="white")
    ))
    fig.add_trace(
        go.Scatter(
            x=[stock_var_items_df['Año'],stock_var_items_df['Mes']],
            y=stock_var_items_df['Nro Items'],
            yaxis="y2",
            name="Nro Items",
            #marker=dict(color="crimson"),
            cliponaxis=False,
            hovertemplate ='<br>'+'Periodo'+': <b>%{x}</b><br>'+'Nro Items'+': <b>%{y}</b>',hoverlabel=dict(font_size=15)
        )
    )
    fig.update_layout(
        #legend=dict(orientation="v"),
        yaxis=dict(
            title=dict(text="Stock Valorizado"),
            side="left",
            range=[0, stock_var_items_df[var_numerica].max()]
        ),
        yaxis2=dict(
            title=dict(text="Nro Items"),
            side="right",
            range=[0, stock_var_items_df['Nro Items'].max()],
            overlaying="y",
            tickmode="auto",
        ),
        
    )
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    fig.update_layout(
        title = title,
        
        title_font_size = 18,
        
        height = height,
        margin = dict(t = 50, l = 90),
        #title_text="STOCK VALORIZADO Y NRO ITEMS POR MES Y AÑO",
    )
    fig.update_xaxes(tickfont=dict(size=14),showticklabels = True,title_font_size = 13,automargin=True)#,showgrid=True, gridwidth=1, gridcolor='black',
    fig.update_yaxes(tickfont=dict(size=14),showticklabels = True,title_font_size = 13,automargin=True)  
    fig.update_layout(yaxis_tickformat = ',')
    return fig

def figure_bar_relative(df = None, height = 300, eje_color = 'ABC Ventas', title = '',var_numerico = 'Soles'):
    
    stock_abc_dff=df.groupby(['Año', 'Mes','Mes_',eje_color])[[var_numerico]].sum().sort_values(['Año','Mes_']).reset_index()
    lista_letras = sorted(stock_abc_dff[eje_color].unique())
    pivot_stick_adc_dff=stock_abc_dff.pivot_table(index=['Año', 'Mes','Mes_'],values=(var_numerico),columns=(eje_color)).sort_values(['Año','Mes_']).reset_index()
    for letra in lista_letras:
        pivot_stick_adc_dff[f'{letra} %'] = pivot_stick_adc_dff[letra]/(pivot_stick_adc_dff[lista_letras].sum(axis=1))
    #pivot_stick_adc_dff['B %'] = pivot_stick_adc_dff['B']/(pivot_stick_adc_dff[['A','B','C']].sum(axis=1))
    #pivot_stick_adc_dff['C %'] = pivot_stick_adc_dff['C']/(pivot_stick_adc_dff[['A','B','C']].sum(axis=1))
    x_stock_abc = [pivot_stick_adc_dff['Año'],pivot_stick_adc_dff['Mes']]
    fig_e = go.Figure()
    for letra in lista_letras:
        fig_e.add_bar(x = x_stock_abc,
                    y = pivot_stick_adc_dff[f'{letra} %'],
                    name = letra,
                    customdata=create_stack_np(pivot_stick_adc_dff,letra),
                    hovertemplate ='<br>'+'Periodo'+': <b>%{x}</b><br>'+''+' <b>%{y}</b>'+'<br>'+letra+': <b>%{customdata[0]:,.0f}</b><br>',
                                    
                    #hoverlabel=dict(font_size=15,bgcolor="white")
                    )

    fig_e.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    fig_e.update_layout(
        title = title,
        title_font_size = 18,
        margin = dict( l = 50, r = 40, b = 70, t = 40, pad = 5, autoexpand = True),
        height = height,
        
        #title_text="STOCK VALORIZADO Y NRO ITEMS POR MES Y AÑO",
    )
    fig_e.update_layout(barmode="relative")
    fig_e.update_layout(yaxis_tickformat = '.0%')
    return fig_e

def figure_stock_alm_y2(df = None, height = 450 , moneda = 'Importe Dolares', tipo = 'Grupo'):
    tipo_alm_dff = df.groupby([tipo])[['Stock', moneda]].sum().sort_values(moneda,ascending = False).reset_index()
    #tipo_alm_dff = tipo_alm_dff[tipo_alm_dff['Stock']>0]
    fig = go.Figure()

    fig.add_trace(go.Bar(
    x = tipo_alm_dff[tipo],
    y = tipo_alm_dff[moneda],
    name = moneda,
    cliponaxis=False,
    hovertemplate ='<br>'+tipo+': <b>%{x}</b><br>'+moneda+': <b>%{y}</b>',hoverlabel=dict(font_size=15)
    ))
    fig.add_trace(
        go.Scatter(
            x=tipo_alm_dff[tipo],
            y=tipo_alm_dff['Stock'],
            yaxis="y2",
            name='Stock',
            #marker=dict(color="crimson"),
            cliponaxis=False,
            hovertemplate ='<br>'+tipo+': <b>%{x}</b><br>'+'Stock'+': <b>%{y}</b>',hoverlabel=dict(font_size=15)
        )
    )
    fig.update_layout(
        #legend=dict(orientation="v"),
        yaxis=dict(
            title=dict(text=moneda),
            side="left",
            range=[0, tipo_alm_dff[moneda].max()]
        ),
        yaxis2=dict(
            title=dict(text='Stock'),
            side="right",
            range=[0, tipo_alm_dff['Stock'].max()],
            overlaying="y",
            tickmode="auto",
        ),
        
    )
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    
    fig.update_layout(
        title = f"{tipo} por {moneda} y Stock ",
        title_font_size = 18,
        height = height,
        margin = dict( t = 20, b = 20),
    )
    fig.update_xaxes(tickfont=dict(size=11),showticklabels = True,title_font_size = 13,automargin=True)#,showgrid=True, gridwidth=1, gridcolor='black',
    fig.update_yaxes(tickfont=dict(size=12),showticklabels = True,title_font_size = 13,automargin=True)  
    fig.update_layout(yaxis_tickformat = ',')
    fig.update_layout(yaxis2_tickformat = ',')
    size_list = len(tipo_alm_dff[tipo].unique())
    if  size_list== 1:
            fig.update_layout(bargap=0.7)
    elif size_list== 2:
            fig.update_layout(bargap=0.4)
    elif size_list== 3:
            fig.update_layout(bargap=0.3)
    return fig
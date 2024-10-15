


import pandas as pd 
import numpy as np 
import plotly.graph_objects as go
import streamlit as st
import matplotlib.pyplot as plt  
import seaborn as sns 
sns.set_palette(palette='pastel')








def loans_amortisation (amount,payment_periode,interest):
    rate = (df["interest"]/100)/df["payment per years"]
    n = df["payment periode"] * df["payment per years"]
    annuite = df["amount"] * rate / (1 - (1 + rate) ** -n)

    schedule = []
    balance = amount
    cummule = 0

    for i in range(1,n+1):
        interest_1 = rate * balance
        principal = annuite - interest_1
        cummule+= principal
        balance-= principal
        schedule.append([i, annuite, principal, interest_1, balance,cummule])

    df_2 = pd.DataFrame(data=schedule, columns=['Period', 'Payment', 'Principal', 'Interest', 'Balance','Cummule'])

    total_interest = sum([row[3] for row in schedule]) 
    total_annuite = sum([row[1] for row in schedule])

    df_3 = pd.DataFrame({
    "Capital": [amount],
    "Sum of Annuities": [total_annuite],
    "Sum of Interest": [total_interest]
    })
    ratio_in = total_annuite/amount
    ratio_2= total_interest/amount
    ratio_3 = total_interest/total_annuite
    with col2 : 
        st.subheader('Ratios')
        st.text(f"payment/Capital Ratio: {round(ratio_in,3)}")
        st.text(f"Interest/Capital Ratio: {round(ratio_2,3)}")
        st.text(f"Interest/annuite Ratio: {round(ratio_3,3)}")

    return annuite ,df_2,df_3
 



st.set_page_config(page_title="loan amortization",
                   page_icon='🏦',
                   layout='wide')



st.title('loans amortisation calculator 💵')
st.divider()
st.sidebar.title('loans variables')

amount = st.sidebar.text_input(label="amount",key=1)
payment_periode = st.sidebar.number_input(label="numbers of payment (years)",max_value=12,min_value=3,step=1,value=3,key=2)
interest = st.sidebar.number_input(label="interst rate % ",max_value=12,min_value=1,step=1,value=1,key=3)
payment_per_years = st.sidebar.number_input(label='payment per years',max_value=8,min_value=1,value=1,step=1,key=4)
calculate = st.sidebar.button(label="calculate")


col1, col2 = st.columns(2)

if calculate :
    if len(amount) == 0 :
        st.error('please fill in the data', icon="🚨")
    else :
        df= {'amount' :int(amount),
               'payment periode' :payment_periode,
               'interest' : interest,
               'payment per years' : payment_per_years
            }
        
        montly_payment,df_2,df_3 = loans_amortisation(df['amount'],df["payment periode"],df['interest'])
        with st.container(border=True):
            st.subheader('payment schedule')
            st.dataframe(df_2,hide_index=True,use_container_width=True)

        with col2:
            with st.container(border=True):
                st.subheader("loans information")
                st.dataframe(pd.DataFrame([df]),hide_index=True,height=30)
                st.subheader("loans analysis")
                st.dataframe(df_3,hide_index=True)
            
            


        df_T3 = df_3.T.reset_index()    
        df_T3.columns = ['category','value']

        fig_3 = go.Figure()
        fig_3.add_trace(go.Bar(
            x=df_T3.category,
            y=df_T3.value,
            name = 'metrics',
            marker_color ='darkblue',
            

        ))

        fig_3.update_layout(
            title = "loans metrics",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
            
        ) 
        
            

        fig1 = go.Figure()
        fig1.add_trace(go.Bar(
            x=df_2.Period,
            y=df_2.Interest,
            name = 'interest',
            marker_color='blue',
        ))

        fig1.add_trace(go.Bar(
            x=df_2.Period,
            y=df_2.Principal,
            name = 'Principal',
            marker_color='orange'
        ))
        fig1.update_layout(
                title="Interest Payment Over Time",
                xaxis_title="Period",
                yaxis_title="Interest Payment",
                barmode='group',
                xaxis=dict(showgrid=False),  
                yaxis=dict(showgrid=False),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
            
        )



        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_2.Period,
            y=df_2.Principal,
            mode = 'lines',
            name = 'pricipal',
            line=dict(color='orange')))
        fig.add_trace(go.Scatter(
            x=df_2.Period,
            y=df_2.Interest,
            mode = 'lines',
            name = 'interest',
            line=dict(color='blue')))
        
        fig.update_layout(
        title="Principal and Interest Payments Over Time",
        xaxis_title="Period",
        yaxis_title="Amount ($)",
        legend_title="Payment Breakdown",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False),  
        yaxis=dict(showgrid=False)
            
    )
        
        with col1:
            st.container(border=True).plotly_chart(fig)
            st.container(border=True).plotly_chart(fig1)
        with col2 : 
            st.container(border=True).plotly_chart(fig_3)
            
        

            

        


    
        

        

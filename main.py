# Import necessary librariries
import streamlit as st
import pandas as pd
import numpy as np
import hydralit_components as hc
import requests
import inspect
from streamlit_lottie import st_lottie
from numerize import numerize
from itertools import chain
import plotly.graph_objects as go
import plotly.express as px
import joblib
import statsmodels.api as sm
import sklearn
from PIL import Image
import matplotlib.pyplot as plt


# data = pd.read_csv("/data/Data_HA.csv")
data_ha = pd.read_csv("/Users/macpro/Desktop/Roula/HealthCare Analytics/streamlit/data_ha.csv")

# Set Page Icon,Title, and Layout
st.set_page_config(layout="wide",  page_title = "The Impact of Antidepressants")

# Load css style file from local disk
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html=True)
# Load css style from url
def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">',unsafe_allow_html = True)

# Display lottie animations
def load_lottieurl(url):
    # get the url
    r = requests.get(url)
    # if error 200 raised return Nothing
    if r.status_code !=200:
        return None
    return r.json()
# Navigation Bar Design
menu_data = [
{'label':"Home", 'icon': "bi bi-house"},
{'label':"EDA", 'icon': "bi bi-clipboard-data"},
{'label':'Overview', 'icon' : "bi bi-graph-up-arrow"},
{'label':'Analysis', 'icon' : "📋"}]

over_theme = {'txc_inactive': 'white','menu_background':'#87CEFA', 'option_active':'white'}
menu_id = hc.nav_bar(
    menu_definition=menu_data,
    override_theme=over_theme,
    hide_streamlit_markers=True,
    sticky_nav=True,
    sticky_mode='sticky',
)

# Component1: Home
if menu_id == "Home":

    st.markdown("<h2 style='text-align: center; color: #87CEFA;'>The Impact of Antidepressants<i class='bi bi-heart-fill' style='color: #87CEFA;'</h2>", unsafe_allow_html=True)
    
    # Splitting page into 2 columns
    col1, col2 = st.columns([1,2])
    with col1:
        st.image('image.png')

    with col2:
        st.markdown(" ")
        st.markdown("") 
        st.markdown(" ")
        st.markdown("") 
        st.markdown(" ")
        st.markdown("") 
        st.markdown("""
    <article>
    <div class="container">
        <div class="column">
        </div>
        <div class="column">
        <p class="f5 f4-ns lh-copy measure mb4" style="text-align: justify;">
        Depression is a widespread mental health condition characterized by persistent sadness and loss of interest. Antidepressants have transformed the treatment landscape by targeting brain chemicals to alleviate symptoms. These medications aim to restore balance and enhance mood, providing hope for those affected. However, their effectiveness varies, and finding the right medication and dosage may take time.         </p>
        </div>
    </div>
    </article>
    """, unsafe_allow_html=True)


if menu_id == "EDA":

    st.markdown("<h2 style='text-align: center; color:  #87CEFA;'>Data Exploration<i class='bi bi-heart-fill' style='color:  #87CEFA;'</h2>", unsafe_allow_html=True)
    
    # Splitting page into 2 columns
    col1, col2= st.columns([2,2])
    with col1:
        st.markdown(" ")
        st.markdown("""
    <article>
    <div class="container">
        <div class="column">
        </div>
        <div class="column">
        <p class="f5 f4-ns lh-copy measure mb4" style="text-align: justify;">
            It is a good practice to understand the data first and try gather as many insights from it. 
            EDA is all about making sense of data in hand,before getting them dirty with it.
        </p>
        </div>
    </div>
    </article>
    """, unsafe_allow_html=True)
        st.markdown(" ")
    with col2:
        st.markdown(" ")
        st.image('image1.png', width=400, use_column_width=False, clamp=False)
        st.markdown(" ")
# Calculate the count of individuals with cardio values 0 and 1
    gender_counts = data_ha['GENDER'].value_counts().reset_index()
    gender_counts.columns = ['Gender', 'Count']
    # Define gender labels
    gender_labels = {
        1: 'Male',
        2: 'Female'
}  
# Map gender labels to the Gender column
    gender_counts['Gender'] = gender_counts['Gender'].map(gender_labels)   
# Create a pie chart using Plotly
    fig = px.pie(gender_counts, values='Count', names='Gender', title='Gender Distribution')
# Display the pie chart
    st.plotly_chart(fig)        
    # Splitting page into 2 columns
    col1, col2= st.columns([1,1])    
    with col1:
        # Define the age brackets and their corresponding numbers
        conditions = [
            (data_ha['AGE'] >= 0) & (data_ha['AGE'] <= 17),
            (data_ha['AGE'] >= 18) & (data_ha['AGE'] <= 24),
            (data_ha['AGE'] >= 25) & (data_ha['AGE'] <= 29),
            (data_ha['AGE'] >= 30) & (data_ha['AGE'] <= 34),
            (data_ha['AGE'] >= 35) & (data_ha['AGE'] <= 39),
            (data_ha['AGE'] >= 40) & (data_ha['AGE'] <= 44),
            (data_ha['AGE'] >= 45) & (data_ha['AGE'] <= 49),
            (data_ha['AGE'] >= 50) & (data_ha['AGE'] <= 54),
            (data_ha['AGE'] >= 55) & (data_ha['AGE'] <= 59),
            (data_ha['AGE'] >= 60) & (data_ha['AGE'] <= 64),
            (data_ha['AGE'] >= 65) & (data_ha['AGE'] <= 69),
            (data_ha['AGE'] >= 70) & (data_ha['AGE'] <= 74),
            (data_ha['AGE'] >= 75) & (data_ha['AGE'] <= 79),
            (data_ha['AGE'] >= 80)]
        age_bracket_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
# Create a new column 'age_bracket_number' based on the conditions and age bracket numbers
    data_ha['age_bracket_number'] = np.select(conditions, age_bracket_numbers, default=np.nan)

# Count the number of individuals in each age bracket
    age_counts = data_ha['age_bracket_number'].value_counts().sort_index()

# Create a bar chart using Plotly
    fig = go.Figure(data=[go.Bar(x=age_counts.index, y=age_counts.values)])

# Customize the bar chart layout
    fig.update_layout(
        title="Age Distribution",
        xaxis_title="Age Bracket Number",
        yaxis_title="Number of Individuals",
        template="plotly_white"
)

    # Display the bar chart
    st.markdown(" ")
    st.plotly_chart(fig)
    with col2:
        st.markdown(" ")

    # Calculate the count of each class in Class_treatment_M0
    class_counts = data_ha['Class_treatment_M0'].value_counts().reset_index()
    class_counts.columns = ['Class', 'Count']

# Create a horizontal bar chart using Plotly
    fig = go.Figure(go.Bar(
        x=class_counts['Count'],
        y=class_counts['Class'],
        orientation='h',
    ))

# Customize the bar chart layout
    fig.update_layout(
        xaxis_title='Count',
        yaxis_title='Class',
        title='Class Treatment Distribution',
        template="plotly_white"
    )  

    # Display the bar chart
    st.plotly_chart(fig)


if menu_id == "Overview":

    st.markdown("<h2 style='text-align: center; color:  #87CEFA;'>Data Overview<i class='bi bi-heart-fill' style='color:  #87CEFA;'</h2>", unsafe_allow_html=True)
    
    st.markdown(" ")
    time_points = ['M0', 'M3', 'M6']

    # Calculate the median weight values for each time point for gender 1 (male)
    HDRS_mean_male = [data_ha[data_ha['GENDER'] == 1]['HDRS_M0'].mean(),
                        data_ha[data_ha['GENDER'] == 1]['HDRS_M3'].mean(),
                        data_ha[data_ha['GENDER'] == 1]['HDRS_M6_bon'].mean()]

    # Calculate the median weight values for each time point for gender 2 (female)
    HDRS_mean_female = [data_ha[data_ha['GENDER'] == 2]['HDRS_M0'].mean(),
                        data_ha[data_ha['GENDER'] == 2]['HDRS_M3'].mean(),
                        data_ha[data_ha['GENDER'] == 2]['HDRS_M6_bon'].mean()]

    # Create a line chart for weight changes for each gender using Plotly
    fig = go.Figure()

    # Add a line for male weight changes
    fig.add_trace(go.Scatter(x=time_points, y=HDRS_mean_male, mode='lines+markers', name='Male'))

    # Add a line for female weight changes
    fig.add_trace(go.Scatter(x=time_points, y=HDRS_mean_female, mode='lines+markers', name='Female'))

    # Customize the line chart layout
    fig.update_layout(
        xaxis_title='Time',
        yaxis_title='HDRS',
        title='HDRS Median Changes Over Time',
        template="plotly_white"
    )

    # Display the line chart
    st.plotly_chart(fig)


    st.markdown(" ")

    # Calculate the count of each gender and smoking status combination
    group_counts = data_ha.groupby(['GENDER', 'drugfree_ka']).size().reset_index(name='Count')

    # Map gender values to corresponding labels
    group_counts['Gender'] = group_counts['GENDER'].map({1: 'Male', 2: 'Female'})

    # Create a grouped bar chart
    fig = go.Figure(data=[
        go.Bar(name='Drug Free', x=group_counts[group_counts['drugfree_ka'] == 0]['Gender'], y=group_counts[group_counts['drugfree_ka'] == 0]['Count']),
        go.Bar(name='On Drugs', x=group_counts[group_counts['drugfree_ka'] == 1]['Gender'], y=group_counts[group_counts['drugfree_ka'] == 1]['Count'])
    ])

    # Customize the bar chart layout
    fig.update_layout(
        xaxis_title='Gender',
        yaxis_title='Count',
        title='Gender and Drug Free Status Distribution',
        template="plotly_white",
        barmode='group'
    )

    # Display the grouped bar chart
    st.plotly_chart(fig)
    st.markdown(" ")

    # Define the time points
    time_points = ['M0', 'M3', 'M6']

    # Define the variables to plot
    variables = ['WC', 'SBP', 'DBP', 'TRIGLY', 'HDL', 'LDL', 'GLYC']

    # Create empty lists to store the values for each variable at each time point
    values_m0 = []
    values_m3 = []
    values_m6 = []

    # Iterate over the variables and retrieve the values for each time point
    for variable in variables:
        values_m0.append(data_ha[f'{variable}_M0'].mean())
        values_m3.append(data_ha[f'{variable}_M3'].mean())
        values_m6.append(data_ha[f'{variable}_M6'].mean())

    # Create the grouped bar chart
    fig = go.Figure(data=[
        go.Bar(name='M0', x=variables, y=values_m0),
        go.Bar(name='M3', x=variables, y=values_m3),
        go.Bar(name='M6', x=variables, y=values_m6)
    ])

    # Customize the bar chart layout
    fig.update_layout(
        barmode='group',
        xaxis_title='Variables',
        yaxis_title='Value',
        title='Trend of Variables Over Time',
        template='plotly_white'
    )

    # Display the grouped bar chart
    st.plotly_chart(fig)

if menu_id == "Analysis":

    st.markdown("<h2 style='text-align: center; color:  #87CEFA;'>Analysis<i class='bi bi-heart-fill' style='color:  #87CEFA;'</h2>", unsafe_allow_html=True)
   
    # Create a list of time points
    time_points = ['M0', 'M3', 'M6']

    # Filter the data for gender 1 (male) and METS status 0 (not developed METS)
    male_not_mets = data_ha[(data_ha['GENDER'] == 1) & (data_ha['mets_M0'] == 0)]['id'].count()
    # Filter the data for gender 1 (male) and METS status 1 (developed METS)
    male_mets = data_ha[(data_ha['GENDER'] == 1) & (data_ha['mets_M0'] == 1)]['id'].count()

    # Filter the data for gender 2 (female) and METS status 0 (not developed METS)
    female_not_mets = data_ha[(data_ha['GENDER'] == 2) & (data_ha['mets_M0'] == 0)]['id'].count()
    # Filter the data for gender 2 (female) and METS status 1 (developed METS)
    female_mets = data_ha[(data_ha['GENDER'] == 2) & (data_ha['mets_M0'] == 1)]['id'].count()

    # Create stacked bar charts for each combination of gender and METS status
    fig = go.Figure()

    # Add bar chart for male not developed METS
    fig.add_trace(go.Bar(x=time_points, y=[male_not_mets, male_not_mets, male_not_mets], name='Male Not Developed METS', marker_color='blue'))

    # Add bar chart for male developed METS
    fig.add_trace(go.Bar(x=time_points, y=[0, male_mets, male_mets], name='Male Developed METS', marker_color='red'))

    # Add bar chart for female not developed METS
    fig.add_trace(go.Bar(x=time_points, y=[female_not_mets, female_not_mets, female_not_mets], name='Female Not Developed METS', marker_color='green'))

    # Add bar chart for female developed METS
    fig.add_trace(go.Bar(x=time_points, y=[0, female_mets, female_mets], name='Female Developed METS', marker_color='orange'))

    # Customize the bar chart layout
    fig.update_layout(
        xaxis_title='Time',
        yaxis_title='Count',
        title='Development of METS Over Time by Gender',
        barmode='stack',
        template='plotly_white'
    )

    # Display the bar chart
    st.plotly_chart(fig)
    st.markdown(" ")

    # Create a list of time points
    time_points = ['M0', 'M3', 'M6']

    # Filter the data for gender 1 (male) and smoking status 0 (non-smoker)
    male_non_smoker = data_ha[(data_ha['GENDER'] == 1) & (data_ha['FUM_M0'] == 0)].shape[0]
    # Filter the data for gender 1 (male) and smoking status 1 (smoker)
    male_smoker = data_ha[(data_ha['GENDER'] == 1) & (data_ha['FUM_M0'] == 1)].shape[0]

    # Filter the data for gender 2 (female) and smoking status 0 (non-smoker)
    female_non_smoker = data_ha[(data_ha['GENDER'] == 2) & (data_ha['FUM_M0'] == 0)].shape[0]
    # Filter the data for gender 2 (female) and smoking status 1 (smoker)
    female_smoker = data_ha[(data_ha['GENDER'] == 2) & (data_ha['FUM_M0'] == 1)].shape[0]

    # Create stacked bar charts for each combination of gender and smoking status
    fig = go.Figure()

    # Add bar chart for male non-smokers
    fig.add_trace(go.Bar(x=time_points, y=[male_non_smoker, male_non_smoker, male_non_smoker], name='Male Non-Smoker', marker_color='blue'))

    # Add bar chart for male smokers
    fig.add_trace(go.Bar(x=time_points, y=[0, male_smoker, male_smoker], name='Male Smoker', marker_color='red'))

    # Add bar chart for female non-smokers
    fig.add_trace(go.Bar(x=time_points, y=[female_non_smoker, female_non_smoker, female_non_smoker], name='Female Non-Smoker', marker_color='green'))

    # Add bar chart for female smokers
    fig.add_trace(go.Bar(x=time_points, y=[0, female_smoker, female_smoker], name='Female Smoker', marker_color='orange'))

    # Customize the bar chart layout
    fig.update_layout(
        xaxis_title='Time',
        yaxis_title='Count',
        title='Gender and Smoking Status Distribution Over Time',
        barmode='stack',
        template='plotly_white'
    )

    # Display the bar chart
    st.plotly_chart(fig)

    st.markdown(" ")

    time_points = ['M0', 'M3', 'M6']

    # Calculate the median weight values for each time point for gender 1 (male)
    weight_median_male = [data_ha[data_ha['GENDER'] == 1]['POIDS_M0'].median(),
                        data_ha[data_ha['GENDER'] == 1]['POIDS_M3'].median(),
                        data_ha[data_ha['GENDER'] == 1]['POIDS_M6'].median()]

    # Calculate the median weight values for each time point for gender 2 (female)
    weight_median_female = [data_ha[data_ha['GENDER'] == 2]['POIDS_M0'].median(),
                        data_ha[data_ha['GENDER'] == 2]['POIDS_M3'].median(),
                        data_ha[data_ha['GENDER'] == 2]['POIDS_M6'].median()]

    # Create a line chart for weight changes for each gender using Plotly
    fig = go.Figure()

    # Add a line for male weight changes
    fig.add_trace(go.Scatter(x=time_points, y=weight_median_male, mode='lines+markers', name='Male'))

    # Add a line for female weight changes
    fig.add_trace(go.Scatter(x=time_points, y=weight_median_female, mode='lines+markers', name='Female'))

    # Customize the line chart layout
    fig.update_layout(
        xaxis_title='Time',
        yaxis_title='Weight',
        title='Weight Median Changes Over Time',
        template="plotly_white"
    )
   # Display the line chart
    st.plotly_chart(fig)
    st.markdown(" ")


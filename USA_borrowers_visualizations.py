# -*- coding: utf-8 -*-
"""Visualization Final Project.ipynb
"""
####################################### Imports ######################################

import streamlit as st
import pandas as pd
import numpy as np
import re
from datetime import datetime
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from streamlit_echarts import Map
from streamlit_echarts import JsCode
from streamlit_echarts import st_echarts
import plotly.figure_factory as ff

####################################### Intro ######################################

st.set_page_config(page_title="Streamlit Project",
                   page_icon=":bar_chart:",
                  layout="wide")

with st.container():
    col1, col2, col3 = st.columns([0.7, 0.2, 0.1])
    col1.title('LendingClub Loan - Visualization')
with st.container():
    col1, col2, col3 = st.columns([0.30, 0.5, 0.20])
    col1.subheader('Ido Pascaro')
with st.container():
    col1, col2, col3 = st.columns([0.32, 0.5, 0.20])
    col1.subheader('Itay Saig')
    st.write("\n")

st.header("Overview")
st.markdown("##### The subject of our visualization is to examine the change in the characteristics of borrowers in the United States over the years in various aspects.")
st.markdown("##### Our visualization theme focuses on the ‘Lending Club Loan’ dataset from Kaggle which contains data from LendingClub company. The data available on Kaggle is a comprehensive dataset of loan information from LendingClub from 2012 to 2016.")
st.markdown("##### The main question we would like to investigate is: In what and how the characteristics of borrowers in the US change over the years?")
st.markdown("---")


################################# Color Blind Button #################################

color_blind = st.radio("The visualizations are color blind friendly. Are you color blind?",['No','Yes'],key=51) # Did you know that 9% of men are color blind?
graph_1_colors = ["hsl(207, 100%, 98%)", "hsl(207, 95%, 90%)", "hsl(207, 90%, 82%)", "hsl(207, 85%, 74%)", "hsl(207, 80%, 66%)", "hsl(207, 75%, 58%)", "hsl(207, 70%, 50%)", "hsl(207, 65%, 42%)", "hsl(207, 60%, 34%)", "hsl(207, 55%, 26%)", "hsl(207, 50%, 18%)"]  # Shade of blue

if color_blind == 'Yes':
  graph_3_color_1 = "#0072B2"  # Shade of blue
  graph_3_color_2 = "#CD950C"  # Shade of orange
  graph_4_color_1 = 'rgb(0, 120, 200)'  # Blue
  graph_4_color_2 = 'rgb(255, 153, 18)'  # Orange
  graph_5_colors = ['#1f77b4', '#ff7f0e', '#2ca02c']  # Blue, orange, green
  
else:
  graph_3_color_1 = "#BFEFFF"
  graph_3_color_2 = "#B23AEE"  # darkorchid2 (purple)
  graph_4_color_1 = 'rgb(55, 83, 109)'
  graph_4_color_2 = 'rgb(26, 118, 255)'
  graph_5_colors = ['#e6194B', '#3cb44b', '#4363d8']  # Red, green, blue
  st.markdown("---")  

  
################################### Preprocessing ###################################
############################### General Preprocessing ###############################

data = pd.read_csv('lending_club_loan_two.csv') # read csv

# Replace 'RN' with 'Registered Nurse' in 'emp_title' column
data['emp_title'] = data['emp_title'].replace('RN', 'Registered Nurse')

# Replace 'manager' with 'Manager' in 'emp_title' column
data['emp_title'] = data['emp_title'].replace('manager', 'Manager')

# Create 'id' coulmn in the DataFrame
data['id'] = range(1, len(data) + 1)  # Create 'id' column for each borrower to use in aggregation operations

# Create 'issue_year' coulmn in the DataFrame
data['issue_d'] = pd.to_datetime(data['issue_d'], format='%m/%d/%Y')  # Convert 'issue_d' column to datetime format
data['issue_year'] = data['issue_d'].apply(lambda x: datetime.strftime(x, '%Y'))  # Extract the year and create a new column 'issue_year'

# Create states acronyms dict for each state in USA, each key is acronyms and each value is the full state name
states_acro_dict = {'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas', 'KL': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland', 'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri', 'MT': 'Montana',
'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming'}

# Create 'borrower_state' coulmn in the DataFrame
# Extract states acronyms
pattern = r'\b([A-Z]{2})\b'  # Regex pattern to extract states (assuming a two-letter state code)
states = [re.search(pattern, address).group(1) if re.search(pattern, address) else None for address in data['address']]  # Extract states from addresses
data['borrower_state'] = states  # Create a new column with extracted states
data['borrower_state'] = data['borrower_state'].map(states_acro_dict)  # Replaces any acronyms with the full name of the state

# Create 'income_range' coulmn in the DF
incomes_df = pd.DataFrame()
income_ranges = [0, 25000, 50000, 75000, 100000, 150000, float('inf')]  # Define income ranges
# income_labels = ['< $25,000', '$25,000 - $50,000', '$50,000 - $75,000', '$75,000 - $100,000', '$100,000 - $150,000', '> $150,000']
income_labels = ['< $25k', '$25k - $50k', '$50k - $75k', '$75k - $100k', '$100k - $150k', '> $150k']

data['income_range'] = pd.cut(data['annual_inc'], bins=income_ranges, labels=income_labels, right=False)  # Categorize the values into income ranges

# Create separate DataFrames for each year
unique_years = data['issue_year'].unique().tolist()
sorted_unique_years = sorted(unique_years)
year_dataframes = {}
for year in sorted_unique_years:
  year_dataframes[year] = data[data['issue_year'] == year]


#################################### OUR GRAPHS #####################################


###################################### Graph 1 ######################################
################################### Preprocessing ###################################

# Create population dict for each state in USA
states_pop_dict = {'Alabama': 4903185, 'Alaska': 710249, 'Arizona': 7278717, 'Arkansas': 3017804, 'California': 39368078, 'Colorado': 5758736, 'Connecticut': 3565287, 'Delaware': 973764, 'District of Columbia': 712816, 'Florida': 21733312, 'Georgia': 10617423, 'Hawaii': 1415872, 'Idaho': 1787065, 'Illinois': 12671821, 'Indiana': 6732219, 'Iowa': 3155070, 'Kansas': 2913314, 'Kentucky': 4467673, 'Louisiana': 4648794, 'Maine': 1344212, 'Maryland': 6045680, 'Massachusetts': 6892503,
                   'Michigan': 9883635, 'Minnesota': 5639632, 'Mississippi': 2976149, 'Missouri': 6137428, 'Montana': 1068778, 'Nebraska': 1934408, 'Nevada': 3080156, 'New Hampshire': 1359711, 'New Jersey': 8882190, 'New Mexico': 2096829, 'New York': 19336776, 'North Carolina': 10488084, 'North Dakota': 762062, 'Ohio': 11689100, 'Oklahoma': 3980783, 'Oregon': 4217737, 'Pennsylvania': 12801989, 'Puerto Rico': 3285874, 'Rhode Island': 1059361, 'South Carolina': 5148714,
                   'South Dakota': 884659, 'Tennessee': 6829174, 'Texas': 29360759, 'Utah': 3205958, 'Vermont': 623989, 'Virginia': 8535519, 'Washington': 7614893, 'West Virginia': 1792147, 'Wisconsin': 5822434, 'Wyoming': 578759}

# Calculate num of borrowers per state
borrowers_per_state_df = data.groupby(['borrower_state'])['id'].count().reset_index()
borrowers_per_state_df.rename(columns={'id': 'num_of_borrowers'}, inplace=True)  # Change the 'id' column name to 'num_of_borrowers'

# Calculate the ratio between the amount of borrowers in a state and the size of its population
percentage_borrowers_per_state = {}
for state in states_pop_dict:
  try:
    num_of_borrowers = 10000 * (borrowers_per_state_df.loc[borrowers_per_state_df['borrower_state'] == state, 'num_of_borrowers'].item())
    percentage_borrowers_per_state[state] = (num_of_borrowers / states_pop_dict[state]) + 6
  except:
    percentage_borrowers_per_state[state] = 0


################################### Visualization ###################################

def render_usa(graph_1_colors):
    formatter = JsCode(
        "function (params) {"
        + "var value = (params.value + '').split('.');"
        + "value = value[0].replace(/(\d{1,3})(?=(?:\d{3})+(?!\d))/g, '$1,');"
        + "return params.seriesName + '<br/>' + params.name + ': ' + value;}"
    ).js_code

    with open("./USA.json", "r") as f:
        map = Map(
            "USA",
            json.loads(f.read()),
            {
                "Alaska": {"left": -131, "top": 25, "width": 15},
                "Hawaii": {"left": -110, "top": 28, "width": 5},
                "Puerto Rico": {"left": -76, "top": 26, "width": 2},
            },
        )
    options = {
        "title": {
            "text": "Percentage of Borrowers by State: United States Heat Map",
            "left": "center",  # Align the title to the center
            "top": "0%",  # Move the title further up
        },
        "tooltip": {
            "trigger": "item",
            "showDelay": 0,
            "transitionDuration": 0.2,
            "formatter": formatter,
        },
        "visualMap": {
            "left": "right",
            "min": min(list(percentage_borrowers_per_state.values())),
            "max": np.ceil(max(list(percentage_borrowers_per_state.values()))) + 2,
            "inRange": {
                "color": graph_1_colors },
            "text": ["High", "Low"],
            "calculable": True,
        },
        "toolbox": {
            "show": True,
            "left": "left",
            "top": "top",
            "feature": {
                "dataView": {"readOnly": False},
                "restore": {},
                "saveAsImage": {},
            },
        },
        "series": [
            {
                "name": "Percentage of Borrowers by State:",
                "type": "map",
                "roam": True,
                "map": "USA",
                "top": "20%",
                "right": "15%",
                "emphasis": {"label": {"show": True}},
                "textFixed": {"Alaska": [20, -20]},
                "data": [
                    {"name": "Alabama", "value": percentage_borrowers_per_state["Alabama"]},
                    {"name": "Alaska", "value": percentage_borrowers_per_state["Alaska"]},
                    {"name": "Arizona", "value": percentage_borrowers_per_state["Arizona"]},
                    {"name": "Arkansas", "value": percentage_borrowers_per_state["Arkansas"]},
                    {"name": "California", "value": percentage_borrowers_per_state["California"]},
                    {"name": "Colorado", "value": percentage_borrowers_per_state["Colorado"]},
                    {"name": "Connecticut", "value": percentage_borrowers_per_state["Connecticut"]},
                    {"name": "Delaware", "value": percentage_borrowers_per_state["Delaware"]},
                    {"name": "District of Columbia", "value": percentage_borrowers_per_state["District of Columbia"]},
                    {"name": "Florida", "value": percentage_borrowers_per_state["Florida"]},
                    {"name": "Georgia", "value": percentage_borrowers_per_state["Georgia"]},
                    {"name": "Hawaii", "value": percentage_borrowers_per_state["Hawaii"]},
                    {"name": "Idaho", "value": percentage_borrowers_per_state["Idaho"]},
                    {"name": "Illinois", "value": percentage_borrowers_per_state["Illinois"]},
                    {"name": "Indiana", "value": percentage_borrowers_per_state["Indiana"]},
                    {"name": "Iowa", "value": percentage_borrowers_per_state["Iowa"]},
                    {"name": "Kansas", "value": percentage_borrowers_per_state["Kansas"]},
                    {"name": "Kentucky", "value": percentage_borrowers_per_state["Kentucky"]},
                    {"name": "Louisiana", "value": percentage_borrowers_per_state["Louisiana"]},
                    {"name": "Maine", "value": percentage_borrowers_per_state["Maine"]},
                    {"name": "Maryland", "value": percentage_borrowers_per_state["Maryland"]},
                    {"name": "Massachusetts", "value": percentage_borrowers_per_state["Massachusetts"]},
                    {"name": "Michigan", "value": percentage_borrowers_per_state["Michigan"]},
                    {"name": "Minnesota", "value": percentage_borrowers_per_state["Minnesota"]},
                    {"name": "Mississippi", "value": percentage_borrowers_per_state["Mississippi"]},
                    {"name": "Missouri", "value": percentage_borrowers_per_state["Missouri"]},
                    {"name": "Montana", "value": percentage_borrowers_per_state["Montana"]},
                    {"name": "Nebraska", "value": percentage_borrowers_per_state["Nebraska"]},
                    {"name": "Nevada", "value": percentage_borrowers_per_state["Nevada"]},
                    {"name": "New Hampshire", "value": percentage_borrowers_per_state["New Hampshire"]},
                    {"name": "New Jersey", "value": percentage_borrowers_per_state["New Jersey"]},
                    {"name": "New Mexico", "value": percentage_borrowers_per_state["New Mexico"]},
                    {"name": "New York", "value": percentage_borrowers_per_state["New York"]},
                    {"name": "North Carolina", "value": percentage_borrowers_per_state["North Carolina"]},
                    {"name": "North Dakota", "value": percentage_borrowers_per_state["North Dakota"]},
                    {"name": "Ohio", "value": percentage_borrowers_per_state["Ohio"]},
                    {"name": "Oklahoma", "value": percentage_borrowers_per_state["Oklahoma"]},
                    {"name": "Oregon", "value": percentage_borrowers_per_state["Oregon"]},
                    {"name": "Pennsylvania", "value": percentage_borrowers_per_state["Pennsylvania"]},
                    {"name": "Rhode Island", "value": percentage_borrowers_per_state["Rhode Island"]},
                    {"name": "South Carolina", "value": percentage_borrowers_per_state["South Carolina"]},
                    {"name": "South Dakota", "value": percentage_borrowers_per_state["South Dakota"]},
                    {"name": "Tennessee", "value": percentage_borrowers_per_state["Tennessee"]},
                    {"name": "Texas", "value": percentage_borrowers_per_state["Texas"]},
                    {"name": "Utah", "value": percentage_borrowers_per_state["Utah"]},
                    {"name": "Vermont", "value": percentage_borrowers_per_state["Vermont"]},
                    {"name": "Virginia", "value": percentage_borrowers_per_state["Virginia"]},
                    {"name": "Washington", "value": percentage_borrowers_per_state["Washington"]},
                    {"name": "West Virginia", "value": percentage_borrowers_per_state["West Virginia"]},
                    {"name": "Wisconsin", "value": percentage_borrowers_per_state["Wisconsin"]},
                    {"name": "Wyoming", "value": percentage_borrowers_per_state["Wyoming"]},
                    {"name": "Puerto Rico", "value": percentage_borrowers_per_state["Puerto Rico"]},
                ],
            }
        ],
    }
    st_echarts(options, map=map)

render_usa(graph_1_colors)
st.markdown("---")  


###################################### Graph 2 ######################################
################################### Preprocessing ###################################

# Create Selectbox for filtering by years
with st.container():
    col1, col2 = st.columns([0.2, 0.8])
    
    with col1:
        option = st.selectbox(
            "Which year would you like to examine?",
            ('Overall', '2012', '2013', '2014', '2015', '2016')
        )
    
    # Extract the 7 most frequent loan purposes in the data
    top_7_purposes = data['purpose'].value_counts().head(7).index.tolist()
    sorted_top_7_purposes = sorted(top_7_purposes, reverse=True)  # Sorted in descending alphabetical order
    sorted_top_7_purposes = [s.replace('_', ' ').title() for s in sorted_top_7_purposes]  # Corrected list, replacing underscore with a space and putting a capital letter at the beginning of each word
    
    # Create a dictionary of the number of borrowers from each purpose by each year
    borrowers_per_year_purpose_dict = {}
    for year_df in year_dataframes.values():
      year = year_df['issue_year'].iloc[0, ]  # Extract the current year
      year_df = year_df[year_df['purpose'].isin(top_7_purposes)]  # Filter the DataFrame to get only records with purpose of the top 7
      curr_borrowers_per_year_purpose_df = year_df.groupby(['purpose'])['id'].count().reset_index()  # Group the records by purpose for each year
      curr_borrowers_per_year_purpose_df.rename(columns={'id': 'num_of_borrowers'}, inplace=True)  # Change the 'id' column name to 'num_of_borrowers'
      curr_borrowers_per_year_purpose_list = curr_borrowers_per_year_purpose_df['num_of_borrowers'].tolist()[::-1]
      borrowers_per_year_purpose_dict[year] = curr_borrowers_per_year_purpose_list
      
    
if option == 'Overall':
    with col2:
      options = {
          "title": {
              "text": "Loan Distribution by Purpose: The most Requested Loan Purposes",
              "left": "center",
              "top": "-3%",
              "padding": 20,
              "textStyle": {"fontWeight": "bold"}
          },
          "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"},
          },
          "legend": {
              "top": "7%",
              "data": sorted_unique_years
          },
          "grid": {"left": "3%", "right": "4%", "bottom": "10%", "top": "20%", "containLabel": True},
          "xAxis": {
                "type": "value",
                "axisLabel": {
                "show": True,
                "formatter": "{value}",
                "textStyle": {
                "fontSize": 12
                    }
              },
                "name": "Number of Borrowers",
                "nameLocation": "middle",
                "nameGap": 30
              },
          "yAxis": {
              "type": "category",
              "data": sorted_top_7_purposes,
              "name": "Loan Purpose"
          },
          "series": [
              {
                  "name": "2012",
                  "type": "bar",
                  "stack": "total",
                  "label": {"show": False},
                  "emphasis": {"focus": "series"},
                  "data": borrowers_per_year_purpose_dict["2012"],
              },
              {
                  "name": "2013",
                  "type": "bar",
                  "stack": "total",
                  "label": {"show": False},
                  "emphasis": {"focus": "series"},
                  "data": borrowers_per_year_purpose_dict["2013"],
              },
              {
                  "name": "2014",
                  "type": "bar",
                  "stack": "total",
                  "label": {"show": False},
                  "emphasis": {"focus": "series"},
                  "data": borrowers_per_year_purpose_dict["2014"],
              },
              {
                  "name": "2015",
                  "type": "bar",
                  "stack": "total",
                  "label": {"show": False},
                  "emphasis": {"focus": "series"},
                  "data": borrowers_per_year_purpose_dict["2015"],
              },
              {
                  "name": "2016",
                  "type": "bar",
                  "stack": "total",
                  "label": {"show": False},
                  "emphasis": {"focus": "series"},
                  "data": borrowers_per_year_purpose_dict["2016"],
              },
          ],
      }
      st_echarts(options=options, height="500px")


else:
    # Calculate num of borrowers per each year and loan purpose
    user_purpose_choice_df = year_dataframes[option]  # The DataFrame with records of the year selected by the user
    user_purpose_choice_df = user_purpose_choice_df[user_purpose_choice_df['purpose'].isin(top_7_purposes)]  # Filter the DataFrame to get only records with purpose of the top 7
    grade_per_year_dict = {}
    borrowers_per_year_purpose_df = user_purpose_choice_df.groupby(['purpose'])['id'].count().reset_index()  # Group the records by purpose for each year
    borrowers_per_year_purpose_df.rename(columns={'id': 'num_of_borrowers'}, inplace=True)  # Change the 'id' column name to 'num_of_borrowers'
    borrowers_per_year_purpose_df = borrowers_per_year_purpose_df.sort_values('purpose', ascending=False)  # Sort the DataFrame by the 'purpose' column in descending alphabetical order
    borrowers_per_year_purpose_list = borrowers_per_year_purpose_df['num_of_borrowers'].tolist()  # Create a list of 'num_of_borrowers' values in descending alphabetical order of 'purpose'

        
################################### Visualization ###################################

    with col2:
        def render_horizontal_bar_by_purpose(sorted_top_7_purposes, borrowers_per_year_purpose_list):
          options = {
              "title": {
                  "text": "Loan Distribution by Purpose: The most Requested Loan Purposes",
                  "left": "center",
                  "top": "-3%",
                  "padding": 20,
                  "textStyle": {"fontWeight": "bold"}
                },
              "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
              "grid": {"left": "3%", "right": "4%", "bottom": "10%", "top": "20%", "containLabel": True},
              "xAxis": {
                  "type": "value",
                  "axisLabel": {
                  "show": True,
                  "formatter": "{value}",
                  "textStyle": {
                  "fontSize": 12
                    }
                },
                "name": "Number of Borrowers",
                "nameLocation": "middle",
                "nameGap": 30
              },
              "yAxis": {
                  "type": "category",
                  "data": sorted_top_7_purposes,
                  "name": "Loan Purpose"
              },
              "series": [
                  {
                      "name": "Number of Borrowers",
                      "type": "bar",
                      "stack": "total",
                      "label": {"show": True},
                      "emphasis": {"focus": "series"},
                      "data": borrowers_per_year_purpose_list,
                  },
              ],
          }
          st_echarts(options=options, height="500px")
            
        render_horizontal_bar_by_purpose(sorted_top_7_purposes, borrowers_per_year_purpose_list)
st.markdown("---")  


###################################### Graph 3 ######################################
################################### Preprocessing ###################################

loan_status_values = ["Fully Paid", "Charged Off"]

# Create Selectbox for filtering by years
with st.container():
    col1, col2 = st.columns([0.2, 0.8])
    
    with col1:
        option = st.selectbox(
            "Which year are you interested in?",
            ('2012', '2013', '2014', '2015', '2016')
        )

    # Create separate DataFrame for each loan status
    user_choice_df = year_dataframes[option]  # The DataFrame with records of the year selected by the user
    fully_paid_df = user_choice_df[user_choice_df['loan_status'] == 'Fully Paid']
    charged_off_df = user_choice_df[user_choice_df['loan_status'] == 'Charged Off']

    # Calculate num of borrowers per each year and loan status
    loan_status_dict = {}
    i = 0
    for df in [fully_paid_df, charged_off_df]:
      borrowers_per_income_range_df = df.groupby(['income_range'])['id'].count().reset_index()  # Group the records with the selected year to income ranges
      borrowers_per_income_range_df.rename(columns={'id': 'num_of_borrowers'}, inplace=True)  # Change the 'id' column name to 'num_of_borrowers'
      if i == 0:
        loan_status_dict['fully_paid'] = borrowers_per_income_range_df['num_of_borrowers'].tolist()
        i += 1
      else:
        loan_status_dict['charged_off'] = borrowers_per_income_range_df['num_of_borrowers'].tolist()

        
################################### Visualization ###################################

    with col2:
        def render_stacked_vertical_bar(fully_paid_list, charged_off_list):
            options = {
                "title": {
                    "text": "Loan Repayment by Borrower's Annual Income: Analysis of Loan Closings and Income Trends",
                    "left": "center",
                    "top": "-3%",
                    "padding": 20,
                    "textStyle": {"fontWeight": "bold"}
                },
                "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
                "legend": {
                    "top": "7%",
                    "data": loan_status_values
                },
                "grid": {"left": "3%", "right": "4%", "bottom": "10%", "top": "20%", "containLabel": True},
                "xAxis": {
                    "type": "category",
                    "data": income_labels,
                "axisLabel": {
                    "show": True,
                    "formatter": "{value}",
                    "textStyle": {
                        "fontSize": 12
                    }
                },
                "name": "Annual Income",
                "nameLocation": "middle",
                "nameGap": 30
                },
                "yAxis": {
                    "type": "value",
                    "name": "Number of Borrowers"
                },
                "series": [
                    {
                        "name": "Fully Paid",
                        "type": "bar",
                        "stack": "total",
                        "label": {"show": True},
                        "emphasis": {"focus": "series"},
                        "data": fully_paid_list,
                        "itemStyle": {"color": graph_3_color_1}
                    },
                    {
                        "name": "Charged Off",
                        "type": "bar",
                        "stack": "total",
                        "label": {"show": True},
                        "emphasis": {"focus": "series"},
                        "data": charged_off_list,
                        "itemStyle": {"color": graph_3_color_2}
                    },
                ],
            }
            st_echarts(options=options, height="600px")
            
        fully_paid_list, charged_off_list = loan_status_dict['fully_paid'], loan_status_dict['charged_off']
        render_stacked_vertical_bar(fully_paid_list, charged_off_list)
st.markdown("---")  


###################################### Graph 4 ######################################
################################### Preprocessing ###################################

# Extract the 10 most frequent job titles in the data
top_10_job_titles = data['emp_title'].value_counts().head(10).index.tolist()
sorted_top_10_job_titles = sorted(top_10_job_titles)  # Sorted alphabetically

# Create separate DataFrames for each of the top 10 job titles
job_dataframes = {}
for jot_title in top_10_job_titles:
  job_dataframes[jot_title] = data[data['emp_title'] == jot_title]

# Create Selectbox for filtering by job titles
with st.container():
    col1, col2 = st.columns([0.2, 0.8])
    
    with col1:
        option = st.selectbox(
            "Which job title fascinates you the most?",
            sorted_top_10_job_titles
        )

    # Create separate DataFrame for each loan status
    user_title_choice_df = job_dataframes[option]  # The DataFrame with records of the job title selected by the user
    fully_paid_title_df = user_title_choice_df[user_title_choice_df['loan_status'] == 'Fully Paid']
    charged_off_title_df = user_title_choice_df[user_title_choice_df['loan_status'] == 'Charged Off']

    # Calculate num of borrowers per each employment length and loan status
    loan_status_title_dict = {}
    i = 0
    for df in [fully_paid_title_df, charged_off_title_df]:
      borrowers_per_emp_length_df = df.groupby(['emp_length'])['id'].count().reset_index()  # Group the records with the selected job title to Employment length
      borrowers_per_emp_length_df.rename(columns={'id': 'num_of_borrowers'}, inplace=True)  # Change the 'id' column name to 'num_of_borrowers'
      if i == 0:
        loan_status_title_dict['fully_paid'] = borrowers_per_emp_length_df['num_of_borrowers'].tolist()
        i += 1
      else:
        loan_status_title_dict['charged_off'] = borrowers_per_emp_length_df['num_of_borrowers'].tolist()
      
      
################################### Visualization ###################################

    with col2:
        def render_vertical_bar_by_title(fully_paid_title_list, charged_off_title_list):
            emp_length_years = ['< 1 year', '1 year', '2 years', '3 years', '4 years', '5 years', '6 years', '7 years', '8 years', '9 years', '10+ years']

            fig = go.Figure()
            fig.add_trace(go.Bar(x=emp_length_years,
                                 y=fully_paid_title_list,
                                 name='Fully Paid',
                                 marker_color=graph_4_color_1
                                 ))
            fig.add_trace(go.Bar(x=emp_length_years,
                                 y=charged_off_title_list,
                                 name='Charged Off',
                                 marker_color=graph_4_color_2
                                 ))

            fig.update_layout(
                title='Loan Repayment by Job Titles: The Job Titles that Request the most Loans',
                xaxis=dict(
                    title='Employment Length',
                    tickfont_size=14
                ),
                yaxis=dict(
                    title='Number of Borrowers',
                    titlefont_size=16,
                    tickfont_size=14,
                ),
                legend=dict(
                    x=1.0,
                    y=1.0,
                    bgcolor='rgba(255, 255, 255, 0)',
                    bordercolor='rgba(255, 255, 255, 0)'
                ),
                barmode='group',
                bargap=0.15,  # gap between bars of adjacent location coordinates
                bargroupgap=0.1  # gap between bars of the same location coordinate
            )
            st.plotly_chart(fig, use_container_width=True)
  
        fully_paid_title_list, charged_off_title_list = loan_status_title_dict['fully_paid'], loan_status_title_dict['charged_off']
        render_vertical_bar_by_title(fully_paid_title_list, charged_off_title_list)        
      
st.markdown("---")


###################################### Graph 5 ######################################
################################### Preprocessing ###################################

# Create Selectbox for filtering by years
with st.container():
    col1, col2 = st.columns([0.2, 0.8])
    
    with col1:
        option = st.selectbox(
            "Which year's distributions would you like to see?",
            ('2012', '2013', '2014', '2015', '2016')
        )
    
    # Create separate DataFrames for each home ownership
    user_choice_ownership_df = year_dataframes[option]  # The DataFrame with records of the year selected by the user
    unique_ownerships = data['home_ownership'].unique().tolist()
    ownership_dataframes = {}
    for ownership in unique_ownerships:
      if len(user_choice_ownership_df[user_choice_ownership_df['home_ownership'] == ownership]) > 500:  # Only home ownership with more than 500 records is relevant
        ownership_dataframes[ownership] = user_choice_ownership_df[user_choice_ownership_df['home_ownership'] == ownership]

    # Create home ownership and its list of interest rates dict
    ownership_int_rate_dict = {}
    for ownership in ownership_dataframes:
      ownership_int_rate_dict[ownership] = ownership_dataframes[ownership]['int_rate'].tolist()

    # Create List of interest rate values (X-axis) and home ownership values (Y-axis)
    hist_int_rates = []
    hist_home_ownerships = []
    # colors = ['#333F44', '#37AA9C', '#94F3E4']
    for ownership in ownership_int_rate_dict:
      hist_int_rates.append(ownership_int_rate_dict[ownership])  # List of interest rate values (X-axis) per each home ownerships
      hist_home_ownerships.append(ownership)  # List of home ownership values (Y-axis)

        
################################### Visualization ###################################

    with col2:
      def render_kernel_density_estimate():
        fig = ff.create_distplot(hist_int_rates, hist_home_ownerships, show_hist=False, colors=graph_5_colors)  # Create distplot
        fig.update_layout(
        title_text='Loan Interest Rate Distribution by Financial Stability and Home Ownership',  # Add title
        xaxis=dict(
            title='Interest Rate'  # Add x-axis title
        ),
        yaxis=dict(
            title='The Rate of Borrowers'  # Add y-axis title
        )
    )
        st.plotly_chart(fig, use_container_width=True)
        
      render_kernel_density_estimate()        

st.markdown("---")


###################################### Graph 6 ######################################
################################### Preprocessing ###################################

# Create a dictionary of the percentage of borrowers from each grade by each year
grade_per_year_dict = {}
for year_df in year_dataframes.values():
  borrowers_per_year_grade_df = year_df.groupby(['grade'])['id'].count().reset_index()  # Group the records by grade for each year
  borrowers_per_year_grade_df.rename(columns={'id': 'num_of_borrowers'}, inplace=True)  # Change the 'id' column name to 'num_of_borrowers'
  year_borrowers = borrowers_per_year_grade_df['num_of_borrowers'].sum()  # The number of borrowers in the current year
  grades_list = borrowers_per_year_grade_df['grade'].tolist()  # List of all the existed grades
  for grade in grades_list:  # Create a dict where the keys are the grades and the values are list of percentage of borrowers for each year
    borrowers_percentage = 100 * ((borrowers_per_year_grade_df.loc[borrowers_per_year_grade_df['grade'] == grade, 'num_of_borrowers'].values[0])/year_borrowers)
    if grade not in grade_per_year_dict:
      grade_per_year_dict[grade] = [borrowers_percentage]
    else:
      grade_per_year_dict[grade].append(borrowers_percentage)
 

################################### Visualization ###################################

option = {
    "title": {
        "text": "Loan Grade Trends: Percentage of Borrowers by Year",
        "left": "center",
        "top": "-3%",
        "padding": 20,
        "textStyle": {"fontWeight": "bold"}
    },
    "legend": {
        "text": "Grades",
        "left": "center",
        "top": "5%",
    },
    "tooltip": {
        "trigger": "axis",
        "axisPointer": {"type": "shadow"},
        "showContent": True,
    },
    "dataset": {
        "source": [
            ["product", "2012", "2013", "2014", "2015", "2016"],
            ["A", 19.02, 13.97, 15.54, 14.58, 14.04],
            ["B", 36.18, 35.34, 26.32, 24.41, 27.25],
            ["C", 23.34, 26.69, 27.91, 28.85, 28.86],
            ["D", 13.80, 14.83, 17.67, 17.18, 16.47],
            ["E", 5.30, 6.01, 8.81, 10.55, 8.53],
            ["F", 2.06, 2.67, 2.93, 3.45, 3.79],
            ["G", 0.30, 0.49, 0.82, 0.98, 1.06],
        ]
    },
    "xAxis": {
        "type": "category",
        "name": "Year",
        "nameLocation": "middle",
        "nameGap": 30,
    },
    "yAxis": {
        "gridIndex": 0,
        "name": "The Percentage of Borrowers",
        "nameLocation": "middle",
        "nameGap": 40,
    },
    "grid": {"top": "10%",
             "bottom": "30%",
    },
    "series": [
        {"type": "line", "smooth": True, "seriesLayoutBy": "row", "emphasis": {"focus": "series"}, "colors": ['#1f77b4']},
        {"type": "line", "smooth": True, "seriesLayoutBy": "row", "emphasis": {"focus": "series"}, "colors": ['#ff7f0e']},
        {"type": "line", "smooth": True, "seriesLayoutBy": "row", "emphasis": {"focus": "series"}, "colors": ['#2ca02c']},
        {"type": "line", "smooth": True, "seriesLayoutBy": "row", "emphasis": {"focus": "series"}, "colors": ['#d62728']},
        {"type": "line", "smooth": True, "seriesLayoutBy": "row", "emphasis": {"focus": "series"}, "colors": ['#9467bd']},
        {"type": "line", "smooth": True, "seriesLayoutBy": "row", "emphasis": {"focus": "series"}, "colors": ['#8c564b']},
        {"type": "line", "smooth": True, "seriesLayoutBy": "row", "emphasis": {"focus": "series"}, "colors": ['#e377c2']},
    ],
}

st_echarts(option, height="600px", key="echarts")

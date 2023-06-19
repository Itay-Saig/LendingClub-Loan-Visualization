# -*- coding: utf-8 -*-
"""Visualization Final Project.ipynb
"""
####################################### Imports #######################################

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

####################################### Intro #######################################

st.set_page_config(page_title="Streamlit Project",
                   page_icon=":bar_chart:",
                  layout="wide")

with st.container():
    col1, col2, col3 = st.columns([0.25, 0.5, 0.25])
    col2.title('Information Visualization - Final Project')
with st.container():
    col1, col2, col3 = st.columns([0.30, 0.5, 0.20])
    col2.header('Ido Pascaro - 206589749')
with st.container():
    col1, col2, col3 = st.columns([0.32, 0.5, 0.20])
    col2.header('Itay Saig - 206961609')
    
st.header("Intro")
st.subheader("""The subject of our simulation is to examine the change in characteristics of borrowers in the United States over the years in various aspects.""")
st.subheader("""Our visualization theme focuses on the ‘Lending Club Loan’ dataset from Kaggle which contains data from LendingClub company. LendingClub is a financial services company headquartered in San Francisco, California. The data available on Kaggle is a comprehensive dataset of loan information from LendingClub from 2007 to 2018.""")
st.subheader("""Music, often revered as a universal language, has been used for centuries to convey emotions and thoughts. Music is valued, among other things, for its therapeutic potential, especially in the treatment of mental health problems in situations such as depression, anxiety, post-traumatic stress disorder (PTSD) and more. However, the mechanisms underlying music's apparent positive effects on mental health remain elusive and unclear to this day.""")
st.subheader("""The main question we would like to investigate is: In what and how the characteristics of borrowers in the US change over the years?""")
st.markdown("---")  
color_blind = st.radio("This Project is Color-blind friendly, Are you color blind?",['No','Yes'],key=51) # Did you know that 9% of men are color blind?
if color_blind == 'Yes': 
  cmap_graph_4 = "balance" # graph 4
  color_map_graphs12 = {
        "Classical":  px.colors.qualitative.Dark24[19],  # Blue
        "EDM":  px.colors.qualitative.Dark2[4], # Green
        "Folk":  px.colors.qualitative.Antique[5], # Purple
        "Hip hop": px.colors.qualitative.Dark24[14], # Olive
        "Metal": px.colors.qualitative.Set1[5],  # Yellow
        "Pop": px.colors.qualitative.Set1[0],  # Red
        "R&B": px.colors.qualitative.Dark24[5], # Black
        "Rock": px.colors.qualitative.Dark2[0], # Dark Green
        "Video game music":  px.colors.qualitative.Plotly[8] # Pink
    }
  color_map_graph3 = {
        "Anxiety": px.colors.qualitative.Dark24[5],  # Black
        "Depression": px.colors.qualitative.Set1[0],  # Red
        "Insomnia": px.colors.qualitative.Set1[1],  # Blue
        "OCD": px.colors.qualitative.Set1[5]  # Yellow
    } 
else:
  cmap_graph_4 = "Tempo" # graph 4
  color_map_graphs12 = {
        "Classical": px.colors.qualitative.Dark24[19], # Deep Blue
        "EDM":  px.colors.qualitative.D3[5], # Brown
        "Folk":  px.colors.qualitative.T10[9], # Grey
        "Hip hop": px.colors.qualitative.Alphabet[6], # Light Green
        "Metal": px.colors.qualitative.Alphabet[24], # Yellow
        "Pop": px.colors.qualitative.Light24[0], # Red
        "R&B": px.colors.qualitative.Dark24[5], # Black
        "Rock": px.colors.qualitative.Dark2[0], # Dark Green
        "Video game music":  px.colors.qualitative.Prism[6], # Orange
      }
  color_map_graph3 = {
        "Anxiety": px.colors.qualitative.Bold[2],  # Blue
        "Depression": px.colors.qualitative.Bold[3],  # Pink
        "Insomnia": px.colors.qualitative.Bold[4],  # Yellow
        "OCD": px.colors.qualitative.Bold[5]  # Green
    }
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

# # Create population dict for each state in USA
# states_pop_dict = {'Alabama': 4903185, 'Alaska': 710249, 'Arizona': 7278717, 'Arkansas': 3017804, 'California': 39368078, 'Colorado': 5758736, 'Connecticut': 3565287, 'Delaware': 973764, 'Florida': 21733312, 'Georgia': 10617423, 'Hawaii': 1415872, 'Idaho': 1787065, 'Illinois': 12671821, 'Indiana': 6732219, 'Iowa': 3155070, 'Kansas': 2913314, 'Kentucky': 4467673, 'Louisiana': 4648794, 'Maine': 1344212, 'Maryland': 6045680, 'Massachusetts': 6892503, 'Michigan': 9883635,
#                    'Minnesota': 5639632, 'Mississippi': 2976149, 'Missouri': 6137428, 'Montana': 1068778, 'Nebraska': 1934408, 'Nevada': 3080156, 'New Hampshire': 1359711, 'New Jersey': 8882190, 'New Mexico': 2096829, 'New York': 19336776, 'North Carolina': 10488084, 'North Dakota': 762062, 'Ohio': 11689100, 'Oklahoma': 3980783, 'Oregon': 4217737, 'Pennsylvania': 12801989, 'Rhode Island': 1059361, 'South Carolina': 5148714, 'South Dakota': 884659, 'Tennessee': 6829174,
#                    'Texas': 29360759, 'Utah': 3205958, 'Vermont': 623989, 'Virginia': 8535519, 'Washington': 7614893, 'West Virginia': 1792147, 'Wisconsin': 5822434, 'Wyoming': 578759}

# Calculate num of borrowers per state
borrowers_per_state_df = data.groupby(['borrower_state'])['id'].count().reset_index()
borrowers_per_state_df.rename(columns={'id': 'num_of_borrowers'}, inplace=True)  # Change the 'id' column name to 'num_of_borrowers'


################################### Visualization ###################################

def render_usa():
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
            "text": "Percentage of Borrowers by State in the United States",
            "subtext": "Data from www.census.gov",
            "sublink": "http://www.census.gov/popest/data/datasets.html",
            "left": "right",
        },
        "tooltip": {
            "trigger": "item",
            "showDelay": 0,
            "transitionDuration": 0.2,
            "formatter": formatter,
        },
        "visualMap": {
            "left": "right",
            "min": 500000,
            "max": 38000000,
            "inRange": {
                "color": ["#E6F5FF", "#B3E6FF", "#80D4FF", "#4DC3FF", "#1AB1FF", "#008FFF", "#0077CC", "#0055AA", "#003377", "#001155", "#000033",] },
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
                "name": "Percentage of Borrowers in the State",
                "type": "map",
                "roam": True,
                "map": "USA",
                "emphasis": {"label": {"show": True}},
                "textFixed": {"Alaska": [20, -20]},
                "data": [
                    {"name": "Alabama", "value": 4822023},
                    {"name": "Alaska", "value": 731449},
                    {"name": "Arizona", "value": 6553255},
                    {"name": "Arkansas", "value": 2949131},
                    {"name": "California", "value": 38041430},
                    {"name": "Colorado", "value": 5187582},
                    {"name": "Connecticut", "value": 3590347},
                    {"name": "Delaware", "value": 917092},
                    {"name": "District of Columbia", "value": 632323},
                    {"name": "Florida", "value": 19317568},
                    {"name": "Georgia", "value": 9919945},
                    {"name": "Hawaii", "value": 1392313},
                    {"name": "Idaho", "value": 1595728},
                    {"name": "Illinois", "value": 12875255},
                    {"name": "Indiana", "value": 6537334},
                    {"name": "Iowa", "value": 3074186},
                    {"name": "Kansas", "value": 2885905},
                    {"name": "Kentucky", "value": 4380415},
                    {"name": "Louisiana", "value": 4601893},
                    {"name": "Maine", "value": 1329192},
                    {"name": "Maryland", "value": 5884563},
                    {"name": "Massachusetts", "value": 6646144},
                    {"name": "Michigan", "value": 9883360},
                    {"name": "Minnesota", "value": 5379139},
                    {"name": "Mississippi", "value": 2984926},
                    {"name": "Missouri", "value": 6021988},
                    {"name": "Montana", "value": 1005141},
                    {"name": "Nebraska", "value": 1855525},
                    {"name": "Nevada", "value": 2758931},
                    {"name": "New Hampshire", "value": 1320718},
                    {"name": "New Jersey", "value": 8864590},
                    {"name": "New Mexico", "value": 2085538},
                    {"name": "New York", "value": 19570261},
                    {"name": "North Carolina", "value": 9752073},
                    {"name": "North Dakota", "value": 699628},
                    {"name": "Ohio", "value": 11544225},
                    {"name": "Oklahoma", "value": 3814820},
                    {"name": "Oregon", "value": 3899353},
                    {"name": "Pennsylvania", "value": 12763536},
                    {"name": "Rhode Island", "value": 1050292},
                    {"name": "South Carolina", "value": 4723723},
                    {"name": "South Dakota", "value": 833354},
                    {"name": "Tennessee", "value": 6456243},
                    {"name": "Texas", "value": 26059203},
                    {"name": "Utah", "value": 2855287},
                    {"name": "Vermont", "value": 626011},
                    {"name": "Virginia", "value": 8185867},
                    {"name": "Washington", "value": 6897012},
                    {"name": "West Virginia", "value": 1855413},
                    {"name": "Wisconsin", "value": 5726398},
                    {"name": "Wyoming", "value": 576412},
                    {"name": "Puerto Rico", "value": 3667084},
                ],
            }
        ],
    }
    st_echarts(options, map=map)


# ST_MAP_DEMOS = {
#     "Map: USA Population estimates": (
#         render_usa,
#         "https://echarts.apache.org/examples/en/editor.html?c=map-usa",
#     ),
# }
render_usa()
st.markdown("---")  


###################################### Graph 2 ######################################
################################### Preprocessing ###################################

# Create a dataframe
# df = pd.DataFrame({'group': list(map(chr, range(65, 85))), 'values': np.random.uniform(size=20)})

# # Reorder it based on the values
# ordered_df = df.sort_values(by='values')
# my_range = range(1, len(df.index) + 1)

# # Create a horizontal bar trace
# trace = go.Bar(
#     x=ordered_df['values'],
#     y=my_range,
#     orientation='h',
#     marker=dict(color='skyblue')
# )

# # Create the layout
# layout = go.Layout(
#     title="Interactive Horizontal Lollipop Graph",
#     xaxis=dict(title="Value of the variable"),
#     yaxis=dict(title="Group")
# )

# # Create the figure
# fig = go.Figure(data=[trace], layout=layout)

# # Render the figure using Streamlit
# st.plotly_chart(fig)

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
                "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
                "legend": {
                    "data": loan_status_values
                },
                "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
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
                    },
                    {
                        "name": "Charged Off",
                        "type": "bar",
                        "stack": "total",
                        "label": {"show": True},
                        "emphasis": {"focus": "series"},
                        "data": charged_off_list,
                    },
                ],
            }
            st_echarts(options=options, height="500px")
            
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
                                 marker_color='rgb(55, 83, 109)'
                                 ))
            fig.add_trace(go.Bar(x=emp_length_years,
                                 y=charged_off_title_list,
                                 name='Charged Off',
                                 marker_color='rgb(26, 118, 255)'
                                 ))

            fig.update_layout(
                title='Loan Repayment by Job Titles: Top 10 Loan Requested Job Titles',
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
                bargap=0.15,  # gap between bars of adjacent location coordinates.
                bargroupgap=0.1  # gap between bars of the same location coordinate.
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
    colors = ['#333F44', '#37AA9C', '#94F3E4']
    for ownership in ownership_int_rate_dict:
      hist_int_rates.append(ownership_int_rate_dict[ownership])  # List of interest rate values (X-axis) per each home ownerships
      hist_home_ownerships.append(ownership)  # List of home ownership values (Y-axis)

        
################################### Visualization ###################################

    with col2:
      def render_kernel_density_estimate():
        fig = ff.create_distplot(hist_int_rates, hist_home_ownerships, show_hist=False, colors=colors)  # Create distplot
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

# option = {
#     "legend": {"top": "90%"},
#     "tooltip": {"trigger": "axis", "showContent": False},
#     "dataset": {
#         "source": [
#             ["product", "2012", "2013", "2014", "2015", "2016"],
#             ["A", 19.024986420423684, 13.969972926409058, 15.543398308201544, 14.57862204130861, 14.040063818471902],
#             ["B", 36.17599130907116, 35.33841988678317, 26.314821625597645, 24.408261721694558, 27.24694203155469],
#             ["C", 23.343291689299296, 26.689638198375587, 27.91007723427731, 28.845670636715415, 28.860131182414467],
#             ["D", 13.796849538294406, 14.826482894412996, 17.667340934166972, 17.181767928036585, 16.46871122141464],
#             ["E", 5.296034763715372, 6.010337189269014, 8.808385435821993, 10.548268757223981, 8.526856940258819],
#             ["F", 2.0640956002172732, 2.6729017967019444, 2.933063626333211, 3.452434795718378, 3.793653607516398],
#             ["G", 0.29875067897881585, 0.49224710804824023, 0.822912835601324, 0.9849741193024776, 1.0636411983690834],
#         ]
#     },
#     "xAxis": {"type": "category"},
#     "yAxis": {"gridIndex": 0},
#     "grid": {"top": "0%"},  # Adjust the top value to remove the space above the graph
#     "series": [
#         {"type": "line", "smooth": True, "seriesLayoutBy": "row", "emphasis": {"focus": "series"}},
#         {"type": "line", "smooth": True, "seriesLayoutBy": "row", "emphasis": {"focus": "series"}},
#         {"type": "line", "smooth": True, "seriesLayoutBy": "row", "emphasis": {"focus": "series"}},
#         {"type": "line", "smooth": True, "seriesLayoutBy": "row", "emphasis": {"focus": "series"}},
#         {"type": "line", "smooth": True, "seriesLayoutBy": "row", "emphasis": {"focus": "series"}},
#         {"type": "line", "smooth": True, "seriesLayoutBy": "row", "emphasis": {"focus": "series"}},
#         {"type": "line", "smooth": True, "seriesLayoutBy": "row", "emphasis": {"focus": "series"}},
#     ],
# }

# st_echarts(option, height="500px", key="echarts")



# # Update the tooltip formatter to access the correct data
# option["tooltip"]["formatter"] = "({b}, {c})".format(
#     b=option["dataset"]["source"][0][0],
#     c=option["dataset"]["source"][1][1],
# )

# source = option["dataset"]["source"]  # Get the source data

# # Iterate over each column (excluding the first column)
# for i in range(1, len(source[0])):
#     year = source[0][i]  # Get the year value from the first row
#     line_data = []  # List to store tuples of (year, value) for each line

#     # Iterate over each line (excluding the first line)
#     for j in range(1, len(source)):
#         product = source[j][0]  # Get the product value from the first column
#         value = source[j][i]  # Get the corresponding value from the current column
#         line_data.append((year, value))  # Append the (year, value) tuple to the line_data list

#     print(line_data)  # Do something with the line_data, such as displaying or processing it

    
# st_echarts(option, height="500px", key="echarts")


# option = {
#     "legend": {"top": "90%"},
#     "tooltip": {
#         "trigger": "axis",
#         "axisPointer": {"type": "shadow"},
#         "showContent": True,
#     },
#     "dataset": {
#         "source": [
#             ["product", "2012", "2013", "2014", "2015", "2016"],
#             ["A", 19.024986420423684, 13.969972926409058, 15.543398308201544, 14.57862204130861, 14.040063818471902],
#             ["B", 36.17599130907116, 35.33841988678317, 26.314821625597645, 24.408261721694558, 27.24694203155469],
#             ["C", 23.343291689299296, 26.689638198375587, 27.91007723427731, 28.845670636715415, 28.860131182414467],
#             ["D", 13.796849538294406, 14.826482894412996, 17.667340934166972, 17.181767928036585, 16.46871122141464],
#             ["E", 5.296034763715372, 6.010337189269014, 8.808385435821993, 10.548268757223981, 8.526856940258819],
#             ["F", 2.0640956002172732, 2.6729017967019444, 2.933063626333211, 3.452434795718378, 3.793653607516398],
#             ["G", 0.29875067897881585, 0.49224710804824023, 0.822912835601324, 0.9849741193024776, 1.0636411983690834],
#         ]
#     },
#     "xAxis": {"type": "category"},
#     "yAxis": {"gridIndex": 0},
#     "grid": {"top": "0%"},
#     "series": [
#         {"type": "line", "smooth": True, "seriesLayoutBy": "row", "emphasis": {"focus": "series"}},
#         {"type": "line", "smooth": True, "seriesLayoutBy": "row", "emphasis": {"focus": "series"}},
#         {"type": "line", "smooth": True, "seriesLayoutBy": "row", "emphasis": {"focus": "series"}},
#         {"type": "line", "smooth": True, "seriesLayoutBy": "row", "emphasis": {"focus": "series"}},
#         {"type": "line", "smooth": True, "seriesLayoutBy": "row", "emphasis": {"focus": "series"}},
#         {"type": "line", "smooth": True, "seriesLayoutBy": "row", "emphasis": {"focus": "series"}},
#         {"type": "line", "smooth": True, "seriesLayoutBy": "row", "emphasis": {"focus": "series"}},
#     ],
# }
# st_echarts(option, height="500px", key="echarts")

# source = option["dataset"]["source"]  # Get the source data

# # Iterate over each column (excluding the first column)
# for i in range(1, len(source[0])):
#     year = source[0][i]  # Get the year value from the first row
#     line_data = []  # List to store tuples of (year, value) for each line

#     # Iterate over each line (excluding the first line)
#     for j in range(1, len(source)):
#         product = source[j][0]  # Get the product value from the first column
#         value = source[j][i]  # Get the corresponding value from the current column
#         line_data.append((year, value))  # Append the (year, value) tuple to the line_data list

#     # Update the formatter function for the corresponding series
#     option["series"][i-1]["label"] = {
#         "formatter": "{{b}}: ({})".format(", ".join(["{}, {}".format(year, value) for year, value in line_data]))
#     }

# option = {
#     "legend": {"right": "10%", "top": "5%"},  # Move legend to the right side
#     "tooltip": {
#         "trigger": "axis",
#         "axisPointer": {"type": "shadow"},
#         "showContent": True,
#     },
#     "dataset": {
#         "source": [
#             ["product", "2012", "2013", "2014", "2015", "2016"],
#             ["A", 19.024986420423684, 13.969972926409058, 15.543398308201544, 14.57862204130861, 14.040063818471902],
#             ["B", 36.17599130907116, 35.33841988678317, 26.314821625597645, 24.408261721694558, 27.24694203155469],
#             ["C", 23.343291689299296, 26.689638198375587, 27.91007723427731, 28.845670636715415, 28.860131182414467],
#             ["D", 13.796849538294406, 14.826482894412996, 17.667340934166972, 17.181767928036585, 16.46871122141464],
#             ["E", 5.296034763715372, 6.010337189269014, 8.808385435821993, 10.548268757223981, 8.526856940258819],
#             ["F", 2.0640956002172732, 2.6729017967019444, 2.933063626333211, 3.452434795718378, 3.793653607516398],
#             ["G", 0.29875067897881585, 0.49224710804824023, 0.822912835601324, 0.9849741193024776, 1.0636411983690834],
#         ]
#     },
#     "xAxis": {
#         "type": "category",
#         "name": "Year",
#         "nameLocation": "middle",
#         "nameGap": 30,
#     },
#     "yAxis": {
#         "gridIndex": 0,
#         "name": "The Percentage of Borrowers",
#         "nameLocation": "middle",
#         "nameGap": 40,
#     },
#     "grid": {"top": "0%"},
#     "series": [
#         {"type": "line", "smooth": True, "seriesLayoutBy": "row", "emphasis": {"focus": "series"}},
#         {"type": "line", "smooth": True, "seriesLayoutBy": "row", "emphasis": {"focus": "series"}},
#         {"type": "line", "smooth": True, "seriesLayoutBy": "row", "emphasis": {"focus": "series"}},
#         {"type": "line", "smooth": True, "seriesLayoutBy": "row", "emphasis": {"focus": "series"}},
#         {"type": "line", "smooth": True, "seriesLayoutBy": "row", "emphasis": {"focus": "series"}},
#         {"type": "line", "smooth": True, "seriesLayoutBy": "row", "emphasis": {"focus": "series"}},
#         {"type": "line", "smooth": True, "seriesLayoutBy": "row", "emphasis": {"focus": "series"}},
#     ],
# }

# st_echarts(option, height="500px", key="echarts")


option = {
    "title": {
        "text": "Loan Grade Trends: Percentage of Borrowers by Year",
        "left": "center",
        "top": "-3%",  # Move the title further up
        "padding": 20,
        "textStyle": {"fontWeight": "bold"}
    },
    "legend": {"right": "2%", "top": "10%"},  # Move legend to the top-right corner
    "tooltip": {
        "trigger": "axis",
        "axisPointer": {"type": "shadow"},
        "showContent": True,
    },
    "dataset": {
        "source": [
            ["product", "2012", "2013", "2014", "2015", "2016"],
            ["A", 19.024986420423684, 13.969972926409058, 15.543398308201544, 14.57862204130861, 14.040063818471902],
            ["B", 36.17599130907116, 35.33841988678317, 26.314821625597645, 24.408261721694558, 27.24694203155469],
            ["C", 23.343291689299296, 26.689638198375587, 27.91007723427731, 28.845670636715415, 28.860131182414467],
            ["D", 13.796849538294406, 14.826482894412996, 17.667340934166972, 17.181767928036585, 16.46871122141464],
            ["E", 5.296034763715372, 6.010337189269014, 8.808385435821993, 10.548268757223981, 8.526856940258819],
            ["F", 2.0640956002172732, 2.6729017967019444, 2.933063626333211, 3.452434795718378, 3.793653607516398],
            ["G", 0.29875067897881585, 0.49224710804824023, 0.822912835601324, 0.9849741193024776, 1.0636411983690834],
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
        "interval": 5  # Set the interval to 5 to make the spacing smaller
    },
    "grid": {"top": "10%", "bottom": "5%",
    },
    "series": [
        {"type": "line", "smooth": True, "seriesLayoutBy": "row", "emphasis": {"focus": "series"}},
        {"type": "line", "smooth": True, "seriesLayoutBy": "row", "emphasis": {"focus": "series"}},
        {"type": "line", "smooth": True, "seriesLayoutBy": "row", "emphasis": {"focus": "series"}},
        {"type": "line", "smooth": True, "seriesLayoutBy": "row", "emphasis": {"focus": "series"}},
        {"type": "line", "smooth": True, "seriesLayoutBy": "row", "emphasis": {"focus": "series"}},
        {"type": "line", "smooth": True, "seriesLayoutBy": "row", "emphasis": {"focus": "series"}},
        {"type": "line", "smooth": True, "seriesLayoutBy": "row", "emphasis": {"focus": "series"}},
    ],
}

st_echarts(option, height="600px", key="echarts")






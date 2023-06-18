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

################################### Preprocessing ###################################
############################### General Preprocessing ###############################

data = pd.read_csv('lending_club_loan_two.csv') # read csv

# Replace 'RN' with 'Registered Nurse'
data['emp_title'] = data['emp_title'].replace('RN', 'Registered Nurse')

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
income_ranges = [0, 20000, 40000, 60000, 80000, 100000, 150000, float('inf')]  # Define income ranges
income_labels = ['< $20,000', '$20,000 - $40,000', '$40,000 - $60,000', '$60,000 - $80,000', '$80,000 - $100,000', '$100,000 - $150,000', '> $150,000']
data['income_range'] = pd.cut(data['annual_inc'], bins=income_ranges, labels=income_labels, right=False)  # Categorize the values into income ranges

# Create separate DataFrames for each year
unique_years = data['issue_year'].unique().tolist()
year_dataframes = {}
for year in unique_years:
  year_dataframes[year] = data[data['issue_year'] == year]


#################################### OUR GRAPHS ##################################### 


###################################### Graph 1 ######################################
################################### Preprocessing ###################################

# # Create population dict for each state in USA
# states_pop_dict = {'Alabama': 4903185, 'Alaska': 710249, 'Arizona': 7278717, 'Arkansas': 3017804, 'California': 39368078, 'Colorado': 5758736, 'Connecticut': 3565287, 'Delaware': 973764, 'Florida': 21733312, 'Georgia': 10617423, 'Hawaii': 1415872, 'Idaho': 1787065, 'Illinois': 12671821, 'Indiana': 6732219, 'Iowa': 3155070, 'Kansas': 2913314, 'Kentucky': 4467673, 'Louisiana': 4648794, 'Maine': 1344212, 'Maryland': 6045680, 'Massachusetts': 6892503, 'Michigan': 9883635,
#                    'Minnesota': 5639632, 'Mississippi': 2976149, 'Missouri': 6137428, 'Montana': 1068778, 'Nebraska': 1934408, 'Nevada': 3080156, 'New Hampshire': 1359711, 'New Jersey': 8882190, 'New Mexico': 2096829, 'New York': 19336776, 'North Carolina': 10488084, 'North Dakota': 762062, 'Ohio': 11689100, 'Oklahoma': 3980783, 'Oregon': 4217737, 'Pennsylvania': 12801989, 'Rhode Island': 1059361, 'South Carolina': 5148714, 'South Dakota': 884659, 'Tennessee': 6829174,
#                    'Texas': 29360759, 'Utah': 3205958, 'Vermont': 623989, 'Virginia': 8535519, 'Washington': 7614893, 'West Virginia': 1792147, 'Wisconsin': 5822434, 'Wyoming': 578759}

# Calculate num of borrowers per state
data['id'] = range(1, len(data) + 1)  # Create 'id' column for each borrower to use in aggregation operations
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

# Create annual income ranges
incomes_df = pd.DataFrame()
income_ranges = [0, 20000, 40000, 60000, 80000, 100000, 150000, float('inf')]  # Define income ranges
income_labels = ['< $20,000', '$20,000 - $40,000', '$40,000 - $60,000', '$60,000 - $80,000', '$80,000 - $100,000', '$100,000 - $150,000', '> $150,000']
incomes_df['income_range'] = pd.cut(data['annual_inc'], bins=income_ranges, labels=income_labels, right=False)  # Categorize the values into income ranges
loan_status_values = ["Fully Paid", "Charged Off"]

# Create Selectbox for filtering by years
with st.container():
    col1, col2 = st.columns([0.2, 0.8])
    with col1:
      option = st.selectbox(
        "Which year are you interested in?",
        ('2012', '2013', '2014', '2015', '2016')
    )

# Create seperate DataFrame for each loan status
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
              },
              "yAxis": {"type": "value"},
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
st.markdown("---")  




















# def apply_bins_hours(time): # divide to hour bins for graph number 4
#   if time <= 2:
#     return "[0-2]"
#   if time < 3:
#     return "(2-3]"
#   if time < 5:
#     return "(3-4]"
#   return "(4-24]"
# df['Hours bins'] = df['Hours per day'].apply(apply_bins_hours)

# # calculate the mean of targets for graph number 4
# df['Average Score'] = df.apply(lambda row: row[['Anxiety', 'Depression', 'Insomnia', 'OCD']].mean(), axis=1)
          
# # make a DF for graph number 3 : 
# third_graph_df = pd.DataFrame(columns=['Genre','Mental Disorder', 'Average Score'])
# targets = ['Anxiety','Depression','Insomnia','OCD']
# names = sorted(['Rock','Video game music','R&B','EDM', 'Hip hop','Pop','Classical', 'Metal', 'Folk'])
# j=0
# for name in names:
#     curr_df = df[df['Favorite Genre']==name]
#     for target in targets:
#         j+=1
#         curr_avg = np.mean(curr_df[target])
#         third_graph_df.loc[j] = [name ,target, curr_avg]

    
    
    
    
    
    
    
    
# st.markdown("---")  
# ####################################### OUR GRAPHS ####################################### 


# ##################################### First Graph #####################################

    
# st.subheader('Age & Mental Health Disorders scores - Scatter plot')
# st.text('Would you like to see how age affects the Average of the Mental health scores? Or compare between two or more specific scores?')
# comparison = st.radio("Choose one of:", ['None', 'Average', 'Comparison'], key=50)
  
# if comparison == 'Comparison':
#     st.text("Which Mental Health Disorders would you like to compare?")
#     with st.container():
#         col1, col2, col3, col4 = st.columns([0.15, 0.15, 0.15, 0.55])
#         checkbox1 = col1.checkbox('Anxiety', key=1)
#         checkbox2 = col2.checkbox('Depression', key=2)
#         checkbox3 = col3.checkbox('Insomnia', key=3)    
#         checkbox4 = col4.checkbox('OCD', key=4) 
     
#     list_of_trues = [False, False, False, False]
#     if (checkbox1):
#         list_of_trues[0] = True
#     else:
#         list_of_trues[0] = False
          
#     if (checkbox2):
#         list_of_trues[1] = True
#     else:
#         list_of_trues[1] = False
          
#     if (checkbox3):
#         list_of_trues[2] = True
#     else:
#         list_of_trues[2] = False
          
#     if (checkbox4):
#         list_of_trues[3] = True
#     else:
#         list_of_trues[3] = False
          
#     true_indices = [index for index, value in enumerate(list_of_trues) if value]
#     graphs_amount = sum(list_of_trues)
      
     
  
#     if sum(list_of_trues) > 0:

#       bool_genres = st.radio("Please choose view method for genres:",['I prefer to choose the genres manually','Select all genres'],key=777)
#       if bool_genres=='I prefer to choose the genres manually':
#         with st.container():
#           col1, col2, col3, col4,col5, col6, col7, col8 ,col9 = st.columns(9)
#           classical = col1.checkbox('Classical', key=9)
#           edm = col2.checkbox('EDM', key=10)
#           folk = col3.checkbox('Folk', key=11)    
#           hiphop = col4.checkbox('Hip hop', key=12) 
#           metal = col5.checkbox('Metal', key=13)
#           pop = col6.checkbox('Pop', key=14)  
#           rnb = col7.checkbox('R&B', key=15)    
#           rock = col8.checkbox('Rock', key=16) 
#           videogame = col9.checkbox('Video game music', key=17) 
#       elif bool_genres=='Select all genres':
#         with st.container():
#           col1, col2, col3, col4,col5, col6, col7, col8 ,col9 = st.columns(9)
#           classical = col1.checkbox('Classical',value=True, key=956555)
#           edm = col2.checkbox('EDM',value=True, key=10555)
#           folk = col3.checkbox('Folk',value=True, key=155551)    
#           hiphop = col4.checkbox('Hip hop',value=True, key=125555) 
#           metal = col5.checkbox('Metal',value=True, key=1555553)
#           pop = col6.checkbox('Pop',value=True, key=145555)  
#           rnb = col7.checkbox('R&B',value=True, key=15555)    
#           rock = col8.checkbox('Rock',value=True, key=165555) 
#           videogame = col9.checkbox('Video game music',value=True, key=15557) 
#       check_box_booleans_graph_1 = [classical,edm,folk,hiphop,metal,pop,rnb,rock,videogame]        
#       genres = ['Classical','EDM','Folk','Hip hop','Metal','Pop','R&B','Rock','Video game music'] 
#       to_show_graph1 =[]
#       for i in range(len(genres)):
#           if check_box_booleans_graph_1[i]:
#               to_show_graph1.append(genres[i])   
  
#       to_show_df_graph1 = df[df["Favorite Genre"].isin(to_show_graph1)]
  
    
#       Anxiety = px.scatter(to_show_df_graph1,x="Age", y = 'Anxiety',
#                           color="Favorite Genre",
#                           title="Age Vs. Anxiety",
#                           color_discrete_map = color_map_graphs12)
  
      
#       Depression = px.scatter(to_show_df_graph1,x="Age", y = 'Depression',
#                           color="Favorite Genre",
#                           title="Age Vs. Depression",
#                           color_discrete_map = color_map_graphs12)
      
#       Insomnia = px.scatter(to_show_df_graph1,x="Age", y = 'Insomnia',
#                           color="Favorite Genre",
#                           title="Age Vs. Insomnia",
#                           color_discrete_map = color_map_graphs12)
      
#       OCD = px.scatter(to_show_df_graph1,x="Age", y = 'OCD',
#                           color="Favorite Genre",
#                           title="Age Vs. OCD",
#                           color_discrete_map = color_map_graphs12)


                                            








      
      
#       graphs = [Anxiety, Depression, Insomnia, OCD]
#       for g in graphs:
#           g.update_xaxes(tickmode='linear', dtick=10)
#           g.update_xaxes(title_font=dict(size=20), tickfont=dict(size=14))
#           g.update_yaxes(title_font=dict(size=20), tickfont=dict(size=14))
#           g.update_layout(font=dict(size=28))
                  


        
#           for trace in g.data:
#               trace.update(marker=dict(size=10, opacity=0.7))
#       if graphs_amount == 0:
#           pass
      
#       elif graphs_amount == 1:
#           for i in range(len(list_of_trues)):
#               if list_of_trues[i]:
#                   st.plotly_chart(graphs[i], use_container_width=True)
                  
#       elif graphs_amount == 2:
#             col1, col2 = st.columns(2, gap="large")
#             g1_idx = true_indices[0]
#             g2_idx = true_indices[1]
#             with col1:
#               st.plotly_chart(graphs[g1_idx], use_container_width=False)
#             with col2:
#               st.plotly_chart(graphs[g2_idx], use_container_width=False)
#       elif graphs_amount == 3:
#             col1, col2 = st.columns(2, gap="large")
#             g1_idx = true_indices[0]
#             g2_idx = true_indices[1]
#             g3_idx = true_indices[2]
#             with col1:
#               st.plotly_chart(graphs[g1_idx], use_container_width=False)
#             with col2:
#               st.plotly_chart(graphs[g2_idx], use_container_width=False)
#             col3, _ = st.columns(2, gap="large")
#             with col3:
#               st.plotly_chart(graphs[g3_idx], use_container_width=False)
  
#       elif graphs_amount == 4:
#           col1, col2 = st.columns(2, gap="large")
  
#           with col1:
#               st.plotly_chart(graphs[0], use_container_width=False)
#           with col2:
#               st.plotly_chart(graphs[1], use_container_width=False)
              
#           col3, col4 = st.columns(2, gap="large")
#           with col3:
#               st.plotly_chart(graphs[2], use_container_width=False)   
#           with col4:
#               st.plotly_chart(graphs[3], use_container_width=False)   
  
  
# elif comparison == 'Average':
#       bool_genres = st.radio("Choose view method for genres:",['I prefer to choose the genres manually','Select all genres'],key=779)
#       if bool_genres=='I prefer to choose the genres manually':
#         with st.container():
#           col1, col2, col3, col4,col5, col6, col7, col8 ,col9 = st.columns(9)
#           classical = col1.checkbox('Classical', key=93)
#           edm = col2.checkbox('EDM', key=1330)
#           folk = col3.checkbox('Folk', key=1331)    
#           hiphop = col4.checkbox('Hip hop', key=1332) 
#           metal = col5.checkbox('Metal', key=13333)
#           pop = col6.checkbox('Pop', key=1334)  
#           rnb = col7.checkbox('R&B', key=1335)    
#           rock = col8.checkbox('Rock', key=333333) 
#           videogame = col9.checkbox('Video game music', key=1337) 
#       elif bool_genres=='Select all genres':
#         with st.container():
#           col1, col2, col3, col4,col5, col6, col7, col8 ,col9 = st.columns(9)
#           classical = col1.checkbox('Classical',value=True, key=95653355)
#           edm = col2.checkbox('EDM',value=True, key=1053355)
#           folk = col3.checkbox('Folk',value=True, key=1555331)    
#           hiphop = col4.checkbox('Hip hop',value=True, key=33333333333333333) 
#           metal = col5.checkbox('Metal',value=True, key=155533553)
#           pop = col6.checkbox('Pop',value=True, key=145333555)  
#           rnb = col7.checkbox('R&B',value=True, key=15553335)    
#           rock = col8.checkbox('Rock',value=True, key=165533355) 
#           videogame = col9.checkbox('Video game music',value=True, key=1533557) 
#       check_box_booleans_graph_1 = [classical,edm,folk,hiphop,metal,pop,rnb,rock,videogame]        
#       genres = ['Classical','EDM','Folk','Hip hop','Metal','Pop','R&B','Rock','Video game music'] 
#       to_show_graph1 =[]
#       for i in range(len(genres)):
#           if check_box_booleans_graph_1[i]:
#               to_show_graph1.append(genres[i])
   
  
#       to_show_df_graph1 = df[df["Favorite Genre"].isin(to_show_graph1)]
  
#       g = px.scatter(to_show_df_graph1, x="Age", y="Average Score",
#                            color="Favorite Genre",
#                            title="Age Vs. Average of scores",
#                           color_discrete_map = color_map_graphs12)
#       for trace in g.data:
#             trace.update(marker=dict(size=10, opacity=0.7))
#       g.update_layout(yaxis_title='Average of Mental Health Scores')
#       g.update_xaxes(range=[-0.5, 90.5], tickmode='linear', dtick=10)  
#       g.update_xaxes(title_font=dict(size=20), tickfont=dict(size=14))
#       g.update_yaxes(title_font=dict(size=20), tickfont=dict(size=14))
#       st.plotly_chart(g, use_container_width=True)
  

# st.markdown("---")     
  
  
  
  
  
  
# ##################################### Second Graph #####################################
# st.subheader('Hours of listening (Daily) & Mental Health Disorders scores - Scatter plot')
# st.text('Would you like to see how Hours of listening affects the Average of the Mental health scores? Or compare between two or more specific scores?')

# comparison = st.radio("Choose one of:", ['None', 'Average', 'Comparison'], key=52)
# if comparison == 'Comparison':
#     st.text("Which Mental Health Disorders would you like to compare?")
#     with st.container():
#         col1, col2, col3, col4 = st.columns([0.15, 0.15, 0.15, 0.55])
#         checkbox5 = col1.checkbox('Anxiety', key=5)
#         checkbox6 = col2.checkbox('Depression', key=6)
#         checkbox7 = col3.checkbox('Insomnia', key=7)    
#         checkbox8 = col4.checkbox('OCD', key=8) 
        
#     list_of_trues = [False, False, False, False]
#     if (checkbox5):
#         list_of_trues[0] = True
#     else:
#         list_of_trues[0] = False
        
#     if (checkbox6):
#         list_of_trues[1] = True
#     else:
#         list_of_trues[1] = False
        
#     if (checkbox7):
#         list_of_trues[2] = True
#     else:
#         list_of_trues[2] = False
        
#     if (checkbox8):
#         list_of_trues[3] = True
#     else:
#         list_of_trues[3] = False
        
#     true_indices = [index for index, value in enumerate(list_of_trues) if value]
#     graphs_amount = sum(list_of_trues)



#     if sum(list_of_trues) > 0:
      

#       bool_genres2 = st.radio("Please choose view method for genres:",['I prefer to choose the genres manually','Select all genres'],key=877)
#       if bool_genres2=='I prefer to choose the genres manually':
#         with st.container():
#           col1, col2, col3, col4,col5, col6, col7, col8 ,col9 = st.columns(9)
#           classical = col1.checkbox('Classical', key=29)
#           edm = col2.checkbox('EDM', key=210)
#           folk = col3.checkbox('Folk', key=211)    
#           hiphop = col4.checkbox('Hip hop', key=212) 
#           metal = col5.checkbox('Metal', key=213)
#           pop = col6.checkbox('Pop', key=214)  
#           rnb = col7.checkbox('R&B', key=125)    
#           rock = col8.checkbox('Rock', key=216) 
#           videogame = col9.checkbox('Video game music', key=217) 
#       elif bool_genres2=='Select all genres':
#         with st.container():
#           col1, col2, col3, col4,col5, col6, col7, col8 ,col9 = st.columns(9)
#           classical = col1.checkbox('Classical',value=True, key=9256555)
#           edm = col2.checkbox('EDM',value=True, key=120555)
#           folk = col3.checkbox('Folk',value=True, key=1552551)    
#           hiphop = col4.checkbox('Hip hop',value=True, key=1252555) 
#           metal = col5.checkbox('Metal',value=True, key=1555253)
#           pop = col6.checkbox('Pop',value=True, key=1455255)  
#           rnb = col7.checkbox('R&B',value=True, key=155255)    
#           rock = col8.checkbox('Rock',value=True, key=1652555) 
#           videogame = col9.checkbox('Video game music',value=True, key=125557) 



#       check_box_booleans_graph_2 = [classical,edm,folk,hiphop,metal,pop,rnb,rock,videogame]        
#       genres = ['Classical','EDM','Folk','Hip hop','Metal','Pop','R&B','Rock','Video game music'] 
#       to_show_graph2 =[]
#       for i in range(len(genres)):
#           if check_box_booleans_graph_2[i]:
#               to_show_graph2.append(genres[i])
 

#       to_show_df_graph2 = df[df["Favorite Genre"].isin(to_show_graph2)]

    
    
#       Anxiety = px.scatter(to_show_df_graph2,x="Hours per day", y = 'Anxiety',
#                         color="Favorite Genre",
#                         title="Hours per day Vs. Anxiety",
#                         color_discrete_map = color_map_graphs12)
#       Depression = px.scatter(to_show_df_graph2,x="Hours per day", y = 'Depression',
#                         color="Favorite Genre",
#                         title="Hours per day Vs. Depression",
#                         color_discrete_map = color_map_graphs12)
#       Insomnia = px.scatter(to_show_df_graph2,x="Hours per day", y = 'Insomnia',
#                         color="Favorite Genre",
#                         title="Hours per day Vs. Insomnia",
#                         color_discrete_map = color_map_graphs12)
#       OCD = px.scatter(to_show_df_graph2,x="Hours per day", y = 'OCD',
#                         color="Favorite Genre",
#                         title="Hours per day Vs. OCD",
#                         color_discrete_map = color_map_graphs12)

#       graphs = [Anxiety, Depression, Insomnia, OCD]
#       for g in graphs:
#         g.update_xaxes(range=[-0.5, 24.5], tickmode='linear', dtick=2)  
#         g.update_xaxes(title_font=dict(size=20), tickfont=dict(size=14))
#         g.update_yaxes(title_font=dict(size=20), tickfont=dict(size=14))
#         for trace in g.data:
#             trace.update(marker=dict(size=10, opacity=0.7))
#       if graphs_amount == 0:
#           pass
    
#       elif graphs_amount == 1:
#           for i in range(len(list_of_trues)):
#               if list_of_trues[i]:
#                   st.plotly_chart(graphs[i], use_container_width=True)
                
#       elif graphs_amount == 2:
#            col1, col2 = st.columns(2, gap="large")
#            g1_idx = true_indices[0]
#            g2_idx = true_indices[1]
#            with col1:
#               st.plotly_chart(graphs[g1_idx], use_container_width=False)
#            with col2:
#               st.plotly_chart(graphs[g2_idx], use_container_width=False)
#       elif graphs_amount == 3:
#            col1, col2 = st.columns(2, gap="large")
#            g1_idx = true_indices[0]
#            g2_idx = true_indices[1]
#            g3_idx = true_indices[2]
#            with col1:
#               st.plotly_chart(graphs[g1_idx], use_container_width=False)
#            with col2:
#               st.plotly_chart(graphs[g2_idx], use_container_width=False)
#            col3, _ = st.columns(2, gap="large")
#            with col3:
#               st.plotly_chart(graphs[g3_idx], use_container_width=False)

#       elif graphs_amount == 4:
#           col1, col2 = st.columns(2, gap="large")

#           with col1:
#               st.plotly_chart(graphs[0], use_container_width=False)
#           with col2:
#               st.plotly_chart(graphs[1], use_container_width=False)
            
#           col3, col4 = st.columns(2, gap="large")
#           with col3:
#               st.plotly_chart(graphs[2], use_container_width=False)   
#           with col4:
#               st.plotly_chart(graphs[3], use_container_width=False)   


# elif comparison == 'Average':
    
#     bool_genres2 = st.radio("Please choose view method for genres:",['I prefer to choose the genres manually','Select all genres'],key=77229)
#     if bool_genres2=='I prefer to choose the genres manually':
#         with st.container():
#           col1, col2, col3, col4,col5, col6, col7, col8 ,col9 = st.columns(9)
#           classical = col1.checkbox('Classical', key=943)
#           edm = col2.checkbox('EDM', key=13340)
#           folk = col3.checkbox('Folk', key=13431)    
#           hiphop = col4.checkbox('Hip hop', key=14332) 
#           metal = col5.checkbox('Metal', key=133433)
#           pop = col6.checkbox('Pop', key=14334)  
#           rnb = col7.checkbox('R&B', key=13435)    
#           rock = col8.checkbox('Rock', key=3343333) 
#           videogame = col9.checkbox('Video game music', key=14337) 
#     elif bool_genres2=='Select all genres':
#         with st.container():
#           col1, col2, col3, col4,col5, col6, col7, col8 ,col9 = st.columns(9)
#           classical = col1.checkbox('Classical',value=True, key=956543355)
#           edm = col2.checkbox('EDM',value=True, key=10534355)
#           folk = col3.checkbox('Folk',value=True, key=15545331)    
#           hiphop = col4.checkbox('Hip hop',value=True, key=333334333333333333) 
#           metal = col5.checkbox('Metal',value=True, key=1555335543)
#           pop = col6.checkbox('Pop',value=True, key=1453335455)  
#           rnb = col7.checkbox('R&B',value=True, key=155533435)    
#           rock = col8.checkbox('Rock',value=True, key=1655343355) 
#           videogame = col9.checkbox('Video game music',value=True, key=15334557) 
#     check_box_booleans_graph_2 = [classical,edm,folk,hiphop,metal,pop,rnb,rock,videogame]        
#     genres = ['Classical','EDM','Folk','Hip hop','Metal','Pop','R&B','Rock','Video game music'] 
#     to_show_graph2 =[]
#     for i in range(len(genres)):
#         if check_box_booleans_graph_2[i]:
#             to_show_graph2.append(genres[i])
 

#     to_show_df_graph22 = df[df["Favorite Genre"].isin(to_show_graph2)]
#     g = px.scatter(to_show_df_graph22, x="Hours per day", y="Average Score",
#                          color="Favorite Genre",
#                          title="Hours per day Vs. Average of scores",
#                         color_discrete_map = color_map_graphs12)
#     for trace in g.data:
#         trace.update(marker=dict(size=10, opacity=0.7))
#     g.update_layout(yaxis_title='Average of Mental Health Scores')
#     g.update_xaxes(range=[-0.5, 24.5], tickmode='linear', dtick=1)
#     g.update_xaxes(title_font=dict(size=20), tickfont=dict(size=14))
#     g.update_yaxes(title_font=dict(size=20), tickfont=dict(size=14))

#     st.plotly_chart(g, use_container_width=True)#fix this


# st.markdown("---") 
  
  
  
  
  
# ##################################### Third Graph #####################################

# st.subheader('Genres & Mental Health Scores, by Mental Health Disorder - Histogram')
# order = st.radio("Which type of view would you prefer?",['Overall view (Compare all 4 disorders)','Specific view (Zoom in on one disorder)'],key=40000)
# if order != 'Overall view (Compare all 4 disorders)':
#   disorder = st.radio("Please choose disorder to view:",['Anxiety','Depression','Insomnia','OCD'],key=40001)
  
# st.text("Would you like to view all Genres at once?")
# select_all = st.radio("Choose one of: ",['Yes please.','No, I will choose myself.'])
# if select_all == 'Yes please.': 
#   with st.container():
#       col1, col2, col3, col4,col5, col6, col7, col8 ,col9 = st.columns(9)
#       classical = col1.checkbox('Classical',value=True, key=9999699)
#       edm = col2.checkbox('EDM',value=True, key=10999999)
#       folk = col3.checkbox('Folk',value=True, key=11999999)    
#       hiphop = col4.checkbox('Hip hop',value=True, key=12999999) 
#       metal = col5.checkbox('Metal',value=True, key=139999999)
#       pop = col6.checkbox('Pop',value=True, key=1499999)
#       rnb = col7.checkbox('R&B',value=True, key=159999999)    
#       rock = col8.checkbox('Rock',value=True, key=16999999) 
#       videogame = col9.checkbox('Video game music',value=True, key=17999999) 
# else:
#   with st.container():
#       col1, col2, col3, col4,col5, col6, col7, col8 ,col9 = st.columns(9)
#       classical = col1.checkbox('Classical', key=97777777777)
#       edm = col2.checkbox('EDM', key=1077777777)
#       folk = col3.checkbox('Folk', key=117777777777)    
#       hiphop = col4.checkbox('Hip hop', key=12777777) 
#       metal = col5.checkbox('Metal', key=1377777777)
#       pop = col6.checkbox('Pop', key=14777777777)
#       rnb = col7.checkbox('R&B', key=159595)    
#       rock = col8.checkbox('Rock', key=1677777777) 
#       videogame = col9.checkbox('Video game music', key=7777777717) 

# check_box_booleans = [classical,edm,folk,hiphop,metal,pop,rnb,rock,videogame]        
# genres = ['Classical','EDM','Folk','Hip hop','Metal','Pop','R&B','Rock','Video game music'] 
# to_show =[]
# for i in range(len(genres)):
#     if check_box_booleans[i]:
#         to_show.append(genres[i])
 

# to_show_df = third_graph_df[third_graph_df["Genre"].isin(to_show)]


# if order == 'Overall view (Compare all 4 disorders)':
#     third_graph_fig1 = px.histogram(to_show_df, x="Genre", y='Average Score',
#                color='Mental Disorder', barmode='group',
#                histfunc='avg',
#                height=400,
#                color_discrete_map=color_map_graph3)
#     third_graph_fig1.update_layout(title="Histogram ordered Alphabetically",
#                                  xaxis=dict(
#                                          tickfont=dict(size=17),  # Set font size for x-axis tick numbers
#                                          title=dict(text="Favorite Genre",font=dict(size=20))  # Set font size for x-axis label
#                                           ),
#                                  yaxis=dict(
#                                          tickfont=dict(size=17),  # Set font size for y-axis tick numbers
#                                          title=dict(text="Mental Health Score", font=dict(size=20))  # Set font size for y-axis label
#                                           ))
#     st.plotly_chart(third_graph_fig1, use_container_width=True)


# elif order != 'Overall view (Compare all 4 disorders)':
  
#   disorder_df = to_show_df[to_show_df['Mental Disorder']==disorder]
#   third_graph_fig1 = px.histogram(disorder_df, x="Genre", y='Average Score',
#                barmode='group',
#                histfunc='avg',
#                height=400,
#                color_discrete_map=color_map_graph3)
#   third_graph_fig1.update_layout(title=f'Histogram ordered by {disorder} Score',
#                                  xaxis=dict(
#                                          tickfont=dict(size=17),  # Set font size for x-axis tick numbers
#                                          title=dict(text="Favorite Genre",font=dict(size=20))  # Set font size for x-axis label
#                                           ),
#                                  yaxis=dict(
#                                          tickfont=dict(size=17),  # Set font size for y-axis tick numbers
#                                          title=dict(text="Mental Health Score", font=dict(size=20))  # Set font size for y-axis label
#                                           ))
  
#   third_graph_fig1.update_xaxes(categoryorder="total descending")
#   st.plotly_chart(third_graph_fig1, use_container_width=False)










# st.markdown("---") 
# ##################################### Fourth Graph #####################################

# st.subheader('Hours of listening per day & Genres, Aggregating Mental Health Scores - Heatmap')

# hours_bins_order = ["[0-2]","(2-3]","(3-4]","(4-24]"]
# df["Hours bins"] = pd.Categorical(df["Hours bins"], categories=hours_bins_order, ordered=True)

# df_avg = df.groupby(["Hours bins", "Favorite Genre"]).mean().reset_index()
# df_avg['Average Score'] = df_avg['Average Score'].apply(lambda x: round(x, 2))
# fourth_graph_fig1 = px.density_heatmap(df_avg, x="Favorite Genre", y="Hours bins", z="Average Score",
#                          labels=dict(x="Favorite Genre", y="Hours Bins", z="Average Score"),
#                          text_auto ="Average Score",
#                          color_continuous_scale=cmap_graph_4
#                                       )
                                      
# fourth_graph_fig1.update_layout(title="Average Mental Health Score by Hours Bins and Favorite Genre",
#                                xaxis=dict(
#                                        tickfont=dict(size=17),  # Set font size for x-axis tick numbers
#                                        title=dict(text="Favorite Genre",font=dict(size=20))  # Set font size for x-axis label
#                                         ),
#                                yaxis=dict(
#                                        tickfont=dict(size=17),  # Set font size for y-axis tick numbers
#                                        title=dict(text="Hours of listening (Daily)", font=dict(size=20))  # Set font size for y-axis label
#                                         ),
#                                coloraxis=dict(
#                                       colorbar=dict(
#                                             title="Mental Health Average Score",
#                                             titleside="top",
#                                             titlefont=dict(size=15),
#                                             tickfont=dict(size=15))
#                                               ),
#                                 font=dict(
#                                       size=32  # Set the font size here
#                                           )
#                                  )

# #fourth_graph_fig1.update_layout(uniformtext_minsize=20, uniformtext_mode='hide')      
# st.plotly_chart(fourth_graph_fig1, use_container_width=True)
# st.text("""
# Note - the brackets we use indicate whether or not the number
# near the bracket is included in the bin. Exmaple: (2,3] means 2 < x <= 3
# """)


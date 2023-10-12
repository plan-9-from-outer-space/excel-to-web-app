import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image

st.set_page_config(page_title='Survey Results')
st.header(':robot_face: Survey Results 2021')

### --- LOAD DATAFRAME
excel_file = 'Survey_Results.xlsx'
sheet_name = 'DATA'

df = pd.read_excel(
        io = excel_file,
        sheet_name = sheet_name,
        usecols = 'B:D',
        header = 3)

df_participants = pd.read_excel(
        io = excel_file,
        sheet_name = sheet_name,
        usecols = 'F:G',
        header = 3)
df_participants.dropna(inplace=True)

# --- STREAMLIT SELECTION
departments = df['Department'].unique().tolist()
ages = df['Age'].unique().tolist()

# st.dataframe(df)

age_selection = st.slider(label = 'Age:',
                        min_value = min(ages),
                        max_value = max(ages),
                        value = (min(ages), max(ages)))
# print(age_selection)

department_selection = st.multiselect(label = 'Department:',
                                    options = departments,
                                    default = departments)
# print(department_selection)

# --- FILTER DATAFRAME BASED ON SELECTIONS
# age_selection = (23, 65)
# department_selection = ['Marketing', 'Logistic', 'Purchasing', 'Sales', 'Finance']
# combined filters into a mask
mask = (df['Age'].between(*age_selection)) & (df['Department'].isin(department_selection))
number_of_result = df[mask].shape[0]
st.markdown(f'*Available Rows: {number_of_result}*')

# --- GROUP DATAFRAME AFTER SELECTION
df_grouped = df[mask].groupby(by=['Rating']).count()[['Age']]
df_grouped = df_grouped.rename(columns={'Age': 'Votes'})
df_grouped = df_grouped.reset_index()

# --- PLOT BAR CHART
bar_chart = px.bar(data_frame = df_grouped,
                   x='Rating',
                   y='Votes',
                   text='Votes',
                   color_discrete_sequence = ['#F63366'] * len(df_grouped),
                   template= 'plotly_white')
st.plotly_chart(bar_chart)

# --- DISPLAY IMAGE & DATAFRAME
col1, col2 = st.columns(2)
image = Image.open('images/survey.jpg')
col1.image(
        image = image,
        caption = 'Designed by slidesgo / Freepik',
        use_column_width = True)
col2.dataframe(df[mask])

# --- PLOT PIE CHART
pie_chart = px.pie(
        data_frame = df_participants,
        title = 'Total Number of Participants',
        values = 'Participants',
        names = 'Departments')
st.plotly_chart(pie_chart)

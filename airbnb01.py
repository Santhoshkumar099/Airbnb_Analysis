import pandas as pd
from PIL import Image
import streamlit as st
import plotly.express as px
from matplotlib import pyplot as plt
from streamlit_option_menu import option_menu
import pygwalker as pyg
from pygwalker.api.streamlit import StreamlitRenderer

# - - - - - - - - - - - - - - -set st addbar page - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
st.set_page_config(page_title="Airbnb",
                    page_icon="F:/IT Field/Python01/MDTM20/Project03/ICN.webp",
                    layout="wide")

df=pd.read_csv("F:/IT Field/Python01/MDTM20/Project03/airbnbproject.csv")

st.sidebar.image("F:/IT Field/Python01/MDTM20/Project03/Img.jpg",caption="Hotel booking")

with st.sidebar:
    selected = option_menu("Menu", ["🏠Home","🗺 Search","🌍Explore","📊Insights","🌟Pyg","❗About"],
                menu_icon= "menu-button-wide",
                default_index=0,
                styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#FF5A5F"},
                        "nav-link-selected": {"background-color": "#FF5A5F"}})


#menu Home
if selected=="🏠Home":
    col1,col2=st.columns([2,3],gap="small")
    with col1:
        st.image("F:/IT Field/Python01/MDTM20/Project03/HOME1.png")
        st.markdown("###### :white Airbnb was born in 2007 when two hosts welcomed three guests to their San Francisco home, and has since grown to over 5 million hosts who have welcomed over 1.5 billion guest arrivals in almost every country across the globe. Every day, hosts offer unique stays and experiences that make it possible for guests to connect with communities in a more authentic way.")

    with col2:
        st.video("https://www.youtube.com/watch?v=zgFoS3Kyt2E")

        st.write("")
        st.write("")
        st.write("")

    
    st.image("F:/IT Field/Python01/MDTM20/Project03/BG02.jpg")
    
    st.image("F:/IT Field/Python01/MDTM20/Project03/Home 1.jpg")

if selected=="🗺 Search":
    #Switcher
    st.sidebar.header("Please Filter")
    region=st.sidebar.multiselect(
        "Select Country",
        options=df["Country"].unique().tolist()
    )
    Location=st.sidebar.multiselect(
        "Select Location",
        options=df["Market"].unique().tolist()
    )

    df_selection=df.query(
        "Country == @region & Market == @Location"
        )

    try:
        
        a=df_selection["Rating"]/10
        average_rating=round(a.mean(),1)
        star_rating=":star:" * int(round(average_rating,0))

        c1,c2=st.columns(2)
        with c1:
            st.subheader("Average Rating")
            st.subheader(f"{average_rating} {star_rating}")
    except:
        st.write("Select the correct Location")


    df.groupby(by=['Name']).sum()[['Prize']].sort_values(by='Prize')


    a=df_selection[['Name','Rating','Prize']]
    sorted_value=a.sort_values(by=['Rating','Name'],ascending=[False,True])
    filtered_value=sorted_value.head(10)


    fig = px.pie(filtered_value, values='Rating',
                                    names='Name',
                                    title='Top 10 Hotels',
                                    color_discrete_sequence=px.colors.sequential.Agsunset,
                                    hover_data=['Prize'],
                                    labels={'Prize':'Prize'})

    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig,use_container_width=True)
    st.write('')

    try:
        selected_hotel=st.selectbox("Select the Hotel",options=df_selection['Name'].tolist(),index=None)
        
        filtered_df = df[df['Name'] == selected_hotel]
        c1,c2=st.columns(2)

        with c1:
            st.subheader(f"Details of {selected_hotel}")
            st.image(filtered_df['Images'].values[0], caption=filtered_df['Name'].values[0],width=300)
            st.write(f"**Price:** ${filtered_df['Prize'].values[0]}")
            st.write(f"**:green[Listing URL]:** {filtered_df['Url'].values[0]}")
            st.write(f"**:green[Description]:** {filtered_df['Description'].values[0]}")
            st.write(f"**:green[Room Type]:** {filtered_df['Room_type'].values[0]}")
            st.write(f"**:green[Bed Type]:** {filtered_df['Room_type'].values[0]}")
            st.write(f"**:green[Bedrooms]:** {filtered_df['Bedrooms'].values[0]}")
            st.write(f"**:green[Beds]:** {filtered_df['Beds'].values[0]}")
            
            
        with c2:
            st.write("")
            st.write("")
            st.image("F:/IT Field/Python01/MDTM20/Project03/BG02.jpg",width=550)
            #st.write('<div style="height: 300px;"></div>', unsafe_allow_html=True)
            st.write(f"**:green[Neighborhood overview]:** {filtered_df['Neighborhood_overview'].values[0]}")
            st.write(f"**:green[House Rules]:** {filtered_df['House_rules'].values[0]}")
            st.write(f"**:green[Property Type]:** {filtered_df['Property_type'].values[0]}")   
            st.write(f"**:green[Amenities]:** {filtered_df['Amenities'].values[0]}")               
            st.write(f"**:green[Minimum Nights]:** {filtered_df['Min_nights'].values[0]}") 
            st.write(f"**:green[Maximum Nights]:** {filtered_df['Max_nights'].values[0]}") 
            

        c1,c2=st.columns(2)
        with c1:
            st.subheader("Host Details")
            st.write(f"**Host Name:** {filtered_df['Host_name'].values[0]}")
            st.image(filtered_df['Host_pic_url'].values[0], caption=filtered_df['Host_name'].values[0])
            st.write(f"**Host ID:** {filtered_df['Host_id'].values[0]}")
            st.write(f"**Host URL:** {filtered_df['Host_url'].values[0]}")
            st.write(f"**Host Location:** {filtered_df['Host_location'].values[0]}")
            st.write(f"**About Host:** {filtered_df['Host_about'].values[0]}")
            st.write(f"**Host Response:** {filtered_df['Host_response'].values[0]}")

        with c2:
            st.image("F:/IT Field/Python01/MDTM20/Project03/col1.jpeg",width=600)
    except:
        st.write(f"<span style='color:#FF0000'>{"Please select  the hotel name"}</span>", unsafe_allow_html=True)



if selected =="📊Insights":
    opt=   ['Top 10 Hotels with Highest Price',
            'Top 10 Hotels with Lowest Price',
            'Price Based on Host Neighbourhood',
            'Average price on Host Neighbourhood',
            'Top 10 Countries with the Most Listings']
    
    question=st.selectbox(':red[Select the question]',options=opt,index=None)

    if question==opt[0]:
        sorted_df = df.sort_values(by='Prize', ascending=False)
        aa = sorted_df.head(10)
        aa=aa[['Name','Country','Prize']]

        # Plotting a sunburst chart with Plotly
        fig = px.sunburst(aa, 
                        path=['Country', 'Name'], 
                        values='Prize', 
                        title='Top 10 Most Expensive Accommodations',
                        color_continuous_scale='RdBu',
                        hover_data=['Prize'],
                        labels={'Country': 'Country', 'Name': 'Name', 'Prize': 'Prize'})

        # Displaying the sunburst chart in Streamlit
        st.plotly_chart(fig)

        # Plotting an interactive pie chart with Plotly
        fig = px.pie(aa, 
                    values='Prize', 
                    names='Name', 
                    title='Top 10 Most Expensive Accommodations',
                    hover_data=['Country', 'Prize'],
                    labels={'Name': 'Hotel', 'Country': 'Country', 'Prize': 'Prize'})
        # Displaying the pie chart in Streamlit
        st.plotly_chart(fig)


    elif question==opt[1]:
        sorted_df = df.sort_values(by='Prize', ascending=True)
        aa = sorted_df.head(10)
        aa=aa[['Name','Country','Prize']]

        # Plotting a sunburst chart with Plotly
        fig = px.sunburst(aa, 
                        path=['Country', 'Name'], 
                        values='Prize', 
                        title='Top 10 Most Expensive Accommodations',
                        color_continuous_scale='RdBu',
                        hover_data=['Prize'],
                        labels={'Country': 'Country', 'Name': 'Name', 'Prize': 'Prize'})

        # Displaying the sunburst chart in Streamlit
        st.plotly_chart(fig)

        # Plotting an interactive pie chart with Plotly
        fig = px.pie(aa, 
                    values='Prize', 
                    names='Name', 
                    title='Top 10 Most Expensive Accommodations',
                    hover_data=['Country', 'Prize'],
                    labels={'Name': 'Hotel', 'Country': 'Country', 'Prize': 'Prize'})
        # Displaying the pie chart in Streamlit
        st.plotly_chart(fig)

    elif question==opt[2]:
        c_t = df["Country"].unique()[0]
        df_c_t = df[df["Country"] == c_t]
        df_c_t_sorted = df_c_t.sort_values(by="Prize")
        df_p_n = pd.DataFrame(df_c_t_sorted.groupby("Host_neighbour")["Prize"].agg(["sum", "mean"])).reset_index()
        df_p_n.columns = ["Host_neighbourhood", "Total_price", "Average_price"]
        fig = px.bar(df_p_n, 
                        x="Total_price", 
                        y="Host_neighbourhood", 
                        orientation='h',
                        title="PRICE BASED ON HOST_NEIGHBOURHOOD", 
                        width=600, height=800)
        st.plotly_chart(fig)

    elif question==opt[3]:
        c_t = df["Country"].unique()[0]
        df_c_t = df[df["Country"] == c_t]
        df_c_t_sorted = df_c_t.sort_values(by="Prize")
        df_p_n = pd.DataFrame(df_c_t_sorted.groupby("Host_neighbour")["Prize"].agg(["sum", "mean"])).reset_index()
        df_p_n.columns = ["Host_neighbourhood", "Total_price", "Average_price"]

        fig = px.bar(df_p_n, 
                        x="Average_price", 
                        y="Host_neighbourhood", 
                        orientation='h',
                        title="AVERAGE PRICE BASED ON HOST_NEIGHBOURHOOD", 
                        width=600, height=800)
        st.plotly_chart(fig)
        
    elif question==opt[4]:
        country_listings_count = df['Country'].value_counts()

        # Selecting the top 10 countries with the most listings
        top_10_countries = country_listings_count.head(10)

        # Streamlit application
        st.title('Top 10 Countries with the Most Listings')

        # Creating a bar chart
        fig, ax = plt.subplots(figsize=(3,2))
        top_10_countries.plot(kind='bar', ax=ax)

        # Adding labels and title
        plt.xlabel('Country')
        plt.ylabel('Number of Listings')

        # Displaying the bar chart in Streamlit
        st.pyplot(fig)   






if selected == "🌍Explore":
    tab1, tab2= st.tabs([ "Geospatial Visualization", "Geo Visual"])

    with tab1:
        st.title("Geospatial Visualization")
        st.write("")
        fig = px.scatter_mapbox(df,lat='Latitude', lon='Longitude', color='Prize', size='Accomodates',
                        color_continuous_scale= "rainbow",hover_name='Name',
                        hover_data={'Longitude':False,'Latitude':False, 'Prize': True},
                        range_color=(0,49000),
                        mapbox_style="carto-positron",
                        zoom=1)
        fig.update_layout(width=1150,height=800,title='Geospatial Distribution of Listings')
        st.plotly_chart(fig)

    with tab2:
        selected_country = st.selectbox('Select a country', df['Country'].unique())
        # Filter data based on the selected country
        filtered_df = df[df['Country'] == selected_country]

        # Plotting the data on a scatter mapbox
        fig = px.scatter_mapbox(
            filtered_df,
            lat=filtered_df['Latitude'],
            lon=filtered_df['Longitude'],
            hover_name="Name",
            hover_data={"Country": False, "Name": True, "Prize": True, "Longitude":False,"Latitude":False},
            #color=filtered_df["Prize"],  # This will color the points based on the price
            zoom=8,
            height=600
        )

        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

        # Display the plot in Streamlit
        st.plotly_chart(fig,use_container_width=True)


if selected == "🌟Pyg":   

    df1=pd.read_csv("F:/IT Field/Python01/MDTM20/Project03/airbnbproject02.csv")
    pyg_app = StreamlitRenderer(df1)
    pyg_app.explorer()


if selected == "❗About":
        col1,col2=st.columns(2)
        with col1:
            st.subheader(':red[What is Airbnb ?]')
            st.markdown('''Airbnb is an online marketplace that connects people who want to rent out their 
                        homes or spare rooms with those who are looking for accommodations. Founded in 2008, 
                        Airbnb has grown to become a significant player in the hospitality industry, 
                        offering a wide range of lodging options around the world.''')
            st.link_button('AIRBNB WEBSITE',url='https://www.airbnb.co.in/')

        with col2:
            st.video('https://www.youtube.com/watch?v=dA2F0qScxrI&list=PLe_YVMnS1oXZb4zCNsh_fRqXh5kgx21V_')

        st.subheader(':red[FAQ]')


        with st.expander('**What is the concept of Airbnb?**'):
            st.write('''Airbnb (ABNB) is an online marketplace that connects people who want to rent out 
                    their homes with people looking for accommodations in specific locales''')
            
        with st.expander('**How does Airbnb make money?**'):
            st.write(''' The company operates in over 200 countries and has 6.6 million listings. 
                    The company charges its host and guests a percentage in fees to earn revenues''')

        with st.expander('**Who is CEO of Airbnb?**'):
            st.image('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQms4guS1SX_UTgYEEwbCWy9HQutO7HUGmr8cUwVdXsBw&s',width=100)
            st.write('''Brian Chesky is the co-founder and Chief Executive Officer of Airbnb and sets the vision and strategy for the company.''')
                

        with st.expander('**Is Airbnb legal in India?**'):
            st.write('''Yes, Airbnb is legal in India as long as you have all the required licenses 
                    and permissions to start one.
                    In India, there are several legal registrations required before hosting on Airbnb. 
                    Firstly, you must register your property with the local
                    municipality and obtain a valid license to operate as an accommodation provider.''')
            
        
            
        
        with st.expander('**What type of hotel is Airbnb?**'):
            st.write('''an Airbnb can be anything from a hotel, to a quaint B&B, to a treehouse, to a tent, 
                    to an igloo, to a church, the list goes on… What makes 
                    an Airbnb property popular with guests is how special and unique it is able to be, 
                    and this doesn't have to rely solely on the architecture (or lack thereof)''')
            
        
        st.header('Personal Information')
        Name = (f'{"Name :"}  {"Santhosh Kumar M"}')
        mail = (f'{"Mail :"}  {"sksanthoshhkumar99@gmail.com"}')
        st.markdown(Name)
        st.markdown(mail)
        c1,c2=st.columns(2)
        with c1:
            if st.button('Show Github Profile'):
                st.markdown('[Click here to visit github](https://github.com/Santhoshkumar099)')

        with c2:
            if st.button('Show Linkedin Profile'):
                st.markdown('[Click here to visit linkedin](https://www.linkedin.com/in/santhosh-kumar-2040ab188/)')

        github = (f'{"Github :"}  {"https://github.com/Santhoshkumar099"}')
        linkedin = (f'{"LinkedIn :"}  {""}')
        description = "An Aspiring DATA-SCIENTIST..!"

        st.markdown("This project is done by Santhosh Kumar M")






















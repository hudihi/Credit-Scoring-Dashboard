import streamlit as st
import pageOne
import main

# Add title and introduction
st.set_page_config(
    page_title="Loan Dashboard",
    page_icon=":bar_chart:",
    layout="wide"
)
# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Welcome", "Visualization", "Prediction"])

# Navigation logic
if page == "Welcome":
    st.header("📊 Loan Dashboard: Empowering Financial Decisions")
    st.markdown("<h1 style='font-size:24px; font-weight:normal; font-style:italic;'>"
                "In today’s fast-changing financial world, it's important to stay ahead by "
                "understanding your loan data and spotting risks early. Our Loan Dashboard gives "
                " you easy-to-understand insights into how loans are performing and helps predict "
                "future issues using advanced technology. With simple and clear visuals, you can track "
                "and analyze loans in real time, whether you're handling many loans or just one."
                " This tool helps you make smart, informed decisions, manage risks, and improve your "
                "loan management."
                "</h1>",
                unsafe_allow_html=True
                )
    image_url = "loan.png"
    st.image(image_url, caption="Image for FinScope 2018 survey ", use_column_width=True)
elif page == "Visualization":
    st.header("📊 Loan Dashboard: Empowering Financial Decisions")
    main.show()  # Call the show function from page1.py
elif page == "Prediction":
    pageOne.show()  # Call the show function from page2.py

import pandas as pd
import streamlit as st
import pickle
import time


def show():
    # Load the trained model and scaler
    with open('SVM1.pkl', 'rb') as f:
        model = pickle.load(f)

    with open('scaler_poject3.pkl', 'rb') as scale_file:
        scale = pickle.load(scale_file)

    product_category_mapping = {
        'Airtime': 1,
        'Data bundle': 2,
        'financial service':3,
        'movie' : 4,
        'retail' : 5,
        'TV': 6,
        'Utility bill': 7
    }

    payback = {
        'no': 0,
        'yes': 1
    }

    # Streamlit app layout
    st.title("Credit Default Prediction for E-Commerce Client")

    col1, col2, col3 = st.columns(3)

    # Collect user input
    with col1:
        product_category = st.selectbox("Product Category", list(product_category_mapping.keys()))

    with col2:
        isfinalpayback = st.selectbox("Is it the last payback installment", list(payback.keys()))

    with col3:
        # Input to accept a number of entries (Avoiding multiple widgets with the same key)
        num = st.number_input("How many installments done?", min_value=1, max_value=10, step=1, key='num_input')

    # Initialize session state to store entries
    if 'entries' not in st.session_state:
        st.session_state.entries = []

    # Dynamically create value, Amount, and date fields based on the number of entries
    if num:
        if len(st.session_state.entries) != num:
            st.session_state.entries = [
                {"Value": None, "AmountLoan": None, "date1": None, "date2": None,
                 "ProductCategory": None, "IsFinalPayBack": None, "Number_Of_Split_Payments": None}
                for _ in range(num)]

        st.write("Enter details for each transaction:")

        for i in range(num):
            st.write(f"Transaction {i + 1}:")
            with st.container():
                entry_col1, entry_col2, entry_col3 = st.columns(3)

                with entry_col1:
                    value = st.number_input(f"Amount with charge {i + 1}:", key=f'value_{i}')
                    amount = st.number_input(f"Transaction amount {i + 1}:", key=f'amount_{i}')

                with entry_col2:
                    date1 = st.date_input(f"PaidOnDate {i + 1}:", key=f'date1_{i}')

                with entry_col3:
                    date2 = st.date_input(f"DueDate {i + 1}:", key=f'date2_{i}')

                # Update session state with user inputs
                st.session_state.entries[i] = {
                    "IsFinalPayBack": payback[isfinalpayback],
                    "ProductCategory": product_category_mapping[product_category],
                    "Number_Of_Split_Payments": num,  # Add num (total number of installments),
                    "AmountLoan": amount,
                    "Value": value,
                    "date1": date1,
                    "date2": date2,
                }

    # Display the results and allow for predictions after the form is submitted
    if st.button("Submit"):
        # Show splash message for successful submission
        success_message = st.success("Submission Successful!")

        # Sleep for 2 seconds
        time.sleep(2)

        # Clear the success message
        success_message.empty()

        df = pd.DataFrame(st.session_state.entries)
        df['date1'] = pd.to_datetime(df['date1'])
        df['date2'] = pd.to_datetime(df['date2'])

        # Calculate the difference in days between the two dates
        df['days_between'] = (df['date2'] - df['date1']).dt.days

        # Compute features based on the days_between
        df['before_due_mean'] = df['days_between'].mean()
        df['before_due_min'] = df['days_between'].min()
        df['before_due_max'] = df['days_between'].max()

        # Display the DataFrame with new features
        col = ['date1', 'date2', 'days_between']
        df = df.drop(col, axis='columns')

        st.session_state.df = df  # Store the DataFrame in session state
        st.dataframe(df)

        # Set the submission flag
        st.session_state.submitted = True

    # Show the Predict button if the form is submitted and DataFrame is available
    if st.session_state.get('submitted') and st.session_state.df is not None:
        if st.button("Predict"):
            # Get the DataFrame from session state
            df = st.session_state.df

            # Scale the input data
            input_data = scale.transform(df)

            # Make a prediction
            prediction = model.predict(input_data)

            # Display the prediction result
            if prediction[0] == 0:
                st.success("Prediction: Not Defaulted")
            else:
                st.error("Prediction: Defaulted")

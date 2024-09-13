import streamlit as st
import pandas as pd
import seaborn as sns
import pylab
import matplotlib.pyplot as plt


def show():
    data1 = pd.read_csv("bila_caro_tungeaibika.csv.")
    data2 = pd.read_csv('Data.csv')

    defLabel = {1: "Yes", 0: "No", 2: 'Applicant Rejected'}
    lastLabel = {1: "Yes", 0: "No", 2: 'Applicant Rejected'}
    thirdLabel = {1: "Yes", 0: "No", 2: 'Applicant Rejected'}
    prod = {

    }

    data1.IsDefaulted = data1.IsDefaulted.map(defLabel)
    data1.IsFinalPayBack = data1.IsFinalPayBack.map(lastLabel)
    data1.IsThirdPartyConfirmed = data1.IsThirdPartyConfirmed.map(thirdLabel)

    st.markdown("###")
    st.sidebar.title("Please filter here!")
    transaction = st.sidebar.multiselect(
        "Select the Transaction Status",
        options=data1['TransactionStatus'].unique(),
        default=data1['TransactionStatus'].unique()
    )

    default = st.sidebar.multiselect(
        "Select the Exceeded Agreed PayBack Time Status",
        options=data1['IsDefaulted'].unique(),
        default=data1['IsDefaulted'].unique()
    )

    backPay = st.sidebar.multiselect(
        "Select the Final Payment Back status",
        options=data1['IsFinalPayBack'].unique(),
        default=data1['IsFinalPayBack'].unique()
    )

    thirdPart = st.sidebar.multiselect(
        "Select the Loan Order Succeeded Status",
        options=data1["IsThirdPartyConfirmed"].unique(),
        default=data1['IsThirdPartyConfirmed'].unique()
    )

    df_selection = data1.query(
        "TransactionStatus == @transaction & IsDefaulted == @default & IsFinalPayBack == @backPay & "
        "IsThirdPartyConfirmed == @thirdPart"
    )

    # st.dataframe(df_selection)

    main_right, main_middle, main_left = st.columns(3)

    totalUsers = data1.TransactionStatus.count()
    acceptedUsers = data1[data1['TransactionStatus'].values == 'Accepted'].count().TransactionStatus
    rejectedUsers = data1[data1['TransactionStatus'].values == 'Rejected'].count().TransactionStatus
    print(acceptedUsers)
    print(rejectedUsers)
    with main_right:
        st.markdown(
            f"<span style=10px>Platform Users</span>",
            unsafe_allow_html=True
        )
        st.markdown(
            f"<span style=10px>No: {totalUsers}</span>",
            unsafe_allow_html=True
        )

    with main_middle:
        st.markdown(
            f"<span style=10px>Loan Accepted 😊</span>",
            unsafe_allow_html=True
        )
        st.markdown(
            f"<span style=10px>No:\t {acceptedUsers}</span>",
            unsafe_allow_html=True
        )

    with main_left:
        st.markdown(
            f"<span style=10px>Loan Rejected 😭</span>",
            unsafe_allow_html=True
        )
        st.markdown(
            f"<span style=10px>No: \t {rejectedUsers}</span>",
            unsafe_allow_html=True
        )

    st.markdown("---")

    cont1, cont2 = st.columns(2)

    with cont1:
        st.markdown(
            "<span style=20px>Exceeded Agreed PayBack Time \nStatus</span>",
            unsafe_allow_html=True
        )
        fig, ax = plt.subplots()
        plt.figure(figsize=(6, 6))
        sns.countplot(x="IsDefaulted", hue="IsDefaulted", data=df_selection, ax=ax,
                      )
        plt.xticks(
            fontweight='light',
            fontsize='x-large'
        )
        pylab.xlabel("Default")
        st.pyplot(fig)

        st.markdown(
            "<span style=20px>Loan Application Status</span>",
            unsafe_allow_html=True
        )
        fig, ax = plt.subplots()
        isDefaulted_counts = df_selection['IsDefaulted'].value_counts()
        plt.pie(isDefaulted_counts, labels=isDefaulted_counts.index, colors=['green', 'orange', 'cyan'],
                autopct='%1.1f%%',
                shadow=True)
        st.pyplot(fig)

        filtered_data = df_selection[df_selection['IsDefaulted'].isin(['No', 'Yes'])]
        st.markdown(
            "<span style=20px>Exceeded PayBackTime Status vs Loan Issuer</span>",
            unsafe_allow_html=True
        )
        fig, ax = plt.subplots()
        sns.countplot(x='InvestorId', hue='IsDefaulted', data=filtered_data, ax=ax)
        st.pyplot(fig)

        # fig = ex.bar(df_selection, x="TransactionStatus", y="Value", title="Value of Loan vs Transaction Status")
        # st.pyplot(fig)


        st.markdown(
            f"<span style=20px>Exceeded PayBackTime Status vs Success in Loan Order</span>",
            unsafe_allow_html=True
        )
        fig, ax = plt.subplots()
        sns.countplot(x='IsThirdPartyConfirmed', hue='IsDefaulted', data=df_selection, ax=ax)
        st.pyplot(fig)

    with cont2:
        st.markdown(
            f"<span style=10px>Exceeded PayBackTime Status vs SubscriptionID</span>",
            unsafe_allow_html=True
        )
        fig, ax = plt.subplots()
        plt.figure(figsize=(6, 8))
        sns.countplot(x='SubscriptionId', hue='IsDefaulted', data=df_selection, ax=ax)
        st.pyplot(fig)

        st.markdown(
            f"<span style=10px>Exceeded PayBackTime Status vs Transaction Status</span>",
            unsafe_allow_html=True
        )
        fig, ax = plt.subplots()
        sns.countplot(x='TransactionStatus', hue='IsDefaulted', data=df_selection, ax=ax)
        st.pyplot(fig)

        st.markdown(
            f"<span style=10px>Exceeded PayBackTime Status vs Product Category</span>",
            unsafe_allow_html=True
        )
        fig, ax = plt.subplots()
        plt.figure(figsize=(6, 8))
        sns.countplot(x='ProductCategory', hue='IsDefaulted', data=df_selection, ax=ax)
        ax.set_xticklabels(ax.get_xticklabels(),rotation = 45, ha = 'right')
        st.pyplot(fig)

        st.markdown(
            f"<span style=10px>Exceeded PayBackTime Status vs Last PayBack Installment</span>",
            unsafe_allow_html=True
        )
        fig, ax = plt.subplots()
        sns.countplot(x='IsFinalPayBack', hue='IsDefaulted', data=df_selection, ax=ax)
        st.pyplot(fig)

    # fig, ax = plt.subplot()
    # plt.pie(df_selection.SubscriptionId.values.count(), labels=df_selection.IsDefault.values)
    # st.pyplot(fig)

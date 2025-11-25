import streamlit as st
import pandas as pd
import io
from datetime import datetime, timedelta

# ---------------------------------------------------------
#  HARD-CODED MAPPINGS
# ---------------------------------------------------------

normal_mapping = {
    "Internal ID": "internal_id",
    "Site Name": "site_name",
    "Site Address 1": "site_address_1",
    "Site Address 2": "site_address_2",
    "Site Post Code": "site_post_code",
    "Item to Order": "item_to_order",
    "Date of Visit": "date_of_visit",
    "Time of Visit": "time_of_visit",
    "Site Code": "site_code",
    "Primary Result": "primary_result",
    "Please detail why you were unable to conduct this audit:": "Please detail why you were unable to conduct this audit:",
    "What was the Operator number from the receipt?": "What was the Operator number from the receipt?",
    "From the top of the receipt, please enter the store name and any visible codes.": "From the top of the receipt, please enter the store name and any visible codes.",
    "What type of alcohol did you try to purchase?": "What type of alcohol did you try to purchase?",
    "Please give details of the product that you tried to purchase:": ["Please give details of the alcohol that you purchased:", "Please give details of the e-cig product that you tried to purchase:", "Please give details of the cigarettes that you tried to purchase:"],
    "How many people were in the queue?": "How many people were in the queue?",
    "At which type of till was the purchase made?": "At which type of till was the purchase made?",
    "Did you make the purchase on its own or as part of a larger shop?": "Did you make the purchase on its own or as part of a larger shop?",
    "Was there any generic 'Think 25' or 'Think 21' material visible from the till?": "Was there any generic 'Think 25' or 'Think 21' material visible from the till?",
    "Was the staff member who served you working entirely alone?": "Was the staff member who served you working entirely alone?",
    "Did the staff member who served you make eye contact with you during the transaction?": "Did the staff member who served you make eye contact with you during the transaction?",
    "When was eye contact first made?": "When was eye contact first made?",
    "Did the staff member who served you look at you long enough to assess your age?": "Did the staff member who served you look at you long enough to assess your age?  ",
    "Did the staff member who served you ask your age?": "Did the staff member who served you ask your age?",
    "Was the cabinet open before the staff member retrieved your cigarettes?": "Was the cabinet open before the staff member retrieved your cigarettes?",
    "Did the staff member who served you ask for ID?": "Did the staff member who served you ask for ID?",
    "Were you asked for ID before the cigarettes had been retrieved from the cabinet?": "Were you asked for ID before the cigarettes had been retrieved from the cabinet?",
    "If cigarettes were retrieved, was the cabinet shut immediately after the staff member had retrieved your cigarettes?": "If cigarettes were retrieved, was the cabinet shut immediately after the staff member had retrieved your cigarettes?",
    "Was a supervisor called at any point during the transaction?": "Was a supervisor called at any point during the transaction?",
    "Please use this space to explain anything unusual about your visit or to clarify any detail of your report:": "Please use this space to explain anything unusual about your visit or to clarify any detail of your report:",
}

rapid_mapping = {
    "Internal ID": "internal_id",
    "Site Name": "site_name",
    "Site Address 1": "site_address_1",
    "Site Address 2": "site_address_2",
    "Site Post Code": "site_post_code",
    "Item to Order": "item_to_order",
    "Date of Visit": "date_of_visit",
    "Time of Visit": "time_of_visit",
    "Site Code": "site_code",
    "Primary Result": "primary_result",
    "Please detail why you were unable to conduct this audit:": "Please detail why you were unable to conduct this audit:",
    "Please enter the order number from your online receipt:": "Please enter the order number from your online receipt:",
    "Please enter the date you placed your order:": "Please enter the date you placed your order:",
    "Please enter the time you placed your order:": "Please enter the time you placed your order:",
    "Please select the service provider used: ": "Please select the service provider used: ",
    "Please detail the store name you ordered it from:": "Please detail the store name you ordered it from:",
    "Please confirm the postcode of the store you ordered it from:": "Please confirm the postcode of the store you ordered it from:",
    "What is your age?": "What is your age?",
    "What was the total cost of your purchase? ": "What was the total cost of your purchase? ",
    "Please give details of the age restricted product(s) purchased:": "Please give details of the age restricted product(s) purchased:",
    "Did you order via the app or website?": "Did you order via the app or website?",
    "Please state the Co-op store name and address you ordered from:": "Please state the Co-op store name and address you ordered from:",
    "Was it easy to find the store on the app or website? ": "Was it easy to find the store on the app or website? ",
    "Was the app or website easy to use? ": "Was the app or website easy to use? ",
    "Was your order delivered within 30 minutes of placing the order?": "Was your order delivered within 30 minutes of placing the order?",
    "Did the driver ask your age?": "Did the driver ask your age?",
    "Did the driver ask you to enter your date of birth into a device?": "Did the driver ask you to enter your date of birth into a device?",
    "Did the driver ask for ID?": "Did the driver ask for ID?",
    "Were any of the items damaged?": "Were any of the items damaged?",
    "Were any of the items missing?": "Were any of the items missing?",
    "Please confirm what items were actually missing:": "Please confirm what items were actually missing:",
    "Did the delivery bag arrive sealed with a sticker / sealed by staples / bag was not sealed?": "Did the delivery bag arrive sealed with a sticker / sealed by staples / bag was not sealed?",
    "Did the delivery bag have a Think 25 or age restricted type sticker?": "Did the delivery bag have a Think 25 or age restricted type sticker?",
    "Was the delivery driver dressed in branded attire coinciding with the app/website used?": "Was the delivery driver dressed in branded attire coinciding with the app/website used?",
    "Did the driver make eye contact with you during the interaction? ": "Did the driver make eye contact with you during the interaction? ",
    "Was the driver friendly?": "Was the driver friendly?",
    "Based on your online shopping experience, please rate the service from 1 to 10 (where 1 is very poor and 10 is excellent): ": "Based on your online shopping experience, please rate the service from 1 to 10 (where 1 is very poor and 10 is excellent): ",
    "Please explain the reason for your score:": "Please explain the reason for your score:",
    "Based on your delivery experience, please rate your experience from 1 to 10 (where 1 is very poor and 10 is excellent): ": "Based on your delivery experience, please rate your experience from 1 to 10 (where 1 is very poor and 10 is excellent): ",
    "Were you able to order all items you wanted?": "Were you able to order all items you wanted?",
    "Was the item you wanted to order unavailable? ": "Was the item you wanted to order unavailable? ",
    "What was the item you were unable to order?": "What was the item you were unable to order?",
    "Please use this space to explain anything unusual about your visit or to clarify any detail of your report:": "Please use this space to explain anything unusual about your visit or to clarify any detail of your report:",
}

# ---------------------------------------------------------
#  HELPER FUNCTIONS
# ---------------------------------------------------------

def load_audits_from_upload(file):
    df = pd.read_csv(file, dtype=str)
    df["date_of_visit_parsed"] = pd.to_datetime(df["date_of_visit"], dayfirst=True, errors="coerce")
    df["_time_sort"] = pd.to_datetime(df["time_of_visit"], format="%H:%M", errors="coerce").dt.time
    return df

def filter_to_most_recent_saturday(df):
    df = df.sort_values(["date_of_visit_parsed", "_time_sort"], ascending=[True, True])
    today = datetime.now().date()
    weekday = today.weekday()
    days_since_sat = (weekday - 5) % 7
    most_recent_sat = today - timedelta(days=days_since_sat)
    mask = df["date_of_visit_parsed"].notna() & (df["date_of_visit_parsed"].dt.date <= most_recent_sat)
    return df.loc[mask].copy()

def split_by_type(df):
    rapid = df[df["item_to_order"] == "Rapid Delivery"].copy()
    normal = df[df["item_to_order"] != "Rapid Delivery"].copy()
    return normal, rapid

def build_output(df, mapping):
    out = pd.DataFrame()
    for report_col, csv_source in mapping.items():
        if isinstance(csv_source, list):
            merged = df[csv_source[0]].fillna("") if csv_source[0] in df.columns else pd.Series([""] * len(df))
            for c in csv_source[1:]:
                if c in df.columns:
                    merged = merged + " | " + df[c].fillna("")
            out[report_col] = merged.str.strip(" |")
        else:
            out[report_col] = df[csv_source] if csv_source in df.columns else ""
    return out

# ---------------------------------------------------------
#  STREAMLIT UI
# ---------------------------------------------------------

st.title("Co-op UK Report Mapper")

st.write("""
          1. Export the previous 2 weeks worth of Co-op data
          2. Drop the file in the box below – it’ll then give you the two Co-op output files
          3. Standard bits - Check data vs previous week, remove data already reported, add new data
          4. Done.
          """)

uploaded = st.file_uploader("Upload audits_basic_data_export.csv", type=["csv"])

if uploaded:
    df = load_audits_from_upload(uploaded)
    df = filter_to_most_recent_saturday(df)
    normal_df, rapid_df = split_by_type(df)

    normal_out = build_output(normal_df, normal_mapping)
    rapid_out = build_output(rapid_df, rapid_mapping)

    if "Site Post Code" in rapid_out.columns:
        rapid_out["Site Post Code"] = "-"

    normal_bytes = io.BytesIO()
    rapid_bytes = io.BytesIO()

    normal_out.to_csv(normal_bytes, index=False, encoding="utf-8-sig")
    rapid_out.to_csv(rapid_bytes, index=False, encoding="utf-8-sig")

    st.success("Files processed!")

    st.download_button("Download Normal Audit CSV", normal_bytes.getvalue(), "Co-op UK Report Data.csv", "text/csv")
    st.download_button("Download Rapid Delivery CSV", rapid_bytes.getvalue(), "Co-op UK Rapid Delivery Data.csv", "text/csv")

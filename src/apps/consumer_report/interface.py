import streamlit as st

from src.apps.consumer_report.job import make_consumer_report

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

st.title("Consumer Report Generator")
st.caption("A consumer report generator powered by OpenAI LLMs and made by Theo Bayard de Volo")

user_request = st.text_input("Consumer Report Request")

if user_request.strip() == "":
    user_request = None

consumer_report = None
if user_request:
    with st.spinner("Creating your report. This may take a few minutes..."):
        consumer_report = make_consumer_report(user_request)

if consumer_report:
    st.markdown(consumer_report['final_report'])

    st.markdown('## All products considered')
    for product_report in consumer_report['product_reports']:
        with st.expander(product_report['product_name']):
            st.markdown(f"## Review \n{product_report['general_comments']}")

            st.markdown("## Ratings")

            for rating in product_report['ratings']:
                st.markdown(f'- **{rating["rating_name"]}**: {rating["score"]}')


        


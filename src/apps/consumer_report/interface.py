from openai import OpenAI
import streamlit as st

from src.apps.consumer_report.job_update_handler import job_update_handler
from src.models import TextModel, CHAT_DEFAULT
from src.apps.consumer_report.job import ConsumerReportJobState, make_consumer_report

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

st.title("Consumer Report Generator")
st.caption("A consumer report generator powered by OpenAI LLMs and made by Theo Bayard de Volo")

if not openai_api_key:
    st.warning("Input your OpenAPI Key to use this app")

user_request = st.text_input("Consumer Report Request", disabled = not openai_api_key)

if user_request.strip() == "" or not openai_api_key:
    user_request = None

consumer_report_job_state = None
if user_request:
    consumer_report_job_state = ConsumerReportJobState(
        user_prompt=user_request,
        text_model=TextModel(
            CHAT_DEFAULT.tag,
            token_limit=CHAT_DEFAULT.token_limit,
            client=OpenAI(api_key=openai_api_key)
        ),
        on_update = job_update_handler
    )
    with st.status("Creating your consumer report...", expanded=True) as status:
        consumer_report = make_consumer_report(consumer_report_job_state)
        status.update(label="Consumer Report Created!", state="complete", expanded=False)

if consumer_report_job_state:
    st.markdown(consumer_report_job_state.final_report)

    st.markdown('## All products considered')
    for product_report in consumer_report_job_state.product_reports:
        with st.expander(product_report['product_name']):
            st.markdown(f"## Review \n{product_report['general_comments']}")

            st.markdown("## Ratings")

            for rating in product_report['ratings']:
                st.markdown(f'- **{rating["rating_name"]}**: {rating["score"]}')


        


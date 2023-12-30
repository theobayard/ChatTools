import json
from ...job.job_state import JobState
from . import tasks
from ...task.text_task import parse_chat_gpt_json

class ConsumerReportJobState(JobState):
    product_candidates: list[str]
    catagories: str
    product_reports: list[dict]
    final_report: str

def make_consumer_report(job_state: ConsumerReportJobState):
    job_state.current_task = "Find Product Candidates"
    product_candidates = job_state.text_model.simple_call(tasks.FIND_BEST_PRODUCT_CANDIDATES_TASK,
        job_state.user_prompt)
    product_candidates = product_candidates.split('|')
    job_state.product_candidates = product_candidates

    job_state.current_task = "Find Rating Catagories"
    catagories = job_state.text_model.simple_call(tasks.CREATE_RATING_CATAGORIES,
        job_state.user_prompt)
    job_state.catagories = catagories

    rating_requests = [
        create_rating_request(product, job_state.user_prompt, catagories) for product in product_candidates
    ]
    product_reports = []
    for rating_request, product in zip(rating_requests, product_candidates):
        job_state.current_task = f"Creating Product Report for {product}"

        raw_product_report = job_state.text_model.simple_call(tasks.RESEARCH_PRODUCT,rating_request)
        parsed_product_report = parse_chat_gpt_json(raw_product_report)
        
        product_reports.append(parsed_product_report)
        job_state.product_reports = product_reports

    job_state.current_task = "Making Final Report"
    final_report_request = {
        'user_request': job_state.user_prompt,
        'product_reports': product_reports,
    }
    final_report = job_state.text_model.simple_call(tasks.FINAL_RECOMMENDATION_AND_SUMMARY,
        str(final_report_request))
    job_state.final_report = final_report

    return job_state


def create_rating_request(product, user_request, catagories):
    return f"""
        Product: "{product}"

        User Request: "{user_request}"

        Catagories: "{catagories}"
        """
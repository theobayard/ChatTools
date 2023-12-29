import json
from src.apps.consumer_report import tasks
from src.task.text_task import parse_chat_gpt_json


def make_consumer_report(user_request: str):
    product_candidates = tasks.FIND_BEST_PRODUCT_CANDIDATES_TASK.run(user_request)
    product_candidates = product_candidates.split('|')
    print(f'Product Candidates Found: {product_candidates}')

    catagories = tasks.CREATE_RATING_CATAGORIES.run(user_request)
    print(f"Product Catagories Found: {catagories}")

    rating_requests = [
        create_rating_request(product, user_request, catagories) for product in product_candidates
    ]
    product_reports = [
        tasks.RESEARCH_PRODUCT.run(rating_request) for rating_request in rating_requests
    ]
    print(f"Product Reports Made: {product_reports}")

    final_report_request = create_final_report_request(product_reports, user_request)
    final_report = tasks.FINAL_RECOMMENDATION_AND_SUMMARY.run(str(final_report_request))

    return {
        'user_request': user_request,
        'product_reports': [parse_chat_gpt_json(product_report) for product_report in product_reports],
        'final_report': final_report
    }


def create_rating_request(product, user_request, catagories):
    return f"""
        Product: "{product}"

        User Request: "{user_request}"

        Catagories: "{catagories}"
        """

def create_final_report_request(product_reports: list[str], user_request: str):
    return {
        'user_request': user_request,
        'product_reports': product_reports,
    }
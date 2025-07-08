import logging
from app.services.genrate_embeddings import generate_embeddings
from app.database.last_fetched_data import get_last_fetched_question
from app.utils.get_paid_problems import get_paid_problems
from bs4 import BeautifulSoup
import requests
import re


def get_all_problems(categorySlug="", skip=0, limit=10000, filters={}):
    url = 'https://leetcode.com/graphql'
    response = requests.post(url, json={
        "query": """
        query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
  problemsetQuestionList: questionList(
    categorySlug: $categorySlug
    limit: $limit
    skip: $skip
    filters: $filters
  ) {
    total: totalNum
    questions: data {
      frontendQuestionId: questionFrontendId
      paidOnly: isPaidOnly
      title
      titleSlug
    }
  }
}
""",
        "variables": {
            "categorySlug": categorySlug,
            "limit": limit,
            "skip": skip,
            "filters": filters
        }
    })

    if response.status_code == 200:
        data = response.json()
        return data['data']['problemsetQuestionList']['questions']
    else:
        response.raise_for_status()


def filter_problems(problems=[]):
    filtered_problems_free = []
    filtered_problems_paid = []
    for problem in problems:
        if problem['paidOnly']:
            filtered_problems_paid.append({
                'id': problem['frontendQuestionId'],
                'title': problem['title'],
                'slug': problem['titleSlug'],
            })
        else:
            filtered_problems_free.append({
                'id': problem['frontendQuestionId'],
                'title': problem['title'],
                'slug': problem['titleSlug'],
            })
    return filtered_problems_free, filtered_problems_paid


def get_json_problem(problems=[]):
    url = 'https://leetcode-api-pied.vercel.app/problem'
    json_problems = []
    for problem in problems:
        response = requests.get(f"{url}/{problem['slug']}")
        if response.status_code == 200:
            response_data = response.json()
            json_problems.append({
                'id': problem['id'],
                'title': problem['title'],
                'slug': problem['slug'],
                'content': response_data['content'],
            })
        else:
            logging.error(
                f"Failed to fetch problem {problem['id']}: "
                f"{response.status_code}"
            )
    return json_problems


def format_problem(problems=[], type=False):
    formatted_problems = []
    for problem in problems:
        raw_html = problem.get('content', '')
        soup = BeautifulSoup(raw_html, 'html.parser')
        clean_text = soup.get_text(separator=" ").strip().replace("\n", " ")
        clean_text = ' '.join(clean_text.split())
        clean_text = re.sub(r"(?<=\s)(10|2)\s+(\d+)(?=\s)",
                            r"\1^\2", clean_text)
        formatted_problems.append({
            'id': problem['id'],
            'title': problem['title'],
            'url': f"https://leetcode.com/problems/{problem['slug']}",
            'paidOnly': type,
            'slug': problem['slug'],
            'content': clean_text,
            'original_content': raw_html
        })
    return formatted_problems


def get_next_batch(last_fetched, problems, batch_size=30):
    last_fetched = int(last_fetched)-10
    if last_fetched < 0:
        last_fetched = 0
    next_batch = []
    for problem in problems:
        if int(problem['id']) >= last_fetched:
            next_batch.append(problem)
        if len(next_batch) >= batch_size:
            break
    return next_batch


def scrape_problems():
    problems = get_all_problems()
    filtered_problems_free, filtered_problems_paid = filter_problems(problems)
    last_fetched_free = get_last_fetched_question(False)
    if last_fetched_free is None:
        last_fetched_free = {'id_num': 0}
    next_batch_free = get_next_batch(
        last_fetched_free['id_num'], filtered_problems_free)
    json_problems_free = get_json_problem(problems=next_batch_free)
    last_fetched_paid = get_last_fetched_question(True)
    if last_fetched_paid is None:
        last_fetched_paid = {'id_num': 0}
    next_batch_paid = get_next_batch(
        last_fetched_paid['id_num'], filtered_problems_paid)
    logging.info(f"Next batch paid problems: {len(next_batch_paid)}")
    json_problems_paid = get_paid_problems(problems=next_batch_paid)
    logging.info(f"Total paid problems fetched: {len(json_problems_paid)}")
    formatted_problems_paid = format_problem(json_problems_paid, True)
    formatted_problems_free = format_problem(json_problems_free, False)
    formatted_problems_free.extend(formatted_problems_paid)
    generate_embeddings(formatted_problems_free)

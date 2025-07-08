import ast
from app.utils.get_paid_problems import get_paid_problems
from app.utils.get_embeddings import get_embedding
from psycopg2.extensions import adapt
import re
import logging
import os
import json
import requests
import csv
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)


def generate_embeddings(data):
    for problem in data:
        embedding = get_embedding(problem.get('content', ''))
        problem['embedding'] = embedding


def get_all_problems():
    """
    Downloads the LeetCode problems JSON and saves it locally.
    Returns the parsed JSON content.
    """
    download_url = "https://raw.githubusercontent.com/noworneverev/leetcode-api/main/data/leetcode_questions.json"
    json_path = os.path.join(os.path.dirname(
        __file__), 'leetcode_questions.json')

    try:
        response = requests.get(download_url, timeout=10)
        response.raise_for_status()
        with open(json_path, 'w') as f:
            f.write(response.text)
            logging.info("Downloaded and saved leetcode_questions.json")
    except requests.RequestException as e:
        logging.error(f"Failed to download JSON: {e}")
        if not os.path.exists(json_path):
            raise FileNotFoundError(
                "No local leetcode_questions.json file available.")
        else:
            logging.info("Using existing local file")

    with open(json_path, 'r') as f:
        return json.load(f)


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


def filter_problems(problems=[]):
    filtered_problems_free = []
    filtered_problems_paid = []
    for problem in problems:
        problem = problem['data']['question']
        if problem['isPaidOnly']:
            filtered_problems_paid.append({
                'id': problem['questionFrontendId'],
                'title': problem['title'],
                'slug': problem['url'].rstrip('/').split('/')[-1]})
        else:
            filtered_problems_free.append({
                'id': problem['questionFrontendId'],
                'title': problem['title'],
                'slug': problem['url'].rstrip('/').split('/')[-1],
                'content': problem['content'],
            })
    return filtered_problems_free, filtered_problems_paid


def save_to_csv(data, filename='problems.csv'):
    """
    Saves the provided data to a CSV file.
    """
    csv_path = os.path.join(os.path.dirname(__file__), filename)
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['id', 'id_num', 'url', 'title',
                      'paid_only', 'content', 'original_content', 'embedding']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
        logging.info(f"Saved data to {csv_path}")


def to_postgres_array(py_list):
    return "{" + ",".join(f'"{item}"' for item in py_list) + "}"


def order_data(data):
    csv_data = []
    for problem in data:
        csv_data.append({
            'id': problem['id'],
            'id_num': int(problem['id']),
            'url': f"https://leetcode.com/problems/{problem['slug']}",
            'title': problem['title'],
            'paid_only': problem['paidOnly'],
            'content': problem.get('content', ''),
            'original_content': problem.get('original_content', ''),
            'embedding': json.dumps(problem.get('embedding', []))
        })
    return csv_data


def populate_db():
    logging.info("Starting database population...")
    problems = get_all_problems()
    filtered_problems_free, filtered_problems_paid = filter_problems(problems)
    problems_paid_with_content = get_paid_problems(
        problems=filtered_problems_paid)
    formatted_problems_paid = format_problem(problems_paid_with_content, True)
    formatted_problems_free = format_problem(filtered_problems_free, False)
    formatted_problems_free.extend(formatted_problems_paid)
    logging.info(f"Total problems to insert: {len(formatted_problems_free)}")
    generate_embeddings(formatted_problems_free)
    csv_data = order_data(formatted_problems_free)
    save_to_csv(csv_data)

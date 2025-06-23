from bs4 import BeautifulSoup
import requests
import json
import re
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def get_all_problems(categorySlug="", skip=0, limit=4000, filters={}):
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
      topicTags {
        name
      }
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
    filtered_problems = []
    for problem in problems:
        if problem['paidOnly']:
            continue
        filtered_problems.append(
            {
                'id': problem['frontendQuestionId'],
                'title': problem['title'],
                'slug': problem['titleSlug'],
                'tags': [tag['name'] for tag in problem['topicTags']]
            }
        )
    return filtered_problems


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
                'tags': problem['tags'],
                'content': response_data['content'],
            })
        else:
            print(
                f"Failed to fetch problem {problem['id']}: "
                f"{response.status_code}"
            )
    return json_problems


def format_problem(problems=[]):
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
            'slug': problem['slug'],
            'tags': problem['tags'],
            'content': clean_text,
        })
    return formatted_problems


def save_problem(json_problems):
    # Define folder path (outside current folder)
    folder_path = os.path.join(os.path.dirname(
        os.getcwd()), "data")

    # Create the folder if it doesn't exist
    os.makedirs(folder_path, exist_ok=True)

    # Define full file path
    file_path = os.path.join(folder_path, "data.json")

    # Load existing data if file exists
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = []
    else:
        existing_data = []

    existing_data.extend(json_problems)
    seen_ids = set()
    unique_data = []
    for problem in existing_data:
        if problem['id'] not in seen_ids:
            seen_ids.add(problem['id'])
            unique_data.append(problem)
    existing_data = unique_data
    sorted_data = sorted(existing_data, key=lambda x: int(x['id']))

    # Save combined data to file
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(sorted_data, f, ensure_ascii=False, indent=2)

    print(f"✅ Saved {len(json_problems)} problems to {file_path}")


def last_fetched_problem():
    last_fetched = 0
    folder_path = os.path.join(os.path.dirname(os.getcwd()), "data")
    file_path = os.path.join(folder_path, "data.json")
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if data:
                last_fetched = int(data[-1]['id'])
    return last_fetched


def get_next_batch(last_fetched, problems, batch_size=30):
    next_batch = []
    for problem in problems:
        if int(problem['id']) > last_fetched:
            next_batch.append(problem)
        if len(next_batch) >= batch_size:
            break
    return next_batch


if __name__ == "__main__":
    problems = get_all_problems()
    filtered_problems = filter_problems(problems=problems)
    print(f"Found {len(filtered_problems)} problems")
    last_fetched = last_fetched_problem()
    print(f"Last fetched problem ID: {last_fetched}")
    next_batch = get_next_batch(last_fetched, filtered_problems)
    json_problems = get_json_problem(problems=next_batch)
    print(f"Fetched {len(json_problems)} JSON problems")
    formatted_problems = format_problem(json_problems)
    print(f"Formatted {len(formatted_problems)} problems")
    save_problem(formatted_problems)

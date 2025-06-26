from bs4 import BeautifulSoup
import requests
import json
import re
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def download_problems():
    url = "https://raw.githubusercontent.com/noworneverev/leetcode-api/refs/heads/main/data/leetcode_questions.json"
    response = requests.get(url)
    if response.status_code == 200:
        with open('leetcode_questions.json', 'wb') as f:
            f.write(response.content)
        print("✅ Downloaded leetcode_questions.json")
    else:
        print(
            f"❌ Failed to download leetcode_questions.json, status code: {response.status_code}")


def filter_problems(paid_only=False, problems=[]):
    filtered_problems = []
    for problem in problems:
        if problem['paidOnly']:
            continue
        filtered_problems.append(
            {
                'id': problem['id'],
                'title': problem['title'],
                'url': problem['url'],
                'paidOnly': problem['paidOnly'],
                'content': problem['content'],
                'tags': [tag['name'] for tag in problem['topicTags']]
            }
        )
    return filtered_problems


def format_problem(problems=None):
    if problems is None:
        problems = []
    formatted_problems = []
    for problem in problems:
        raw_html = str(problem.get('content', '') or '')
        soup = BeautifulSoup(raw_html, 'html.parser')
        clean_text = soup.get_text(separator=" ").strip().replace("\n", " ")
        clean_text = ' '.join(clean_text.split())
        clean_text = re.sub(r"(?<=\s)(10|2)\s+(\d+)(?=\s)",
                            r"\1^\2", clean_text)
        formatted_problems.append({
            'id': problem['id'],
            'title': problem['title'],
            'url': problem['url'],
            'paidOnly': problem['paidOnly'],
            'tags': problem['tags'],
            'content': clean_text,
            'original_content': raw_html
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
    existing_data = []

    # Append new problems to existing data
    existing_data.extend(json_problems)

    # Save combined data to file
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=2)

    print(f"✅ Saved {len(json_problems)} problems to {file_path}")


if __name__ == "__main__":
    # Example usage
    # get questions from leetcode_questions.json
    download_problems()
    example_problems = []
    with open('leetcode_questions.json', 'r', encoding='utf-8') as f:
        example_problems = json.load(f)
    problem_new = []
    for problem in example_problems:
        problem_new.append({
            'id': problem['data']['question']['questionFrontendId'],
            'title': problem['data']['question']['title'],
            'url': problem['data']['question']['url'],
            'paidOnly': problem['data']['question']['content'] is None,
            'content': problem['data']['question']['content'],
            'topicTags': problem['data']['question']['topicTags']
        })
    print(f"Total problems fetched: {len(problem_new)}")
    filtered = filter_problems(paid_only=False, problems=problem_new)
    formatted = format_problem(problems=filtered)
    print(formatted[0])
    save_problem(json_problems=formatted)

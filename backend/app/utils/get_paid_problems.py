import logging
import requests
import urllib.parse
import re


def extract_description_from_markdown(url: str) -> str:
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(
            f"Failed to fetch content: {response.status_code} for url {url}")
    content = response.text
    match = re.search(
        r"<!-- description:start -->(.*?)<!-- description:end -->", content, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        raise Exception("Description block not found in markdown content.")


def generate_doocs_markdown_url(problem_id: int, title: str) -> str:

    start_range = (problem_id // 100) * 100
    end_range = start_range + 99
    start_range = f"{start_range:04d}"
    end_range = f"{end_range:04d}"
    problem_id_str = f"{problem_id:04d}"
    range_folder = f"{start_range}-{end_range}"

    # Encode title with %20 for spaces
    cleaned_title = title.replace(":", "").strip()
    encoded_title = urllib.parse.quote(cleaned_title)

    return (
        f"https://raw.githubusercontent.com/doocs/leetcode/main/solution/"
        f"{range_folder}/{problem_id_str}.{encoded_title}/README_EN.md"
    )


def get_paid_problems(problems=[]):
    paid_problems = []
    for problem in problems:
        url_slug = generate_doocs_markdown_url(
            problem_id=int(problem['id']),
            title=problem['title']
        )
        logging.info(f"Fetching content from {url_slug}")
        clean_html = extract_description_from_markdown(url_slug)
        if not clean_html:
            logging.warning(f"⚠️ No content found for problem {problem['id']}")
            continue
        paid_problems.append({
            'id': problem['id'],
            'title': problem['title'],
            'slug': problem['slug'],
            'content': clean_html
        })
    return paid_problems

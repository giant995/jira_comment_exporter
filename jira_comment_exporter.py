import os
import requests
from requests.auth import HTTPBasicAuth
import json

from dotenv import load_dotenv

load_dotenv()

JIRA_BASE_URL = "https://mrdltd.atlassian.net"
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_EMAIL = "jean-michel.plourde@tlmgo.com"


def get_ticket_comments(ticket_key):
    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{ticket_key}/comment"
    auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)
    headers = {
        "Accept": "application/json"
    }

    response = requests.request(
        "GET",
        url,
        headers=headers,
        auth=auth
    )

    return json.loads(response.text)


def parse_text(element):
    output = element["text"]
    for mark in element.get("marks", []):
        if mark["type"] == "code":
            output = f"`{output}`"
        elif mark["type"] == "strike":
            output = f"~~{output}~~"
        elif mark["type"] == "underline":
            output = f"<ins>{output}</ins>"
        elif mark["type"] == "subsup":
            if mark["attrs"]["type"] == "sub":
                output = f"~{output}~"
            elif mark["attrs"]["type"] == "sup":
                output = f"^{output}^"

    return output


def parse_paragraph(content):
    paragraph = ""
    for element in content:
        if element["type"] == "text":
            paragraph += parse_text(element)
        elif element["type"] == "hardBreak":
            paragraph += "\n"
        elif element["type"] == "inlineCard":
            url = element["attrs"]["url"]
            paragraph += f"[{url}]({url})"

    return paragraph


def main():
    response = get_ticket_comments("CLD-223")
    comments = response["comments"]

    for comment_idx, comment in enumerate(comments):
        print("\n", "comment:", comment_idx, "----------------")
        content = comment["body"]["content"]
        for part_idx, part in enumerate(content):
            print(part)
            if part["type"] == "paragraph":
                paragraph = parse_paragraph(part["content"])
                if part_idx != 0:
                    paragraph = "\n" + paragraph
                print(paragraph)


if __name__ == "__main__":
    main()

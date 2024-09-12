import requests
import re
import os

# Replace with your personal access token
token = os.getenv('GITHUB_TOKEN')
headers = {'Authorization': f'token {token}'}

# Replace with your organization name
org = 'ministryofjustice'

# Function to fetch all repositories with pagination
def fetch_all_repos(org, headers):
    repos = []
    page = 1
    while True:
        repos_url = f'https://api.github.com/orgs/{org}/repos?page={page}&per_page=100'
        repos_response = requests.get(repos_url, headers=headers)
        if repos_response.status_code != 200:
            print(f"Error fetching repositories: {repos_response.status_code}, {repos_response.text}")
            break
        page_repos = repos_response.json()
        if not page_repos:
            break
        repos.extend(page_repos)
        page += 1
    return repos

# Fetch all repositories in the organization
repos = fetch_all_repos(org, headers)

# Filter repositories that match the pattern 'analytical-platform-*'
pattern = re.compile(r'^analytical-platform-.*')
repo_names = [repo['name'] for repo in repos if pattern.match(repo['name'])]
print(repo_names)

# Function to perform search in chunks
def search_in_chunks(repo_names, chunk_size=5):
    results = []
    for i in range(0, len(repo_names), chunk_size):
        chunk = repo_names[i:i+chunk_size]
        query = 'upload-artifact ' + ' '.join([f'repo:{org}/{repo}' for repo in chunk])
        search_url = f'https://api.github.com/search/code?q={query}'
        search_response = requests.get(search_url, headers=headers)
        if search_response.status_code == 200:
            results.extend(search_response.json().get('items', []))
        else:
            print(f"Error in search: {search_response.status_code}, {search_response.text}")
    return results

# Perform the search in chunks
search_results = search_in_chunks(repo_names)

# Print the results
for item in search_results:
    print(f"Repository: {item['repository']['full_name']}, File: {item['path']}")

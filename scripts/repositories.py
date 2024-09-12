import requests
import re
import zipfile
import os
import logging
import shutil
import subprocess

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_repositories(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        repo_names = re.findall(r'^\s*name\s*=\s*"([^"]+)"', content, re.MULTILINE)
        logging.info(f"Found {len(repo_names)} repositories.")
        return repo_names
    except Exception as e:
        logging.error(f"Error reading file {file_path}: {e}")
        return []

def find_successful_run_with_artifact(repo_name, token):
    url = f"https://api.github.com/repos/ministryofjustice/{repo_name}/actions/runs"
    headers = {'Authorization': f'token {token}'}

    try:
        response = requests.get(url, headers=headers)
        logging.info(f"Request URL: {url}")
        logging.info(f"Response Status Code: {response.status_code}")
        data = response.json()

        if response.status_code == 200 and 'workflow_runs' in data and len(data['workflow_runs']) > 0:
            for run in data['workflow_runs']:
                if run['conclusion'] == 'success':
                    artifacts_url = run['artifacts_url']
                    artifacts_response = requests.get(artifacts_url, headers=headers)
                    artifacts_data = artifacts_response.json()

                    if 'artifacts' in artifacts_data and artifacts_data['total_count'] > 0:
                        for artifact in artifacts_data['artifacts']:
                            download_url = artifact['archive_download_url']
                            file_name = f"{artifact['name']}.zip"
                            download_response = requests.get(download_url, headers=headers)

                            if download_response.status_code == 200:
                                with open(file_name, 'wb') as file:
                                    file.write(download_response.content)
                                logging.info(f"Downloaded {file_name} from {repo_name}")

                                try:
                                    # Try to extract using zipfile first
                                    if zipfile.is_zipfile(file_name):
                                        with zipfile.ZipFile(file_name, 'r') as zip_ref:
                                            zip_ref.extractall(f"{artifact['name']}")
                                        check_for_github_tokens(f"{artifact['name']}")
                                    else:
                                        raise zipfile.BadZipFile
                                except zipfile.BadZipFile:
                                    # If zipfile fails, try using shutil
                                    try:
                                        shutil.unpack_archive(file_name, f"{artifact['name']}")
                                        check_for_github_tokens(f"{artifact['name']}")
                                    except Exception as e:
                                        logging.error(f"Failed to unpack {file_name} using shutil: {e}")
                            else:
                                logging.warning(f"Artifact {artifact['name']} from {repo_name} has expired or is not available for download.")
                        return
                    else:
                        logging.info(f"No artifacts found for the successful run in {repo_name}")
                else:
                    logging.info(f"No successful runs with artifacts found for {repo_name}")
        else:
            logging.info(f"No workflow runs found for {repo_name} -- {url}")
    except Exception as e:
        logging.error(f"Error fetching workflow runs for {repo_name}: {e}")

def check_for_github_tokens(directory):
    try:
        # Run Gitleaks on the directory
        result = subprocess.run(['gitleaks', 'detect', '--source', directory], capture_output=True, text=True)
        if result.returncode == 0:
            logging.info(f"Gitleaks scan completed successfully for {directory}")
            if result.stdout:
                logging.warning(f"Potential secrets found:\n{result.stdout}")
        else:
            logging.error(f"Gitleaks scan failed for {directory} with error:\n{result.stderr}")
    except Exception as e:
        logging.error(f"Error running Gitleaks on {directory}: {e}")

# Replace 'your_github_token' with your actual GitHub token stored in an environment variable
github_token = os.getenv('GITHUB_TOKEN')

if github_token:
    repositories = extract_repositories('analytical-platform-repositories.tf')
    for repo in repositories:
        find_successful_run_with_artifact(repo, github_token)
else:
    logging.error("GitHub token not found. Please set the GITHUB_TOKEN environment variable.")

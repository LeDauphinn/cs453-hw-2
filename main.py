import requests
import json

def get_last_n_merged_prs(github_token, repo_link, n):
    # Extract the owner and repo name from the link
    owner, repo = repo_link.split('/')[-2:]

    # Define the GraphQL query
    query = """
    query {
      repository(owner: "%s", name: "%s") {
        pullRequests(last: %d, states: MERGED) {
          nodes {
            mergedAt
            url
            title
          }
        }
      }
    }
    """ % (owner, repo, n)

    # Define the headers for the request
    headers = {
        'Authorization': f'bearer {github_token}',
        'Content-Type': 'application/json'
    }

    # Define the URL for the GraphQL API request
    url = 'https://api.github.com/graphql'

    # Make the API request
    response = requests.post(url, headers=headers, json={'query': query})

    # Check if the request was successful
    if response.status_code == 200:
        # Get the JSON data from the response
        data = response.json()

        # Extract the merged PRs from the response
        merged_prs = data['data']['repository']['pullRequests']['nodes']

        # Return the merged PRs
        return merged_prs
    else:
        print(f'Error: {response.status_code}')
        return None

def get_diffs_and_save(github_token, pr_urls):
    headers = {'Authorization': f'token {github_token}', 'Accept': 'application/vnd.github.v3.diff'}
    diffs = {}

    for url in pr_urls:
        diff_url = url + '.diff'
        response = requests.get(diff_url, headers=headers)

        if response.status_code == 200:
            diffs[diff_url] = response.text
        else:
            print(f'Error: {response.status_code}')

    with open('diffs.json', 'w') as f:
        json.dump(diffs, f)

def main():
    github_token = input("Please enter your GitHub token: ")
    number = int(input("Please enter a number: "))  # Convert the input to an integer
    github_repo_link = input("Please enter a GitHub repo link: ")

    # Call the function with the inputs
    last_n_merged_prs = get_last_n_merged_prs(github_token, github_repo_link, number)

    # Open a JSON file in write mode
    with open('output.json', 'w') as f:
        # Write the PRs to the file
        json.dump(last_n_merged_prs, f)
        
    # Extract the URLs of the PRs
    pr_urls = [pr['url'] for pr in last_n_merged_prs]

    # Get the diffs and save them to a JSON file
    get_diffs_and_save(github_token, pr_urls)

if __name__ == "__main__":
    main()

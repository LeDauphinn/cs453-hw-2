import requests
import json

def get_last_n_merged_prs(github_token, repo_link, n):
   # Extract the owner and repo name from the link
   owner, repo = repo_link.split('/')[-2:]

   # Define the headers for the request
   headers = {'Authorization': f'token {github_token}'}

   # Define the URL for the API request
   url = f'https://api.github.com/repos/{owner}/{repo}/pulls?state=closed&sort=updated&direction=desc'

   # Make the API request
   response = requests.get(url, headers=headers)

   # Check if the request was successful
   if response.status_code == 200:
      # Get the JSON data from the response
      data = response.json()

      # Filter the data to only include merged PRs
      merged_prs = [pr for pr in data if pr['merged_at'] is not None]

      # Return the last N merged PRs
      return merged_prs[-n:]
   else:
      print(f'Error: {response.status_code}')
      return None

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

if __name__ == "__main__":
    main()
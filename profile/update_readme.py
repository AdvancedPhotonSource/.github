import requests
import os

ORG = "AdvancedPhotonSource"
URL = f"https://api.github.com/orgs/{ORG}/repos?per_page=100"

def get_repos():
    # Fetch all repos in the org
    response = requests.get(URL)
    repos = response.json()
    # Filter out forks and private repos if needed
    return [r for r in repos if not r['fork'] and not r['private']]

def update_readme():
    repos = get_repos()
    
    # 1. Sort by Stars (Popular)
    popular = sorted(repos, key=lambda x: x['stargazers_count'], reverse=True)[:5]
    pop_md = "\n".join([f"- [{r['name']}]({r['html_url']}) — ⭐ {r['stargazers_count']}" for r in popular])
    
    # 2. Sort by Last Pushed (Active)
    active = sorted(repos, key=lambda x: x['pushed_at'], reverse=True)[:5]
    act_md = "\n".join([f"- [{r['name']}]({r['html_url']}) — 🕒 {r['pushed_at'][:10]}" for r in active])

    with open("profile/README.md", "r") as f:
        content = f.read()

    # Replace sections
    import re
    content = re.sub(r"<!-- POPULAR_START -->.*?<!-- POPULAR_END -->", f"<!-- POPULAR_START -->\n{pop_md}\n<!-- POPULAR_END -->", content, flags=re.DOTALL)
    content = re.sub(r"<!-- ACTIVE_START -->.*?<!-- ACTIVE_END -->", f"<!-- ACTIVE_START -->\n{act_md}\n<!-- ACTIVE_END -->", content, flags=re.DOTALL)

    with open("profile/README.md", "w") as f:
        f.write(content)

if __name__ == "__main__":
    update_readme()

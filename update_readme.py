import requests
import re

# Thay bằng username của bạn
USERNAME = "thanhtai21" 

def get_status(topics):
    if 'completed' in topics:
        return "✅ Completed"
    return "🛠 Active"

def get_field(topics):
    if 'trading-bot' in topics or 'finance' in topics:
        return "📈 Finance"
    if 'cybersecurity' in topics or 'security' in topics:
        return "🛡️ Cybersecurity"
    if 'iot' in topics:
        return "🌐 IoT"
    if 'big-data' in topics or 'kafka' in topics or 'spark' in topics:
        return "📊 Big Data"
    return "💻 Development"

# Gọi GitHub API lấy danh sách repo
try:
    repos = requests.get(f"https://api.github.com/users/{USERNAME}/repos?sort=updated&per_page=10").json()

    table_content = "| Dự án | Lĩnh vực | Trạng thái | Chi tiết |\n| :--- | :--- | :--- | :--- |\n"

    # Chỉ lấy các repo không phải là repo cá nhân (profile repo)
    featured_repos = [r for r in repos if r['name'] != USERNAME][:5]

    for repo in featured_repos:
        name = repo['name']
        url = repo['html_url']
        desc = repo['description'] or "No description provided."
        topics = repo.get('topics', [])
        
        field = get_field(topics)
        status = get_status(topics)
        
        table_content += f"| [**{name}**]({url}) | {field} | `{status}` | {desc} |\n"

    # Đọc file README và thay thế đoạn nội dung giữa 2 thẻ ghi chú
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r"<!-- START_PROJECT_TABLE -->.*?<!-- END_PROJECT_TABLE -->"
    new_content = re.sub(pattern, f"<!-- START_PROJECT_TABLE -->\n{table_content}<!-- END_PROJECT_TABLE -->", content, flags=re.DOTALL)

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_content)
    
    print("Successfully updated README.md")

except Exception as e:
    print(f"Error occurred: {e}")

import requests
import re

USERNAME = "thanhtai21" 

# Bản đồ ánh xạ tên Repo sang Tên hiển thị đẹp và Lĩnh vực
REPO_CONFIG = {
    "nba-data-streaming-pipeline": {"name": "NBA Data Analytics", "field": "📊 Big Data", "desc": "Phân tích Reddit Data bằng Kafka & Spark."},
    "MT5_Telegram_Trading_Bot": {"name": "Gold Trading Bot", "field": "📈 Finance", "desc": "Bot tự động giao dịch Vàng trên MT5 bằng Python."},
    "IOT_chatluongkhongkhi": {"name": "Intelligent Air Quality", "field": "🌐 IoT", "desc": "Hệ thống cảnh báo dùng ESP32, MQ-135 & Blynk."},
    "THOR-APT-Scanner": {"name": "THOR APT Scanner", "field": "🛡️ Cybersecurity", "desc": "Triển khai quét mã độc & phân tích Data Exfiltration."}
}

def get_status(topics):
    if 'completed' in topics:
        return "✅ Completed"
    return "🛠 Active"

def get_field(repo_name, topics):
    # Ưu tiên lấy từ cấu hình cứng
    if repo_name in REPO_CONFIG:
        return REPO_CONFIG[repo_name]['field']
    # Nếu không có thì dựa vào topics
    if 'trading-bot' in topics or 'finance' in topics:
        return "📈 Finance"
    if 'cybersecurity' in topics or 'security' in topics:
        return "🛡️ Cybersecurity"
    if 'iot' in topics:
        return "🌐 IoT"
    if 'big-data' in topics or 'kafka' in topics or 'spark' in topics:
        return "📊 Big Data"
    return "💻 Development"

try:
    repos = requests.get(f"https://api.github.com/users/{USERNAME}/repos?sort=updated&per_page=15").json()
    table_content = "| Dự án | Lĩnh vực | Trạng thái | Chi tiết |\n| :--- | :--- | :--- | :--- |\n"
    
    # Lọc bỏ repo profile và các repo không muốn hiển thị
    display_count = 0
    for repo in repos:
        repo_name = repo['name']
        if repo_name == USERNAME or repo_name == "thanhtai" or display_count >= 5:
            continue
            
        url = repo['html_url']
        topics = repo.get('topics', [])
        status = get_status(topics)
        
        # Lấy thông tin từ REPO_CONFIG hoặc từ GitHub
        if repo_name in REPO_CONFIG:
            pretty_name = REPO_CONFIG[repo_name]['name']
            field = REPO_CONFIG[repo_name]['field']
            desc = REPO_CONFIG[repo_name]['desc']
        else:
            pretty_name = repo_name
            field = get_field(repo_name, topics)
            desc = repo['description'] or "Đang cập nhật mô tả..."
        
        table_content += f"| [**{pretty_name}**]({url}) | {field} | `{status}` | {desc} |\n"
        display_count += 1

    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r"<!-- START_PROJECT_TABLE -->.*?<!-- END_PROJECT_TABLE -->"
    new_content = re.sub(pattern, f"<!-- START_PROJECT_TABLE -->\n{table_content}<!-- END_PROJECT_TABLE -->", content, flags=re.DOTALL)

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Successfully updated README.md with smart mapping")

except Exception as e:
    print(f"Error: {e}")

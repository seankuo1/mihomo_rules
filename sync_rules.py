import os
import requests

# 规则配置
RULES_CONFIG = [
    {"url": "https://raw.githubusercontent.com/G4free/clash-ruleset/main/ruleset/ChatGPT.yaml",
     "filename": "ChatGPT.yaml"},
    {"url": "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Gemini/Gemini.list",
     "filename": "Gemini.yaml"},
    {"url": "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Claude/Claude.list",
     "filename": "Claude.yaml"},
    {"url": "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Copilot/Copilot.list",
     "filename": "Copilot.yaml"},
    {"url": "https://raw.githubusercontent.com/G4free/clash-ruleset/main/ruleset/anthropic.txt",
     "filename": "Anthropic.yaml"},
    {"url": "https://ruleset.skk.moe/List/non_ip/sogouinput.conf", "filename": "SogouInput.yaml"},
]


def fetch_and_convert(url):
    try:
        print(f"Fetching {url}...")
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        lines = response.text.splitlines()

        rules = []
        for line in lines:
            line = line.strip()
            # 过滤掉 YAML 标记、注释和空行
            if not line or line.startswith(('#', ';', '//', 'payload:', '---')):
                continue

            # 清理格式，确保是 - DOMAIN,... 这种标准格式
            clean_rule = line.lstrip('- ').strip()
            if ',' in clean_rule:
                rules.append(f"  - {clean_rule}")

        return "payload:\n" + "\n".join(rules)
    except Exception as e:
        print(f"Failed to process {url}: {e}")
        return None


if __name__ == "__main__":
    for item in RULES_CONFIG:
        content = fetch_and_convert(item['url'])
        if content:
            with open(item['filename'], 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Saved {item['filename']}")

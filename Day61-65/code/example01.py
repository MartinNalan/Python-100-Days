"""
example01.py - 最近一周涨星最多的10个项目
通过requests和bs4爬取GitHub Trending周榜，获取最近一周涨星最多的10个项目
"""
import requests
from bs4 import BeautifulSoup

MAX_DESC_LENGTH = 50


def get_weekly_trending(limit=10):
    """爬取GitHub Trending周榜，返回涨星最多的前limit个项目信息"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        resp = requests.get(
            url='https://github.com/trending?since=weekly',
            headers=headers,
            timeout=30
        )
    except requests.exceptions.RequestException as e:
        print(f'请求失败：{e}')
        return []
    repos = []
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, 'lxml')
        articles = soup.select('article.Box-row')[:limit]
        for article in articles:
            # 仓库名称（owner/repo），直接从 href 中提取，格式为 /owner/repo
            name_tag = article.select_one('h2 a')
            name = name_tag['href'].lstrip('/') if name_tag else 'N/A'

            # 仓库描述
            desc_tag = article.select_one('p')
            description = desc_tag.get_text(strip=True) if desc_tag else ''

            # 编程语言
            lang_tag = article.select_one('span[itemprop="programmingLanguage"]')
            language = lang_tag.get_text(strip=True) if lang_tag else ''

            # 本周涨星数量（页面右下角 "X stars this week"）
            stars_tag = article.select_one('span.d-inline-block.float-sm-right')
            stars_this_week = stars_tag.get_text(strip=True) if stars_tag else 'N/A'

            repos.append({
                'name': name,
                'description': description,
                'language': language,
                'stars_this_week': stars_this_week,
            })
    return repos


def main():
    repos = get_weekly_trending()
    if not repos:
        print('未能获取数据，请检查网络连接或稍后重试。')
        return
    print(f'{"排名":<4}  {"项目名称":<45}{"语言":<15}{"本周涨星":<20}{"项目描述"}')
    print('-' * 120)
    for rank, repo in enumerate(repos, start=1):
        desc = repo['description'][:MAX_DESC_LENGTH] + (
            '…' if len(repo['description']) > MAX_DESC_LENGTH else ''
        )
        print(
            f'{rank:<4}  {repo["name"]:<45}{repo["language"]:<15}'
            f'{repo["stars_this_week"]:<20}{desc}'
        )


if __name__ == '__main__':
    main()

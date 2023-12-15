import pandas as pd
import requests
from bs4 import BeautifulSoup
from src.service_news import get_news
# 뉴스 수집(Python) -> Pandas의 데이터프레임 ->Excel 저장


def news_collector(category, page=1, count=1):
    collect_list = []  # 향후 데이터프레임 변환용!
    while True:
        # 실습용(후에 제거 필수)
        if page == 3:
            break
        url = f"https://news.daum.net/breakingnews/{category}?page={page}"
        result = requests.get(url)

        if result.status_code == 200:
            print(result, "접속 성공 → 데이터를 수집합니다.")
            doc = BeautifulSoup(result.text, "html.parser")
            url_list = doc.select("ul.list_news2 a.link_txt")
            if len(url_list) == 0:
                break

            for url in url_list:
                count += 1
                print(f"{count}", "=" * 100)
                data = get_news(url["href"], category)
                collect_list.append(data)
        else:
            print("잘못된 URL 경로입니다. 확인 부탁드립니다.")
        page += 1
    # 뉴스 수집 완료
    # - collect_list -> dataframe
    col_name = ["category", "title", "content", "date"]
    df_review = pd.DataFrame(collect_list, columns=col_name)

    return df_review, count  # tuple type
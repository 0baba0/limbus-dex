import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# 저장 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_SITE_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "web_site"))
IMAGE_DIR = os.path.join(WEB_SITE_DIR, "public", "images", "characters")

os.makedirs(IMAGE_DIR, exist_ok=True)

def download_fallback_images():
    print("🛡️ 네이버 방어막 우회 스크래핑을 시작합니다...")
    TARGET_URL = "https://m.blog.naver.com/baeeunhye13/223055148829"
    
    # 웹페이지 접속용 헤더
    page_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    # 이미지 다운로드 전용 헤더 (네이버 이미지 서버가 좋아하는 PC 버전 Referer로 위장)
    img_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://blog.naver.com/" 
    }

    try:
        response = requests.get(TARGET_URL, headers=page_headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        images = soup.select('img.se-image-resource')
        print(f"✅ 총 {len(images)}개의 이미지를 찾았습니다. 스마트 다운로드를 시작합니다!\n")

        for i, img in enumerate(images):
            # 1. URL 추출 (지연 로딩 대응)
            raw_url = img.get('data-lazy-src') or img.get('src')
            if not raw_url:
                continue
            
            clean_url = raw_url.split('?')[0] # 원본 시도용 URL
            
            # 확장자 추출 및 파일명 지정
            parsed_url = urlparse(clean_url)
            ext = os.path.splitext(parsed_url.path)[1]
            if not ext: ext = ".png"
            
            filename = f"limbus_image_{i+1:03d}{ext}"
            filepath = os.path.join(IMAGE_DIR, filename)

            # 2. [플랜 A] 파라미터 뗀 원본 URL로 먼저 다운로드 시도
            img_response = requests.get(clean_url, headers=img_headers)
            
            # 3. [플랜 B] 만약 막혔다면(403, 404), 원래 URL(raw_url)로 재시도
            if img_response.status_code != 200:
                img_response = requests.get(raw_url, headers=img_headers)

            # 4. 결과 저장 및 출력
            if img_response.status_code == 200:
                with open(filepath, "wb") as f:
                    f.write(img_response.content)
                print(f"  -> 💾 [{filename}] 다운로드 성공")
            else:
                # 그래도 실패하면 에러 코드를 출력해서 디버깅할 수 있게 함
                print(f"  -> ❌ [{filename}] 최종 실패 (에러 코드: {img_response.status_code})")

        print("\n🎉 다운로드 작업이 끝났어! 폴더를 확인해 봐.")

    except Exception as e:
        print(f"❌ 실행 중 치명적 오류 발생: {e}")

if __name__ == "__main__":
    download_fallback_images()
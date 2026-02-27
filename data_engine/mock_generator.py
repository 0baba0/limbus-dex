import os
import json
import requests

# 1. 경로 설정 (현재 스크립트 위치를 기준으로 web_site 폴더 경로 역추적)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_SITE_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "web_site"))

# Astro가 데이터를 읽을 경로 (JSON) / 이미지를 서비스할 경로 (Public)
JSON_DIR = os.path.join(WEB_SITE_DIR, "src", "content", "characters")
IMAGE_DIR = os.path.join(WEB_SITE_DIR, "public", "images", "characters")

# 폴더가 없다면 안전하게 생성해 줍니다.
os.makedirs(JSON_DIR, exist_ok=True)
os.makedirs(IMAGE_DIR, exist_ok=True)

def generate_mock_data():
    print("Mock 데이터 생성을 시작합니다...")

    # 2. 가짜 캐릭터 데이터 정의
    character_id = "sinner_01"
    character_data = {
        "id": character_id,
        "name": "이상",
        "affiliation": "Limbus Company",
        "weapon": "단검",
        "image_url": f"/images/characters/{character_id}.png" # 웹에서 접근할 상대 경로
    }

    # 3. JSON 파일로 저장 (`web_site/src/content/characters/...`)
    json_path = os.path.join(JSON_DIR, f"{character_id}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(character_data, f, ensure_ascii=False, indent=2)
    print(f"✅ JSON 데이터 저장 완료: {json_path}")

    # 4. 가짜 이미지 다운로드 및 저장 (`web_site/public/images/characters/...`)
    # (테스트용으로 300x400 크기의 더미 이미지를 다운받습니다)
    dummy_image_url = "https://dummyimage.com/300x400/2b2b2b/ffffff.png&text=Yi+Sang"
    image_path = os.path.join(IMAGE_DIR, f"{character_id}.png")
    
    response = requests.get(dummy_image_url)
    if response.status_code == 200:
        with open(image_path, "wb") as f:
            f.write(response.content)
        print(f"✅ 이미지 저장 완료: {image_path}")
    else:
        print("❌ 이미지 다운로드 실패")

if __name__ == "__main__":
    generate_mock_data()
import os
import json
import glob

# 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_SITE_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "web_site"))

IMAGE_DIR = os.path.join(WEB_SITE_DIR, "public", "images", "characters")
JSON_DIR = os.path.join(WEB_SITE_DIR, "src", "content", "characters")

os.makedirs(JSON_DIR, exist_ok=True)

def generate_jsons_from_images():
    # [추가된 핵심 로직] 1. 기존 JSON 파일 깨끗하게 청소하기
    print("🧹 기존 JSON 찌꺼기 데이터를 청소합니다...")
    old_jsons = glob.glob(os.path.join(JSON_DIR, "*.json"))
    for old_json in old_jsons:
        os.remove(old_json)
    print(f"  -> 예전 데이터 {len(old_jsons)}개 삭제 완료.\n")

    # 2. 현재 존재하는 이미지 기준으로 새로운 JSON 생성하기
    print("⚙️ 현재 다운로드된 이미지를 바탕으로 새 JSON 데이터를 생성합니다...")
    images = [f for f in os.listdir(IMAGE_DIR) if os.path.isfile(os.path.join(IMAGE_DIR, f))]
    
    if not images:
        print("⚠️ 이미지가 없습니다. 먼저 크롤러를 돌려주세요.")
        return

    for img_filename in images:
        char_id = os.path.splitext(img_filename)[0]
        
        character_data = {
            "id": char_id,
            "name": f"수감자 ({char_id[-3:]})", 
            "affiliation": "Limbus Company",
            "weapon": "미확인 무기",
            "image_url": f"/images/characters/{img_filename}"
        }

        json_path = os.path.join(JSON_DIR, f"{char_id}.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(character_data, f, ensure_ascii=False, indent=2)

    print(f"🎉 현재 이미지와 완벽히 동기화된 {len(images)}개의 JSON 파일이 생성되었습니다!")

if __name__ == "__main__":
    generate_jsons_from_images()
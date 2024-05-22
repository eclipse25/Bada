# Bada

**FastAPI**와 **React**를 사용한 CRUD, RESTful API 기반 대나무숲 개발 프로젝트

## 주요 기능

#### 1차 개발 목표

- 국내 학교 정보 api, 데이터베이스를 활용한 학교 검색 (완료)
- 학교 검색 결과를 통한 게시판 레코드 생성과 페이지 접속 (완료)
- 게시글 작성과 해당하는 게시판에 렌더링(완료)
- 게시물별 댓글 작성 기능(완료)
- 쿠키를 이용한 좋아요 기능(진행중)
- 쿠키를 이용한 방문했던 게시판 메뉴바에 표시
- 게시물 작성 시점에 입력한 키를 통해 게시물 삭제 가능
- 메인 페이지에 모든 게시물, 추천수 상위 게시물 노출
- 게시물 검색 기능(태그, 검색어)

#### 1.5차 개발 목표

- AWS EC2, Nginx, Gunicorn을 활용한 배포
  - HTTPS 적용

#### 2차 개발 목표

- 게시판 카테고리 추가
  - 국내 지역구 (api 활용)
  - 국내 회사 목록 (api를 활용)
  - 신청에 의한 생성 (가상의 집단, 소규모)
- 단순 식별번호를 통한 메세지 기능
- 게시물 추천 세션별 1회
- 추천수 상위 게시물 선정시 일간 혹은 실시간 집계

#### 2.5차 개발 목표

- AWS RDS의 Postgresql로 DB 마이그레이션
- 도메인 이름 구매 + 적용

#### 3차 개발 목표

- AI api를 활용한 광고, 불건전 게시물 등 이슈게시물 필터링
- 구글 애드센스 적용
- 서버 추가 + 로드밸런싱

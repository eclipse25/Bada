# Bada

**FastAPI**와 **React**를 사용한 CRUD, RESTful API 기반 대나무숲 개발 프로젝트

## 주요 기능

#### 1차 개발 목표

- 국내 학교 정보 api, 데이터베이스를 활용한 학교 검색 (완료)
- 학교 검색 결과를 통한 게시판 페이지 접속 (완료)
- 첫 게시물 생성을 통한 해당 게시판 데이터 항목 생성과 페이지 개발 (진행중)
- 게시물 작성 시점에 입력한 키를 통해 게시물 삭제 가능
- 메인 페이지에 추천수 상위 게시물 노출
- 게시물 검색 기능

#### 1.5차 개발 목표

- AWS EC2, Nginx, Gunicorn을 활용한 배포
  - HTTPS 적용

#### 2차 개발 목표

- 게시판 즐겨찾기를 위한 로그인 or 쿠키 활용
  - 메뉴바에 즐겨찾기한 게시판 고정
- 게시판 생성
  - 국내 지역구 api 활용
  - 국내 회사 목록 api를 활용
  - 가상의 집단, 신청에 의한 생성
- 단순 식별번호를 통한 메세지 기능
- 개시글에 게시 기간 선택
- 게시물 추천을 로그인 시 3회까지, 비로그인시 세션별 1회
- 추천수 상위 게시물 선정시 일간 혹은 실시간 집계

#### 2.5차 개발 목표

- AWS RDS의 Postgresql로 DB 마이그레이션
- 도메인 이름 구매 + 적용

#### 3차 개발 목표

- AI api를 활용한 광고, 불건전 게시물 등 이슈게시물 필터링
- 프로페셔널 계정의 광고, 공고 게시 지원
- 서버 추가 + 로드밸런싱

## 추가 프로젝트 진행 개요

- 백엔드 개발 → 프론트엔드 개발 반복으로 Agile한 개발
- 팀원이 더 생길 경우 Notion 활용(절찬리 모집중! `yk99902@naver.com`)

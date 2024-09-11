create database blog_db;

drop table if exists blog;

create table blog_db.blog
(id integer auto_increment primary key,
title varchar(200) not null,
author varchar(100) not null,
content varchar(4000) not null,
image_loc varchar(300) null,
modified_dt datetime not null
);

truncate table blog;

insert into blog(title, author, content, modified_dt)
values ('FastAPI는 어떤 장점이 있는가?', '둘리', 
'FastAPI는 Python을 사용한 웹 애플리케이션 및 API 개발을 위한 현대적인 프레임워크로, 빠른 성능과 쉬운 사용성, 자동 문서화, 그리고 모던한 설계가 주요 장점입니다. \n
비동기 I/O 기능을 활용하여 높은 성능을 자랑하며, Python의 타입 힌트를 적극 활용해 타입 검사와 코드 자동 완성이 뛰어나 개발자가 실수를 줄이고 생산성을 높일 수 있습니다. \n
또한, 자동으로 API 문서를 생성하고 유지해주어 개발자가 인터랙티브한 문서를 쉽게 제공할 수 있습니다. \n
최신 웹 표준과 기술을 반영한 설계로 확장성과 유지보수성이 뛰어나며, 빠르게 성장하는 커뮤니티와 생태계를 통해 다양한 플러그인과 확장 기능을 지원받을 수 있습니다.'
, now());

insert into blog(title, author, content, modified_dt)
values ('FastAPI 주요 요소는 무엇인가', '고길동', 
'FastAPI의 주요 구성 요소에는 클라이언트로부터 받은 HTTP 요청을 처리하는 Request 객체와 서버에서 클라이언트로 보내는 HTTP 응답을 생성하는 Response 객체가 포함됩니다.\n
 또한, 경로와 경로 동작을 정의하여 API 엔드포인트를 설정하고, 의존성 주입을 통해 코드의 모듈화와 재사용성을 높일 수 있습니다.\n
 요청 바디는 Pydantic 모델을 사용해 자동으로 유효성 검사되며, 경로 및 쿼리 매개변수로 API 요청에서 전달되는 데이터를 처리합니다. \n
 FastAPI는 OpenAPI와 JSON Schema를 기반으로 API 문서를 자동 생성하며, Swagger UI와 ReDoc을 통해 실시간으로 API를 탐색하고 테스트할 수 있는 기능을 제공합니다.\n
 템플릿 렌더링 기능을 통해 HTML 페이지를 동적으로 생성할 수 있어, API뿐만 아니라 전체 웹 애플리케이션도 쉽게 구축할 수 있습니다.'
, now());

insert into blog(title, author, content, modified_dt)
values ('FastAPI를 어떻게 사용하면 좋을까요?', '도우넛', 
'FastAPI는 빠른 성능과 간단한 사용성 덕분에 다양한 분야에서 널리 사용되고 있습니다.\n
FastAPI는 고성능 API 서버 구축, 머신 러닝 모델 서빙, 마이크로서비스 아키텍처, 실시간 데이터 처리 애플리케이션, 백엔드 API 서버, 그리고 CRUD 애플리케이션 개발 등 다양한 분야에서 사용됩니다.\n
특히, 비동기 처리를 통한 빠른 성능과 자동 문서화 기능 덕분에 실시간 데이터 처리나 챗봇, IoT 애플리케이션 같은 응답 속도가 중요한 프로젝트에 적합합니다.\n
또한, 웹 애플리케이션의 백엔드 API 서버로 사용되거나, Pydantic과 SQLAlchemy 같은 라이브러리와 결합해 CRUD 애플리케이션을 빠르고 효율적으로 개발할 수 있습니다.\n
FastAPI는 다양한 규모와 유형의 프로젝트에서 성능과 개발 효율성을 높이는 데 큰 역할을 합니다.'
, now());

COMMIT;


create table user
(
    id integer auto_increment primary key,
    name varchar(100) not null,
    email varchar(100) not null unique,
    hashed_password varchar(200) not null
);

/* connection 모니터링 스크립트. root로 수행 필요. */
select * from sys.session where db='blog_db' order by conn_id;
# PAA Server
PAA Portfolio 용 RESTful API Server
- Endpoint : [https://smtp-ku.appspot.com](https://smtp-ku.appspot.com)

## API
### admin
 - `/admin/` : 관리자 페이지
### ticker
- `/ticker/` : 전체 Ticker List
- `/ticker/[id]` : 해당 ID의 Ticker 정보
### price
- `/price/monthly/` : 전체 월별 가격 List
- `/price/daily/` : 전체 일별 가격 List
- `/price/monthly/?lb=[lookback_period]` : Lookback Period 기준 월별 가격 List
- `/price/daily/?lb=[lookback_period]` : Lookback Period 기준 일별 가격 List

## Project Description
 - [Django](https://www.djangoproject.com/)
 - [Django REST framework](https://www.django-rest-framework.org/)
 - [Google Cloud SQL](https://console.cloud.google.com/sql/)
 - [Alpha Vantage](https://www.alphavantage.co/documentation/#) API
    - (차후 금융 API 유동성+학습 목적으로 라이브러리 미활용)
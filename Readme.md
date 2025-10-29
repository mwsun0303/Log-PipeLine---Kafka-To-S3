# Log PipeLine - Kafka To S3

## 프로젝트 개요

**Kafka To S3** 은 Kafka Topic에 저장된 Json 형태의 로그 데이터를 실시간으로 수신하여  
S3에 Batch(Bulk)로 저장하는 **Log Consumer** Applicaion.

Kafka Producer(예: Log To Kafka)에서 전송한 로그 데이터를  
실시간 수집 및 저장을 통해 **Logging DB** 구성

S3 + Athena 구성 필요

**deploy.sh** 를 통해 Build & Deploy

---

## 버전 정보

| 구성 요소 | 버전 |
|------------|-------|
| Python     | 3.10  |
| OS Base    | Debian slim |
| Docker     | 최신 (23.x 이상 권장) |
| Kafka      | 3.8 |
| 앱 버전    | v1.0.0 |

---

## 디렉터리 구조

```bash
project-root/
├── app.py                # Main Application 
├── requirements.txt      # Python Dependency
├── Dockerfile            # Docker File
├── deploy.sh             # Build & Deploy Script
└── README.md             

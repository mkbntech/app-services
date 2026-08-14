# TrailHead Supply Co. — Microservices (`app-services`)

[![Pipeline Status](https://gitlab.com/trailhead-supply-co/app-services/badges/main/pipeline.svg)](https://gitlab.com/trailhead-supply-co/app-services/-/commits/main)
![Kaniko Build](https://img.shields.io/badge/Build-Kaniko-orange?logo=docker&logoColor=white)
![Trivy Security Scan](https://img.shields.io/badge/Security-Trivy%20Scan-blue?logo=aquasec&logoColor=white)
![Skopeo Registry Sync](https://img.shields.io/badge/Registry-Skopeo-red?logo=redhat&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-blue.svg)

Core microservices repository for the **TrailHead Supply Co.** e-commerce platform. 

This repository manages **build and test automation** for four microservices: it runs unit & integration tests, builds un-pushed container images using rootless Kaniko, scans local image tarballs for vulnerabilities using Trivy, pushes verified images to Azure Container Registry (ACR) via Skopeo, and automatically updates image tags in the GitOps deployment repository ([`env-config-gitops`](../env-config-gitops)).

---

## Owner & Maintainer Information

* **Owner**: Trailhead Supply Co. Microservices & Engineering Team
* **Maintainers**: Application Engineering ([@mkbntech](https://github.com/mkbntech))
* **Repository**: [`trailhead-supply-co/app-services`](https://github.com/mkbntech/app-services.git)

---

## Microservices Architecture

| Service | Directory | Tech Stack | Port | Database / Persistence |
| :--- | :--- | :--- | :--- | :--- |
| **UI (Storefront)** | `services/ui-service` | Node.js 20 + Express + EJS | `3000` | Local Storage (theme state) |
| **Product Catalogue** | `services/catalogue-service` | Python 3.12 + FastAPI | `8001` | In-memory JSON dataset |
| **Recommendation Engine** | `services/recommendation-service` | Go 1.22 | `8002` | Stateless algorithm |
| **Voting & Reviews** | `services/review-service` | Java 21 + Spring Boot + JPA | `8003` | PostgreSQL (`reviews-db`) / H2 fallback |

---

## Repository Layout

```text
app-services/
├── services/
│   ├── ui-service/             # Storefront UI (Node.js/Express, responsive theme toggle)
│   ├── catalogue-service/      # Product Catalogue API (FastAPI)
│   ├── recommendation-service/ # Product Recommendation Engine (Go)
│   └── review-service/         # Reviews & Ratings Service (Spring Boot + PostgreSQL)
├── monitoring/                 # Monitoring configurations & metrics scrapers
├── docker-compose.yml          # Local multi-container development environment
└── .gitlab-ci.yml              # Build, scan, push & GitOps auto-trigger pipeline
```

---

## Local Development

Run all microservices locally alongside a real PostgreSQL instance:

```bash
docker compose up --build
```

Access the application in your browser:
* **Storefront UI**: [http://localhost:3000](http://localhost:3000)
* **Catalogue API Docs**: [http://localhost:8001/docs](http://localhost:8001/docs)
* **Recommendation Health**: [http://localhost:8002/health](http://localhost:8002/health)
* **Review Service API**: [http://localhost:8003/api/reviews](http://localhost:8003/api/reviews)

## License

This repository is licensed under the [MIT License](LICENSE).
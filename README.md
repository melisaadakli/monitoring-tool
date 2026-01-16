#### **Monitoring \& Health Check Tool**



CLI-based Python tool for monitoring HTTP services and measuring response time with a DevOps / SRE mindset.

**Usage:**


python monitor.py --url https://example.com


**Development Progress**
---



**Day 1 — Project Setup \& CLI Skeleton**



**Goal:** Create a real CLI tool structure



**What was done:**



Project structure created



CLI argument parsing planned



Base files added (monitor.py, README, requirements.txt)



**Concepts:**



CLI design



Tool mindset



Project structuring





**Day 2 — HTTP Health Check**



**Goal:** Check if a service is reachable



**What was done:**



HTTP GET request using requests



Status code validation



Response time measurement



**Example Output:**



Status: UP

HTTP Code: 200

Response Time: 120 ms



**Concepts:**



HTTP fundamentals



Monitoring basics



Latency awareness





**Day 3 — Error Handling \& Stability**



**Goal:** Handle failures gracefully



**What was done:**



Exception handling for connection errors



Timeout detection



Clear and user-friendly error messages



**Concepts:**



Defensive programming



Troubleshooting mindset



Observability basics

 ### Day 4 — Exit Codes & CI/CD Compatibility
**Goal:** Make the tool automation-friendly

**What was done:**
- Exit codes added for monitoring systems
- `0` returned when service is healthy (UP)
- `1` returned when service is unhealthy (DOWN)

**Why this matters:**
- Enables usage in CI/CD pipelines
- Compatible with cron jobs, schedulers, and monitoring tools

**Concepts:**
- Unix exit codes
- CI/CD integration
- Production readiness

---

### Day 5 — Logging & Structured Output
**Goal:** Improve observability and integrations

**What was done:**
- File-based logging using Python `logging`
- Timestamped and structured log entries
- Optional JSON output for integrations (`--json` flag)

**Example Log Entry:**
```text
2026-01-16 21:59:05 INFO target=https://example.com status=UP code=200 time_ms=2301 attempts=1
Example JSON Output:

json
Kodu kopyala
{
  "target": "https://example.com",
  "status": "UP",
  "attempts_used": 1,
  "retries_configured": 3,
  "http_code": 200,
  "response_time_ms": 670,
  "error": null
}
Concepts:

Logging & observability

Structured output

Tool integration readiness



**What This Project Demonstrates:**



Practical Python usage for system tooling



Monitoring \& health check concepts



CLI tool development



Error handling and resilience



DevOps / SRE-oriented thinking





**Author**

Melisa Adaklı Mertdoğan


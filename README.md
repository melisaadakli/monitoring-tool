# Monitoring Tool

A simple but production-oriented Python CLI tool for monitoring HTTP services.
It performs health checks, measures response time, supports retries, logging,
JSON output, and configuration files.

This project was built incrementally to demonstrate a DevOps / SRE-oriented
approach to tool development.

---

## Features
- HTTP health checks with retry logic
- Response time measurement (milliseconds)
- Exit codes for CI/CD compatibility (0 = UP, 1 = DOWN)
- File-based logging with timestamps
- Optional JSON output for integrations
- Config file support for environment-based configuration

---

## Installation

```bash
pip install -r requirements.txt
Usage
Basic check
bash
Kodu kopyala
python monitor.py --url https://example.com
Using a config file
bash
Kodu kopyala
python monitor.py --config config.json
Config + CLI override
bash
Kodu kopyala
python monitor.py --config config.json --retries 1
JSON output (for integrations)
bash
Kodu kopyala
python monitor.py --url https://example.com --json
Exit code example (PowerShell)
powershell
Kodu kopyala
python monitor.py --url https://example.com
echo $LASTEXITCODE
Logging
Each execution writes a structured log entry to monitor.log.

Example log entry:

text
Kodu kopyala
2026-01-16 21:59:05 INFO target=https://example.com status=UP code=200 time_ms=2301 attempts=1
Configuration File
Example config.json:

json
Kodu kopyala
{
  "url": "https://example.com",
  "retries": 3,
  "delay": 1,
  "timeout": 5,
  "log_file": "monitor.log"
}
CLI arguments always override values from the config file.

Development Progress
Day 1–3
Project setup and CLI skeleton

HTTP health check implementation

Retry logic and response time measurement

Day 4
Exit codes added for CI/CD and schedulers

Tool made automation-friendly

Day 5
Logging with timestamps and structured messages

Optional JSON output for integrations

Day 6
Config file support (--config)

CLI override logic for flexible environments

Day 7
Documentation polished

requirements.txt and .gitignore added

Project finalized for public use

What This Project Demonstrates
Practical Python usage for system tooling

Monitoring and troubleshooting mindset

CLI tool design

Observability (logging, structured output)

DevOps / SRE-oriented thinking
import argparse
import requests
import time
import sys
import logging
import json
def load_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def setup_logger(log_file="monitor.log"):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )

def check_health_once(url, timeout=5):
    start_time = time.time()

    response = requests.get(url, timeout=timeout)
    response_time = int((time.time() - start_time) * 1000)

    status = "UP" if response.status_code < 400 else "DOWN"

    return {
        "status": status,
        "code": response.status_code,
        "time": response_time,
    }


def check_health_with_retry(url, retries=3, delay=2, timeout=5):
    last_error = None

    for attempt in range(1, retries + 1):
        try:
            result = check_health_once(url, timeout=timeout)
            result["attempt"] = attempt

            # Başarılı sayılma kriteri: status UP
            if result["status"] == "UP":
                return result

            # 4xx/5xx geldi -> DOWN sayıyoruz, retry devam edebilir
            last_error = f"HTTP {result['code']}"

        except requests.exceptions.RequestException as e:
            last_error = str(e)

        # Son attempt değilse bekle
        if attempt < retries:
            print(f"Attempt {attempt} failed ({last_error}). Retrying in {delay}s...")
            time.sleep(delay)

    # Buraya geldiysek: tüm denemeler başarısız
    return {
        "status": "DOWN",
        "error": last_error,
        "attempt": retries,
    }


def main():
    parser = argparse.ArgumentParser(description="Simple HTTP health check tool with retry logic")

    parser.add_argument(
    "--config",
    help="Path to JSON config file",
    )

    parser.add_argument(
        "--url",
        help="Target URL to monitor (e.g. https://example.com)",
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=3,
        help="Number of retry attempts (default: 3)",
    )
    parser.add_argument(
        "--delay",
        type=int,
        default=2,
        help="Delay between retries in seconds (default: 2)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=5,
        help="Request timeout in seconds (default: 5)",
    )
    parser.add_argument(
        "--log-file",
        default="monitor.log",
        help="Log file path (default: monitor.log)",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Print output as JSON",
    )


    args = parser.parse_args()
    # Load config file if provided
    if args.config:
        cfg = load_config(args.config)

        if not args.url:
            args.url = cfg.get("url")

        if args.retries == 3:  # default value
            args.retries = cfg.get("retries", args.retries)

        if args.delay == 1:    # default value
            args.delay = cfg.get("delay", args.delay)

        if args.timeout == 5:  # default value
            args.timeout = cfg.get("timeout", args.timeout)

        if args.log_file == "monitor.log":
            args.log_file = cfg.get("log_file", args.log_file)
    setup_logger(args.log_file)

    result = check_health_with_retry(
        args.url,
        retries=args.retries,
        delay=args.delay,
        timeout=args.timeout,
    )
        # log line (tek satır özet)
    if result["status"] == "UP":
        logging.info(
            'target=%s status=UP code=%s time_ms=%s attempts=%s',
            args.url, result.get("code"), result.get("time"), result.get("attempt")
        )
    else:
        logging.error(
            'target=%s status=DOWN error="%s" attempts=%s',
            args.url, result.get("error"), result.get("attempt")
        )
    payload = {
        "target": args.url,
        "status": result["status"],
        "attempts_used": result.get("attempt"),
        "retries_configured": args.retries,
        "http_code": result.get("code"),
        "response_time_ms": result.get("time"),
        "error": result.get("error"),
    }

    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print("\n--- HEALTH CHECK REPORT ---")
        print(f"Target: {args.url}")
        print(f"Attempts: {result.get('attempt')} / {args.retries}")

        if result["status"] == "UP":
            print("Status: UP ✅")
            print(f"HTTP Code: {result['code']}")
            print(f"Response time: {result['time']} ms")
        else:
            print("Status: DOWN ❌")
            print(f"Last error: {result.get('error')}")

    # Exit codes for CI/CD and schedulers
    sys.exit(0 if result["status"] == "UP" else 1)

if __name__ == "__main__":
    main()

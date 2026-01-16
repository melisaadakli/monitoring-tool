import argparse
import requests
import time


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
        "--url",
        required=True,
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

    args = parser.parse_args()

    result = check_health_with_retry(
        args.url,
        retries=args.retries,
        delay=args.delay,
        timeout=args.timeout,
    )

    print("\n--- HEALTH CHECK REPORT ---")
    print(f"Target: {args.url}")
    print(f"Attempts: {result.get('attempt')} / {args.retries}")

    if result["status"] == "UP":
        print(f"Status: UP ✅")
        print(f"HTTP Code: {result['code']}")
        print(f"Response time: {result['time']} ms")
    else:
        print("Status: DOWN ❌")
        print(f"Last error: {result.get('error')}")


if __name__ == "__main__":
    main()

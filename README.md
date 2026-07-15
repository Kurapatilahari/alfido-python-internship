# Task 2: API Integration & JSON Handling

## Goal
Learn how Python communicates with external APIs and handles JSON data.

## What This Script Does
- Fetches live data using the **`requests`** library from a free public API
  ([JSONPlaceholder](https://jsonplaceholder.typicode.com))
- Parses the JSON response into Python objects
- Applies **filtering** (by city) and **search** (by name) logic
- Handles API errors gracefully: connection errors, timeouts, bad status codes,
  and invalid JSON — the script never crashes
- Saves the final filtered results to `users_output.json`

## Setup
```bash
pip install -r requirements.txt
```

## How to Run
```bash
python3 api_integration.py
```

## Sample Output (abridged)
```
======================================================================
TASK 2: API INTEGRATION & JSON HANDLING
======================================================================
[OK] Fetched data from https://jsonplaceholder.typicode.com/users (status 200)

Total users fetched: 10

--- All Users ---
ID | Name                 | Email                       | City
----------------------------------------------------------------------
 1 | Leanne Graham        | Sincere@april.biz           | Gwenborough
 2 | Ervin Howell         | Shanna@melissa.tv           | Wisokyburgh
 ...

--- Filter: cities containing 'south' ---
 5 | Chelsey Dietrich     | Lucio_Hettinger@annie.ca    | South Elvis

--- Search: names containing 'a' ---
 1 | Leanne Graham        | Sincere@april.biz           | Gwenborough
 ...

--- Demonstrating error handling (bad endpoint) ---
[ERROR] HTTP error from https://jsonplaceholder.typicode.com/this-endpoint-does-not-exist: 404 Client Error
[OK] Error was handled gracefully, script did not crash.

[OK] Saved output to users_output.json

[DONE] API integration task complete.
```

## Key Concepts Demonstrated
| Concept | Where |
|---|---|
| Fetching data | `fetch_data()` using `requests.get()` |
| Parsing JSON | `response.json()` |
| Filtering | `filter_users_by_city()` |
| Search logic | `search_users_by_name()` |
| Error handling | `try/except` for `ConnectionError`, `Timeout`, `HTTPError`, `RequestException`, `JSONDecodeError` |
| Saving results | `save_json()` writes formatted JSON to disk |

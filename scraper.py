def get_market_prices(title, issue, grade):
    # In a real version, you’d scrape or query actual listings based on title/issue/grade.
    # This mock returns a price range based on grade

    grade_price_map = {
        '9.8': 400,
        '9.6': 350,
        '9.4': 300,
        '9.2': 250,
        '9.0': 200,
        '8.5': 180,
        '8.0': 160,
        '7.5': 140,
        '7.0': 120,
        '6.5': 100,
        '6.0': 80
    }

    return grade_price_map.get(grade, 50)

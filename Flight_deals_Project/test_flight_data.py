from flight_data import find_cheapest_flight


def _flight(price, segments):
    return {
        "price": price,
        "flights": [
            {
                "departure_airport": {"id": dep, "time": f"2026-05-10 {9 + i:02d}:00"},
                "arrival_airport": {"id": arr, "time": f"2026-05-10 {10 + i:02d}:00"},
            }
            for i, (dep, arr) in enumerate(segments)
        ],
    }


def test_no_data_returns_placeholder():
    result = find_cheapest_flight(None, return_date="2026-06-08")
    assert result.price == "N/A"
    result = find_cheapest_flight({}, return_date="2026-06-08")
    assert result.price == "N/A"


def test_picks_cheapest_flight_with_its_own_stop_count():
    data = {
        "best_flights": [_flight(50000, [("LHR", "DPS")])],
        "other_flights": [_flight(30000, [("LHR", "SIN"), ("SIN", "DPS")])],
    }
    result = find_cheapest_flight(data, return_date="2026-06-08")
    assert result.price == 30000
    assert result.origin_airport == "LHR"
    assert result.destination_airport == "DPS"
    assert result.out_date == "2026-05-10"
    assert result.return_date == "2026-06-08"
    assert result.stops == 1


def test_skips_flights_without_price():
    data = {"best_flights": [_flight(40000, [("LHR", "DPS")]), {"flights": []}]}
    result = find_cheapest_flight(data, return_date="2026-06-08")
    assert result.price == 40000
    assert result.stops == 0

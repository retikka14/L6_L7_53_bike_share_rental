
import pytest

from bike_share_rental import ride_cost, dock_status, can_unlock


# ==========================================
# RIDE COST TESTS
# ==========================================

def test_unknown_bike_type():
    with pytest.raises(ValueError):
        ride_cost("mountain", 30, False, False)


def test_invalid_duration():
    with pytest.raises(ValueError):
        ride_cost("standard", 0, False, False)


def test_standard_ride():
    assert ride_cost("standard", 45, False, False) == 40


def test_electric_ride():
    assert ride_cost("electric", 30, False, False) == 35


def test_cargo_ride():
    assert ride_cost("cargo", 30, False, False) == 50


def test_subscriber_free_ride():
    assert ride_cost("standard", 30, True, False) == 0


def test_subscriber_pays_after_free_block():
    assert ride_cost("electric", 60, True, False) == 35


def test_peak_hour_standard():
    assert ride_cost("standard", 30, False, True) == 35


def test_long_ride_surcharge():
    assert ride_cost("standard", 181, False, False) == 240


# ==========================================
# DOCK STATUS TESTS
# ==========================================

def test_invalid_capacity():
    with pytest.raises(ValueError):
        dock_status(0, 0)


def test_negative_bike_count():
    with pytest.raises(ValueError):
        dock_status(-1, 10)


def test_bike_count_exceeds_capacity():
    with pytest.raises(ValueError):
        dock_status(11, 10)


def test_empty_dock():
    assert dock_status(0, 10) == "empty"


def test_full_dock():
    assert dock_status(10, 10) == "full"


def test_few_bikes():
    assert dock_status(2, 10) == "few bikes"


def test_few_slots():
    assert dock_status(8, 10) == "few slots"


def test_available_dock():
    assert dock_status(5, 10) == "available"


# ==========================================
# CAN UNLOCK TESTS
# ==========================================

def test_active_ride_prevents_unlock():
    assert can_unlock(500, True, 25) is False


def test_underage_rider():
    assert can_unlock(500, False, 15) is False


def test_minor_insufficient_balance():
    assert can_unlock(99, False, 16) is False


def test_minor_sufficient_balance():
    assert can_unlock(100, False, 17) is True


def test_adult_insufficient_balance():
    assert can_unlock(49, False, 18) is False


def test_adult_sufficient_balance():
    assert can_unlock(50, False, 25) is True

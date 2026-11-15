import pytest
from coffee_shop_order import process_order_batch, check_espresso_machine


def order(**kwargs):
    item = {"paid": True, "size": "medium", "strict_allergy": False,
            "is_member": False, "customizations": []}
    item.update(kwargs)
    return item


def test_empty_and_unpaid():
    assert process_order_batch([], 0) == {"total": 0.0, "status": "NO_SALE"}
    assert process_order_batch([order(paid=False)], .1)["status"] == "NO_SALE"


def test_all_sizes_and_unknown_size():
    assert process_order_batch([order(size="small"), order(size="medium"), order(size="large")], 0)["total"] == 13.5
    assert process_order_batch([order(size="jumbo")], 0)["status"] == "NO_SALE"


def test_customization_paths_and_syrup_cap():
    result = process_order_batch([order(customizations=[{"type": "syrup", "cost": 2}, {"type": "standard", "cost": .5}])], 0)
    assert result["total"] == 6.5
    assert process_order_batch([order(customizations=[{"type": "standard", "cost": -1}])], 0)["status"] == "NO_SALE"


def test_allergy_paths():
    alert = {"type": "allergen_alert", "cost": 0}
    assert process_order_batch([order(customizations=[alert])], 0)["total"] == 4.5
    assert process_order_batch([order(strict_allergy=True, customizations=[alert])], 0)["status"] == "NO_SALE"


def test_membership_tax_and_audit_threshold():
    assert process_order_batch([order(is_member=True)], .1)["total"] == 4.46
    assert process_order_batch([order(size="bad") for _ in range(5)], 0)["status"] == "AUDIT_REJECTED"
    assert process_order_batch([order(size="bad") for _ in range(4)], 0)["status"] == "NO_SALE"


def test_invalid_batch_inputs_and_bad_records():
    with pytest.raises(ValueError):
        process_order_batch("not-list", .1)
    for rate in [-.1, float("nan"), float("inf"), "0.1", True]:
        with pytest.raises(ValueError):
            process_order_batch([], rate)
    assert process_order_batch([None, order(customizations="bad"), order(customizations=[None])], 0)["status"] == "NO_SALE"
    assert process_order_batch([order(customizations=[{"type": "x", "cost": "bad"}])], 0)["status"] == "NO_SALE"


def test_espresso_no_data_and_optimal():
    assert check_espresso_machine([]) == "NO_DATA"
    assert check_espresso_machine([[], [95, 96]]) == "OPTIMAL"


def test_espresso_shutdown_and_streak_reset():
    assert check_espresso_machine([[97, 98]]) == "SHUTDOWN"
    assert check_espresso_machine([[97, 96, 97, 98]]) == "SHUTDOWN"
    assert check_espresso_machine([[97, 96, 97]]) == "OPTIMAL"


def test_espresso_invalid_data():
    for value in ["bad", ["bad-cycle"], [["hot"]], [[float("nan")]]]:
        with pytest.raises(ValueError):
            check_espresso_machine(value)

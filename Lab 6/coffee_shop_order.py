"""Coffee shop order processing and espresso-machine safety checks."""
import math


def process_order_batch(orders, tax_rate):
    """Calculate a batch total; invalid records are rejected rather than crashing."""
    if not isinstance(orders, list):
        raise ValueError("orders must be a list")
    if isinstance(tax_rate, bool) or not isinstance(tax_rate, (int, float)):
        raise ValueError("tax_rate must be a finite non-negative number")
    if not math.isfinite(float(tax_rate)) or tax_rate < 0:
        raise ValueError("tax_rate must be a finite non-negative number")

    batch_total = 0.0
    rejected_items = 0
    for order in orders:
        if not isinstance(order, dict):
            rejected_items += 1
            continue
        if not order.get("paid", False):
            continue

        prices = {"small": 3.0, "medium": 4.5, "large": 6.0}
        size = order.get("size", "medium")
        if size not in prices:
            rejected_items += 1
            continue

        customizations = order.get("customizations", [])
        if not isinstance(customizations, list):
            rejected_items += 1
            continue

        item_total = prices[size]
        invalid_customization = False
        strict_allergy_rejection = False
        for mod in customizations:
            if not isinstance(mod, dict):
                rejected_items += 1
                invalid_customization = True
                break
            mod_type = mod.get("type", "")
            cost = mod.get("cost", 0.0)
            if (isinstance(cost, bool) or not isinstance(cost, (int, float))
                    or not math.isfinite(float(cost)) or cost < 0):
                rejected_items += 1
                invalid_customization = True
                break

            if mod_type == "allergen_alert":
                rejected_items += 1
                if order.get("strict_allergy", False):
                    strict_allergy_rejection = True
                    break
            elif mod_type == "syrup":
                item_total += min(float(cost), 1.5)
            else:
                item_total += float(cost)

        if invalid_customization or strict_allergy_rejection:
            continue
        if order.get("is_member", False):
            item_total *= 0.90
        batch_total += item_total

    final_total = batch_total * (1 + float(tax_rate))
    if rejected_items > 4:
        return {"total": round(final_total, 2), "status": "AUDIT_REJECTED"}
    if batch_total == 0.0:
        return {"total": 0.0, "status": "NO_SALE"}
    return {"total": round(final_total, 2), "status": "COMPLETED"}


def check_espresso_machine(temperature_cycles):
    """Shutdown after two consecutive readings above 96°C, resetting per cycle."""
    if not temperature_cycles:
        return "NO_DATA"
    if not isinstance(temperature_cycles, (list, tuple)):
        raise ValueError("temperature_cycles must be a sequence of cycles")
    for cycle in temperature_cycles:
        if not isinstance(cycle, (list, tuple)):
            raise ValueError("each temperature cycle must be a sequence")
        overheat_streak = 0
        for temp in cycle:
            if isinstance(temp, bool) or not isinstance(temp, (int, float)):
                raise ValueError("temperature readings must be numeric")
            if not math.isfinite(float(temp)):
                raise ValueError("temperature readings must be finite")
            if temp > 96.0:
                overheat_streak += 1
                if overheat_streak >= 2:
                    return "SHUTDOWN"
            else:
                overheat_streak = 0
    return "OPTIMAL"

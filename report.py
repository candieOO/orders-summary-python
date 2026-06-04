
def get_orders_summary(*, data, from_, to, group_by, min_amount=None):
    filtered_orders = []

    for order in data:
        order_date = order["orderDate"]

        if from_ <= order_date <= to:
            total = 0

            for item in order["items"]:
                total += item["quantity"] * item["unitPrice"]

            if min_amount is None or total >= min_amount:
                order["_computed_total"] = total
                filtered_orders.append(order)

    grouped = {}

    for order in filtered_orders:
        if group_by == "day":
            key = order["orderDate"]
        else:
            key = order["customerId"]

        if key not in grouped:
            grouped[key] = {
                "key": key,
                "count": 0,
                "totalAmount": 0,
            }

        grouped[key]["count"] += 1
        grouped[key]["totalAmount"] += order["_computed_total"]

    results = []

    for key in sorted(grouped.keys()):
        group = grouped[key]

        avg = group["totalAmount"] / group["count"]

        results.append({
            "key": group["key"],
            "count": group["count"],
            "totalAmount": group["totalAmount"],
            "avgAmount": avg,
        })

    return results

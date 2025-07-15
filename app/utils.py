
def stats_cart(cart):
    total_price, total_quantity = 0, 0
    if cart:
        for c in cart.values():
            total_quantity += c["quantity"]
            total_price += c["price"] * c["quantity"]

    return {
        "Total_price" : total_price,
        "Total_quantity": total_quantity
    }

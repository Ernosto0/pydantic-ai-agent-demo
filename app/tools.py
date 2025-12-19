"""Tool functions for the e-commerce support agent."""

import random


def get_order_status(order_id: str) -> str:
    """
    Get the current status of an order.
    
    Args:
        order_id: The order ID to check.
        
    Returns:
        The order status as a string.
    """
    # Fake logic: randomly return a status based on order_id hash
    statuses = ["Preparing", "Shipped", "Delivered", "Processing", "Out for Delivery"]
    # Use order_id to generate consistent status for same order
    index = hash(order_id) % len(statuses)
    status = statuses[index]
    
    # Add some extra context
    if status == "Shipped":
        return f"Order {order_id} is Shipped. Expected delivery in 2-3 business days."
    elif status == "Delivered":
        return f"Order {order_id} was Delivered on the expected date."
    elif status == "Out for Delivery":
        return f"Order {order_id} is Out for Delivery. It should arrive today!"
    else:
        return f"Order {order_id} is currently {status}."


def start_return(order_id: str) -> str:
    """
    Initiate a return request for an order.
    
    Args:
        order_id: The order ID to return.
        
    Returns:
        Confirmation message for the return request.
    """
    # Fake logic: always succeed
    return_id = f"RET-{order_id[-4:].upper()}-{random.randint(1000, 9999)}"
    return (
        f"Return request created successfully for order {order_id}. "
        f"Your return ID is {return_id}. "
        f"Please ship the item within 14 days using the prepaid label we'll email you."
    )



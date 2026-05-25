def should_serve_customer(customer_age, on_break, time): 
    # NOTE: Time does not have datetime.datetime(5:00PM - 10:00PM)
    return (customer_age >= 21) and (on_break == False) and (time >= 5 and time <= 10)


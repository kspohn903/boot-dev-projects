def exponential_growth(n, factor, days):
    return [n * (factor ** day) for day in range(days + 1)]

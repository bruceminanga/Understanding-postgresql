def calculate_price(academic_level, service_type, currency):
    base_prices = {'high_school': 10, 'undergraduate': 20, 'masters': 30, 'phd': 40}
    service_multipliers = {'writing': 1, 'editing': 0.8, 'proofreading': 0.6}
    currency_rates = {'USD': 1, 'EUR': 0.85, 'GBP': 0.75, 'KES': 110.15}
    base_price = base_prices[academic_level]
    service_multiplier = service_multipliers[service_type]
    currency_rate = currency_rates[currency]
    price = base_price * service_multiplier * currency_rate
    return price
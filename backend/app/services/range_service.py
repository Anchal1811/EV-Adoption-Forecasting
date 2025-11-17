# backend/app/services/range_service.py

def calculate_remaining_range(battery_level: float, battery_kwh: float, consumption_per_km: float = 0.15):
    """
    Estimate remaining driving range.
    consumption_per_km default: 0.15 kWh per km (average for EVs)
    """
    remaining_energy_kwh = (battery_level / 100) * battery_kwh
    remaining_km = remaining_energy_kwh / consumption_per_km
    return round(remaining_km, 2)

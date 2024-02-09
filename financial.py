def generate_solar_system_report(area_m2, azimuth_degrees, pitch_degrees, electric_yield, monthly_electrical_bill):
    print(f"Received Input Values - Area: {area_m2} sqm, Azimuth: {azimuth_degrees} degrees, Pitch: {pitch_degrees} degrees, Electric Yield: {electric_yield} kWh/year, Monthly Electrical Bill: €{monthly_electrical_bill}")

    # Constants and Assumptions
    PANEL_EFFICIENCY = 0.18  # Average efficiency of solar panels
    PANEL_SIZE = 1.7  # Average size of a solar panel in square meters
    COST_PER_KW = 1500  # Updated cost per kW for solar systems
    LIFESPAN = 25  # Lifespan of the solar system in years
    CO2_SAVINGS_PER_KWH = 0.4  # Average CO2 savings per kWh produced
    AVERAGE_ELECTRICITY_RATE = 0.15  # Average electricity rate (€/kWh)

    # Step 1: Calculate potential system size based on area
    max_num_of_panels = area_m2 // PANEL_SIZE
    potential_system_size = max_num_of_panels * (PANEL_SIZE * PANEL_EFFICIENCY)
    print(f"Max Number of Panels: {max_num_of_panels}, Potential System Size: {potential_system_size} kW")

    # Step 2: Use the provided annual electric yield
    annual_yield = electric_yield
    print(f"Annual Electricity Production: {annual_yield} kWh")

    # Step 3: Estimate financial benefits based on monthly electrical bill
    annual_savings = (monthly_electrical_bill * 12) - (annual_yield * AVERAGE_ELECTRICITY_RATE)
    total_system_cost = potential_system_size * COST_PER_KW
    payback_period = total_system_cost / annual_savings if annual_savings != 0 else "Infinity"

    print(f"Annual Savings: €{annual_savings:.2f}, Total System Cost: €{total_system_cost:.2f}, Payback Period: {payback_period} years")

    # Step 4: Compute environmental benefits
    annual_co2_savings = annual_yield * CO2_SAVINGS_PER_KWH
    print(f"Annual CO₂ Savings: {annual_co2_savings:.2f} kg")

    # Step 5: Compile the report
    report = {
        "Potential System Size": f"{potential_system_size:.2f} kW",
        "Annual Electricity Production": f"{annual_yield:.2f} kWh",
        "Financial Benefits": {
            "Annual Savings": f"€{annual_savings:.2f}",
            "Total System Cost": f"€{total_system_cost:.2f}",
            "Payback Period": f"{payback_period} years"
        },
        "Environmental Benefits": f"{annual_co2_savings:.2f} kg CO₂ saved annually",
        "Lifespan": f"{LIFESPAN} years"
    }

    return report


def generate_solar_system_report(area_m2, azimuth_degrees, pitch_degrees, electric_yield, monthly_electrical_bill):
    print(f"Received Input Values - Area: {area_m2} sqm, Azimuth: {azimuth_degrees} degrees, Pitch: {pitch_degrees} degrees, Electric Yield: {electric_yield} kWh/year, Monthly Electrical Bill: €{monthly_electrical_bill}")

    # Constants and Assumptions
    PANEL_EFFICIENCY = 0.18  # Average efficiency of solar panels
    PANEL_SIZE = 1.7  # Average size of a solar panel in square meters
    COST_PER_KW = 1500  # Updated cost per kW for solar systems
    LIFESPAN = 25  # Lifespan of the solar system in years
    CO2_SAVINGS_PER_KWH = 0.4  # Average CO2 savings per kWh produced
    AVERAGE_ELECTRICITY_RATE = 0.15  # Average electricity rate (€/kWh)
    DEGRADATION_RATE = 0.005  # Annual degradation rate of panel efficiency
    EFFICIENCY_LOSS_ORIENTATION = 0.05  # Efficiency loss due to non-ideal orientation
    EFFICIENCY_LOSS_PITCH = 0.03  # Efficiency loss due to non-ideal pitch

    # Adjust efficiency based on orientation and pitch
    adjusted_efficiency = PANEL_EFFICIENCY * (1 - EFFICIENCY_LOSS_ORIENTATION) * (1 - EFFICIENCY_LOSS_PITCH)

    # Step 1: Calculate optimal system size based on monthly bill and electricity rate
    annual_consumption = (monthly_electrical_bill / AVERAGE_ELECTRICITY_RATE) * 12
    optimal_system_size_kw = annual_consumption / (365 * 24 * adjusted_efficiency)  # Convert to kW

    # Ensure the system size does not exceed the maximum possible installation size
    max_possible_system_size = (area_m2 / PANEL_SIZE) * PANEL_EFFICIENCY
    system_size_kw = min(optimal_system_size_kw, max_possible_system_size)

    print(f"Optimal System Size: {system_size_kw} kW, Adjusted for Installation Limit: {max_possible_system_size} kW")

    # Step 2: Estimate financial benefits
    # Adjust annual production for degradation over the lifespan
    annual_production_kwh = system_size_kw * 365 * 24 * adjusted_efficiency * (1 - DEGRADATION_RATE * LIFESPAN / 2)
    annual_savings = annual_production_kwh * AVERAGE_ELECTRICITY_RATE
    total_system_cost = system_size_kw * COST_PER_KW
    payback_period = total_system_cost / annual_savings

    print(f"Annual Savings: €{annual_savings:.2f}, Total System Cost: €{total_system_cost:.2f}, Payback Period: {payback_period:.2f} years")

    # Step 3: Compute environmental benefits
    annual_co2_savings = annual_production_kwh * CO2_SAVINGS_PER_KWH
    print(f"Annual CO₂ Savings: {annual_co2_savings:.2f} kg")

    # Step 4: Compile the report
    report = {
        "System Size kW": f"{system_size_kw:.2f} kW",
        "Adjusted Efficiency": f"{adjusted_efficiency:.2%}",
        "Annual Electricity Production": f"{annual_production_kwh:.2f} kWh",
        "Financial Benefits": {
            "Annual Savings": f"€{annual_savings:.2f}",
            "Total System Cost": f"€{total_system_cost:.2f}",
            "Payback Period": f"{payback_period:.2f} years"
        },
        "Environmental Benefits": f"{annual_co2_savings:.2f} kg CO₂ saved annually",
        "Lifespan": f"{LIFESPAN} years"
    }

    return report


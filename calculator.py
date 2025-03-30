# calculator.py
import pandas as pd

def calculate_emissions(scada_data, emission_factors):
    """
    Calculate GHG emissions based on SCADA data and emission factors.

    Tier 1 (Measured): If gas analyzer data is available (both CO2_ppm and flow_rate),
    emissions are computed as: CO2_ppm × flow_rate × conversion_factor.
    (For simplicity, we use a conversion factor of 0.001 to get kg CO₂e.)

    Tier 2 (Calculated): If analyzer data is not available, calculate emissions as:
         emissions = activity × emission_factor.

    Returns a DataFrame with:
      - Scope (e.g., Scope1, Scope2, Scope3)
      - Fuel type
      - Emissions (in kg CO₂e)
      - Method ("Measured" or "Calculated")
    """
    results = []
    for scope, data in scada_data.get("scope", {}).items():
        analyzer = data.get("analyzer_data", {})
        activity = data.get("activity", None)
        fuel = data.get("fuel", None)
        
        # Tier 1: Use measured gas analyzer data if available.
        if analyzer and analyzer.get("CO2_ppm") is not None and analyzer.get("flow_rate") is not None:
            co2_ppm = analyzer.get("CO2_ppm")
            flow_rate = analyzer.get("flow_rate")
            # Example conversion factor (simplified)
            emissions = co2_ppm * flow_rate * 0.001  
            method = "Measured"
        else:
            # Tier 2: Calculate emissions from activity data.
            factor_row = emission_factors[emission_factors['Fuel'] == fuel]
            if not factor_row.empty and activity is not None:
                emission_factor = factor_row.iloc[0]['EmissionFactor']
                emissions = activity * emission_factor
            else:
                emissions = 0
            method = "Calculated"
        
        results.append({
            "Scope": scope,
            "Fuel": fuel,
            "Emissions_kg_CO2e": emissions,
            "Method": method
        })
    
    return pd.DataFrame(results)

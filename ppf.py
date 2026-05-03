import numpy as np
import pandas as pd

from power_grid_model import (
    PowerGridModel,
    ComponentType,
    CalculationMethod,
)

from network_construction import (
    build_network_from_lines,
    print_network_summary,
)


def assign_loads_from_nodes_csv(
    input_data: dict,
    node_csv: str,
    node_to_load_index: dict,
    p_unit: str = "kW",
    q_unit: str = "kVAr",
):
    load_df = pd.read_csv(node_csv)

    # Unit conversion
    p_multiplier = {"W": 1, "kW": 1e3, "MW": 1e6}[p_unit]
    q_multiplier = {"var": 1, "kVAr": 1e3, "MVAr": 1e6}[q_unit]

    # Reset loads
    input_data[ComponentType.sym_load]["p_specified"][:] = 0.0
    input_data[ComponentType.sym_load]["q_specified"][:] = 0.0

    for _, row in load_df.iterrows():
        node_id = int(row["NODES"])

        if node_id not in node_to_load_index:
            continue

        idx = node_to_load_index[node_id]

        input_data[ComponentType.sym_load]["p_specified"][idx] = row["PD"] * p_multiplier
        input_data[ComponentType.sym_load]["q_specified"][idx] = row["QD"] * q_multiplier

    return input_data


def run_power_flow(line_csv: str, node_csv: str):
    

    #  Build network
    input_data, node_to_load_index, _ = build_network_from_lines(
        line_csv=line_csv,
        v_base_kV=11.0,
    )

    print_network_summary(input_data, node_to_load_index)

   
    # Assign loads
    input_data = assign_loads_from_nodes_csv(
        input_data=input_data,
        node_csv=node_csv,
        node_to_load_index=node_to_load_index,
        p_unit="kW",
        q_unit="kVAr",
    )

    print("\n------assigned load data------")
    print(pd.DataFrame(input_data[ComponentType.sym_load])[
        ["id", "node", "p_specified", "q_specified"]
    ])

   
    #  Create model
    model = PowerGridModel(input_data)

    
    # Run power flow
    output_data = model.calculate_power_flow(
        symmetric=True,
        error_tolerance=1e-8,
        max_iterations=20,
        calculation_method=CalculationMethod.newton_raphson,
    )

   
    #  Results
    print("\n------node result------")
    print(pd.DataFrame(output_data[ComponentType.node]))
    print("\n------line result------")
    print(pd.DataFrame(output_data[ComponentType.line]))

    return output_data



# Usage example

if __name__ == "__main__":
    line_csv = "data/Lines_34.csv"
    node_csv = "data/Nodes_34.csv"

    output = run_power_flow(line_csv, node_csv)
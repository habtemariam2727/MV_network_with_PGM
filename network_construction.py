import numpy as np
import pandas as pd
from power_grid_model import (
    CalculationType,
    ComponentType,
    DatasetType,
    LoadGenType,
    initialize_array,
)
from power_grid_model.validation import assert_valid_input_data


def build_network_from_lines(line_csv: str, v_base_kV: float = 11.0):
   
    # Read line data
    line_df = pd.read_csv(line_csv)
    n_nodes = int(max(line_df["FROM"].max(), line_df["TO"].max()))

    # create node components
    node = initialize_array(DatasetType.input, ComponentType.node, n_nodes)
    node["id"] = np.arange(1, n_nodes + 1)
    node["u_rated"] = np.full(n_nodes, v_base_kV * 1e3)  # Convert kV to V

    # create line components
    n_lines = len(line_df)
    line = initialize_array(DatasetType.input, ComponentType.line, n_lines)
    line["id"] = np.arange(100, 100 + n_lines)
    line["from_node"] = line_df["FROM"].to_numpy()
    line["to_node"] = line_df["TO"].to_numpy()
    line["from_status"] = line_df["STATUS"].to_numpy()
    line["to_status"] = line_df["STATUS"].to_numpy()
    line["r1"] = line_df["R"].to_numpy() 
    line["x1"] = line_df["X"].to_numpy() 
    line["c1"] = np.full(n_lines, 10e-6)  
    line["tan1"] = np.zeros(n_lines)     
    line["i_n"] = np.full(n_lines, 200.0)  # Rated current (A)

    # create symmetric load components
    load_nodes = np.arange(2, n_nodes + 1)
    n_loads = len(load_nodes)
    sym_load = initialize_array(DatasetType.input, ComponentType.sym_load, n_loads)
    sym_load["id"] = np.arange(200, 200 + n_loads)
    sym_load["node"] = load_nodes
    sym_load["status"] = np.ones(n_loads, dtype=int)
    sym_load["type"] = np.full(n_loads, LoadGenType.const_power)
    sym_load["p_specified"] = np.zeros(n_loads)  
    sym_load["q_specified"] = np.zeros(n_loads)  

    # create source component (slack bus)
    source = initialize_array(DatasetType.input, ComponentType.source, 1)
    source["id"] = [1000]
    source["node"] = [1]  # Node 1 is the slack bus
    source["status"] = [1]
    source["u_ref"] = [1.0]  # Reference voltage in per-unit

    # Compile all components into input data dictionary
    input_data = {
        ComponentType.node: node,
        ComponentType.line: line,
        ComponentType.sym_load: sym_load,
        ComponentType.source: source,
    }

    # Validate input data for power flow calculation
    assert_valid_input_data(
        input_data=input_data,
        calculation_type=CalculationType.power_flow,
        symmetric=True,
    )

    # Create mappings from node ID to array indices
    node_to_load_index = {int(n): i for i, n in enumerate(load_nodes)}

    return input_data, node_to_load_index,  n_nodes


def get_network_info(input_data: dict) -> dict:
    
    info = {
        "n_nodes": len(input_data[ComponentType.node]),
        "n_lines": len(input_data[ComponentType.line]),
        "n_loads": len(input_data[ComponentType.sym_load]),
        "n_sources": len(input_data[ComponentType.source]),
        "v_rated_kV": input_data[ComponentType.node]["u_rated"][0] / 1e3,
    }
    return info


def print_network_summary(input_data: dict, node_to_load_index: dict):
    
    info = get_network_info(input_data)
    
    print("\n" + "="*60)
    print("NETWORK SUMMARY")
    print("="*60)
    print(f"Nodes:           {info['n_nodes']}")
    print(f"Lines:           {info['n_lines']}")
    print(f"Load buses:      {info['n_loads']} (nodes 2..{info['n_nodes']})")
    print(f"Slack bus:       Node 1")
    print(f"Base voltage:    {info['v_rated_kV']:.1f} kV")
    print("="*60 + "\n")


if __name__ == "__main__":
  pass
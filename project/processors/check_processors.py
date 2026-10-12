
import json
from pathlib import Path

# Find the folder containing this Python file
project_folder = Path(__file__).parent
processor_folder = project_folder / "processors"

# Load and check both processor configurations
for filename in ["processor_A.json", "processor_B.json"]:
    file_path = processor_folder / filename

    with open(file_path, "r", encoding="utf-8") as file:
        processor = json.load(file)

    print(f"\n{processor['name']}")
    print("Number of qubits:", processor["num_qubits"])
    print("Connections:", processor["coupling_map"])
    print("Supported gates:", processor["basis_gates"])

    # Basic checks
    assert processor["num_qubits"] > 0
    assert all(
        0 <= q1 < processor["num_qubits"]
        and 0 <= q2 < processor["num_qubits"]
        and q1 != q2
        for q1, q2 in processor["coupling_map"]
    )

print("\nBoth processor configuration files passed the basic checks!")

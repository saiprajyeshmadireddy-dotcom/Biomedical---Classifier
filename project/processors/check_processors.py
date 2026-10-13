import json
from pathlib import Path

# The JSON files live beside this script in project/processors/.
PROCESSOR_DIR = Path(__file__).resolve().parent


def load_and_validate(filename):
    path = PROCESSOR_DIR / filename
    with path.open("r", encoding="utf-8") as file:
        processor = json.load(file)

    required = {"name", "num_qubits", "coupling_map", "basis_gates"}
    missing = required - processor.keys()
    if missing:
        raise ValueError(f"{filename} is missing required keys: {sorted(missing)}")

    num_qubits = processor["num_qubits"]
    if not isinstance(num_qubits, int) or num_qubits < 1:
        raise ValueError(f"{filename}: num_qubits must be a positive integer")

    seen_edges = set()
    for edge in processor["coupling_map"]:
        if not isinstance(edge, list) or len(edge) != 2:
            raise ValueError(f"{filename}: each coupling_map entry must contain two qubit indices")
        q1, q2 = edge
        if not all(isinstance(q, int) for q in edge):
            raise ValueError(f"{filename}: qubit indices must be integers")
        if not (0 <= q1 < num_qubits and 0 <= q2 < num_qubits):
            raise ValueError(f"{filename}: edge {edge} refers to a qubit outside 0..{num_qubits - 1}")
        if q1 == q2:
            raise ValueError(f"{filename}: self-loop {edge} is not a valid coupling")
        normalized = tuple(sorted(edge))
        if normalized in seen_edges:
            raise ValueError(f"{filename}: duplicate coupling edge {edge}")
        seen_edges.add(normalized)

    if not isinstance(processor["basis_gates"], list) or not processor["basis_gates"]:
        raise ValueError(f"{filename}: basis_gates must be a non-empty list")

    print(f"\n{processor['name']}")
    print("Number of qubits:", num_qubits)
    print("Connections:", processor["coupling_map"])
    print("Supported gates:", processor["basis_gates"])
    if processor.get("definition_status") == "participant_assumption_not_official":
        print("WARNING: connectivity is a participant assumption, not an official processor specification.")

    return processor


def main():
    for filename in ("processor_A.json", "processor_B.json"):
        load_and_validate(filename)
    print("\nBoth processor configuration files passed the basic checks.")


if __name__ == "__main__":
    main()

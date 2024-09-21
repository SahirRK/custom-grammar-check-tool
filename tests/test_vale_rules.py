import os
import subprocess
import json
import re

def run_vale(file_path):
    run_vale_script = os.path.join('scripts', 'run-vale-no-sync.sh')
    
    command = [run_vale_script, '--output', 'JSON', file_path]
    print(f"Executing command: {' '.join(command)}")
    
    result = subprocess.run(command, capture_output=True, text=True)
    
    print("Command executed. Result details:")
    print(f"Return code: {result.returncode}")
    print(f"stdout length: {len(result.stdout)}")
    print(f"stderr length: {len(result.stderr)}")
    
    if result.returncode not in (0, 1):
        print("Vale execution failed.")
        print("Error message:", result.stderr)
        print("Output:", result.stdout)
        return None

    json_match = re.search(r'(\{.*\})', result.stdout, re.DOTALL)
    if json_match:
        json_output = json_match.group(1)
        try:
            output_json = json.loads(json_output)
            print("Successfully parsed JSON output")
            return output_json
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON: {str(e)}")
            print("Raw output:", result.stdout)
            return None
    else:
        print("No valid JSON found in the output.")
        print("Raw output:", result.stdout)
        return None

def load_test_files(file_path):
    with open(file_path, 'r') as f:
        # Base names are stored in the JSON, but the .md files are in test_files directory
        return [os.path.join('tests', 'test_files', line.strip()) for line in json.load(f)]

def load_expected_counts(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def count_errors(output_json, expected):
    error_counts = {key: 0 for key in expected}
    for file_name, errors in output_json.items():
        for error in errors:
            if 'Check' in error and error['Check'] in error_counts:
                error_counts[error['Check']] += 1
    return error_counts

import os
import subprocess
import json
import re

def run_vale(file_path):
    run_vale_script = os.path.join('scripts', 'run-vale-no-sync.sh')
    command = [run_vale_script, '--output', 'JSON', file_path]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode not in (0, 1):
        return None
    json_match = re.search(r'(\{.*\})', result.stdout, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            return None
    return None

def load_test_files(file_path):
    with open(file_path, 'r') as f:
        return [os.path.join('tests', 'test_files', line.strip()) for line in json.load(f)]

def load_expected_counts(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def count_errors(output_json, expected):
    error_counts = {key: 0 for key in expected}
    for file_name, errors in output_json.items():
        for error in errors:
            if 'Check' in error and error['Check'] in error_counts:
                error_counts[error['Check']] += 1
    return error_counts

def test_vale_rules():
    test_files = load_test_files('tests/test_file_names.json')  # Load test files from JSON
    expected_counts = load_expected_counts('tests/expected_counts.json')  # Load expected counts

    overall_pass = True  # Track overall status of all tests

    for file_path in test_files:
        base_name = os.path.basename(file_path)
        print(f"\nTesting {file_path}...")

        output_json = run_vale(file_path)

        if output_json is not None:
            if base_name in expected_counts:
                counts = count_errors(output_json, expected_counts[base_name])
                print("Vale Error counts:", counts)

                file_pass = True  # Track status for this particular test file

                # Check against expected counts
                for key, expected in expected_counts[base_name].items():
                    actual = counts.get(key, 0)
                    if actual == expected:
                        print(f"Count for {key} is correct: {actual}")
                    else:
                        file_pass = False
                        print(f"FAIL: Count for {key} is incorrect: expected {expected}, got {actual}")

                # Output PASS/FAIL for the individual file
                if file_pass:
                    print(f"All counts passed for {base_name}. TEST STATUS: PASS")
                else:
                    overall_pass = False  # If any file fails, set overall status to FAIL
                    print(f"Some counts failed for {base_name}. TEST STATUS: FAIL")
            else:
                print(f"WARNING: No expected counts for {base_name}")
                overall_pass = False
        else:
            print(f"ERROR: Failed to parse Vale output for {file_path}")
            overall_pass = False

    # Final overall test summary
    if overall_pass:
        print("\nAll tests passed. FINAL STATUS: PASS")
    else:
        print("\nSome tests failed. FINAL STATUS: FAIL")

if __name__ == "__main__":
    test_vale_rules()

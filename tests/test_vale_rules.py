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

def count_errors(output_json):
    error_counts = {
        'Custom.WATcloud': 0,
        'Custom.RejectPlurals': 0,
        'Custom.PossessiveCapitalization': 0,
        'Custom.WATonomous': 0
    }
    
    for file_name, errors in output_json.items():
        for error in errors:
            if 'Check' in error and error['Check'] in error_counts:
                error_counts[error['Check']] += 1
    
    return error_counts

def test_vale_rules():
    test_files = [
        'tests/custom-rules/BrandNames.md',
    ]
    
    expected_counts = {
        'Custom.WATcloud': 10,
        'Custom.RejectPlurals': 5,
        'Custom.PossessiveCapitalization': 4,
        'Custom.WATonomous': 12
    }
    
    overall_pass = True

    for file_path in test_files:
        print(f"\nTesting {file_path}...")
        output_json = run_vale(file_path)
        
        if output_json is not None:
            counts = count_errors(output_json)
            print("Vale Error counts:", counts)

            # Check against expected counts
            for key, expected in expected_counts.items():
                actual = counts.get(key, 0)
                if actual == expected:
                    print(f"Count for {key} is correct: {actual}")
                else:
                    overall_pass = False
                    print(f"FAIL: Count for {key} is incorrect: expected {expected}, got {actual}")

    if overall_pass:
        print("All counts passed. TEST STATUS: PASS")
    else:
        print("Some counts failed. TEST STATUS: FAIL")

if __name__ == "__main__":
    test_vale_rules()

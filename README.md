# Grammar-Checker-Tool for WATcloud

This repository is a project for a grammar-checking tool developed for use in WATcloud. It leverages a custom configuration of Vale, an open-source linter, based on the [WATcloud Guidelines](https://cloud.watonomous.ca/docs/community-docs/watcloud/guidelines#communicate-accurately). The tool can be expanded in the future, with plans to integrate a more robust grammar-checking tool like LanguageTool.

## Version

Current version: 0.1.0 (Beta)

## Overview

This Vale configuration includes:
- **Custom rules for brand name capitalization**: Enforces correct usage of WATcloud and WATonomous.
- **Data unit usage suggestions**: Ensures consistent and clear use of data units, suggesting binary prefixes (e.g., KiB, MiB).
- **Google Developer Documentation Style Guide**: Applies the grammar and style rules from the Google Developer Style Guide.
- **Future expansion**: Designed to accommodate future grammar checkers like LanguageTool.

For more details, see the [Vale Documentation](https://vale.sh/docs/vale-cli/installation/).

## Installation

### Option 1: Using an Existing Vale Installation

1. Download the Vale configuration files from the [Releases page](https://github.com/SahirRK/custom-grammar-check-tool/releases) and install Vale by following the [official installation instructions](https://vale.sh/docs/vale-cli/installation/).
   
2. Update your `.vale.ini` file with the directory to the styles from `custom-grammar-check-tool/styles`, or:
   - Add `custom-grammar-check-tool/styles/Custom` to your existing styles directory.
   - Add `custom-grammar-check-tool/styles/config/vocabularies/BrandNames` to your existing `styles/config/vocabularies` directory to ensure proper handling of brand names.

Example `.vale.ini` configuration:
```ini
StylesPath = custom-grammar-check-tool/styles
MinAlertLevel = suggestion

[*.md]
BasedOnStyles = Custom, Google
```

### Option 2: Using Docker

1. Clone this repository:
   ```bash
   git clone https://github.com/SahirRK/custom-grammar-check-tool.git
   ```

2. Ensure Docker is installed on your machine.

3. Grant execution permissions for the Vale runner script:
   ```bash
   chmod +x custom-grammar-check-tool/scripts/run-vale.sh
   ```

4. Run the script to execute Vale using Docker:
   ```bash
   ./custom-grammar-check-tool/scripts/run-vale.sh
   ```

### Docker Compose (Optional)

You can also run Vale via Docker Compose:

1. Ensure `docker-compose` is installed.
2. Run the following command:
   ```bash
   docker-compose run vale
   ```

## Usage with GitHub Actions

To integrate this tool with GitHub Actions:

1. Create a `.github/workflows/vale.yml` file in your repository with the following content:

   ```yaml
   name: Vale
   on: [pull_request]

   jobs:
     vale:
       name: Grammar Check with Vale
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3
         - uses: errata-ai/vale-action@reviewdog
           with:
            # github-pr-check, github-pr-review, github-check
             reporter: github-pr-check
             fail_on_error: true
             #
             files: all
   ```

2. Ensure your `.vale.ini` file is properly configured with the correct styles path.

### Recommended Repository Structure for GitHub Actions

For optimal organization when using GitHub Actions, your repository structure should look like this:

```plaintext
.github
├── styles
│   ├── config
│   │   └── vocabularies
│   │       └── BrandNames  # Custom brand name vocabulary
│   └── your-styles-go-here  # Custom grammar rules and styles
└── workflows
    └── vale.yml            # GitHub Actions workflow for Vale
.vale.ini                    # Vale configuration
```

For more help with setting up Vale in your GitHub Actions, refer to the [Vale Action documentation](https://github.com/errata-ai/vale-action/blob/reviewdog/README.md).

This structure separates vocabularies from custom grammar rules:

- **`styles/config/vocabularies/`**: Contains custom vocabulary files like `BrandNames` to ensure correct brand name capitalization.
- **`styles/stylefolder/`**: Holds a folder with .yml files for the rules of a given style

## Running Tests Locally

To validating the custom rules, the repository includes test files. You can run the tests locally with the following command:

```bash
python3 scripts/test_vale_rules.py
```

This script compares the actual output with the expected results defined in `tests/expected_counts.json` and prints a summary of pass/fail status.

## Contributing

If you find any issues or have suggestions for improvements, please open an issue or submit a pull request. Contributions are welcome and appreciated.

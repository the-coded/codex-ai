#!/bin/bash

# Function to get the Python executable
get_python_executable() {
    if command -v python3 &> /dev/null; then
        echo "python3"
    elif command -v python &> /dev/null; then
        echo "python"
    else
        echo "Error: Python not found" >&2
        exit 1
    fi
}

# Main script
main() {
    # Improve directory and path variables
    CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    if [ -z "$CURRENT_DIR" ]; then
        CURRENT_DIR="$( cd "$( dirname "$0" )" && pwd )"
    fi
    if [ -z "$CURRENT_DIR" ]; then
        echo "Error: Unable to determine current directory" >&2
        exit 1
    fi

    # Ensure we're in the .nexus directory
    SCRIPT_DIR="$CURRENT_DIR"
    if [[ "$SCRIPT_DIR" != */.nexus ]]; then
        SCRIPT_DIR="$CURRENT_DIR/.nexus"
    fi

    PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
    VENV_PATH="$PROJECT_ROOT/venv"
    
    # Make requirements path point to the .nexus directory
    REQUIREMENTS_PATH="$SCRIPT_DIR/requirements.txt"

    PYTHON_EXECUTABLE=$(get_python_executable)

    # Create virtual environment if it doesn't exist
    if [ ! -d "$VENV_PATH" ]; then
        echo "Creating virtual environment..."
        $PYTHON_EXECUTABLE -m venv "$VENV_PATH"
    fi

    # Determine the path to the Python executable in the virtual environment
    if [[ "$OSTYPE" == "win"* ]]; then
        VENV_PYTHON="$VENV_PATH/Scripts/python.exe"
        ACTIVATE_CMD="$VENV_PATH/Scripts/activate"
    else
        VENV_PYTHON="$VENV_PATH/bin/$PYTHON_EXECUTABLE"
        ACTIVATE_CMD="$VENV_PATH/bin/activate"
    fi

    # Check if requirements.txt exists
    if [ -f "$REQUIREMENTS_PATH" ]; then
        echo "Installing requirements..."
        "$VENV_PYTHON" -m pip install -r "$REQUIREMENTS_PATH"
        echo -e "\nRequirements installed successfully!"
    else
        echo -e "\nWarning: requirements.txt not found at $REQUIREMENTS_PATH"
        echo "Skipping requirements installation."
    fi

    # Activate the virtual environment
    echo -e "\nActivating python environment..."
    source "$ACTIVATE_CMD"
    echo -e "\nPython env activated!"
    echo "To deactivate the virtual environment when finished, type 'deactivate'.\n"
}

main

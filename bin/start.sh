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
    # Check if already in a virtual environment
    if [[ -n "$VIRTUAL_ENV" ]]; then
        echo "✅ Virtual environment is already active!"
        echo "📂 Using: $VIRTUAL_ENV"
        exit 0
    fi

    # Get the project root directory (parent of bin directory)
    SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
    
    if [ -z "$PROJECT_ROOT" ]; then
        echo "Error: Unable to determine project root directory" >&2
        exit 1
    fi

    VENV_PATH="$PROJECT_ROOT/venv"
    PYTHON_EXECUTABLE=$(get_python_executable)

    # Create virtual environment if it doesn't exist
    if [ ! -d "$VENV_PATH" ]; then
        echo "📦 Creating virtual environment in project root..."
        $PYTHON_EXECUTABLE -m venv "$VENV_PATH"
    fi

    # Determine the path to activate script
    if [[ "$OSTYPE" == "win"* ]]; then
        ACTIVATE_CMD="$VENV_PATH/Scripts/activate"
    else
        ACTIVATE_CMD="$VENV_PATH/bin/activate"
    fi

    # Activate the virtual environment
    echo -e "\n🚀 Activating python environment..."
    source "$ACTIVATE_CMD"
    
    if [[ -n "$VIRTUAL_ENV" ]]; then
        echo -e "\n✅ Python env activated successfully!"
        echo "📂 Virtual environment location: $VENV_PATH"
        echo "💡 To deactivate the virtual environment when finished, type 'deactivate'.\n"
    else
        echo -e "\n❌ Failed to activate virtual environment!"
        echo "💡 Try running: source bin/start.sh\n"
        exit 1
    fi
}

main

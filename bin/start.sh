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

# Parse command line arguments
MODE="prod"  # Default mode
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --mode)
            if [ "$2" = "dev" ] || [ "$2" = "prod" ]; then
                MODE="$2"
                shift 2
            else
                echo "❌ Error: Mode must be 'dev' or 'prod'" >&2
                exit 1
            fi
            ;;
        *)
            echo "❌ Error: Unknown parameter: $1" >&2
            echo "💡 Usage: source bin/start.sh [--mode dev|prod]" >&2
            exit 1
            ;;
    esac
done

# Main script
main() {
    # Check if already in a virtual environment
    if [[ -n "$VIRTUAL_ENV" ]]; then
        echo "✅ Virtual environment is already active!"
        echo "📂 Using: $VIRTUAL_ENV"
        exit 0
    fi

    # Get absolute paths
    CURRENT_DIR="$(pwd)"
    echo "DEBUG: CURRENT_DIR = $CURRENT_DIR"
    echo "DEBUG: MODE = $MODE"

    if [ "$MODE" = "dev" ]; then
        echo "DEBUG: Running in dev mode"
        # In dev mode, we're in the codex-ai repository
        SCRIPT_PATH="$CURRENT_DIR/bin"
        CODEX_ROOT="$CURRENT_DIR"
        VENV_DIR="$CODEX_ROOT/venv"  # venv inside codex-ai
        PROJECT_ROOT="$CURRENT_DIR"
    else
        echo "DEBUG: Running in prod mode"
        # In prod mode, we're in another project with .nexus
        if [[ "$CURRENT_DIR" == *"/.nexus" ]]; then
            echo "DEBUG: Currently in .nexus directory"
            PROJECT_ROOT="$(dirname "$CURRENT_DIR")"
        else
            echo "DEBUG: Currently in project root"
            PROJECT_ROOT="$CURRENT_DIR"
        fi
        echo "DEBUG: Setting SCRIPT_PATH to $PROJECT_ROOT/.nexus/bin"
        SCRIPT_PATH="$PROJECT_ROOT/.nexus/bin"
        echo "DEBUG: Setting CODEX_ROOT to $PROJECT_ROOT/.nexus"
        CODEX_ROOT="$PROJECT_ROOT/.nexus"
        VENV_DIR="$PROJECT_ROOT/venv"  # venv in project root
    fi

    echo "DEBUG: SCRIPT_PATH = $SCRIPT_PATH"
    echo "DEBUG: CODEX_ROOT = $CODEX_ROOT"
    echo "DEBUG: PROJECT_ROOT = $PROJECT_ROOT"
    
    # Create virtual environment if it doesn't exist
    if [ "$MODE" = "dev" ]; then
        echo "📦 Creating virtual environment in dev mode..."
        echo "📂 Location: $VENV_DIR"
    else
        echo "📦 Creating virtual environment in prod mode..."
        echo "📂 Location: $VENV_DIR"
    fi

    PYTHON_EXECUTABLE=$(get_python_executable)
    if [ ! -d "$VENV_DIR" ]; then
        $PYTHON_EXECUTABLE -m venv "$VENV_DIR"
    fi

    # Determine the path to activate script
    if [[ "$OSTYPE" == "win"* ]]; then
        ACTIVATE_CMD="$VENV_DIR/Scripts/activate"
    else
        ACTIVATE_CMD="$VENV_DIR/bin/activate"
    fi

    # Activate the virtual environment
    echo -e "\n🚀 Activating python environment..."
    source "$ACTIVATE_CMD"
    
    if [[ -n "$VIRTUAL_ENV" ]]; then
        echo -e "\n✅ Python env activated successfully!"
        echo "📂 Virtual environment location: $VENV_DIR"
        echo "🔧 Mode: $MODE"
        echo "💡 To deactivate the virtual environment when finished, type 'deactivate'.\n"
    else
        echo -e "\n❌ Failed to activate virtual environment!"
        echo "💡 Try running: source bin/start.sh [--mode dev|prod]\n"
        exit 1
    fi
}

main

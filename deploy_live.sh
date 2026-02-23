#!/usr/bin/env bash
set -euo pipefail

# One-command live deploy helper for autodidact.uk (frontend) and optional backend.
#
# Examples:
#   ./deploy_live.sh
#   ./deploy_live.sh --frontend-only
#   ./deploy_live.sh --with-backend --backend-path /home/ubuntu/autodidact --backend-mode docker
#   ./deploy_live.sh --with-backend --backend-path /home/ubuntu/autodidact --backend-mode systemd --backend-service autodidact-backend

VPS_HOST="51.38.234.237"
VPS_USER="ubuntu"
FRONTEND_LOCAL_DIR="frontend"
FRONTEND_BUILD_DIR="dist/autodidact-frontend/browser"
FRONTEND_TMP_DIR="/tmp/latest-frontend"
FRONTEND_WEB_DIR="/var/www/html"
FRONTEND_RELEASES_DIR="/tmp/autodidact-releases"

DEPLOY_FRONTEND=true
DEPLOY_BACKEND=false
BACKEND_PATH=""
BACKEND_MODE=""
BACKEND_SERVICE=""
BRANCH_NAME="${1:-}"

print_help() {
  cat <<EOF
Usage:
  ./deploy_live.sh [options]

Options:
  --frontend-only                    Deploy only frontend (default behavior).
  --with-backend                     Also deploy backend from current git branch.
  --backend-path <path>              Backend repo path on VPS (required with --with-backend).
  --backend-mode <docker|systemd>    How backend runs on VPS (required with --with-backend).
  --backend-service <name>           Systemd service name (required if --backend-mode systemd).
  --host <ip-or-hostname>            VPS host (default: 51.38.234.237).
  --user <ssh-user>                  SSH user (default: ubuntu).
  -h, --help                         Show this help.

Notes:
  - Frontend deploy updates https://autodidact.uk via NGINX.
  - Backend deploy checks out and pulls the current local branch on VPS.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --frontend-only)
      DEPLOY_FRONTEND=true
      shift
      ;;
    --with-backend)
      DEPLOY_BACKEND=true
      shift
      ;;
    --backend-path)
      BACKEND_PATH="${2:-}"
      shift 2
      ;;
    --backend-mode)
      BACKEND_MODE="${2:-}"
      shift 2
      ;;
    --backend-service)
      BACKEND_SERVICE="${2:-}"
      shift 2
      ;;
    --host)
      VPS_HOST="${2:-}"
      shift 2
      ;;
    --user)
      VPS_USER="${2:-}"
      shift 2
      ;;
    -h|--help)
      print_help
      exit 0
      ;;
    *)
      echo "Unknown option: $1"
      echo
      print_help
      exit 1
      ;;
  esac
done

if [[ "$DEPLOY_BACKEND" == "true" ]]; then
  if [[ -z "$BACKEND_PATH" || -z "$BACKEND_MODE" ]]; then
    echo "Error: --backend-path and --backend-mode are required with --with-backend."
    exit 1
  fi

  if [[ "$BACKEND_MODE" != "docker" && "$BACKEND_MODE" != "systemd" ]]; then
    echo "Error: --backend-mode must be either 'docker' or 'systemd'."
    exit 1
  fi

  if [[ "$BACKEND_MODE" == "systemd" && -z "$BACKEND_SERVICE" ]]; then
    echo "Error: --backend-service is required when --backend-mode systemd."
    exit 1
  fi
fi

for cmd in git ssh scp node npm; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "Error: '$cmd' is required but not found in PATH."
    exit 1
  fi
done

BRANCH_NAME="$(git branch --show-current)"
if [[ -z "$BRANCH_NAME" ]]; then
  echo "Error: could not determine current git branch."
  exit 1
fi

echo "Branch: $BRANCH_NAME"
echo "Target VPS: $VPS_USER@$VPS_HOST"

if [[ "$DEPLOY_FRONTEND" == "true" ]]; then
  echo "Building Angular app..."
  (
    cd "$FRONTEND_LOCAL_DIR"
    npm install
    npm exec ng build --configuration production
  )

  if ! compgen -G "$FRONTEND_LOCAL_DIR/$FRONTEND_BUILD_DIR/*" >/dev/null; then
    echo "Error: build output not found in $FRONTEND_LOCAL_DIR/$FRONTEND_BUILD_DIR"
    exit 1
  fi

  RELEASE_ID="$(date +%Y%m%d%H%M%S)"
  REMOTE_RELEASE_DIR="$FRONTEND_RELEASES_DIR/$RELEASE_ID"

  echo "Preparing frontend release directory on VPS..."
  ssh "$VPS_USER@$VPS_HOST" "
    set -euo pipefail
    mkdir -p $REMOTE_RELEASE_DIR
  "

  echo "Uploading frontend build to VPS..."
  scp -r "$FRONTEND_LOCAL_DIR/$FRONTEND_BUILD_DIR/"* "$VPS_USER@$VPS_HOST:$REMOTE_RELEASE_DIR/"

  echo "Updating NGINX static files..."
  ssh "$VPS_USER@$VPS_HOST" "
    set -euo pipefail
    mkdir -p $FRONTEND_TMP_DIR
    rm -rf $FRONTEND_TMP_DIR/*
    cp -r $REMOTE_RELEASE_DIR/* $FRONTEND_TMP_DIR/
    sudo rm -rf $FRONTEND_WEB_DIR/*
    sudo cp -r $FRONTEND_TMP_DIR/* $FRONTEND_WEB_DIR/
    sudo systemctl restart nginx
  "
fi

if [[ "$DEPLOY_BACKEND" == "true" ]]; then
  echo "Deploying backend from branch '$BRANCH_NAME'..."

  if [[ "$BACKEND_MODE" == "docker" ]]; then
    ssh "$VPS_USER@$VPS_HOST" "
      set -euo pipefail
      cd $BACKEND_PATH
      git fetch origin
      git checkout $BRANCH_NAME
      git pull origin $BRANCH_NAME
      docker compose up -d --build backend
    "
  else
    ssh "$VPS_USER@$VPS_HOST" "
      set -euo pipefail
      cd $BACKEND_PATH
      git fetch origin
      git checkout $BRANCH_NAME
      git pull origin $BRANCH_NAME
      sudo systemctl restart $BACKEND_SERVICE
    "
  fi
fi

echo
echo "Deploy complete."
echo "Frontend: https://autodidact.uk"
echo "Backend docs: https://api.autodidact.uk/docs"

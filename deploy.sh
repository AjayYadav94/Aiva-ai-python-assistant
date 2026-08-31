#!/usr/bin/env bash
set -euo pipefail

: "${GOOGLE_CLOUD_PROJECT:?Set GOOGLE_CLOUD_PROJECT first}"
: "${GEMINI_API_KEY:?Set GEMINI_API_KEY first}"
REGION="${REGION:-asia-south1}"
SERVICE="${SERVICE:-aiva-ai-assistant}"

printf 'Deploying %s to %s in %s\n' "$SERVICE" "$GOOGLE_CLOUD_PROJECT" "$REGION"

gcloud config set project "$GOOGLE_CLOUD_PROJECT"
gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com
gcloud run deploy "$SERVICE" \
  --source . \
  --region "$REGION" \
  --allow-unauthenticated \
  --set-env-vars "GEMINI_API_KEY=${GEMINI_API_KEY},GEMINI_MODEL=${GEMINI_MODEL:-gemini-2.5-flash-lite}"

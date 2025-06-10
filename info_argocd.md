#!/bin/bash

# Get current timestamp in seconds
now=$(date +%s)

# Get all apps in JSON format
apps_json=$(argocd app list -o json)

# Check if jq and apps data are available
if [ -z "$apps_json" ]; then
    echo "No apps found or unable to fetch apps."
    exit 1
fi

echo "Applications older than 7 days:"
echo "--------------------------------"

# Loop through apps and check age
echo "$apps_json" | jq -r '.[] | "\(.metadata.name) \(.metadata.creationTimestamp)"' | while read name created; do
    created_ts=$(date -d "$created" +%s)
    age_days=$(( (now - created_ts) / 86400 ))

    if [ "$age_days" -gt 7 ]; then
        echo "$name (Age: ${age_days} days)"
    fi
done

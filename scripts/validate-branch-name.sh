#!/bin/bash
#
# Branch name validation script
# Enforces format: <type>/<scope>-#<issue-number>-<short-description>
#

branch=$(git rev-parse --abbrev-ref HEAD)

# Allow main and develop branches
if [[ "$branch" == "main" || "$branch" == "develop" ]]; then
    exit 0
fi

# Check if branch name matches the required format
if [[ "$branch" =~ ^(feat|fix|chore|refactor|style|test|docs)/(frontend|backend|shared|docs|ci|config|database|api)-#[0-9]+-[a-z0-9-]+$ ]]; then
    exit 0
else
    echo "❌ Invalid branch name: $branch"
    echo ""
    echo "Branch name must follow format: <type>/<scope>-#<issue-number>-<short-description>"
    echo ""
    echo "Valid types: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert"
    echo "Valid scopes: frontend, backend, shared, docs, ci, config, database, api"
    echo ""
    echo "Examples:"
    echo "  feat/frontend-#123-user-login-page"
    echo "  fix/backend-#456-email-validation-error"
    echo "  chore/shared-#789-update-dependencies"
    echo "  docs/readme-#101-setup-instructions"
    echo "  feat/api-#202-user-authentication-endpoint"
    echo "  fix/database-#303-migration-script-error"
    echo "  chore/ci-#404-update-github-actions"
    exit 1
fi 
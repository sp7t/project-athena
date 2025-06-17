# Contributing to Project Athena (Internal Guide for Interns)

Welcome, interns, to Project Athena! This guide is designed specifically for you, providing everything you need to get started with development in this repository, from setting up your environment to submitting your first pull request.

## 🚀 Getting Started

Follow these steps to set up your development environment.

### Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Make**: A build automation tool.
  - To check if it's installed, run: `make --version`
- **uv**: A fast Python package installer and resolver.
  - To check if it's installed, run: `uv --version`
  - If not installed, follow the [official uv installation guide](https://github.com/astral-sh/uv#installation).
- **Python 3.13**: This project uses Python 3.13.
  - `uv` can help manage Python versions. You can install a specific Python version using `uv python install 3.13`.

### 1. Clone the Repository

```bash
git clone https://github.com/sp7t/project-athena.git
cd project-athena
```

### 2. Install Dependencies & Git Hooks

We use `make` to simplify the setup process. These commands will install all necessary project dependencies using `uv` and set up Git hooks to ensure code quality and consistency.

```bash
make install
```

### 3. Configure Git for Linear History

To maintain a clean, linear project history, configure Git to always rebase when pulling changes:

```bash
git config --global pull.rebase true
git config --global rebase.autoStash true
```

These settings ensure that:

- `git pull` will automatically rebase your local commits on top of the remote changes
- Your work-in-progress changes are automatically stashed and restored during rebase

### 4. Set Up Environment Variables

Environment variables are crucial for configuring the application, especially for API keys and other sensitive information.

1.  Copy the example environment file:
    ```bash
    cp .env.example .env
    ```
2.  Edit the `.env` file and add your specific configurations:
    - **Gemini API Key**: You'll need a Gemini API Key for certain features.
      - _Instructions_: Obtain your Gemini API key from [Google AI Studio](https://ai.google.dev/gemini-api/docs/api-key) and add it to your `.env` file.
    - **Other Project Variables**: For other necessary environment variables, please contact your supervisor.

## 🛠️ Our Tech Stack

This project leverages a modern set of tools and methodologies. Familiarizing yourself with them will be beneficial:

- **Python 3.13**: The primary programming language.
- **`uv`**: For fast Python package installation, resolution, and virtual environment management. ([uv documentation](https://github.com/astral-sh/uv))
- **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python, used for our backend. ([FastAPI documentation](https://fastapi.tiangolo.com/))
- **Streamlit**: An open-source app framework for Machine Learning and Data Science projects, used for our frontend. ([Streamlit documentation](https://docs.streamlit.io/))
- **Ruff**: An extremely fast Python linter and formatter, written in Rust. ([Ruff documentation](https://docs.astral.sh/ruff/))
- **Domain-Driven Design (DDD)**: An approach to software development that emphasizes modeling the software to match a domain according to input from that domain's experts. (Refer to the "Backend Development" section for our application of DDD).
- **Conventional Commits**: A specification for adding human and machine readable meaning to commit messages. ([Conventional Commits](https://www.conventionalcommits.org/))
- **Git & GitHub**: For version control and collaborative development.
- **`make`**: For simplifying common development tasks and build automation.

## ⚙️ Useful `make` Commands

We use a `Makefile` to provide convenient shortcuts for common development tasks. Here are some of the most frequently used commands:

- `make install`: Installs all project dependencies using `uv` and sets up pre-commit hooks. Run this first after cloning the repository.
- `make dev`: Runs both the backend and frontend in development mode concurrently.
- `make backend-dev`: Runs the backend server in development mode (with auto-reload).
- `make frontend-dev`: Runs the frontend application in development mode.
- `make prod`: Runs both the backend and frontend in production mode concurrently.
- `make backend-prod`: Runs the backend server in production mode.
- `make frontend-prod`: Runs the frontend application in production mode.
- `make lint`: Checks the codebase for linting issues using Ruff.
- `make format`: Formats the codebase using Ruff.
- `make fix`: Formats the codebase and automatically fixes any fixable linting issues using Ruff.

You can run these commands from the root of the project directory.

## 💻 Development Workflow

This section outlines how to contribute code to the project.

### Understanding GitHub Issues

All tasks, features, bugs, and improvements are tracked as GitHub Issues.

**Creating an Issue:**

As an intern, you'll often be responsible for identifying and creating issues for the tasks you'll be working on. When creating a new issue:

1.  **Navigate to the "Issues" tab** in the repository.
2.  **Click the "New issue" button.**
3.  **Choose the appropriate template** for your issue. We have templates for:
    - **Bug Report**: For reporting unexpected behavior or errors. (Uses `bug.md`)
    - **Feature Request**: For proposing new features or enhancements. (Uses `feature.md`)
    - **Documentation**: For tasks related to creating or updating documentation. (Uses `docs.md`)
    - **Chore**: For routine maintenance tasks, refactoring, or other non-feature/bug work. (Uses `chore.md`)
    - **Setup**: For issues related to project setup or environment configuration. (Uses `setup.md`)
    - **Test**: For tasks related to writing or updating tests. (Uses `test.md`)
4.  **Fill out the template fields** as thoroughly as possible. Provide clear titles, detailed descriptions, steps to reproduce (for bugs), and any other relevant information.
5.  **Assign yourself** or relevant team members if applicable.
6.  **Add appropriate labels** (e.g., `bug`, `feature`, `documentation`, `backend`, `frontend`).

Clear, well-defined issues are crucial for smooth development. If you're unsure which template to use or how to best describe your issue, please ask your supervisor.

**Finding an Issue:**

1.  Browse the [Issues tab](https://github.com/sp7t/project-athena/issues) to find something to work on.
2.  Read the issue description carefully. If anything is unclear, ask for clarification by commenting on the issue.
3.  If you decide to work on an issue, please assign it to yourself.

### Branching Strategy

We follow a trunk-based development approach with a focus on clear and descriptive branch names.

- `main`: This is the stable, production-ready branch. Direct pushes to `main` are restricted.
- `develop`: This is the primary integration branch where features are merged before being promoted to `main`. All feature branches should be based off `develop`.
- **Feature Branches**: Create a new branch for every issue or feature you work on. This keeps your changes isolated and makes them easier to review.

  - **Naming Convention**: Use the following structure for your branch names. This is important for clarity, especially in a monorepo context.

    ```
    <type>/<scope>-#<issue-number>-<short-description>
    ```

    - `<type>`: `feat` (new feature), `fix` (bug fix), `chore` (maintenance, docs), `refactor`, `style`, `test`.
    - `<scope>`: `frontend`, `backend`, `shared`, `docs`, etc.
    - `<issue-number>`: The GitHub issue number (e.g., `#123`).
    - `<short-description>`: A brief, hyphenated description of the change (e.g., `user-login-form`).

    **Examples:**

    ```bash
    git checkout -b feat/frontend-#123-user-login-page
    git checkout -b fix/backend-#142-email-validation-error
    git checkout -b chore/shared-#99-update-prettier-config
    git checkout -b docs/readme-#201-add-setup-instructions
    ```

### Making Changes

1.  **Pull the latest changes**: Before starting work, ensure your `develop` branch is up-to-date:
    ```bash
    git checkout develop
    git pull origin develop
    ```
2.  **Create your feature branch**:
    ```bash
    git checkout -b feat/backend-#101-fix-auth-token-expiry develop
    ```
3.  **Write your code!**
4.  **Using `uv` for Package Management**:
    - To add a new package: `uv add <package-name>`
    - To remove a package: `uv remove <package-name>`
    - After modifying dependencies, `uv` will update `pyproject.toml` and `uv.lock`. Make sure to commit these files.

### Commit Message Guidelines

Clear and consistent commit messages are essential. We follow the [Conventional Commits specification](https://www.conventionalcommits.org/). This makes the commit history easier to read and helps automate changelog generation.

A commit message should be structured as follows:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

- **Examples**:

  ```
  feat(backend): add user authentication endpoint
  ```

  ```
  fix(frontend): correct typo on login button

  The button text was previously "Lgoin", corrected to "Login".

  Refs: #123
  ```

  ```
  docs: update contributing guide with commit conventions
  ```

### Keeping Your Branch Updated (Rebasing)

To maintain a clean and linear project history, we prefer rebasing your feature branch onto `develop` rather than merging `develop` into your branch.

1.  **Fetch the latest changes from `develop`**:
    ```bash
    git fetch origin develop
    ```
2.  **Rebase your feature branch**:
    ```bash
    git checkout your-feature-branch
    git rebase origin/develop
    ```
3.  **Resolve conflicts**: If there are merge conflicts, Git will pause the rebase and ask you to resolve them. After resolving conflicts, continue the rebase:
    ```bash
    git add . # Add resolved files
    git rebase --continue
    ```
4.  **Force push (with lease)**: After a successful rebase, you'll need to force push your branch. Use `git push --force-with-lease` to avoid accidentally overwriting work if someone else has pushed to the branch.

    ```bash
    git push origin your-feature-branch --force-with-lease
    ```

    _Why rebase?_ Rebasing helps keep the commit history clean by placing your feature branch commits on top of the latest `develop` branch, avoiding unnecessary merge commits.

### Submitting Pull Requests (PRs)

Once your changes are ready and you've pushed them to your feature branch on GitHub:

1.  **Open a Pull Request**: Go to the repository on GitHub. You should see a prompt to create a PR from your recently pushed branch. Target the `develop` branch for your PR.
2.  **Write a Clear Description**:

    - Explain the "what" and "why" of your changes.
    - Link the relevant GitHub Issue(s) using keywords like `Closes #123`, `Fixes #456`, or `Addresses #789`. This helps automatically close issues when the PR is merged.
    - Example:

      ```
      Closes #101

      This PR addresses the auth token expiry bug by...
      ```

3.  **Labels**: Add relevant labels to your PR (e.g., `backend`, `frontend`, `bug`, `feature`).
4.  **Request Review**: Request reviews from team members.
5.  **Address Feedback**: Be prepared to discuss your changes and make adjustments based on feedback. Push new commits to your branch to update the PR.
6.  **Merge**: Once the PR is approved and passes all checks, your supervisor will merge it into `develop`.

### Example Workflow Summary

1.  Developer picks up issue `#101` (e.g., a backend bug).
2.  Ensures `develop` is up to date: `git checkout develop && git pull origin develop`.
3.  Creates a branch: `git checkout -b fix/backend-#101-fix-auth-token-expiry develop`.
4.  Makes changes, commits them using Conventional Commits.
5.  (If `develop` has new commits) Rebases branch: `git rebase origin/develop`.
6.  Pushes branch: `git push origin fix/backend-#101-fix-auth-token-expiry --force-with-lease`.
7.  Opens a PR against `develop`.
8.  Adds `backend` label, links issue with `Closes #101` in the PR description.
9.  After review and approval, the PR is merged by a maintainer.
10. The issue `#101` is automatically closed.

### Recommended Workflow for Full-Stack Features

When working on features that involve both backend and frontend changes, follow this sequence to ensure smooth development:

**Why Backend First?**
Since our frontend depends on the backend APIs, it's essential to have the backend functionality working before implementing the UI. This approach ensures that:

- Frontend developers have working APIs to integrate with
- Functionality is prioritized over appearance (which is the right approach)
- Integration issues are caught early
- Testing can be done incrementally

**Step-by-Step Process:**

1. **Backend Development:**

   ```bash
   # Create backend branch
   git checkout -b feat/backend-#123-user-authentication develop

   # Implement backend functionality
   # - Add API endpoints
   # - Implement business logic
   # - Add tests
   # - Update documentation

   # Submit backend PR
   git push origin feat/backend-#123-user-authentication
   # Open PR against develop, get it reviewed and merged
   ```

2. **Frontend Development (after backend is merged):**

   ```bash
   # Update your develop branch
   git checkout develop
   git pull origin develop

   # Create frontend branch
   git checkout -b feat/frontend-#123-user-authentication develop

   # Implement frontend functionality
   # - Create UI components
   # - Integrate with backend APIs
   # - Add user interactions
   # - Test the complete flow

   # Submit frontend PR
   git push origin feat/frontend-#123-user-authentication
   # Open PR against develop
   ```

**Important Notes:**

- Use separate branches for backend and frontend work, even if they're for the same feature
- Both PRs should reference the same issue number (e.g., `#123`)
- Only the final frontend PR should include `Closes #123` to auto-close the issue
- The backend PR can use `Refs #123` to link without closing
- Test the complete end-to-end functionality before marking the feature as complete

This workflow ensures that each component is properly reviewed and tested before moving to the next layer of the application.

## 🎨 Coding Standards

To maintain code quality and consistency, please adhere to the following standards.

### Backend Development (Domain-Driven Design - DDD)

We organize our backend code using a method called **Domain-Driven Design (DDD)**. Think of it as building our code to mirror how our project's specific area (its "domain") actually works. This helps us keep even complex projects understandable and well-organized.

**How Our Backend is Organized (The Big Picture):**

Our `backend` code is divided into main areas or "modules," each in its own folder (like `job_descriptions` and `resume_evaluations`). Each module handles one specific part of our project.

- The goal is to keep these modules separate and focused. For example, everything about job descriptions stays in the `job_descriptions` folder. In DDD, this idea of clear boundaries for each part of the project is called a "Bounded Context."

To give you a clearer picture, here's a typical file structure you'll encounter within the `backend` directory, along with the purpose of key files and directories:

```
backend/
├── main.py             # FastAPI app entry point, global configurations, includes module routers. Connects all the pieces.
├── config.py           # Application-wide settings (e.g., environment variables, external service URLs).
├── database.py         # Database connection setup, session management, and potentially base ORM configurations.
│
├── core/               # Shared components used by multiple modules.
│
└── <module_name>/      # Represents a specific domain, e.g., `job_descriptions/`, `resume_evaluations/`.
│ ├── __init__.py       # Standard Python package marker.
│ ├── router.py         # Defines API endpoints (FastAPI routers) for this module. Handles HTTP requests and responses.
│ ├── service.py        # Contains the core business logic for the module. Orchestrates operations, calling repositories and other services.
│ ├── schemas.py        # Pydantic models used for API request/response validation, serialization, and as Data Transfer Objects (DTOs) between layers.
│ ├── exceptions.py     # Custom exception classes specific to this module, helping to handle errors gracefully.
│ ├── utils.py          # Helper functions and utilities specific to this module. Contains reusable code that doesn't fit elsewhere.
│ └── constants.py      # Module-specific constants, enums, and configuration values that don't change during runtime.
```

This structure promotes separation of concerns and makes it easier to navigate and maintain the codebase as it grows. When creating new features or modules, try to follow this pattern.

**Good Habits for Backend Code:**

- **Keep Modules Tidy (Encapsulation)**: Each module should manage its own affairs. Other modules should only interact with it through clear, defined ways (like calling its service functions or API endpoints), not by directly meddling with its internal code.
- **Speak the Same Language (Ubiquitous Language)**: Try to use names in your code (for classes, functions, variables) that match the terms our team and project use when discussing these features. If we talk about "Candidate Submissions," our code should use similar terms. This makes it easier for everyone to understand.
- **Model the Real World (Focus on the Domain)**: Our main goal is to make the code accurately represent and solve the actual problems or tasks of our project.

If you are creating a new domain module or are unsure how to structure code within an existing one using these DDD principles, please discuss it with your supervisor. They can provide guidance and point you to relevant examples in the codebase as it evolves.

### Linting and Formatting

We use `ruff` for linting and formatting. These are enforced by pre-commit hooks, which you installed during setup.

- Before committing, the hooks will automatically check and format your code.
- If there are linting errors, the commit will be blocked. Please fix these errors before trying to commit again. You can also use the `make fix` command to automatically format and fix many issues.
- You can also run the linters and formatters manually using `make`:
  ```bash
  # To check for linting issues
  make lint
  # To format code
  make format
  # To format code and automatically fix linting issues
  make fix
  ```

## ❓ Where to Get Help

If you get stuck, have questions, or need clarification on anything, please don't hesitate to:

- **Ask in the relevant GitHub Issue.**
- **Reach out on our team's communication channel.**
- **Contact your supervisor.**

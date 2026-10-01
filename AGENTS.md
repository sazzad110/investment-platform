# Project Development Rules

This file defines the project-wide instructions for Codex and all contributors. It applies to the entire repository. Read it before making any change, then inspect the relevant existing code and documentation.

## Product Scope

This project is a Bangladesh-focused platform where small businesses submit investment opportunities and potential investors browse published opportunities. An investor may request the business's complete public contact information and then contact the business directly outside the platform.

Keep the current MVP intentionally narrow:

- There is no public user authentication.
- There are no investor or business-owner accounts.
- There are no reviews or ratings.
- There are no payments, escrow, wallets, messaging, or investment transaction handling.
- There is no pending/rejected workflow status.
- A business owner submits an investment opportunity.
- An admin will eventually review submissions manually and control public visibility.
- Publication state is represented only by `is_published: bool`.
- Public browsing must include only published opportunities.
- Complete public business contact information is returned only through a dedicated contact endpoint, not embedded in every opportunity-list response.

Do not implement speculative features. Features such as public authentication, business and investor accounts, verified deals, reviews, notifications, analytics, payments, and trust or verification systems may be added later only when explicitly requested. Keep reasonable extension points, but do not build unused abstractions or infrastructure for them now.

## Approved Technology

Use:

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy with modern typed declarative mappings
- Alembic for every database schema migration
- Pydantic
- Pydantic Settings
- pytest
- HTTPX
- Ruff for linting and formatting
- Docker and Docker Compose

Do not add Redis, Celery, Kafka, Elasticsearch, microservices, or other infrastructure unless a concrete future requirement needs it. Any new dependency must have a clear current use and should be the smallest suitable choice.

## Architecture

Build a modular monolith organized by domain. Use this direction as the application grows:

```text
app/
  core/
  modules/
    businesses/
    opportunities/
    documents/
    admin/
  shared/
```

Each domain module may contain its own models, schemas, repository, service, and router. Add those components only when the domain needs them. Keep cross-cutting configuration and application concerns in `core`; keep genuinely reusable, domain-neutral code in `shared`. Do not turn `shared` into a dumping ground or create global model/router/service directories that cut across domains.

Maintain these layer boundaries:

- **Router:** HTTP concerns, request and response handling, dependency injection, and status codes.
- **Service:** business logic, application rules, and orchestration.
- **Repository:** database queries and persistence.
- **Schema:** API input validation and output serialization.
- **Model:** database representation and explicit relationships.

Routers must not contain business logic. Repositories must not decide HTTP behavior. Schemas and ORM models have different responsibilities and should not be treated as interchangeable. Prefer direct, readable dependencies between layers over generic base classes or unnecessary patterns.

## Database Rules

- PostgreSQL is the supported database.
- Use UUID primary keys internally.
- Store UTC-aware timestamps and keep timezone handling explicit.
- Use Alembic migrations for every schema change, and commit the corresponding migration with the model change.
- Never use `Base.metadata.create_all()` as the production schema-management strategy.
- Define relationships, foreign keys, nullability, uniqueness, and deletion behavior explicitly.
- Add indexes only for demonstrated query patterns or clear integrity/query needs; do not index speculatively.
- Do not store uploaded binary files in PostgreSQL.
- For future uploads, store file metadata and object-storage references in the database. Validate file type and size at the system boundary when uploads are implemented.

Migration history should remain reviewable and deterministic. Do not edit an already-applied migration to change the schema; add a new migration instead, unless the project is explicitly resetting unreleased migration history.

## API Rules

- Place every API endpoint under `/api/v1`.
- Use REST-style resource names, normally plural nouns rather than action-oriented paths.
- Keep public and admin APIs clearly separated in routing and authorization boundaries.
- Use consistent, structured error responses.
- Map expected application failures to appropriate HTTP status codes at the HTTP boundary.
- Never expose internal exceptions, SQL details, or stack traces in API responses.
- Use explicit request and response schemas; do not return ORM objects without a defined response contract.
- Keep list responses focused on browsing needs. Retrieve complete public contact information through a dedicated contact endpoint.

Do not imply that the platform facilitates, guarantees, or records an investment transaction when investors and businesses contact each other directly.

## Security and Privacy

- Never commit secrets, credentials, tokens, private keys, or populated `.env` files.
- Read configuration from environment variables through Pydantic Settings and maintain a safe `.env.example` containing names and non-secret examples only.
- Do not log passwords, secrets, tokens, private identity documents, sensitive financial data, or full sensitive request payloads.
- Treat public contact details as intentionally disclosed data, but expose them only through the dedicated endpoint required by the product flow.
- Validate and normalize untrusted input at API boundaries; apply business validation in the service layer.
- When uploads are added, allow only explicitly supported file types and enforce size limits. Object keys and client-supplied filenames must not permit path traversal.
- Use generic client-facing errors and log only the safe diagnostic context needed for operations.

## Code Quality

- Use Python type hints throughout application code.
- Choose clear names and small, focused functions.
- Minimize duplication without introducing abstractions before repeated needs exist.
- Prefer simple, explicit code over premature optimization or framework-like internal machinery.
- Keep imports and module dependencies directional; avoid circular dependencies between domains.
- Use Ruff as the source of truth for linting and formatting.
- Add tests with meaningful business logic and bug fixes.
- Do not add functionality beyond the requested scope.

## Testing

Use pytest. Prefer:

- Unit tests for business rules and service behavior.
- Integration tests for repositories, database behavior, migrations where appropriate, and API endpoints.
- HTTPX for testing the FastAPI interface.

Tests must be deterministic, isolated, and independent of production services or data. Control time, randomness, identifiers, and external I/O where they affect repeatability. Use PostgreSQL for behavior that depends on PostgreSQL semantics; do not silently substitute a different database when doing so changes the behavior under test.

Test public visibility rules, admin/public separation, validation, and error behavior when those features are implemented. A meaningful change is not complete until its relevant success and failure paths are covered or the missing coverage is explicitly reported.

## Change Workflow

Before making changes:

1. Read this `AGENTS.md` in full.
2. Inspect the relevant existing code, tests, migrations, configuration, and documentation.
3. Check the working tree and preserve unrelated user changes.
4. Identify and make the smallest change that satisfies the request.

While making changes:

- Stay within the requested scope.
- Do not modify unrelated files or silently reformat unrelated code.
- Keep schema changes, Alembic migrations, tests, and documentation synchronized.
- Never discard or overwrite existing contributor changes without explicit authorization.

After making changes:

1. Run the relevant tests.
2. Run the configured Ruff lint and format checks.
3. Run any additional focused validation appropriate to the change, including migration checks when the schema changes.
4. Review `git diff` and `git status` for correctness and unintended files.
5. Report exactly what changed.
6. State which checks ran and clearly mention anything that was not verified.

Do not claim a check passed if it was not run. If tooling is unavailable, report that limitation rather than bypassing the project standard.

## Documentation and Decisions

Keep the README and other relevant documentation current as architecture, setup, commands, configuration, and behavior evolve. Avoid documenting planned features as if they already exist.

For significant architecture decisions, record:

- the current problem and constraints;
- why the selected approach fits the MVP;
- important tradeoffs; and
- how the design permits likely future expansion without implementing future features prematurely.

Favor decisions that keep the modular monolith easy to understand and operate. Reconsider architecture only in response to demonstrated product or operational needs.

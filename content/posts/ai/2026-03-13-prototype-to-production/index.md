+++
date = '2026-03-13T10:00:00+08:00'
draft = false
title = 'Prototype to Production: AI App Deployment Checklist'
description = 'A complete checklist for deploying AI applications from prototype to production, covering testing, security, scalability, observability, and automated ops.'
toc = true
tags = ['AI Agent', 'DevOps', 'Production', 'Deployment']
categories = ['AI Guides']
keywords = ['prototype to production', 'ai agent deployment', 'production checklist ai', 'deploy ai application', 'ai app production ready', 'ai deployment guide']

[[params.faqItems]]
question = "How much of the total work does building an AI prototype represent?"
answer = "Building an AI prototype typically represents only about 10% of the total work needed for a production application. The remaining 90% includes feature completion (25%), testing (15%), security hardening (10%), performance optimization (10%), deployment configuration (10%), and ongoing operations and monitoring (20%)."

[[params.faqItems]]
question = "What are the six gates from AI prototype to production?"
answer = "The six gates are: (1) Working to Testable — adding unit, integration, and E2E tests; (2) Working to Secure — implementing OWASP standards, input validation, and authentication; (3) Working to Scalable — fixing N+1 queries, adding caching, and rate limiting; (4) Working to Observable — setting up logs, metrics, and traces; (5) Working to Automated Ops — deploying AI-SRE and automated incident response; (6) Working to Continuously Evolving — establishing CI/CD pipelines and feedback loops."

[[params.faqItems]]
question = "What are Google's Four Golden Signals for monitoring production AI apps?"
answer = "Google's Four Golden Signals from the SRE handbook are: Latency (response time at P50, P95, P99), Traffic (requests per second), Errors (5xx error rate), and Saturation (CPU, memory, disk utilization). These four metrics form the foundation of production monitoring for any application, including AI-powered ones."

[[params.faqItems]]
question = "Can AI tools like v0 or Claude Code build production-ready applications?"
answer = "AI tools excel at generating prototypes quickly (80%+ automation at the prototype stage), but production readiness requires human oversight. AI's effectiveness drops significantly in later stages: 40-60% for testing, 20-30% for security hardening, and 20-40% for performance optimization. The key is using AI as an accelerator while applying engineering discipline for production quality."
+++

![From Prototype to Production: The Complete AI App Deployment Checklist](cover.webp)

You shipped an AI-generated app in 20 minutes. The demo looked great. Your stakeholders were impressed.

Then reality hit.

The app crashed under 50 concurrent users. A security scan found 12 vulnerabilities. There were zero tests, zero logs, and zero alerts. When it went down at 2 AM, nobody knew until customers started complaining on Twitter.

**Building the prototype was 10% of the work. The other 90% is what separates a demo from a product.**

This article gives you a structured, actionable checklist for crossing that gap. Based on Stanford's CS146S curriculum (Weeks 8-9) on modern software development and real-world deployment patterns, we will walk through six gates that every AI-generated application must pass before it is production-ready.

Whether you are using [Claude Code](/posts/ai/2026-02-28-claude-code-complete-guide/), Cursor, v0, or any other AI coding tool, these gates apply universally.

## The Reality Gap: Prototype vs. Production

### What AI Prototyping Tools Can (and Cannot) Do

Tools like Vercel's v0, Bolt, and AI coding assistants can generate impressive prototypes in minutes. Here is what they handle well:

- Generating UI layouts with responsive design
- Basic CRUD functionality
- Standard navigation and routing
- Common frontend interaction patterns

But here is what they consistently struggle with:

- Complex multi-step business logic
- Performance optimization (lazy loading, bundle splitting, caching)
- Accessibility (a11y compliance)
- Integration with existing authentication systems and legacy APIs
- Production-grade error handling

### The Work Distribution Nobody Talks About

Most developers dramatically underestimate the effort required after the prototype phase. Here is the actual breakdown:

| Phase | % of Total Work | AI Automation Rate |
|-------|----------------|--------------------|
| Prototype / Demo | 10% | 80%+ |
| Feature Completion | 25% | 50-70% |
| Test Coverage | 15% | 40-60% |
| Security Hardening | 10% | 20-30% |
| Performance Optimization | 10% | 20-40% |
| Deployment Configuration | 10% | 30-50% |
| Operations & Monitoring | 20% | 30-50% |

The pattern is clear: **AI is most effective at the phase that represents the least amount of work.** As you move toward production, AI's contribution drops while the complexity rises.

This is not a criticism of AI tools. It is a reality check. Understanding this distribution lets you plan your project timeline accurately instead of assuming the demo means you are "almost done."

## The Six Gates from Prototype to Production

Every AI-generated application must pass through these six gates. Skip one, and your production deployment becomes a ticking time bomb.

### Gate 1: From "Working" to Testable

AI-generated code almost never includes meaningful tests. When it does, the tests are often superficial — they check that a function exists, not that it behaves correctly under edge cases.

#### What You Need

**Unit Tests** for core business logic:

```python
# Bad: AI-generated test that tests nothing meaningful
def test_calculate_price():
    result = calculate_price(100)
    assert result is not None  # This tells us nothing

# Good: Test that validates actual business rules
def test_calculate_price_with_discount():
    # 20% discount for orders over $50
    assert calculate_price(100, discount_tier="gold") == 80.0

def test_calculate_price_rejects_negative():
    with pytest.raises(ValueError, match="Price cannot be negative"):
        calculate_price(-10)

def test_calculate_price_applies_tax():
    # Tax should be applied AFTER discount
    result = calculate_price(100, discount_tier="gold", tax_rate=0.1)
    assert result == 88.0  # (100 * 0.8) * 1.1
```

**Integration Tests** for module interactions:

```python
# Test that the API layer correctly talks to the service layer
async def test_create_order_integration():
    # Setup: seed test database
    user = await create_test_user()
    product = await create_test_product(price=50.0)

    # Act: call the actual API endpoint
    response = await client.post("/api/orders", json={
        "user_id": user.id,
        "product_id": product.id,
        "quantity": 2
    })

    # Assert: check the full chain worked
    assert response.status_code == 201
    order = response.json()
    assert order["total"] == 100.0
    assert order["status"] == "pending"

    # Verify side effects
    db_order = await get_order(order["id"])
    assert db_order is not None
    assert db_order.user_id == user.id
```

**End-to-End Tests** with tools like Playwright:

```typescript
// Test the complete user flow
test('user can complete checkout', async ({ page }) => {
  await page.goto('/products');
  await page.click('[data-testid="add-to-cart-btn"]');
  await page.click('[data-testid="checkout-btn"]');
  await page.fill('#email', 'test@example.com');
  await page.fill('#card-number', '4242424242424242');
  await page.click('[data-testid="pay-btn"]');
  await expect(page.locator('.order-confirmation')).toBeVisible();
});
```

**CI Pipeline** to enforce test gates:

```yaml
# .github/workflows/test.yml
name: Test Suite
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run unit tests
        run: pytest tests/unit/ --cov=src --cov-fail-under=80
      - name: Run integration tests
        run: pytest tests/integration/
      - name: Run E2E tests
        run: npx playwright test
```

#### What AI Can Help With

AI is good at generating test skeletons from existing code. But the **intent** — what to test, why, and what the boundary conditions are — must come from you. Use AI to scaffold tests, then review every assertion to ensure it validates real behavior.

### Gate 2: From "Working" to Secure

Security is where AI-generated code is most dangerous. AI tools optimize for "making it work," not "making it safe." For a deep dive into AI security practices, see [MCP Security in 2026](/posts/ai/2026-03-10-mcp-security-2026/).

#### The OWASP Checklist for AI Apps

Run through these checks systematically:

**Input Validation and Sanitization**

```python
# AI often generates code like this - DANGEROUS
@app.post("/api/query")
async def query(request: Request):
    body = await request.json()
    result = db.execute(f"SELECT * FROM users WHERE name = '{body['name']}'")
    return result

# Production version with proper validation
from pydantic import BaseModel, validator

class QueryRequest(BaseModel):
    name: str

    @validator('name')
    def validate_name(cls, v):
        if len(v) > 100:
            raise ValueError('Name too long')
        # Strip any SQL injection attempts
        if any(char in v for char in [';', '--', "'", '"']):
            raise ValueError('Invalid characters in name')
        return v.strip()

@app.post("/api/query")
async def query(request: QueryRequest):
    result = db.execute(
        "SELECT * FROM users WHERE name = :name",
        {"name": request.name}
    )
    return result
```

**Authentication and Authorization**

- Verify every API endpoint has auth checks
- Implement role-based access control (RBAC)
- Use secure session management (HttpOnly cookies, short-lived tokens)
- Add rate limiting to login endpoints

**Sensitive Data Protection**

- Encrypt data at rest and in transit
- Never log sensitive information (passwords, tokens, PII)
- Use environment variables for secrets, never hardcoded values
- Implement proper key rotation

**Dependency Security**

```bash
# Scan dependencies for known vulnerabilities
npm audit
pip-audit
snyk test

# Keep dependencies updated
npm update
pip install --upgrade -r requirements.txt
```

#### Security Checklist

| Check | Tool | Frequency |
|-------|------|-----------|
| SAST (Static Analysis) | Semgrep, SonarQube | Every PR |
| DAST (Dynamic Analysis) | OWASP ZAP, Burp Suite | Weekly |
| Dependency Scan | Snyk, npm audit | Every build |
| Secret Detection | TruffleHog, GitLeaks | Every commit |
| Container Scan | Trivy, Grype | Every build |

### Gate 3: From "Working" to Scalable

Prototype code typically handles one user at a time. Production means hundreds or thousands of concurrent users. Here are the critical issues to address.

#### Fix N+1 Query Problems

This is the most common performance issue in AI-generated code:

```python
# N+1 Problem: 1 query for orders + N queries for users
orders = db.query(Order).all()
for order in orders:
    user = db.query(User).filter(User.id == order.user_id).first()
    order.user_name = user.name  # This fires a query PER order

# Fixed: Eager loading gets everything in 2 queries
orders = db.query(Order).options(joinedload(Order.user)).all()
for order in orders:
    order.user_name = order.user.name  # No extra query
```

#### Implement Caching

```python
import redis
from functools import wraps

cache = redis.Redis(host='localhost', port=6379)

def cached(ttl=300):
    """Cache function results in Redis for `ttl` seconds."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
            cached_result = cache.get(cache_key)
            if cached_result:
                return json.loads(cached_result)
            result = await func(*args, **kwargs)
            cache.setex(cache_key, ttl, json.dumps(result))
            return result
        return wrapper
    return decorator

@cached(ttl=600)
async def get_product_catalog():
    """Cached for 10 minutes since catalog rarely changes."""
    return await db.query(Product).filter(Product.active == True).all()
```

#### Move Expensive Operations to Background Queues

```python
from celery import Celery

celery_app = Celery('tasks', broker='redis://localhost:6379')

# Instead of sending email synchronously during request
@app.post("/api/orders")
async def create_order(order: OrderCreate):
    db_order = await save_order(order)

    # Offload email to background worker
    send_order_confirmation.delay(db_order.id, order.email)

    return {"order_id": db_order.id, "status": "created"}

@celery_app.task
def send_order_confirmation(order_id: str, email: str):
    """Runs in a background worker, not blocking the API."""
    order = get_order(order_id)
    send_email(to=email, subject="Order Confirmed", body=render_template(order))
```

#### Add Rate Limiting

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/login")
@limiter.limit("5/minute")  # Prevent brute force
async def login(request: Request, credentials: LoginRequest):
    return await authenticate(credentials)

@app.get("/api/data")
@limiter.limit("100/minute")  # Prevent API abuse
async def get_data(request: Request):
    return await fetch_data()
```

#### Scalability Checklist

| Item | Question | Action |
|------|----------|--------|
| Database | Are there N+1 queries? | Profile with query logger, add eager loading |
| Caching | Is hot data cached? | Add Redis/Memcached layer |
| Async | Are slow tasks blocking requests? | Move to Celery/SQS/Bull queues |
| Rate Limits | Can one user overload the system? | Add per-user and global rate limits |
| Horizontal Scaling | Can you run multiple instances? | Remove local state, use shared sessions |
| Connection Pooling | Are DB connections managed? | Use connection pool with limits |

### Gate 4: From "Working" to Observable

Once your app is in production, you need to know what it is doing at all times. Observability has three pillars: logs, metrics, and traces. These align with [Google's SRE Four Golden Signals](https://sre.google/sre-book/introduction/).

#### Structured Logging

```python
import structlog

logger = structlog.get_logger()

@app.post("/api/orders")
async def create_order(order: OrderCreate, user: User = Depends(get_current_user)):
    logger.info(
        "order_created",
        user_id=user.id,
        order_total=order.total,
        product_count=len(order.items),
        payment_method=order.payment_method
    )

    try:
        result = await process_order(order)
        logger.info("order_processed", order_id=result.id, duration_ms=result.processing_time)
        return result
    except PaymentError as e:
        logger.error(
            "payment_failed",
            user_id=user.id,
            error_code=e.code,
            error_message=str(e)
        )
        raise HTTPException(status_code=402, detail="Payment failed")
```

Use JSON format for logs so they are searchable in tools like ELK Stack, Loki, or CloudWatch:

```json
{
  "event": "order_created",
  "user_id": "usr_123",
  "order_total": 99.50,
  "product_count": 3,
  "timestamp": "2026-03-13T10:30:00Z",
  "level": "info"
}
```

#### The Four Golden Signals

These are the metrics every production system must track:

| Signal | What It Measures | Key Metrics | Alert Threshold |
|--------|-----------------|-------------|-----------------|
| **Latency** | Response time | P50, P95, P99 response times | P95 > 500ms |
| **Traffic** | Request volume | Requests per second (RPS) | Sudden 3x spike or 50% drop |
| **Errors** | Failure rate | 5xx error percentage | > 1% of requests |
| **Saturation** | Resource usage | CPU, memory, disk, connections | > 80% utilization |

#### Distributed Tracing

When your app spans multiple services, traces show you the complete path of a request:

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Initialize tracing
provider = TracerProvider()
provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

@app.post("/api/orders")
async def create_order(order: OrderCreate):
    with tracer.start_as_current_span("create_order") as span:
        span.set_attribute("order.total", order.total)

        with tracer.start_as_current_span("validate_inventory"):
            await check_inventory(order.items)

        with tracer.start_as_current_span("process_payment"):
            payment = await charge_card(order.payment)

        with tracer.start_as_current_span("save_order"):
            result = await save_to_database(order, payment)

        return result
```

With tracing, when a request takes 3 seconds, you can see exactly where the time was spent — was it the database? The payment API? The inventory check?

#### Observability Stack Recommendations

| Component | Open Source | Managed Service |
|-----------|-----------|----------------|
| Logs | Loki + Grafana | Datadog, CloudWatch |
| Metrics | Prometheus + Grafana | Datadog, New Relic |
| Traces | Jaeger, Zipkin | Datadog, Honeycomb |
| All-in-One | OpenTelemetry | Datadog, Dynatrace |

### Gate 5: From "Working" to Automated Ops

Traditional incident response is manual and slow. AI-powered operations (AI-SRE) can dramatically reduce mean time to resolution (MTTR).

#### Traditional vs. AI-Enhanced Incident Response

**Traditional flow:**

```
Alert fires → On-call engineer wakes up → Manual investigation
→ Root cause analysis → Manual fix → Write postmortem
```

**AI-enhanced flow:**

```
Alert fires → AI Agent automatically collects context
           → AI analyzes probable root causes
           → AI recommends fix with confidence score
           → Human approves (or AI auto-executes low-risk fixes)
           → AI generates postmortem draft
```

#### Where AI Ops Excels

| Scenario | What AI Does |
|----------|-------------|
| Kubernetes pod crash loops | Auto-check logs, resource quotas, image status, recent deploys |
| Database connection pool exhaustion | Analyze connection sources, identify leak patterns |
| API latency spike | Correlate with deployment history, traffic patterns, dependency status |
| Disk space running low | Identify large files, suggest cleanup strategies |
| Certificate expiration | Early warning, automated renewal |
| Memory leak detection | Trend analysis, identify offending service |

#### From SRE to AI-SRE

The evolution of operations roles:

- **Manual debugging** becomes **guiding AI investigation** — you set the direction, AI gathers data
- **Writing runbooks** becomes **training AI agents** — encode operational knowledge into agent context (see [Context Engineering Guide](/posts/ai/2026-03-10-context-engineering-guide/) for best practices)
- **Reactive firefighting** becomes **proactive prevention** — AI continuously analyzes metrics and predicts issues before they impact users

Tools like [Resolve AI](https://resolve.ai/), PagerDuty AIOps, and Datadog Watchdog are leading this shift. The key is starting with low-risk automated actions (restarting a pod, scaling up replicas) and gradually expanding the AI's authority as trust is established.

### Gate 6: From "Working" to Continuously Evolving

A production system is never "done." It requires continuous iteration: new features, bug fixes, performance improvements, security patches.

#### CI/CD Pipeline Requirements

```yaml
# Complete CI/CD pipeline
name: Deploy
on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm test -- --coverage
      - run: npm run lint
      - run: npx playwright test

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm audit --audit-level=high
      - run: npx semgrep --config=auto

  deploy:
    needs: [test, security]
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to staging
        run: deploy --env staging
      - name: Run smoke tests
        run: npm run test:smoke -- --target=staging
      - name: Deploy to production (canary)
        run: deploy --env production --canary 10%
      - name: Monitor canary metrics
        run: check-metrics --duration 15m --threshold error_rate<0.01
      - name: Full rollout
        run: deploy --env production --canary 100%
```

#### Feedback Loop Architecture

Production data should feed back into your development process:

1. **Error tracking** (Sentry, Bugsnag) captures real user errors
2. **Usage analytics** shows which features are actually used
3. **Performance monitoring** identifies bottlenecks in real workloads
4. **User feedback** through in-app surveys and support tickets
5. **AI agent reports** summarize operational patterns weekly

This feedback loop is where [vibe coding](/posts/ai/2026-02-28-vibe-coding-explained/) meets engineering discipline. You can use AI to rapidly prototype fixes and features, but the direction comes from production data, not guesswork.

## The Complete AI Application Development Lifecycle

Putting all six gates together, here is the full lifecycle from idea to production and beyond:

```
1. Requirements Analysis
   ├── Write clear spec / PRD
   ├── Define acceptance criteria
   └── Identify security and performance requirements

2. Architecture Design
   ├── Choose tech stack (consider AI tool support)
   ├── Design system architecture
   ├── Set up project context (CLAUDE.md, design docs)
   └── Configure tool integrations (MCP servers, APIs)

3. Rapid Prototyping [AI: 80%+ automation]
   ├── Generate prototype with AI
   ├── Validate core functionality
   └── Collect feedback, refine spec

4. Feature Development [AI: 50-70% automation]
   ├── Break requirements into subtasks
   ├── Assign to AI agents for execution
   ├── Checkpoint reviews + human refinement
   └── Code review

5. Quality Assurance [AI: 40-60% automation]
   ├── Unit + integration + E2E test coverage
   ├── Security scanning (SAST + DAST)
   ├── Performance benchmarking
   └── Accessibility audit

6. Deployment [Primarily toolchain automation]
   ├── CI/CD pipeline setup
   ├── Canary / blue-green deployment
   ├── Monitoring and alerting configuration
   └── Rollback plan

7. Operations [AI: 30-50% automation]
   ├── Observability (logs + metrics + traces)
   ├── Automated incident response
   ├── Regular security audits
   └── Continuous optimization

8. Iteration [Loop back to step 1]
   ├── New requirements from production feedback
   └── Update context and documentation
```

## The Production Readiness Checklist

Use this checklist before every production deployment. Print it out, pin it to your monitor, or add it as a PR template.

### Testing

- [ ] Unit test coverage above 80% for core business logic
- [ ] Integration tests for all critical API endpoints
- [ ] E2E tests for primary user flows
- [ ] Tests run automatically in CI on every push
- [ ] Load tests verify the system handles expected traffic

### Security

- [ ] All inputs validated and sanitized
- [ ] Authentication on every protected endpoint
- [ ] Authorization checks (RBAC) implemented
- [ ] Secrets stored in environment variables or vault
- [ ] Dependencies scanned for vulnerabilities
- [ ] OWASP Top 10 checklist reviewed
- [ ] HTTPS enforced everywhere

### Scalability

- [ ] No N+1 database query problems
- [ ] Caching layer for hot data
- [ ] Expensive operations run asynchronously
- [ ] Rate limiting on all public endpoints
- [ ] Application can scale horizontally
- [ ] Database connection pooling configured

### Observability

- [ ] Structured logging with appropriate log levels
- [ ] Four Golden Signals monitored (latency, traffic, errors, saturation)
- [ ] Distributed tracing for multi-service flows
- [ ] Alerting rules configured with proper thresholds
- [ ] Dashboard for real-time system health

### Deployment

- [ ] CI/CD pipeline with automated tests and security scans
- [ ] Canary or blue-green deployment strategy
- [ ] Rollback procedure documented and tested
- [ ] Health check endpoints implemented
- [ ] Graceful shutdown handling

### Operations

- [ ] Incident response runbook created
- [ ] On-call rotation established
- [ ] Backup and disaster recovery plan tested
- [ ] AI-SRE tools configured for automated triage
- [ ] Postmortem process defined

## Key Takeaways

1. **The prototype is 10% of the work.** Plan your timeline accordingly. If the prototype took 1 day, expect 9 more days of engineering work before production.

2. **AI effectiveness decreases as complexity increases.** Use AI heavily for prototyping and test generation, but apply human judgment for security, architecture, and operational decisions.

3. **The six gates are sequential but not one-time.** Every new feature should pass through all six gates before reaching production.

4. **Observability is not optional.** If you cannot see what your application is doing in production, you cannot fix it when it breaks.

5. **Automate everything you can.** From CI/CD pipelines to incident response, automation reduces human error and response time.

The gap between "it works on my machine" and "it works reliably for thousands of users" is where engineering discipline matters most. AI tools are powerful accelerators, but they do not replace the need to think carefully about testing, security, scalability, and operations.

Use this checklist. Pass through all six gates. Ship with confidence.

## Related Reading

- [Claude Code Complete Guide](/posts/ai/2026-02-28-claude-code-complete-guide/) — Set up your AI development environment for production workflows
- [MCP Security 2026](/posts/ai/2026-03-10-mcp-security-2026/) — Deep dive into securing AI tool integrations
- [Vibe Coding Explained](/posts/ai/2026-02-28-vibe-coding-explained/) — Understanding the methodology behind AI-assisted development
- [AI Dev Environment Setup](/posts/ai/2026-03-10-ai-dev-environment-setup/) — Configure your tools for production-grade AI development
- [Context Engineering Guide](/posts/ai/2026-03-10-context-engineering-guide/) — Master the art of providing context to AI agents
- [Google SRE Book](https://sre.google/sre-book/introduction/) — The foundational text on site reliability engineering
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) — The industry standard for web application security risks

+++
date = '2026-01-31T22:00:00+08:00'
draft = false
title = '22 Thinking Frameworks That Turn Vague Ideas Into Clear Requirements'
description = 'A practical guide to SMART, OKR, MECE, JTBD, RICE, PDCA, and 16 more proven methodologies for defining goals, breaking down problems, writing requirements, prioritizing work, and improving continuously.'
toc = true
tags = ['Product Thinking', 'Mental Models', 'AI Collaboration', 'Requirements Analysis', 'Project Management']
categories = ['AI Guides']
keywords = ['product methodology', 'SMART goals', 'MECE principle', 'JTBD framework', 'RICE prioritization', 'OKR goal setting', 'requirements analysis', 'thinking frameworks for developers']
+++

"Build me a user management system."

You hand that sentence to an AI, and it spits out a pile of code. You open it up and it is nothing like what you had in mind. Or you spend thirty minutes explaining requirements to a colleague, only to discover you were talking about completely different things.

**The problem is not that the AI is not smart enough, or that your colleague is not cooperating. The problem is that the requirement was too vague.**

While researching how to communicate product requirements more effectively with AI, I compiled 22 classic methodologies. Some come from McKinsey, some from Toyota, some from Harvard Business School, but they all solve the same fundamental problem: **how to turn the fuzzy idea in your head into something others (including AI) can accurately understand and execute.**

This article is organized into five phases: **Define Goals, Break Down Problems, Describe Requirements, Prioritize, and Continuously Improve.** Each methodology includes real-world examples and practical tips for using it with AI.

## Phase 1: Define Goals — Know Where You Are Going

### 1. SMART: Write Goals That Are Not Wishes

[SMART](https://en.wikipedia.org/wiki/SMART_criteria) is the most widely used goal-setting framework, first introduced by management consultant George T. Doran in his 1981 paper *"There's a S.M.A.R.T. Way to Write Management's Goals and Objectives."* It requires goals to meet five criteria:

| Letter | Meaning | Bad Example | Good Example |
|--------|---------|-------------|--------------|
| **S**pecific | Clearly state what you will do | "Improve user experience" | "Reduce homepage load time to under 2 seconds" |
| **M**easurable | Include concrete metrics | "Get more users" | "Grow MAU from 10K to 30K" |
| **A**chievable | Realistic given your resources | "Build WeChat in three days" | "Complete login/signup module in two weeks" |
| **R**elevant | Connected to core objectives | "Add dark mode" (nobody asked) | "Optimize checkout flow (key conversion bottleneck)" |
| **T**ime-bound | Has a clear deadline | "Someday" | "Ship by February 15" |

**A real-world example:**

"I want to build a blog system" is not a goal. It is a wish. Rewritten with SMART:

> "By February 28, build a Hugo-based personal blog with Markdown support and automated deployment to GitHub Pages, with homepage load time under 3 seconds."

**Using it with AI:** Before sending a request to AI, run it through SMART. Instead of "write me a scraper," say "write a Python scraper that fetches the top 30 Hacker News stories (title and URL) daily, saves them as JSON, and runs in under 10 seconds." For more on communicating precise requirements to AI tools, see [AI Workflow Practical Guide](/posts/ai/2026-01-30-ai-workflow-real-guide/).

### 2. OKR: Aligning Goals Across Teams

OKR (Objectives and Key Results) was invented by Intel's Andy Grove and later brought to Google by John Doerr, where it scaled across the entire organization. The difference between SMART and OKR: **SMART governs the quality of a single goal; OKR governs the alignment of multiple goals.**

The structure is simple:

```
Objective: What do I want to achieve? — Qualitative, inspirational direction
Key Result: How will I know I achieved it? — Quantitative, measurable metrics
```

**Real example:**

```
O: Make new user registration feel effortless
  KR1: Increase registration conversion from 40% to 70%
  KR2: Reduce average registration time from 3 minutes to 45 seconds
  KR3: Improve 7-day retention after registration from 20% to 40%
```

Note: Key Results are not task lists ("launch Google login," "redesign registration page"). They describe the outcome changes you expect. How to get there is up to the team.

**Using it with AI:** When planning product direction, have AI help you structure goals in OKR format. Provide business context and ask it to suggest 3-5 Key Results. AI excels at breaking macro goals into measurable indicators and can surface dimensions you may have missed.

### 3. First Principles Thinking: Reason From the Ground Up

First principles thinking originates from Aristotle but was popularized by Elon Musk.

The core idea is straightforward: **ignore "how others do it" and "how it has always been done." Break the problem down to its most fundamental truths, then build your solution from scratch.**

Think of it like building a house. First principles thinking does not mean copying someone else's interior design. It means going back to "how much do bricks cost, how much does cement cost, how much does labor cost."

**Classic case: SpaceX rocket cost reduction**

When Musk wanted to build rockets, suppliers quoted $65 million per launch. The conventional approach would be to find cheaper suppliers or cut features. [Musk applied first principles](https://jamesclear.com/first-principles):

```
What raw materials make up a rocket? → Aluminum alloys, titanium, copper, carbon fiber
What do those materials cost on the open market? → About 2% of the rocket's price
Why the huge gap? → Middlemen, legacy processes, supply chain markups
Can we build it ourselves? → Yes.
```

SpaceX ended up reducing launch costs to one-tenth of NASA's.

**Using it with AI:** Before asking AI to solve a problem, ask yourself: "Am I stuck in the old way of doing things?" Instead of "optimize this SQL query," first consider: "Does this data really need real-time querying? Would pre-computation work?" For more on challenging habitual thinking, see [Product Thinking Playbook](/posts/ai/2026-01-30-product-thinking-delete-first/).

### 4. 5W2H: Ask All the Right Questions

5W2H is a checklist that helps you gather complete information upfront. Many projects fail not because of technical limitations, but because nobody clarified the basics from the start.

| Dimension | Question | Example |
|-----------|----------|---------|
| **What** | What are we building? | A user feedback collection system |
| **Why** | Why are we building it? | Current email-based collection is slow and loses feedback |
| **Who** | Who builds it? Who uses it? | Dev team: 2 engineers; Users: all paying customers |
| **When** | When is it needed? | MVP by Q1, iterate in Q2 |
| **Where** | Where will it be used? | Embedded in-product + standalone web page |
| **How** | How will it be built? | React frontend, Go backend, PostgreSQL database |
| **How much** | What are the costs? | $8K budget, 2 months development time |

**Using it with AI:** Before discussing requirements with AI, run through 5W2H first. You will find that many things you thought you had figured out are actually still unclear. Giving AI all this information upfront is ten times more efficient than going back and forth.

### 5. Occam's Razor: Keep It Simple

Occam's Razor, proposed by 14th-century philosopher William of Ockham, states: "Entities should not be multiplied beyond necessity." In plain language: **when multiple solutions can solve the problem, choose the simplest one.**

This is not laziness. It is respect for complexity. Every additional abstraction layer, dependency, or configuration option is another potential source of bugs.

**Example:**

The requirement is "remember user login state."

| Solution | Complexity | Maintenance Cost |
|----------|-----------|-----------------|
| JWT + Redis + token refresh + blacklist mechanism | High | High |
| Session + Cookie (framework built-in) | Low | Low |
| Browser localStorage + simple token | Medium | Medium |

If your product has only a few thousand users and no multi-device login requirement, the framework's built-in Session handling is sufficient. Insisting on the full JWT + Redis stack is over-engineering.

**Using it with AI:** When AI gives you a complex solution, follow up with: "Is there a simpler way to achieve the same result?" You will find that very often, there is. For more on the "subtract first" mindset, see [Why Taste Matters More Than Ever in the AI Era](/posts/ai/2026-01-23-taste-matters-in-ai-era/).

## Phase 2: Break Down Problems — Divide and Conquer

### 6. MECE: No Overlaps, No Gaps

MECE (Mutually Exclusive, Collectively Exhaustive) was [invented by Barbara Minto at McKinsey in the 1960s](https://www.mckinsey.com/alumni/news-and-events/global-news/alumni-news/barbara-minto-mece-i-invented-it-so-i-get-to-say-how-to-pronounce-it) as a core component of her famous Pyramid Principle. Minto was a 1963 Harvard Business School graduate (one of only 8 women among 600 students) and the first female MBA hired by McKinsey.

**Two core requirements:**
- **Mutually Exclusive (ME):** Categories do not overlap
- **Collectively Exhaustive (CE):** Categories cover all possibilities

Sounds obvious, but it is surprisingly easy to get wrong.

**Bad example:**

Classifying "user types" as "free users, VIP users, active users" is not MECE because a VIP user can also be an active user (overlap), and "silent paying users" are not covered (not exhaustive).

**Correct breakdown:**

```
By payment status: Free users / Paid users          ← MECE ✓
By activity level:  Active users / Inactive users    ← MECE ✓
Cross-reference:    Free+Active / Free+Inactive / Paid+Active / Paid+Inactive
```

**Using it with AI:** When breaking down requirements, ask AI to check whether your categories are MECE. For example, "Check if this classification has any overlaps or gaps." AI is excellent at logical validation — leverage this capability.

### 7. Pareto Principle: Focus on the Critical 20%

The Pareto Principle (80/20 Rule) states: **80% of results come from 20% of causes.**

This pattern was first observed by Italian economist Vilfredo Pareto in 1906 when he noticed that 80% of Italy's land was owned by 20% of the population. The ratio has since been validated across countless domains:

- 80% of bugs come from 20% of code modules
- 80% of user complaints concentrate on 20% of features
- 80% of revenue comes from 20% of customers

**Practical application:**

If you are optimizing an app's performance, instead of optimizing every endpoint, check your monitoring data and identify the slowest 20% of endpoints. Fixing those will likely improve 80% of the perceived user experience.

**Using it with AI:** Before asking AI to optimize, identify the critical 20% first. Instead of "optimize my entire project's performance," say "these three endpoints account for 80% of response time — help me optimize them."

### 8. 5 Whys: Keep Asking Until You Find the Root Cause

5 Whys is a core tool from the Toyota Production System, invented by Toyota founder Sakichi Toyoda. The method is extremely simple: **keep asking "why" about a problem, and by the fifth answer, you usually reach the root cause.**

**Example:**

```
Problem: User registration conversion rate dropped 30%

Why did it drop?           → Many users abandoned at the verification step
Why did they abandon?      → SMS verification codes often were not delivered
Why were they not delivered?→ The SMS provider throttles during peak hours
Why does it throttle?      → We are on the cheapest tier with concurrency limits
Why the cheapest tier?     → User volume was small when we set it up, and nobody reviewed it since
```

The surface problem is "conversion dropped." The root cause is "SMS provider tier selection is outdated, and there is no periodic review process." If you only looked at the surface, you might have redesigned the registration page UI — completely missing the point.

**Using it with AI:** Describe the problem to AI and ask it to keep asking "why." AI will not stop out of politeness — it will honestly drill all the way down to the root cause.

### 9. SWOT: Four Quadrants for Strategic Clarity

SWOT analysis is a staple of business school curricula. It evaluates a project or product across four dimensions: **S**trengths, **W**eaknesses, **O**pportunities, and **T**hreats.

**Real example: Should we build an AI writing assistant?**

| | Favorable | Unfavorable |
|------|-----------|-------------|
| **Internal** | **S:** Team has NLP expertise, existing user base | **W:** Limited funding, no B2B sales experience |
| **External** | **O:** Exploding demand for AI writing, companies want to cut costs | **T:** Big tech offers free products, low user trust in AI content |

The value of SWOT is not in filling out the table but in the **strategic implications** that follow:

- **SO Strategy** (leverage strengths to seize opportunities): Use NLP expertise to build customized enterprise writing tools
- **WT Strategy** (avoid weaknesses and threats): Do not build a general-purpose writing tool, avoid competing with big tech

**Using it with AI:** Before making product decisions, ask AI to run a SWOT analysis. Provide your product context and market information, and have it analyze from all four dimensions. AI can help you spot threats and opportunities you might have overlooked.

## Phase 3: Describe Requirements — Make Others (and AI) Understand Exactly What You Want

### 10. JTBD: Focus on the Job the User Needs Done

JTBD (Jobs To Be Done) was proposed by Harvard Business School professor Clayton Christensen. The core insight: **users do not "buy products" — they "hire products to get a job done."** Christensen pointed out that [75-85% of new products fail in the market](https://www.christenseninstitute.org/theory/jobs-to-be-done/) precisely because they miss the "job" users actually need done.

**The classic example — McDonald's milkshakes:**

McDonald's wanted to boost milkshake sales. The traditional approach was surveys asking "what flavor milkshake do you want?" They changed the recipe based on feedback. Sales did not budge.

Then Christensen's research team took a different approach: instead of asking what customers wanted, they observed when people bought milkshakes and where they drank them.

They discovered: **40% of milkshakes were sold before 8:30 AM, bought by commuters driving to work.**

The "job" they were "hiring" the milkshake for: **something you can eat one-handed during a boring commute, that keeps you full until lunch, and is more interesting than bread.**

The milkshake's competitors were not other milkshakes — they were bananas, energy bars, and bagels.

Understanding this "job," McDonald's made morning milkshakes thicker (takes longer to drink) and added fruit chunks (more texture). Sales increased 7x.

**Using it with AI:** When describing requirements, do not just say "I want feature X." Say "my users need to accomplish task X in scenario Y, and their current pain point is Z." This gives AI the context behind the "why" and produces far more relevant solutions.

### 11. User Stories: Three-Part Requirement Descriptions

The standard user story format:

```
As a [type of user],
I want [some action or feature],
So that [I achieve some value or outcome].
```

This format forces you to answer three questions: **Who needs it? What do they need? Why do they need it?**

**Example:**

```
Bad:  "Build an export feature"

Good: "As an operations manager,
       I want to export last week's user behavior data as Excel,
       So that I can present it at Monday's team meeting."
```

What does the second version add? **Context.** You now know who uses it (operations manager), what scenario (Monday meeting), and what format (Excel). These details directly affect technical decisions — data volume, async export needs, format customization requirements.

**Using it with AI:** Give AI requirements in user story format. AI excels at extracting key information from structured input. Try it — the results are dramatically better than one-liner requests. Many AI coding tools also support [Skills or custom instructions](/posts/ai/2026-01-19-agent-skills-new-programming/) to preset requirement templates, making this workflow even smoother.

### 12. GWT Acceptance Criteria: Define What "Done" Actually Means

GWT (Given/When/Then) is a standard acceptance criteria format from Behavior-Driven Development (BDD):

```
Given: Some precondition
When:  The user performs some action
Then:  The system should produce some result
```

**Why do you need it?**

Because "done" means completely different things to different people. The product manager thinks "it works." QA thinks "all edge cases are covered." The CEO thinks "it also needs to look good." GWT nails down acceptance criteria explicitly, eliminating ambiguity.

**Real example:**

```gherkin
Feature: User Login

Scenario: Successful login
  Given the user is registered and account is active
  When  the user enters correct email and password, then clicks login
  Then  redirect to homepage showing user's display name

Scenario: Wrong password
  Given the user is registered
  When  the user enters correct email but wrong password
  Then  show "Incorrect email or password" without revealing which one is wrong

Scenario: Account locked
  Given the user has entered wrong password 5 times
  When  the user attempts a 6th login
  Then  show "Account locked. Please try again in 30 minutes"
```

**Using it with AI:** This is a game-changer for AI collaboration. Give AI GWT-format acceptance criteria and the resulting code will be significantly more accurate. You can also have AI generate test cases directly from GWT — one methodology solving both requirement specification and test coverage.

### 13. Kano Model: Not All Requirements Are Equal

The [Kano Model](https://en.wikipedia.org/wiki/Kano_model) was proposed by Tokyo University of Science professor Noriaki Kano in 1984. At the time, conventional wisdom held that "handling complaints + enhancing popular features" was sufficient to improve satisfaction. Kano's research with 900 participants proved customer satisfaction is far more nuanced. He classified requirements into several types:

| Type | Characteristic | Example (food delivery app) |
|------|---------------|---------------------------|
| **Must-be** | Expected by default; absence causes anger | Can place orders, pay, track delivery |
| **One-dimensional** | More is better; less is worse | Delivery speed, food temperature, support response time |
| **Attractive** | Delights when present; not missed when absent | Auto-sends coupons on rainy days, live rider animation |
| **Indifferent** | Users do not care either way | Changing the app icon color |
| **Reverse** | Actually annoys users when present | Forced social sharing to unlock coupons |

**Key insight:** Get Must-be requirements rock-solid first, then invest in One-dimensional improvements, and finally differentiate with Attractive features. A common mistake is chasing Attractive features while Must-be requirements are broken — payments fail regularly, but the team spent a month building a flashy splash screen animation.

**Using it with AI:** When discussing feature lists with AI, classify them using the Kano Model first. Tell AI "this is Must-have — it needs to be stable and reliable; that is Nice-to-have — a simple implementation is fine." This helps AI allocate solution complexity appropriately.

### 14. SCQA: Structure Your Communication

SCQA is a narrative framework recommended by Barbara Minto (yes, her again) in the Pyramid Principle, using four steps to communicate complex information clearly:

| Step | Meaning | Example |
|------|---------|---------|
| **S**ituation | Shared context everyone knows | "Our app has reached 100K MAU" |
| **C**omplication | What went wrong | "But 7-day retention for new users is only 15%, far below the 30% industry average" |
| **Q**uestion | The core question to answer | "How do we raise 7-day retention above 25%?" |
| **A**nswer | Your proposed solution | "Optimize onboarding flow + add next-day push notification touchpoints" |

**Why does SCQA work?**

Because most people communicate by narrating from beginning to end — spending forever on background while the listener still has no idea what the point is. SCQA forces you to **create tension before offering an answer**, helping the listener (or the AI reading your requirement doc) immediately grasp the key issue.

**Using it with AI:** When discussing a complex requirement with AI, lead with SCQA format. For example:

> "Our blog system is built on Hugo, and each article requires manually creating directories and writing front matter (S). As article count grows, this process is increasingly slow and error-prone (C). Is there a way to automate this workflow (Q)? I want a script or tool where I input a title and it generates the complete article scaffold (A)."

This gives AI immediate clarity on your context, pain point, and expectation, resulting in far more precise solutions.

## Phase 4: Prioritize — Decide What to Do First

### 15. Eisenhower Matrix: Urgent Does Not Mean Important

This matrix is attributed to President Eisenhower's quote: "What is important is seldom urgent and what is urgent is seldom important." It sorts tasks into four quadrants based on **urgency** and **importance**:

| | Urgent | Not Urgent |
|------|--------|------------|
| **Important** | **Q1: Do immediately** Server down, P0 production bug | **Q2: Schedule it** Architecture improvements, tech debt, team training |
| **Not Important** | **Q3: Delegate** Routine meetings, non-critical emails | **Q4: Eliminate** Meaningless group chats, over-polishing internal docs |

**Key insight:** Most people spend their time in Q1 (firefighting) and Q3 (busywork), but long-term success is determined by **Q2** — important things that are not urgent.

**Using it with AI:** Give AI your to-do list and ask it to classify items using the Eisenhower Matrix. AI will not be swayed by the emotional urgency of the moment and can more objectively distinguish what is truly important.

### 16. MoSCoW: Four-Tier Priority Classification

[MoSCoW](https://en.wikipedia.org/wiki/MoSCoW_method) was created by Dai Clegg in 1994 at Oracle UK Consulting and later widely adopted through the DSDM agile framework. It divides all requirements into four tiers:

| Tier | Meaning | Suggested Proportion |
|------|---------|---------------------|
| **Must have** | Non-negotiable for this release | ~60% |
| **Should have** | Important but will not block the release | ~20% |
| **Could have** | Nice to have if time permits | ~20% |
| **Won't have** | Explicitly out of scope for this release | — |

**"Won't have" is the most important tier.** Many projects fail not because they did too little, but because they tried to do everything. Writing down what you will *not* do matters more than listing what you will — it sets boundaries.

**Practical example:**

```
Project: Internal Knowledge Base System v1

Must have:
  - Document create, edit, delete
  - Full-text search
  - Role-based access control

Should have:
  - Markdown editor (plain text is fine for now)
  - Document version history

Could have:
  - AI-powered smart search
  - Document templates

Won't have (explicitly out of scope):
  - Multi-language support
  - Mobile app
  - Third-party integrations (Slack, Teams)
```

**Using it with AI:** When assigning tasks to AI, explicitly communicate MoSCoW tiers. For example, "Complete the three Must-have features first. Add the two Should-haves if time permits. Ignore Could-haves for now."

### 17. RICE: Score Your Priorities Objectively

The RICE scoring framework was [developed by Sean McBride on Intercom's product team](https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers/), using four dimensions to score each requirement for more objective prioritization. Intercom created it after realizing their previous approach biased toward "pet projects" rather than ideas that truly impacted the most customers.

| Dimension | Meaning | How to Score |
|-----------|---------|-------------|
| **R**each | How many users will this affect? | Concrete number (e.g., 5,000/month) |
| **I**mpact | How much will each user be affected? | 3=massive / 2=high / 1=medium / 0.5=low / 0.25=minimal |
| **C**onfidence | How confident are you in these estimates? | 100%=data-backed / 80%=experience-based / 50%=gut feeling |
| **E**ffort | How many person-months of work? | Person-months (e.g., 2) |

**Formula:**

```
RICE Score = (Reach × Impact × Confidence) / Effort
```

**Scoring example:**

| Requirement | Reach | Impact | Confidence | Effort | RICE Score |
|-------------|-------|--------|------------|--------|-----------|
| Optimize search results | 5,000 | 2 | 80% | 2 | 4,000 |
| Add dark mode | 2,000 | 1 | 80% | 3 | 533 |
| Refactor payment module | 5,000 | 3 | 50% | 5 | 1,500 |

The conclusion is clear: **optimize search results first.**

**Note:** RICE is a reference, not law. Some low-scoring items may be prerequisites for high-scoring ones, and some are "table stakes" (must-have to even compete). Always combine with practical judgment.

### 18. MVP: Build the Smallest Complete Loop

MVP (Minimum Viable Product) core principle: **build the fewest features needed to complete a full usage loop, ship fast, and validate value.**

The keyword is "loop" — not building half a product and abandoning it, but letting users walk through the entire flow, with each step in its simplest possible form.

**Classic case: Dropbox**

Dropbox's MVP was not a bare-bones cloud drive. It was a 3-minute demo video. Founder Drew Houston demonstrated the file sync concept and posted it to Hacker News. Overnight, the waitlist grew from 5,000 to 75,000 people.

### 19. MLP: Make Users Want to Come Back

MLP (Minimum Lovable Product) was [proposed by Aha! CEO Brian de Haaff in 2013](https://www.aha.io/roadmapping/guide/plans/what-is-a-minimum-lovable-product). It is an evolution of MVP — not just "usable" but including key experience elements that make users *want* to keep using it.

**How to choose:**

| Scenario | Choice | Reason |
|----------|--------|--------|
| New market, demand unvalidated | MVP | Validate before investing |
| Market validated, many competitors | MLP | No differentiated experience = no users |
| Extremely limited resources | MVP | Survival comes first |
| Some resources, targeting retention | MLP | Experience drives retention |

**Using it with AI:** Have AI help you identify "which features form the MVP loop and which are MLP experience boosters." With clear boundaries, AI will not over-engineer or miss critical flows.

### 20. Pre-mortem: Assume Failure and Work Backwards

Pre-mortem is a technique [proposed by psychologist Gary Klein in the Harvard Business Review](https://hbr.org/2007/09/performing-a-project-premortem), endorsed by Nobel laureate Daniel Kahneman. A 1989 study showed that this "prospective hindsight" approach can **increase the ability to accurately predict risks by 30%.**

The approach is counterintuitive: **before the project starts, assume it has already failed, then have the team work backwards to identify why it might have failed.**

Why is this more effective than traditional "risk assessment"? When you say "let's think about risks," nobody wants to be the pessimist. But when you say "the project has failed — why do you think it happened?" — the psychological barrier disappears, and people speak freely.

**How to do it:**

```
Step 1: Announce "Assume our project has completely failed 3 months from now"
Step 2: Everyone independently writes down "possible reasons for failure"
Step 3: Collect, categorize, identify frequently mentioned causes
Step 4: Create prevention measures for high-frequency causes
```

**Common failure cause template:**

| Category | Typical Causes |
|----------|---------------|
| **Technical** | Cannot handle load, unstable third-party APIs, data migration errors |
| **Process** | No rollback plan, insufficient test coverage, chaotic deployment |
| **People** | Key developer quits mid-project, cross-team collaboration stalls |
| **Requirements** | Major scope changes mid-project, edge cases not considered |
| **External** | Regulatory changes, competitor launches first |

**Using it with AI:** This is where AI truly shines. Give AI your project plan and ask it to "assume this project failed — list 10 most likely reasons." AI has no interpersonal concerns and will very directly point out risks you have not considered.

## Phase 5: Continuously Improve — What Happens After Launch

### 21. PDCA: The Continuous Improvement Flywheel

The PDCA cycle (also called the Deming Cycle) was popularized by quality management pioneer W. Edwards Deming and is a cornerstone of lean manufacturing and Six Sigma. Its four steps form a continuously spinning flywheel:

```
Plan → Do → Check → Act → Plan again...
```

Sounds obvious? The key insight is that **most people skip the Check and Act steps.**

**Real example:**

```
Plan:  This week, optimize search. Target: reduce response time from 2s to 500ms
Do:    Added Elasticsearch index, rewrote query logic
Check: Post-launch measurement shows 800ms — did not hit target;
       discovered tokenization strategy caused oversized index
Act:   Adjust tokenization strategy, optimize index structure → enter next PDCA cycle
```

Each cycle makes the system slightly better. It looks slow, but the compounding effect is remarkable.

**Using it with AI:** Every time AI helps you build something, do not stop at "it runs." Add a Check round: "Review this code for performance issues or security vulnerabilities," then Act based on the feedback. This is PDCA applied to AI collaboration. For more on building feedback loops in AI development, see [My AI Development Workflow: From Requirements to Production](/posts/ai/2026-01-19-ai-dev-workflow/).

### 22. Design Thinking: User-Centered Innovation Process

[Design Thinking](https://designthinking.ideo.com/) was popularized by IDEO and has been widely adopted by Uber, Airbnb, IBM, and others. It is a **user-centered innovation process** with five stages:

```
Empathize → Define → Ideate → Prototype → Test
```

| Stage | What to Do | Core Question |
|-------|-----------|---------------|
| **Empathize** | Observe and interview users | What are users' real pain points? |
| **Define** | Distill the core problem | What problem are we actually solving? |
| **Ideate** | Divergent thinking, no judgment | What are the possible solutions? |
| **Prototype** | Build low-cost prototypes quickly | Can we get something tangible in front of users? |
| **Test** | Put it in users' hands, gather feedback | Does the solution actually solve the problem? |

Design Thinking's power lies in being the "operating system" for all the other methodologies. Use JTBD during Empathize, MECE and 5 Whys during Define, SCQA during Ideate, MVP during Prototype, and GWT during Test.

**Using it with AI:** AI can contribute at every Design Thinking stage — analyzing user feedback data during Empathize, helping with MECE breakdowns during Define, brainstorming solutions during Ideate, rapidly generating code during Prototype. Use Design Thinking as your overarching framework for AI collaboration and productivity will increase significantly. For practical implementation guidance, see [Claude Code Best Practices](/posts/ai/2026-01-06-claudecode-best-practices/).

## Putting It All Together: A Complete Requirements Analysis Workflow

These 22 methodologies are not independent — they chain into a complete workflow:

```
1. Define Goals
   SMART        → Write each goal with precision
   OKR          → Ensure goals align with each other
   First Principles → Verify the goal itself is correct
   5W2H         → Fill in all relevant information
   Occam's Razor → Confirm you are not over-engineering

2. Break Down Problems
   MECE         → No overlaps, no gaps
   Pareto       → Find the critical 20%
   5 Whys       → Drill to the root cause
   SWOT         → Map internal and external landscape

3. Describe Requirements
   JTBD         → Identify the job users need done
   User Stories  → Use the standard three-part format
   GWT          → Write explicit acceptance criteria
   Kano Model   → Classify requirement types
   SCQA         → Structure your communication

4. Prioritize
   Eisenhower   → Separate urgent from important
   MoSCoW       → Four-tier classification
   RICE         → Quantitative scoring
   MVP/MLP      → Define the scope of v1
   Pre-mortem   → Identify risks upfront

5. Continuously Improve
   PDCA         → Check and improve every iteration
   Design Thinking → Keep innovating with users at the center
```

**This workflow is especially powerful when discussing product requirements with AI.** You do not need to use all 22 every time, but running through the relevant ones will noticeably improve AI output quality — because you improved the input quality first.

## Conclusion

Methodologies are tools, not dogma. Just as you would not use a wrench every time you tighten a screw (sometimes your fingers are fine), you do not need to run through all 22 methodologies every time you write a requirement.

But when you find that:

- Goals are unclear → Try SMART + OKR
- Requirements are vague → Try User Stories + GWT + SCQA
- You do not know what to do first → Try RICE + MoSCoW + Eisenhower
- Solutions are too complex → Try Occam's Razor + Pareto Principle
- Projects keep hitting surprises → Try Pre-mortem + SWOT
- Features are built but unused → Try JTBD + Kano + 5 Whys
- You do not know what comes next → Try PDCA + Design Thinking

Come back to this article, pick one or two methodologies, and apply them. You do not need to memorize them all — just reference them when needed.

**The real value of these methodologies is not making you look professional. It is helping you transform the fuzzy ideas in your head into something clear, understandable, and actionable.** Whether you are communicating with people or collaborating with AI, this is the most essential skill.

### Further Reading

- [Product Thinking Playbook: Delete First, Question Everything](/posts/ai/2026-01-30-product-thinking-delete-first/) — Making product decisions through subtraction
- [Why Taste Matters More Than Ever in the AI Era](/posts/ai/2026-01-23-taste-matters-in-ai-era/) — When AI can do everything, deciding what is worth doing becomes the key question
- [AI Workflow Practical Guide: From Prompts to Production](/posts/ai/2026-01-30-ai-workflow-real-guide/) — Turning AI from a chat toy into a productivity tool
- [My AI Development Workflow: From Requirements to Production](/posts/ai/2026-01-19-ai-dev-workflow/) — Real-world AI integration across the full software development lifecycle

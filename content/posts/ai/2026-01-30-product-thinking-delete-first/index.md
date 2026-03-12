+++
date = '2026-01-30T10:30:00+08:00'
draft = false
title = 'Delete Before You Optimize: 3 Product Thinking Rules for Solo Developers'
description = 'A practical product methodology for indie hackers and solopreneurs: delete before optimizing, question every assumption, and observe real users. With real-world examples and a reusable decision framework.'
toc = true
tags = ['Product Thinking', 'Indie Development', 'Solopreneur', 'Product Strategy']
categories = ['AI Guides']
keywords = ['product thinking for developers', 'delete before optimize', 'indie developer methodology', 'solopreneur product strategy', 'product decision framework']
+++

What is the most common mistake people make when building products?

It is not building too little. It is **building too much**.

After years of building products, the biggest trap I fell into was not shipping bad features — it was spending weeks polishing a feature that should never have existed. This kind of "productive waste" is especially deadly for solo developers and solopreneurs. We do not have a big company's resources to absorb mistakes. Every day spent on the wrong thing is a day we cannot get back.

Here are three product thinking rules I have internalized and battle-tested. They sound simple, but very few people actually follow them.

## 1. Delete Before You Optimize: Ask "Should This Exist?"

When most product managers (including my past self) see a feature that is not working well, the instinct is to optimize it — better UI, smoother flow, faster performance.

**That instinct is wrong.**

The correct thinking sequence is:

```
Does this feature need to exist? → Can we just remove it? → Only optimize if removal is not an option
```

This is not laziness. It is **zero tolerance for sunk costs**.

### A Real-World Lesson

I once spent two full weeks optimizing an "advanced filter" feature for a tool product — redesigning the interaction, tweaking the UI, adding caching, writing documentation. After launch, I checked the data: usage was nearly zero.

Why? Because users did not want to manually filter anything. What they actually wanted was **one-click recommendations**.

If I had checked the data first and asked "should this feature exist?", those two weeks could have gone toward something that actually mattered.

### How to Decide: Delete or Optimize?

Ask yourself three questions:

| Question | If the answer is "No" |
|----------|----------------------|
| How many users used this feature in the last 30 days? | Usage < 5% → consider deleting |
| If we removed it tomorrow, would anyone complain? | No complaints = nobody cares |
| Is this feature on the core value chain? | Not on it = safe to cut |

**Especially important for solopreneurs**: Your time is your most expensive resource. Every feature you maintain is energy stolen from what truly matters. The more ruthlessly you cut, the longer you survive.

### What Tesla's Production Line Teaches Us

In Tesla's early production lines, a set of automation robots was severely slowing down the entire assembly process. The solution was not to optimize the robot software — it was to physically cut the robots off the line. They had to saw a hole in the wall just to get them out.

It sounds extreme, but the logic is clear: **If something's existence is the problem, optimizing it is pointless. Removing it is the solution.**

This thinking applies across many domains:

- **Code**: Instead of optimizing hard-to-maintain code, ask "do we still need this logic?"
- **Product**: Instead of optimizing a low-usage feature, ask "do users actually need this?"
- **Personal**: Instead of optimizing an inefficient habit, ask "should I be doing this at all?"

For more on subtraction thinking in the AI era, see [Why Personal Taste Matters More Than Ever in the AI Age](/posts/ai/2026-01-23-taste-matters-in-ai-era/).

## 2. Question Every Assumption Until You Find the Source

Product development is full of "industry best practices" and unquestioned conventions:

- "Every SaaS needs multi-tenant architecture"
- "Landing pages must have a demo video"
- "You need to post content daily"
- "An MVP must include a user authentication system"

Who told you these things? **Are they laws of physics?**

Most of the time, these "must-haves" are just **inertia** — something you picked up from a blog post, a conference talk, or a peer, and then accepted as truth without verification.

### Trace Every Requirement to a Specific Person

A powerful thinking habit: **For every requirement, ask who specifically requested it.**

- If a user requested it → validate with data
- If your boss requested it → understand the real need behind it
- If "everyone does it" → it is almost certainly worth questioning

Never accept vague sources like "legal said so", "industry standard", or "we have always done it this way." Every requirement should have a name attached and data to back it up.

### A Classic Cost Example

A large manufacturing company received a supplier quote of $120,000 for a single component. The justification? "Industry standard pricing." Someone felt the number was off and pushed the engineering team to investigate. They ended up building it themselves for about $5,000.

A 24x difference. No one had questioned it before because it came from "the supplier's quote."

### What This Means for Indie Developers

The assumptions we need to challenge are not other people's — they are **the ones inside our own heads**:

```
"Obviously true" → Question → Validate → Keep or cut

"I need a PRD before building" → Really? If you are solo, is a rough sketch enough?
"I must test everything before launch" → Really? Can you ship 50% and see if anyone uses it?
"Competitors have feature X, so I need it too" → Really? Is that why users choose you?
```

Strip away these invisible chains and your MVP becomes lighter and faster. For how to build MVPs efficiently with AI, see [My AI Development Workflow: From Requirements to Launch](/posts/ai/2026-01-19-ai-dev-workflow/).

## 3. Go to the Front Lines: Data Does Not Tell the Whole Story

Many product people make decisions purely by data — DAU, retention, funnel conversion rates. That is not wrong, but it is far from enough.

**Data tells you what happened. It cannot tell you why.**

### When Metrics Lied to Me

I built a small WeChat tool once. The dashboard showed "average session duration: 5 minutes." That sounds great, right? Users spending 5 minutes means deep engagement.

Then I did remote observation sessions with a few real users, watching them use the product for 15 minutes.

The truth hit hard: those 5 minutes were not "deep engagement." Users were **stuck on a step, trying and failing repeatedly**. They were not using the product — they were fighting it.

If I had only looked at the data, I would never have discovered this.

### My Front-Line Observation Method

You do not need to sleep on the factory floor, but you do need a system for **regularly observing real users**:

**At least one user observation per month**:

1. Find a real user (paying customers first)
2. Remote screen share or screen recording
3. Watch them use your product end-to-end (at least 15 minutes)
4. **Do not guide. Do not explain.** Just watch silently.
5. Note every point where they get stuck

This is the essence of Tencent's famous **10/100/1000 rule**:

| Level | Action | Frequency |
|-------|--------|-----------|
| 10 | Deep conversations with 10 users | Monthly |
| 100 | Read 100 pieces of user feedback | Weekly |
| 1000 | Monitor 1000 user behavior data points | Daily |

### Remote Observation Tips

- **Never ask "what do you think?"** — users will politely say "it is fine." Watch what they actually do.
- **Watch for hesitation** — where the cursor stops is where confusion lives.
- **Screen recordings are 100x more valuable than surveys** — 5 minutes of video beats 50 questionnaire responses.

## 4. The Complete Decision Framework: Putting It All Together

These three rules are not isolated principles. They form a complete product decision chain:

```
Step 1: Delete
  → Does this feature/requirement/process need to exist?
  → What does the data say? Would anyone complain if we removed it?
  → If you can delete it, delete it. Do not hesitate.

Step 2: Question
  → For everything that remains, what is the evidence?
  → Who requested it? Is there data to support it?
  → Or is it just "industry standard" / "everyone does it"?

Step 3: Validate
  → After building, observe how real users interact with it
  → Do not just look at data — watch people
  → If you find problems, go back to Step 1
```

This is a loop, not a one-time exercise. Every iteration should run through this chain.

## Key Takeaways

Three rules, distilled to three sentences:

1. **Delete before optimize**: If something should not exist, no amount of polish will make it worthwhile.
2. **Trace to the source**: Every requirement needs a name and data behind it. Reject vague "best practices."
3. **See it yourself**: Data is the map, but you have to walk the ground to know the real terrain.

These rules are useful for PMs at large companies, but they are **critical for indie developers and solopreneurs** — because every minute and every line of code is yours alone. Effort in the wrong direction is not hard work; it is self-sabotage.

In the AI era, this mindset matters more than ever. When AI can produce at high speed for you, "what to build" becomes a hundred times more important than "how to build it." For more on this topic, see [AGI Is Already Here in 2026: From Feature Definition to a 31-Minute Recruiting Sprint](/posts/ai/2026-01-26-agi-is-here/).

### Related Reading

- [Why Personal Taste Matters More Than Ever in the AI Age](/posts/ai/2026-01-23-taste-matters-in-ai-era/)
- [My AI Development Workflow: From Requirements to Launch](/posts/ai/2026-01-19-ai-dev-workflow/)
- [AGI Is Already Here in 2026: From Feature Definition to a 31-Minute Recruiting Sprint](/posts/ai/2026-01-26-agi-is-here/)
- [AI Workflow Playbook: From Prompts to Programming](/posts/ai/2026-01-30-ai-workflow-real-guide/)

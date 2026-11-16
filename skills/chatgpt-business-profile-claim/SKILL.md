---
name: "chatgpt-business-profile-claim"
description: "Use when a business, or the agency or freelancer working for it, wants to claim, verify, create or manage its profile in ChatGPT (Businesses in ChatGPT, Business Hub). Decides the path (claim, create, dispute, wait), prepares everything before the owner opens Business Hub, writes the owner's step-by-step instructions and the DNS TXT handoff, then sets up the profile and reads its insights every month. Triggers: claim my business on ChatGPT, ChatGPT business profile, Business Hub, blue check on ChatGPT, ChatGPT business insights, اعمل كليم على ChatGPT, بروفايل الشركة في ChatGPT."
---

# ChatGPT Business Profile Claim

OpenAI launched Businesses in ChatGPT in beta on November 10, 2026. Through a dashboard called Business Hub, a business can claim the profile ChatGPT shows for it, correct its details, add products, and see how often ChatGPT mentions it and sends clicks to its website.

This skill turns that into a repeatable workflow: decide which path the business is on, prepare everything before anyone touches Business Hub, give the owner clear instructions, then set up the profile and track it.

**The owner claims. You prepare and guide.** This split is the core of the skill. A profile locks to the ChatGPT account that first claims it, cannot be transferred, and cannot be deleted once published. A claim made from the wrong account is close to irreversible.

---

## Governing Rules

1. **Never click Get started then Continue in the claim window for someone else.** Continuing accepts OpenAI's Businesses in ChatGPT Terms, and the owner has to agree to them knowingly.
2. **Never submit the identity check (Persona) or type ID, tax or registration numbers.** Those belong to the owner.
3. **Never claim a client's business from your own account.** The owner claims with a company account, then adds you.
4. **Searching Business Hub and opening a listing's preview to read its status is fine.** Stop at the claim window.
5. **Claiming is not ranking.** A claimed profile controls what ChatGPT says about the business details. It does not change whether ChatGPT recommends the business. Say this to the client before they expect traffic.
6. **The feature is in beta.** Recheck OpenAI's help article ("Setting up your business on ChatGPT") before relying on any rule here, and label anything you could not confirm.
7. **No em dashes or en dashes** in anything you write for the client.

---

## Step 0: Summary of Understanding

Before any checks, come back with what you understood: the business name, website, country, type (local with a physical location, online, or service), whether it has a Google Business Profile, and what the user wants (just the path, the full preparation, or the post-claim setup). Get confirmation before you start.

---

## Step 1: Triage the Path

Work through these in order and record each answer.

### 1. Country

Business Hub is open to eligible businesses in every market where ChatGPT is available, so **starting** a claim works almost anywhere. **Finishing** it is different: the Persona identity check asks for an SSN or EIN and a physical address (no PO box), which in practice limits full verification to businesses with a US entity. Until you have tested a non-US business end to end, treat non-US completion as unconfirmed.

Business Agents (the optional chat assistant on the profile) are US only.

### 2. Business type

- **Local business with a physical location:** can claim an existing listing. OpenAI's help center says local stores and restaurants can claim only an existing US listing, but a test from outside the US showed local listings in that country opening the claim window with Get started. Record which one you see.
- **Online business:** can claim an existing listing, or **Create** one if none exists. Online listings show a website URL instead of an address in search results.

### 3. Regulated category

Trading, CFDs, forex, lending, health and similar categories can be declined or held back by OpenAI on safety or integrity grounds, and products must be lawfully offered and licensed. Flag these and confirm the legal entity and licence the business will claim under before any other step. A published profile cannot be removed, so a mistake here does not get undone.

### 4. Search the listing

Search Business Hub (chatgpt.com/business-hub) by the name customers know, and check the address under each result.

**A listing does not need a Google Business Profile.** ChatGPT builds listings from other sources across the web, so a business with no Google profile can still be listed. Try every name it is known by, including former names and brand names, before you decide it is missing and Create one.

**Search results are biased to the searcher's location.** From one country, searching for a business in another country usually returns only nearby businesses, even with the other city typed in. A missing result when you search from abroad is not proof the listing does not exist. The owner, or someone in the business's country, should run the search.

### 5. Read the status, which decides the path

| What you see | Path |
|---|---|
| Listed, claim window opens | **Claim** |
| Not listed, online business | **Create** |
| Already claimed by someone else | **Dispute**: ••• menu, Dispute ownership, then Persona. The profile stays visible while the dispute is pending. |
| "Contact support" instead of a claim option | **Locked** (common with multi-location brands). The owner selects Contact support. |
| Local business, not listed | **Wait**, and do the site readiness work below meanwhile |

---

## Step 2: Readiness Checklist

Collect all of this before the owner opens Business Hub. Each item is here because missing it stalls or breaks the claim.

- [ ] **Written authorization** from the owner for you to prepare and manage the profile.
- [ ] **The owning account is decided:** a company-controlled ChatGPT account the business will keep, not one employee's personal login. The claiming account becomes the admin, and access has to survive staff changes. Any ChatGPT plan, including free, can claim.
- [ ] **One verification method the owner can complete today.** ChatGPT only shows the methods available for that business:
  - Business phone: an SMS or automated call code to the listed number. Someone has to answer it.
  - Business email: a code to an address on the business's own domain.
  - Website domain: a DNS TXT record. Confirm who holds DNS access (Cloudflare, GoDaddy, the host) and that it is not a former employee or an old developer.
  - Shopify: connect the store and log in.
- [ ] **Persona documents ready**, copied from official records into a note before opening Persona: legal name, physical address, registration or tax number, one photo ID, and a business document of up to 10 pages showing the business name and legal name. A mismatch with official records fails the check.
- [ ] **Profile copy drafted**, matching the website word for word:
  - About text, 300 characters maximum (about two sentences)
  - Category, in the plain words a customer would use
  - Delivery policy and return policy, copied from the website
  - Logo and an optional cover photo
- [ ] **Terms read by the owner.** At minimum, point out: a permanent licence over the submitted name, address, contact details, category, hours and website; ChatGPT may phone the business on behalf of its users unless the owner opts out; submitting a product feed sets aside crawler and text-and-data-mining opt-outs.
- [ ] **Name, address and phone are identical** across the website, Google Business Profile, Bing Places and directories.

---

## Step 3: Owner Instructions

Write a short numbered message for the owner, based on the path.

### Claim path

1. Sign in to ChatGPT with the agreed company account. If OpenAI emailed you a claim invitation, open that link and sign in with the address that received it. Never forward the invitation.
2. Open Business Hub from the ChatGPT sidebar, or go to chatgpt.com/business-hub.
3. Search the business name and pick the result whose address matches. For more than one location, pick the right one: each location and each brand is claimed separately.
4. Select Get started, check the account shown under "You can manage this profile", then select Continue. This accepts OpenAI's terms.
5. Choose the verification method we prepared and complete it.
6. Wait for OpenAI's review email. While the claim is under review you can cancel it (Cancel claim). OpenAI publishes no timeline.
7. After approval, complete Persona: Verify with Persona, then Continue to Persona. If you skipped it, go to the Business tab, open the profile and select Complete verification with Persona. Review usually takes a few days. The blue check appears when Persona approves, not when the claim is approved. Until then the profile shows in the dashboard but its details cannot be edited: ChatGPT asks for the government-issued ID first.
8. Add us from Business Hub, using our own ChatGPT account.

### Create path (online business)

Steps 1 and 2 above, then:

1. Select the Create row, then Get started.
2. Choose how customers reach the business. Pick the true option, even if another one looks faster.
3. Add the website. It must start with https and be a domain the business owns.
4. Verify the domain with the TXT record (Step 4 below), then select Verify domain.
5. Select the category, add the description, the phone and the email, and verify the code.
6. Answer the delivery and returns questions, then Submit.
7. The result is a **draft** customers cannot see. Persona approval publishes a created profile automatically, so every field has to be final before you submit Persona.

---

## Step 4: DNS TXT Handoff

When the domain method is used, write a note for whoever manages DNS:

- Copy all three parts exactly as ChatGPT shows them: **Type, Name (Host) and Value**.
- Add the record the same day. It expires about 24 hours after it is shown.
- A short TTL, such as 5 minutes, helps it apply faster.
- Then go back to ChatGPT and select Verify domain. If it fails, recheck the record character by character and wait before retrying. DNS changes can take a few hours to appear.

---

## Step 5: After Approval

- **Complete the profile** with the copy from Step 2. OpenAI reviews every edit before it appears, and ChatGPT may repeat outdated details from other sources for a while after.
- **Product feed (optional):** prices and availability, including from Shopify. A feed does not guarantee recommendations.
- **Business Agent (optional):** only for eligible US ecommerce and online-service businesses with approved Persona. One agent per profile, free at launch. Before building it, write the 10 questions customers ask most and the answers. The agent has to say it is an AI representing the business. Preview it with a real question, fix it, then Publish.
- **Baseline:** save ChatGPT's current answers to the business's real customer questions now, and ask the same questions again every month to compare.

---

## Step 6: Monthly Insights

Read Insights (Brand and Agent tabs, 7-day or 28-day views) and put them in the client report.

| Metric | What it counts |
|---|---|
| Mentions, online business | When ChatGPT references the website. The brand name alone does not count. |
| Mentions, local business | When ChatGPT shows a result for the location, even with no click. |
| Website clicks | Click-throughs to the website. |
| Discovery topics | Grouped themes in answers that mentioned or cited the business. Not individual prompts. |
| Profile views | Shown on the dashboard, with no published definition. |

- A blank metric can mean the data is below an unpublished threshold or still collecting. It does not mean zero.
- There is no export and no competitor data. Tracking specific prompts and competitors needs a separate AI visibility check.

---

## Businesses That Cannot Claim Yet

For a business stuck at Persona, or a local business with no listing, prepare the site so it is ready when access opens:

- Allow **OAI-SearchBot** in robots.txt and in any CDN or firewall. OAI-SearchBot powers search and GPTBot is for training, so you can allow one and block the other. Changes take about 24 hours to apply.
- Publish **Organization schema** that matches the legal name, logo, website and contact details.
- Keep name, address and phone identical across the website, Google Business Profile, Bing Places and directories.
- Keep the domain verification plan and the Step 2 profile copy ready.

---

## Troubleshooting

| Situation | What to do |
|---|---|
| Listing not found | Check the spelling and any former names, and search from the business's own country. Online: Create. Local: wait. |
| Similar or wrong listing | Check the address on each result before selecting. |
| Risk of a duplicate | Search before creating. Only unpublished drafts can be deleted (Overview, ••• menu, Delete draft). A published profile cannot be deleted, unpublished or hidden, even by OpenAI Support. |
| Persona rejected or expired | Follow the emailed instructions. If Try again is offered, resubmit with details that match official records. |
| Approved but something is still incomplete | The owner contacts OpenAI Support with the step, any error, and a screenshot with sensitive data removed. |
| ChatGPT says wrong things about the business | Fix the profile first, then the third-party sources. Use thumbs-down for a single wrong answer. |
| Using ChatGPT from an unsupported country | Don't. It can get the account blocked. |

---

## Not Confirmed Yet

Write the answer here once you test it:

- Whether Persona can be completed by a business with no US entity (no SSN or EIN).
- Whether adding teammates or an agency needs a paid ChatGPT Business plan. Sources disagree. Claiming itself works on any plan.
- How far a non-US local listing gets after Get started.
- One tutorial mentions a $500 advertising credit. What OpenAI documents is up to $50 a month in ad credits for eligible paid Business workspaces billed in the US, UK, Germany or France, through January 31, 2027.

---

## Output

For each business, hand back:

1. **The path** (claim, create, dispute, locked or wait) and why.
2. **The readiness checklist** with each item marked done or missing.
3. **The owner's instruction message**, ready to send.
4. **The DNS TXT note**, if the domain method is used.
5. **The profile copy**: About text, category, delivery and return policies.
6. **One tracker line:** business, path, status, next check date.

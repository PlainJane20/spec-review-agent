# Spec Review — IT_Project_Intake_Form_MVP.md

**6 blocker(s) · 12 major · 10 minor** across 5 independent review lenses.

⚠️ **This spec has blocking issues and should not move to engineering as-is.**

## Findings (highest severity first)

### 🔴 [BLOCKER] No stated problem statement for why this intake form/system itself is being built (this is a PRD for the intake process, not the requestor's problem field within the form). — *Completeness*
- **Where:** Overall spec
- **Why it matters:** Without a clear problem statement for the intake system, engineering/ops can't tell what pain point (e.g., scattered requests, lack of visibility, slow triage) this MVP is meant to fix, making it impossible to judge if the design actually solves it.
- **Suggested fix:** Add a short 'Problem Statement' section explaining the current-state pain (e.g., 'IT requests come in via email/Slack with no consistent info, causing delays and rework') that this intake form is meant to solve.

### 🔴 [BLOCKER] No non-goals section specifying what this MVP deliberately excludes. — *Completeness*
- **Where:** Overall spec
- **Why it matters:** Without explicit non-goals, stakeholders may assume the form/sheet will handle things like automated routing, SLA tracking, approval workflows, or integration with JIRA/other tools, leading to scope creep or missed expectations when those aren't delivered.
- **Suggested fix:** Add a 'Non-Goals' section explicitly stating what's out of scope for MVP, e.g., no automated JIRA integration, no SLA enforcement, no multi-level approval workflow, no reporting/dashboarding beyond the raw sheet.

### 🔴 [BLOCKER] No success metrics defined for the intake process (e.g., adoption rate, review turnaround time, reduction in ad-hoc requests). — *Completeness*
- **Where:** Overall spec
- **Why it matters:** Without measurable success criteria, there's no way to know post-launch whether this MVP intake process is actually working or should be iterated on/replaced.
- **Suggested fix:** Add a 'Success Metrics' section with measurable targets, e.g., '% of IT requests submitted via form vs other channels', 'average time from submission to IT decision', '5-business-day response SLA met X% of time'.

### 🔴 [BLOCKER] No rollout/launch plan describing how this form will be introduced to the organization beyond 'share link with stakeholders'. — *Completeness*
- **Where:** Overall spec
- **Why it matters:** Without a rollout plan (who gets notified, phased pilot vs full org launch, training/communication plan), adoption may be inconsistent and old request channels (email/Slack) may persist, undermining the MVP's purpose.
- **Suggested fix:** Add a 'Rollout Plan' section covering communication plan, pilot group vs full rollout, deprecation of old request channels, and timeline.

### 🔴 [BLOCKER] No rollback or mitigation plan if the form/process fails or causes issues post-launch (e.g., low adoption, missing fields causing bad decisions, sheet becoming unmanageable). — *Completeness*
- **Where:** Overall spec
- **Why it matters:** Without a fallback plan, there's no defined action if the intake process breaks down (e.g., stakeholders bypass it, IT Leadership can't keep up with weekly review), risking requests falling through the cracks with no recovery path.
- **Suggested fix:** Add a 'Rollback/Mitigation' section describing fallback options, e.g., reverting to email intake temporarily, escalation path if weekly review backlog grows, or a process for handling urgent P0 requests that can't wait for weekly review.

### 🔴 [BLOCKER] No named owner or role is specified for who on 'IT Leadership' actually reviews, decides Approve/Reject/Defer, or fills in the Recommendation/Effort/Quarter columns. — *Ownership & Decision Rights*
- **Where:** IT Leadership reviews all submissions weekly / 'IT Recommendation' column
- **Why it matters:** Without a named DRI, submissions can sit in limbo with everyone assuming someone else is reviewing them, and the 5-business-day SLA has no one accountable to meet it.
- **Suggested fix:** Add a required 'Reviewer/DRI' field or explicitly name the person/role (e.g., 'IT PMO Lead - Jane Doe') accountable for triaging submissions weekly and making the Approve/Reject/Defer call.

### 🟠 [MAJOR] Single short-answer field combines two distinct data points (name and email) with no specified format or delimiter enforcement. — *Ambiguity & Acceptance Criteria*
- **Where:** Question 3: Your Name & Email
- **Why it matters:** Free-text entry means users may format inconsistently (e.g., 'jane.smith@company.com - Jane Smith' or missing comma), making the sheet column 'Requestor' unreliable for automated parsing or lookups.
- **Suggested fix:** Split into two separate required fields: 'Your Name' and 'Your Email', or specify a strict format and add validation.

### 🟠 [MAJOR] Department is a free-text short answer with no defined list of valid values. — *Ambiguity & Acceptance Criteria*
- **Where:** Question 4: Department
- **Why it matters:** Inconsistent spellings/abbreviations (e.g., 'HR' vs 'Human Resources' vs 'People Ops') will fragment reporting and make filtering/aggregating by department unreliable.
- **Suggested fix:** Convert to a dropdown/multiple-choice list of predefined departments, with an 'Other' option if needed.

### 🟠 [MAJOR] No guidance on what value to enter when there is no hard deadline (e.g., for P3 'nice to have' requests), yet the field is marked required. — *Ambiguity & Acceptance Criteria*
- **Where:** Question 8: Target Completion Date
- **Why it matters:** Users will enter arbitrary placeholder dates (today's date, far-future dates) to satisfy the required field, polluting the data and making 'Target Date' meaningless for prioritization.
- **Suggested fix:** Either make the field optional, or add an explicit 'No specific deadline' checkbox/option alongside the date picker.

### 🟠 [MAJOR] The option text implies a fill-in amount but the question type is Multiple choice, which in Google Forms doesn't support an inline text field per option. — *Ambiguity & Acceptance Criteria*
- **Where:** Question 10: Budget Status, option 'Yes, budget approved ($_____ - fill in amount)'
- **Why it matters:** As specified this can't actually be built in Google Forms without a workaround, so the budget amount will never be captured, breaking the intended data collection for 'IT Recommendation' decisions.
- **Suggested fix:** Add a separate conditional short-answer field ('If approved, enter amount') shown only when this option is selected, or clarify that the amount is collected elsewhere.

### 🟠 [MAJOR] The form collects PII (name, email, department) and business-sensitive data (budget figures, project plans) into a Google Sheet with no stated access control, sharing settings, or permissions model. — *Security & Privacy*
- **Where:** Google Sheet Assessment Columns / overall data storage
- **Why it matters:** Without defined access controls, the sheet could be shared too broadly (e.g., 'anyone with link' or org-wide) exposing personal contact info and confidential budget/business data to unauthorized employees or external collaborators.
- **Suggested fix:** Define who owns/administers the sheet, restrict access to a named IT Leadership/PMO group, and document the sharing permission level (view vs edit) explicitly in the spec.

### 🟠 [MAJOR] There is no data retention or deletion schedule for form responses/sheet data (name, email, department, project details, budget amounts). — *Security & Privacy*
- **Where:** No retention policy stated anywhere in spec
- **Why it matters:** Indefinite retention of PII and financial data increases breach exposure and may violate data minimization requirements under privacy regulations (e.g., GDPR/CCPA) if employees or contractors' personal data is kept without justification.
- **Suggested fix:** Add a retention policy (e.g., delete/archive submissions after project closure + X months) and specify who is responsible for enforcing it.

### 🟠 [MAJOR] No process is defined for handling a user's request to have their submitted personal data (name, email) corrected or deleted. — *Security & Privacy*
- **Where:** Confirmation Message / overall spec
- **Why it matters:** If a requestor asks to be forgotten or to correct their info, there's no documented workflow, risking non-compliance with privacy regulations and inconsistent ad-hoc handling.
- **Suggested fix:** Add a stated process/contact for data subject access/deletion requests, e.g., 'Contact IT PMO to request removal of your submission; requests fulfilled within N days.'

### 🟠 [MAJOR] No owner identified for who approves budget or chases pending budget approvals. — *Ownership & Decision Rights*
- **Where:** Budget Status - 'Budget pending approval' / 'No budget yet'
- **Why it matters:** Projects can stall indefinitely with no one responsible for following up on budget approval, causing missed target dates with no accountability.
- **Suggested fix:** Add a field or process note naming who (e.g., requestor's manager, Finance, IT PMO) owns driving budget approval to resolution and by when.

### 🟠 [MAJOR] No named individual is accountable for entering the Decision Date, IT Notes, or making sure these manual columns get filled in after review. — *Ownership & Decision Rights*
- **Where:** Decision Date / IT Notes columns
- **Why it matters:** Manual post-review fields frequently go stale or blank when no specific person is tasked with updating them, undermining reporting and traceability.
- **Suggested fix:** Assign a specific role (e.g., 'IT PMO Coordinator') as owner of updating columns 12-18 within 1 business day of the weekly review meeting.

### 🟠 [MAJOR] 'TPM' is referenced as the one who creates the Epic, but no specific TPM or assignment mechanism is defined for how a TPM gets assigned to a given approved project. — *Ownership & Decision Rights*
- **Where:** TPM creates Epic in JIRA
- **Why it matters:** If assignment of a TPM isn't triggered by a defined owner/process, approved projects can be approved but never get an Epic created, stalling execution silently.
- **Suggested fix:** Specify who assigns a TPM to each approved project (e.g., IT Leadership during the weekly review) and add a 'TPM Assigned' column to the sheet to track it.

### 🟠 [MAJOR] The requestor sets Priority and Target Date, but there's no stated authority for who can override/approve these versus who arbitrates conflicting priorities (e.g., multiple P0 requests). — *Ownership & Decision Rights*
- **Where:** Priority Level and Target Completion Date fields
- **Why it matters:** Self-declared priority without a named approver leads to priority inflation (everyone marks P0) and no clear tie-breaker, causing resourcing conflicts.
- **Suggested fix:** State explicitly that IT Leadership (name the role/person) has final authority to adjust Priority and Target Quarter during weekly review, and note this in the confirmation message.

### 🟠 [MAJOR] The spec has no field, process, or named owner for handling scope changes once a project moves to JIRA/Sprints. — *Ownership & Decision Rights*
- **Where:** Mid-build scope changes (not addressed anywhere in spec)
- **Why it matters:** Without a designated decision-maker for scope changes mid-build, teams may unilaterally expand/cut scope or stall waiting for unclear approval, risking scope creep or missed deadlines.
- **Suggested fix:** Add a section defining who (e.g., TPM + IT Leadership sign-off) approves mid-build scope changes, and require any change to be logged against the JIRA Epic with approver name and date.

### 🟡 [MINOR] Terms like 'business-stopping', 'needed this quarter', and 'nice to have' are not tied to objective criteria for the requester to self-assess. — *Ambiguity & Acceptance Criteria*
- **Where:** Priority Level options (P0-P3)
- **Why it matters:** Different requesters will self-select higher priority than warranted (everyone thinks their P3 is a P1), skewing the priority queue IT Leadership relies on.
- **Suggested fix:** Add brief objective criteria or examples for each priority level (e.g., 'P0: production outage affecting all users').

### 🟡 [MINOR] Not specified whether this SLA counts from submission date or from the next weekly review cycle mentioned in step 1. — *Ambiguity & Acceptance Criteria*
- **Where:** Confirmation Message: 'You'll hear back within 5 business days'
- **Why it matters:** If a request is submitted right after the weekly review, 5 business days may be missed, causing stakeholder complaints about unmet expectations.
- **Suggested fix:** Clarify: 'within 5 business days of the next weekly review' or adjust the SLA to explicitly account for the review cadence.

### 🟡 [MINOR] Small/Medium/Large are not defined in terms of time, story points, or sprint count. — *Ambiguity & Acceptance Criteria*
- **Where:** Google Sheet Assessment Columns: 'Estimated Effort' (Small / Medium / Large)
- **Why it matters:** Different reviewers (or the same reviewer over time) will apply inconsistent thresholds, making effort estimates non-comparable across projects in the backlog.
- **Suggested fix:** Define each size with a rough time/sprint range, e.g., 'Small: 1 sprint, Medium: 2-4 sprints, Large: 5+ sprints'.

### 🟡 [MINOR] The question asks for value with example metrics but doesn't require the requestor to quantify impact, allowing vague qualitative answers. — *Ambiguity & Acceptance Criteria*
- **Where:** Question 6: Business Impact
- **Why it matters:** IT Leadership needs comparable impact data to prioritize across requests; unquantified answers like 'improves efficiency' can't be ranked against dollar/hour figures from other submissions.
- **Suggested fix:** Require at least one quantifiable metric or add a structured sub-field (e.g., dropdown for impact type + numeric value).

### 🟡 [MINOR] Email/name collected as free-text short answer with no validation, and no statement on how this contact info will be used beyond follow-up (e.g., shared with JIRA, other teams). — *Security & Privacy*
- **Where:** 3. Your Name & Email
- **Why it matters:** Lack of validation can lead to malformed/incorrect data; lack of use-limitation statement means requestor doesn't know their contact info may be copied into JIRA or shared with other teams (e.g., Security team per example flow), which is a downstream data-sharing gap.
- **Suggested fix:** Use Google Forms built-in email validation field, and add a short note in the description disclosing that submission details (including name/email) will be visible to IT Leadership and may be copied into JIRA epics visible to broader engineering teams.

### 🟡 [MINOR] The spec states TPM 'copies details from intake form' into JIRA without addressing whether personal identifying info (requestor name/email) or sensitive budget figures should be excluded before pasting into a potentially more widely-visible JIRA project. — *Security & Privacy*
- **Where:** Example Submission Flow - JIRA Epic creation
- **Why it matters:** JIRA epics are often visible to larger engineering teams or even external contractors; copying requestor PII or exact budget numbers there could over-expose personal or financial data beyond the original intended audience.
- **Suggested fix:** Instruct TPMs to exclude or redact personal contact details and sensitive budget specifics when copying content into JIRA, or link back to the sheet instead of duplicating raw data.

### 🟡 [MINOR] No authentication/authorization is specified for who can submit the form (e.g., is it restricted to org domain via Google Workspace, or open to anyone with the link?). — *Security & Privacy*
- **Where:** Overall form access
- **Why it matters:** An open/shareable link with no domain restriction could allow anonymous or external submissions, enabling spam, spoofed requests, or unauthorized disclosure of internal project ideas/budget info to outsiders.
- **Suggested fix:** Restrict form access to authenticated users within the company Google Workspace domain and enable 'Limit to 1 response' / collect email verified by domain login.

### 🟡 [MINOR] Contact is a generic placeholder email/team alias rather than a named accountable individual. — *Ownership & Decision Rights*
- **Where:** Confirmation Message - 'Contact IT PMO: [your-email@company.com]'
- **Why it matters:** Requestors following up on stalled requests have no specific person to escalate to, increasing frustration and reducing accountability.
- **Suggested fix:** Replace the placeholder with a named IT PMO owner (or at minimum a role title with the actual current person's name) responsible for responding to inquiries.

### 🟡 [MINOR] No owner is named for who produces this effort estimate (engineering lead? TPM? IT Leadership itself?). — *Ownership & Decision Rights*
- **Where:** Estimated Effort (Small/Medium/Large)
- **Why it matters:** Estimates without a clear estimator/owner can be inconsistent or skipped, undermining the reliability of the Target Quarter assignment that depends on it.
- **Suggested fix:** Name the role responsible for producing the effort estimate (e.g., 'Engineering Lead reviews and sizes effort before weekly IT Leadership meeting').

### 🟡 [MINOR] No named owner for the handoff step itself between sheet decision and JIRA Epic creation—it's unclear if this is automatic or requires a specific person to act. — *Ownership & Decision Rights*
- **Where:** 'Approved projects move to JIRA for planning'
- **Why it matters:** An undefined handoff step is a common place for approved work to fall through the cracks between the intake sheet and actual JIRA planning.
- **Suggested fix:** Explicitly state who is responsible for initiating JIRA Epic creation once a project is marked Approved (e.g., 'IT PMO notifies assigned TPM within 1 business day of approval').

---
## By lens
- **Ambiguity & Acceptance Criteria**: 8 finding(s)
- **Completeness**: 5 finding(s)
- **Technical Feasibility & Edge Cases**: clean
- **Security & Privacy**: 6 finding(s)
- **Ownership & Decision Rights**: 9 finding(s)
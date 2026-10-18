# DrapeLoop — MVP Scope

Version: 0.1 | Updated: 2026-10-18 | Status: planning; not implemented

## 1. First-release goal

Provide a static virtual try-on experience in a mobile browser for people who frequently shop for tops online, initially in China. Users create a personal profile once, then upload different garment images without taking another personal photo.

The core value is comparing colors, styles, and overall appearance. More clothing categories and realistic 360° viewing are long-term goals. The first release does not promise accurate body measurements, size recommendations, or realistic tightness simulation.

## 2. Hypotheses to validate

- Users accept the effort of providing a full-body photo, height, and weight once.
- Reusing a photo across different tops preserves identity, body proportions, and major garment details.
- Saved profiles reduce repeat-use friction compared with uploading a personal photo again.
- Previews help users compare styles and motivate voluntary reuse during a later shopping occasion.
- Cost per usable result and waiting time allow sustained small-scale trials.

These are hypotheses, not implemented capabilities or proven market findings.

## 3. Core journeys

First visit: open the Chinese interface → sign in through a minimal account flow → review photo and data-use guidance → upload full-body photo → enter height and weight → preview and confirm profile → upload a top image → generate → compare original and result → download or give feedback.

Return visit: sign in → use saved profile → upload another top → generate and compare results. The profile persists across visits without another photo.

Problems: explain unsuitable inputs and allow replacement; offer recovery after generation failure; accept reports of changed identity or body proportions and allow photo updates. Distorted results are not counted as successful try-ons.

The minimum personal profile may simply be the confirmed original photo. A generated 3D person is not required. Height/weight-assisted shape estimation needs separate validation; an unvalidated generated avatar must not replace the original photo.

## 4. Required features

| Feature | First-release boundary | Related stories |
|---|---|---|
| Chinese mobile web interface | Upload, generate, view, and download in a mobile browser | US01–US03 |
| Minimal accounts and private access | Sign in, sign out, recover saved profiles on return; isolate users' data; no social profile pages | US01, US04 |
| Photo guidance and uploads | JPG/PNG, preview, replacement, format/size checks, examples and self-checks; no claims of detecting issues the system cannot identify | US01, US06 |
| Persistent personal profile | Confirmed original photo, height in cm, weight in kg, updates; circumferences are never mandatory | US01, US07 |
| Static top try-on | One top per task, generated from the selected original personal photo; supported categories determined by evaluation | US02 |
| Task states and failure handling | Waiting, success, failure, duplicate-submission prevention, retries, and usage limits | US02 |
| View, compare, download | Label original/result, retain a basic results list, open separate results to compare; an advanced comparison widget is not required | US03 |
| Distortion feedback | Report identity changes, proportion drift, or garment errors; no automatic-repair promise | US02, US07 |
| Updates and deletion | Update profile; delete individual records or profile and associated data; apply US04/US07 version and running-task rules | US04, US07 |
| Controlled trial operations | Private image access, server-side credentials, task limits, spending stop switch, clear retention rules | US04 |

Explain purpose, retention, and external processing before upload. Profiles persist until user deletion or a disclosed account-cleanup deadline; results have a separate retention period. Set and display concrete periods before trials. User photos, body data, and credentials must not enter GitHub.

## 5. Conditional enhancements

| Capability | Required validation | Fallback if not validated |
|---|---|---|
| Height/weight-assisted shape estimation | Better final body-proportion preservation than photo-only input, rather than a more flattering avatar | Explain whether the inputs are being used; use the original photo and make no shape-correction claim |
| Side-view correction | Better body-depth/shape preservation that justifies the extra effort | Do not show an upload field with no working benefit |
| Known-circumference correction | A reliable method and measurable benefit | Do not show fields with no working benefit; keep optional when introduced |

These conditions apply to enhanced US01/US07 flows. The stories describe target requirements; this document limits first delivery. Explain the purpose of collected data and do not collect extra information that validation does not need.

## 6. Deferred features

- 360° rotation, 3D avatars, turning-video capture, and live camera try-on (US05).
- Trousers, skirts/dresses, footwear/accessories, layering, and claims of covering most clothing.
- Exact circumference estimation, size recommendations, tightness, and fabric physics.
- Product-link scraping, shopping plugins, checkout, payments, and memberships.
- Full wardrobe management, social communities, styling recommendations, and custom model training.
- Native mobile apps and WeChat mini programs; validate mobile web first.

## 7. Evaluation and delivery gates

The numbers below are initial internal decision thresholds. They may be revised with recorded reasons before the first evaluation, but not changed after seeing results just to pass. They are not statistical proof.

### Technical validation

- Prepare at least 12 consented person-photo/top combinations across body shapes and plain/patterned tops; retain failure cases.
- Record success, latency, cost, identity preservation, proportions, garment details, and naturalness. Obvious identity changes, slimming, anatomical errors, or major garment-detail errors make a result unusable.
- Initial gate: at least 9 of 12 combinations produce usable results. Record reasons for each judgment, not just successful examples. If the gate fails, continue experiments before general user trials.
- Evaluate shape estimation and try-on separately. Use consented physical measurements or scans if evaluating circumferences; perceived likeness does not prove dimensional accuracy.
- Record actual waiting time and total spending divided by usable results. Set acceptable wait time, per-user usage limits, and a total budget before opening trials, and enforce those limits.

### Functional delivery

- Use at least two independent test accounts to verify that profiles, images, and tasks cannot be accessed across accounts.
- After signing out and back in, a user can try another top with the saved profile.
- Mobile users can upload, generate, compare with the original, download, update, and delete.
- Unsupported formats, oversized files, timeouts, provider errors, and repeated clicks have defined recovery behavior.
- Deletion actually removes corresponding local files/data, including correct handling of running tasks. Local deletion is not represented as proof of external-provider deletion.
- Delivered stories meet applicable acceptance criteria. Conditional enhancements and US05 remain explicitly deferred, not marked complete.

### User trials

- Invite approximately 5–10 target users. Record completion, friction, likeness, and usefulness for shopping comparisons.
- Initial observation targets: at least 70% complete with little help, and at least half can explain a concrete comparison benefit. Report raw counts.
- Observe voluntary reuse only among users with another genuine shopping occasion. Initially seek at least three returning users; extend observation if opportunities are insufficient rather than declaring failure.
- Address distortion, lack of decision value, or unacceptable cost before expanding categories.

## 8. Milestones and dependencies

| Stage | Deliverables | Gate to proceed |
|---|---|---|
| M1: Technical validation | Fixed-sample evaluation, supported top categories, model choice, height/weight findings, cost and latency | Pass technical gates, or narrow scope and reevaluate |
| M2: Single try-on flow | Mobile upload, generation, states, comparison, download, feedback | Normal and failure flows work |
| M3: Reusable profiles | Accounts, private persistence, repeat use, updates, results, deletion, limits | Isolation, reuse, and cleanup checks pass |
| M4: Small user trial | Controlled trial, anonymous feedback, reuse observation, next-step decision | Decide whether to improve, expand, or conclude based on findings |

Proceed by dependency. Schedule dates and implementation tasks after technical feasibility and available time are understood. MVP completion means a controlled, usable product plus initial validation, not documents alone or one successful generation.

## 9. Related documents

- [User scenarios](user-scenarios.md): first setup, repeat use, distortion handling.
- [User stories and acceptance criteria](user-stories.md): intended features and acceptance requirements.

This document defines first delivery. Update scope and relevant acceptance criteria before planning future extensions.

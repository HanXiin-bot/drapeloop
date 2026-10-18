# DrapeLoop — User Stories and Acceptance Criteria

Updated: 2026-10-18

## Product goal

Create a personal profile once and reuse it to try different garments without taking another photo every time. The first release evaluates static try-on for tops; other categories depend on testing. A 360° experience is future research. A single photo cannot guarantee accurate reconstruction of unseen body regions or actual garment fit.

## US01 — Create a reusable personal profile

As an online clothing shopper, I want to create a reusable profile from a full-body photo, height, and weight, so that I can try outfits without knowing my body circumferences or taking another photo each time.

Acceptance criteria:
- Users can upload, preview, and confirm a full-body photo.
- The confirmed photo is saved and available on a later visit.
- Users can replace or delete their photo.
- The intended flow is: upload photo → enter height in centimeters and weight in kilograms → prepare an initial profile → review and confirm → save for reuse.
- Height and weight inputs validate units and numeric values. Their purpose is explained; estimated dimensions are not presented as exact measurements.
- Chest, waist, and hip measurements are optional. Skipping them never blocks profile creation or try-on.
- Shape estimation using the photo, height, and weight requires technical validation. If it fails validation, the system explicitly uses the original photo and does not display unvalidated precise measurements or claim shape correction.
- Photos, height, weight, and optional measurements are accessible only to their owner.

## US02 — Try different garments using the saved profile

As an online shopper, I want to generate try-on previews using my saved profile, so that I can compare different styles without uploading my personal photo again.

Acceptance criteria:
- Users with a profile do not need to upload their personal photo again.
- Users can upload, preview, and replace a garment image.
- Each task uses the selected original personal photo, rather than the previous generated result, to avoid accumulating appearance drift.
- The page explains supported garment categories and image requirements.
- Generation shows a waiting state, prevents duplicate submissions, and offers recovery after failure.
- Results should preserve facial identity and body proportions without intentional slimming, leg lengthening, or body beautification. Obvious deviations count as quality failures.

## US03 — Compare and download results

As an online shopper, I want to compare the original photo with a try-on result and download the result, so that I can compare styles and keep a reference.

Acceptance criteria:
- Original and generated images are clearly labeled and viewable on mobile.
- Users can download the displayed result.
- Results are described as visual references, without guarantees about size or fit.

## US04 — Delete personal try-on data

As a privacy-conscious user, I want to delete my profile and try-on data, so that I can control my personal images and information.

Acceptance criteria:
- Users can delete one try-on record or their profile and all associated try-on records.
- Deleting one try-on record does not delete the reusable profile.
- Deleting a profile and its records removes corresponding stored images and records, with a completion message.
- Profile deletion also clears associated height, weight, optional circumferences, and estimated shape data.
- Third-party processing and retention rules are explained before upload. Deletion within this system is not described as proof of deletion by an external provider.

## US05 — Rotate the try-on view (future exploration)

As an online shopper, I want to rotate a try-on representation, so that I can inspect an outfit from different angles.

Acceptance criteria:
- Users can drag to inspect front, side, and back views.
- Identity, body proportions, and garment appearance remain consistent across views.
- The interface explains that unphotographed views are inferred by AI.
- Before release, user evaluation assesses likeness, garment details, and visible deformation during rotation. Pass thresholds are set after technical experiments.

## US06 — Follow full-body photo guidance

As a first-time user, I want clear, practical photo guidance, so that I can provide a suitable image with less distortion and fewer retakes.

Acceptance criteria:
- Guidance and examples of suitable and unsuitable photos appear before upload.
- Guidance recommends fitted everyday tops and trousers, avoiding thick outerwear and loose clothing that hides the silhouette. Nudity or underwear-only photos are not required.
- Guidance asks for the full head-to-toe body, a natural upright front-facing stance, arms slightly away from the torso, even lighting, and a simple background.
- Guidance recommends a level camera and avoiding wide-angle distortion, downward camera angles, beauty filters, and slimming filters.
- Detectable framing, severe occlusion, or blur issues produce specific feedback. Problems that cannot be reliably detected use a self-check list rather than a claim of accurate body recognition.
- The interface explains that a clothed photo does not reveal exact hidden body dimensions and that a preview is not a measurement or size recommendation.

## US07 — Review and update the personal profile

As a try-on user, I want to check my likeness and update an unsuitable photo or changed body information, so that future previews remain useful.

Acceptance criteria:
- Before profile confirmation and after the first try-on, users can compare facial appearance, shoulders, waist, leg length, and overall proportions with the original and report distortion. Confirmation is not measurement validation.
- Users can update their photo, height, weight, and optional measurements without re-entering them for every try-on.
- Users who find the profile inaccurate may optionally add a side-view photo or known circumferences when those correction features have been validated. Neither is required for basic try-on. Side-view photos follow the same access and deletion rules.
- Replacing a photo does not automatically delete or regenerate existing results; older results show their generation time.
- Explicit deletion of an old photo removes its stored image. Existing results can be deleted separately or together under US04.
- New tasks use the updated photo; running tasks remain bound to the submitted photo version. Deleting that version cancels unfinished associated tasks and triggers cleanup.

## Technical exploration and validation

- Test whether one-time setup reduces friction and encourages repeat use through interviews and real trials.
- Compare photo-only input, photo plus known height/weight, and additional side-view input for shape preservation, effort, and cost. Where measurement accuracy is evaluated, use consented measurements or scans as references; user confirmation is not a substitute.
- Evaluate shape estimation separately from garment generation, then evaluate the final output. A reasonable initial shape does not guarantee preserved proportions after try-on.
- Initially assess visible shoulder, torso, and limb proportions. Hidden regions and body depth remain uncertain; equal height and weight do not uniquely determine body shape or circumferences.
- Compare a single photo with a one-time turning video before selecting an input method for future 360° views.
- Unseen appearance and body shape must be inferred; photorealism does not establish faithful reconstruction.
- Include fitted and loose clothing, different body shapes, poses, and camera angles. Record facial, shoulder, waist, leg-length, and overall proportion changes rather than judging attractiveness alone.
- The MVP evaluates visual styling and likeness, not exact circumferences, sizing, or tightness. Future sizing research needs optional known body measurements plus garment dimensions, cut, and material data, with measured error.
- Research references: [NVIDIA DLA](https://research.nvidia.com/labs/dair/dream-lift-animate/), [SiTH](https://sith-diffusion.github.io/), and [SHAPY](https://shapy.is.tue.mpg.de/). SHAPY is a single-image shape-estimation reference, not validation of this project's height/weight-assisted approach.

## Scope and planning

Reusable personal profiles belong in the first release, replacing the earlier idea of retaining no long-term profile. Persistent storage needs stable user identification, private storage, access control, and revised workload and cleanup rules. The earlier private learning plan is not part of this public requirements document.

See [MVP scope](mvp-scope.md) for first-release boundaries and conditional enhancements, and [user scenarios](user-scenarios.md) for intended journeys.

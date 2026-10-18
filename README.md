# DrapeLoop

**Create your profile once. Try different outfits.**

DrapeLoop is an early-stage AI virtual try-on project exploring how a reusable personal profile can make online clothing shopping easier. The initial audience is online shoppers in China; the documentation is in English so people worldwide can review the idea and contribute feedback.

## Project status

**Planning and technical validation preparation. No working application, demo, or production service is available yet.** The features below describe intended behavior, not implemented capabilities.

## The idea

1. Upload a full-body photo and enter your height and weight once.
2. Review and save your personal profile.
3. Upload a clothing image to preview a different outfit.
4. Reuse the profile next time, without taking another photo.

The MVP focuses on static previews of tops in a mobile browser. Preserving the person's identity, body proportions, and garment details matters more than producing a flattering image. Chest, waist, and hip measurements are not required.

Height/weight-assisted shape estimation remains an experiment. If it does not pass evaluation, the MVP uses the confirmed original photo and explains that limitation. Accurate sizing, fit prediction, and realistic 360° views are future research goals.

## Documentation

- [User scenarios](docs/user-scenarios.md)
- [User stories and acceptance criteria](docs/user-stories.md)
- [MVP scope, evaluation gates, and milestones](docs/mvp-scope.md)

## Feedback welcome

Please open a GitHub issue with questions, suggestions, or relevant research. Useful topics include:

- Whether the one-time setup is convenient enough to use again.
- Ways to preserve identity, body proportions, and garment details.
- Practical model choices, evaluation methods, latency, and cost.
- Photo privacy and a clear, trustworthy user experience.

Please do not upload personal body photos, measurements, credentials, or other private data to public issues.

## Name and inspiration

DrapeLoop combines the drape of clothing with the idea of repeatedly trying outfits using one saved profile. It is a working project name, not a claim of trademark or domain availability.

The concept was inspired in part by Anywear. DrapeLoop is an independent project and is not affiliated with or endorsed by Anywear or Decart.

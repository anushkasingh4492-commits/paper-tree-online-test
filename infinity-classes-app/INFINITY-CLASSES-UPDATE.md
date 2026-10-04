# Infinity Classes app update

Applied in this build:
- Removed the native Explore tab/navigation so the starter Explore screen and black native tab bar are gone.
- Root layout now renders the website directly.
- WebView is forced to occupy the full available viewport and disables automatic content-inset adjustment to reduce mobile cropping/side gaps.
- Removed the starter Explore route and tab components.

Still requires the actual Infinity Classes website source to implement:
- Replacing the website's Mission section with Test / "Target your weak areas".
- Moving/combining Badges, Level and AI Generated Tests into that dashboard area.
- Fixing the website dashboard's responsive layout where content is cropped.
- Applying the user's custom Infinity Classes logo.

The app currently loads https://web.infinityclasses.net, so those website UI changes cannot be made safely from this wrapper project alone.

---
title: "Privacy"
date: 2026-09-01T23:12:00+02:00
draft: false
---

GoToGuy Blog uses Google Analytics only after you explicitly allow analytics in the consent prompt.

When enabled, analytics helps measure page views, engagement, referral sources, outbound clicks, and downloads so the blog can be improved. Google Analytics is not loaded when you reject analytics or before you make a choice.

Your choice is stored in your browser's local storage under `gotoguy-analytics-consent`. Use the button below to remove the saved choice and show the consent prompt again.

<button type="button" id="reset-analytics-consent">Change analytics consent</button>

<script>
document.getElementById("reset-analytics-consent").addEventListener("click", function () {
    localStorage.removeItem("gotoguy-analytics-consent");
    window.location.reload();
});
</script>

The blog does not send its Azure deployment token or other repository secrets to analytics services. The Google Analytics Measurement ID is a public site identifier.

For details about how Google processes analytics data, see [Google's privacy information](https://policies.google.com/privacy).

---
title: "Privacy"
date: 2026-09-01T23:12:00+02:00
draft: false
---

GoToGuy Blog uses two analytics tools, with different privacy models:

- **Umami** (privacy-friendly, always on) &mdash; measures page views, referrers, and countries without cookies and without collecting any personally identifiable information. Because it does not track individuals across sites, it runs without asking for consent.
- **Google Analytics** (optional, consent-based) &mdash; only loads after you explicitly allow analytics in the consent prompt. It provides deeper engagement and referral reporting for readers who choose to opt in.

Even though Umami does not require a consent prompt, here is exactly what it does for full transparency:

- It does not use cookies, browser local storage, or any device fingerprinting to identify you.
- It does not collect your IP address, name, email, or any other personally identifiable information.
- Each pageview is counted anonymously; there is no way to link visits back to an individual person or device over time.
- Data collected is limited to: the page URL, referrer, browser, operating system, device type, screen size, and country (derived momentarily from IP, which is then discarded, not stored).
- Data is hosted by Umami Cloud ([umami.is](https://umami.is)), a third-party service, under their own [privacy policy](https://umami.is/privacy).

When enabled, analytics helps measure page views, engagement, referral sources, outbound clicks, and downloads so the blog can be improved. Google Analytics is not loaded when you reject analytics or before you make a choice; Umami is unaffected by this choice since it does not require consent.

Your Google Analytics choice is stored in your browser's local storage under `gotoguy-analytics-consent`. Use the button below to remove the saved choice and show the consent prompt again.

<button type="button" id="reset-analytics-consent">Change analytics consent</button>

<script>
document.getElementById("reset-analytics-consent").addEventListener("click", function () {
    localStorage.removeItem("gotoguy-analytics-consent");
    window.location.reload();
});
</script>

The blog does not send its Azure deployment token or other repository secrets to analytics services. The Google Analytics Measurement ID and Umami Website ID are public site identifiers, not secrets.

For details about how each service processes data, see [Google's privacy information](https://policies.google.com/privacy) and [Umami's privacy policy](https://umami.is/privacy).

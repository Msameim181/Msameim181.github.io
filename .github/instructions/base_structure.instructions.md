---
applyTo: '**'
---

### Website Requirements:

#### Structure:

* **Homepage ("Me")**: A personal introduction, photo (optional), and a short, well-written bio.
* **Resume Page**: Styled like [https://msameim181.github.io/resume.html](https://msameim181.github.io/resume.html) — a clean, two-column layout with downloadable PDF option and structured headings (e.g., Education, Experience, Skills).
* **Projects Page**: List selected projects with concise descriptions, tech used, and optional external links (e.g., GitHub, live site).
* **Blog Section**: Like [https://hesamrad.com](https://hesamrad.com) — each post is a separate `.html` file with a list view linking to individual posts.
* **Footer**: Must contain links to email, GitHub, LinkedIn, and optionally Twitter, Mastodon, or other networks.

#### Technical:

* Written in **pure HTML5 and CSS3** with **no external dependencies or build tools**.
* Mobile-first responsive design using **flexbox or grid** where necessary.
* Every page should include:

  * `<meta>` tags for SEO (description, keywords, canonical URL)
  * Clean and semantic HTML (e.g., `<header>`, `<main>`, `<footer>`, `<article>`)
  * **Open Graph and Twitter meta tags** for social sharing
  * Favicon and manifest file setup
* All CSS in a single `style.css`, and JavaScript (if any) in a single `script.js` (e.g., for minor enhancements or blog navigation).
* Organized directory structure:

  ```
  /index.html
  /resume.html
  /projects.html
  /blog/
    /post-title.html
  /assets/
    /css/style.css
    /js/script.js
    /images/
  ```

#### Style Guidelines:

* Typography: Use system fonts (e.g., `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif`)
* Color palette: Monochrome or very subtle muted tones
* Layout: White space-focused, no borders or shadows unless absolutely necessary
* Interactions: No animations unless they're purposeful (e.g., smooth scroll)
* Accessibility and readability are top priorities.

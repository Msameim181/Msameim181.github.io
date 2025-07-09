# Mohammad Mahdi Samei - Personal Website

A clean, minimalist personal website built with pure HTML, CSS, and minimal JavaScript. The design follows a minimalist philosophy, focusing on content and intentional design where every element serves a purpose.

## Features

- Fully responsive, mobile-first design
- SEO-optimized with proper meta tags
- Clean, semantic HTML structure
- Pure CSS3 styling without frameworks
- Minimal JavaScript for essential functionality
- Optimized for fast loading
- Timeline-based resume layout
- Skill visualization with experience bars
- Project showcase with filterable categories
- Blog section with technical articles

## Structure

- **Homepage**: Personal introduction and featured projects
- **Resume**: Comprehensive professional experience, education, skills, and certificates 
- **Projects**: Portfolio of work with descriptions, technologies, and links
- **Blog**: Technical articles focused on machine learning and AI
- **Contact**: Contact information and form

## Pages

- `index.html` - Homepage with personal introduction
- `resume.html` - Professional experience, education, skills, and certificates
- `projects.html` - Portfolio of technical projects
- `blog/index.html` - Blog listing page
- `blog/deep-learning-in-medical.html` - Deep Learning for Medical Image Analysis article
- `blog/ethics-in-ai.html` - Ethics in AI article
- `blog/backlog/sample.html` - Machine Learning in Production article
- `contact.html` - Contact information and form

## Development

This website is built with:

- HTML5
- CSS3 (no frameworks or preprocessors)
- Vanilla JavaScript (minimal usage)

No build tools or dependencies are required. Simply edit the HTML and CSS files directly.

## Local Development

1. Clone this repository
2. Start a local development server:
   - Using Python: `python -m http.server 8000`
   - Using Node.js: `npx serve`
3. Open your browser at `http://localhost:8000`

## Deployment

This site is deployed to multiple platforms for redundancy:

### GitHub Pages Deployment
The site is automatically deployed to GitHub Pages when changes are pushed to the main branch using GitHub Actions.

The deployed site is available at: `https://msameim181.github.io`

### Vercel Deployment
The site is also deployed to Vercel for enhanced performance and reliability.

To deploy to Vercel:
1. Sign up for a Vercel account at https://vercel.com
2. Install the Vercel CLI: `npm install -g vercel`
3. In the project directory, run: `vercel`
4. For subsequent deployments: `vercel --prod`

The Vercel deployment is available at: `https://msameim181.vercel.app` (customizable)

## License

Copyright © 2020 Mohammad Mahdi Samei. All rights reserved.

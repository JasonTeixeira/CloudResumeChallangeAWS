# Cloud Resume Challenge - AWS

**Live site:** [jasonteixeira.com](https://jasonteixeira.com)

```
┌─────────────────────────────────────────────────────┐
│  WHAT THIS IS                                       │
├─────────────────────────────────────────────────────┤
│  • Static portfolio website hosted on AWS          │
│  • S3 for storage, CloudFront for CDN              │
│  • Route 53 DNS, ACM for SSL certificates          │
│  • Full HTTPS, www → apex redirect                  │
│  • Actual production site, not a tutorial project  │
└─────────────────────────────────────────────────────┘
```

## Why I Built This

I needed a professional online presence that didn't rely on third-party hosting. I wanted full control over the infrastructure and the ability to demonstrate cloud architecture skills. Plus, I was curious how far I could push AWS free-tier services.

I chose AWS because it's what most enterprises use, and I wanted hands-on experience with the core services (S3, CloudFront, Route 53, ACM). This isn't just a resume site—it's proof I can architect, deploy, and maintain cloud infrastructure.

## Architecture

```
┌─────────────────┐
│   Route 53 DNS  │  (jasonteixeira.com)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   CloudFront    │  (CDN + HTTPS termination)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   S3 Bucket     │  (HTML/CSS/JS/images)
└─────────────────┘
```

**Certificate:** AWS Certificate Manager (free SSL)  
**Redirect:** HTTP → HTTPS, www → apex domain

## What's Inside

The site itself is in `JasonTexeira_AWS_portfolio/`:
- `index.html` - Main portfolio page (31KB of HTML)
- `css/` - 14 stylesheets for responsive design
- `js/` - 29 JavaScript files (jQuery, animations, form handling)
- `fonts/` - Custom web fonts (27 files)
- `images/` - Portfolio images and graphics
- `php/` - Contact form backend (S3 doesn't run PHP, so this is vestigial from the template)

## What Was Hard

**DNS propagation paranoia:** I set up the Route 53 A records and then spent 2 hours refreshing the site thinking I'd misconfigured something. Turns out DNS just takes time. I learned to use `dig` and DNS checkers instead of hammering refresh.

**ACM certificate validation:** You have to validate domain ownership via DNS, which means adding CNAME records to Route 53 that ACM generates. The UX is confusing—the records don't auto-populate, and you have to manually copy them over. Took me three attempts to get the validation working.

**CloudFront cache invalidation:** Made a typo in the HTML, pushed the fix to S3, and the old version kept showing up for 24 hours. That's when I learned about CloudFront's edge caching and how to create invalidation requests (`/*` invalidates everything but costs $0.005 per request after the first 1,000/month).

**Public bucket vs OAI:** Initially made the S3 bucket fully public (bad practice). Later learned about Origin Access Identity (OAI) to restrict S3 access to only CloudFront, but by then the site was working and I didn't want to break it. I'd do this differently next time.

## What I'd Do Differently

**Use an OAI:** I'd configure CloudFront with an Origin Access Identity instead of making the S3 bucket public. Better security posture.

**Infrastructure as Code:** I clicked through the AWS console for everything. If I rebuilt this, I'd use Terraform or CloudFormation to make the setup reproducible.

**Add a visitor counter:** The Cloud Resume Challenge specifically asks for a DynamoDB backend + Lambda function to track visitor count. I focused on getting the hosting right first, but that backend would add a nice serverless component.

**Cost monitoring alerts:** I set up billing alerts after my first AWS bill (only $0.53, but still). Would do this on day one next time.

## Setup Notes

If you're replicating this:

1. **Buy domain in Route 53** (auto-creates hosted zone)
2. **Request ACM certificate** for `example.com` and `www.example.com` (must be in `us-east-1` for CloudFront)
3. **Validate via DNS** (add the CNAME records ACM gives you)
4. **Create S3 bucket**, enable static hosting, upload files
5. **Set bucket policy** to allow public `GetObject` (or use OAI)
6. **Create CloudFront distribution** with S3 origin
7. **Add CNAMEs** (`example.com`, `www.example.com`) and attach ACM cert
8. **Set viewer protocol** to redirect HTTP → HTTPS
9. **Add A records in Route 53** pointing to CloudFront distribution (use Alias records)
10. **Wait 15-20 minutes** for CloudFront deployment

## Current Status

**Live and running** since November 2024. Handles my personal portfolio traffic (~100 visits/month, so not exactly high-scale). Total monthly cost: **$0.50 - $1.00** (Route 53 hosted zone is $0.50/month, CloudFront/S3 are negligible at my traffic level).

The site is responsive, loads fast (CloudFront CDN), and I've had zero downtime. Exactly what I wanted.

---

**Built with:** AWS S3, CloudFront, Route 53, Certificate Manager  
**Deployed:** November 2024  
**Cost:** ~$0.50/month (Route 53 zone only)

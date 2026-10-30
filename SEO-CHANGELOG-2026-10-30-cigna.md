# 2026-10-30: Cigna removed from carrier logos + Cigna exit post

## Logos
- Cigna removed from every carrier logo strip and quote page: 200 logo elements in 101 files
  (carrier marquees, ppo/small-business strips, open-enrollment, /quote, /trucking-health-quote, /small-business-health-quote,
  truckers/quote + cotizar). Script: .seo-work/remove_cigna_logos_oct30.py. Text mentions of Cigna (articles, FAQs) left as is.
- images/carriers/cigna.png left on disk (no longer referenced).

## New post: /blog/cigna-leaving-aca-marketplace-2027
- Facts (checked Oct 30 2026): exit announced Apr 30 2026 with Q1 earnings (STAT); individual market on and off exchange in
  11 states AZ CO FL GA IL IN MS NC TN TX VA (KFF updated Oct 28 2026; ACASignups); ~369,000 members Q1 2026, ~446,000 Q1 2025;
  FL largest (~97,000, Mar 2025 est.). Auto-move varies: Georgia Access moves members; CO and IL require choosing; off-exchange
  buyers not moved (HealthCare Insider Oct 15 2026). 60-day SEP after Jan 1 if auto-enrolled (healthinsurance.org).
  Colorado SEP for Cigna members to Mar 1. Employer plans not affected; Cigna sold Medicare business to HCSC in 2025.
- Lead capture: ZIP form + CTA -> /premium-increase-review?from=blog-cigna-leaving-aca-marketplace-2027.
- Images: compressed/cigna-leaving-aca-marketplace-2027(.jpg/-900/.webp) for OG + blog card, -hero(.jpg/-900) 16:7 for the page.
- Wiring: blog.html card (top), sitemap, llms.txt, links from the rate-increase post and the why-did post.
- Rate-increase post: hero now uses a 16:7 image (-hero) so the logo is no longer cropped.
Builder: .seo-work/build_cigna_post_oct30.py (+ cigna_post_body.html, cigna_post_meta.json).

Next (needs you): request indexing for the new post; GBP/LinkedIn post linking to it.

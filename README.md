# Dalton Braddock — official author website

A fast, responsive, static author website built for GitHub Pages. Evergreen, warm ivory, charcoal, and antique copper frame original landscape and typographic artwork. No build tools, runtime JavaScript, third-party fonts, cookies, or package installation are required.

## Pages

- `index.html` — introduction, four featured books, and author preview.
- `about.html` — concise biography using confirmed author and bibliography information.
- `books.html` — novels and children's books, with individual title anchors and Amazon product links.
- `contact.html` — Amazon author page and official author information. No email address or social profile is fabricated.
- `styles.css` — shared responsive styles, keyboard focus states, and reduced-motion support.

## Develop locally

From the repository root:

```sh
python3 -m http.server 8000
```

Open the local server in your browser. There is no build step. All internal paths are relative so the site works under the GitHub Pages repository subdirectory.

Run the dependency-free checks:

```sh
python3 scripts/check_site.py
```

They validate local links and fragments, assets, unique page metadata, canonical URLs, JSON-LD author/book records, and sitemap consistency. During development, Chromium browser checks also covered all four pages at 320, 375, 768, and 1440 pixels, the keyboard skip link, reduced motion, and browser errors. Repeat visual checks after design changes; the Python checks do not measure layout or contrast.

## Deploy through GitHub Pages

1. Merge the website pull request into `main`.
2. In this repository, open **Settings → Pages**.
3. Set **Source** to **Deploy from a branch**, choose **main** and **/ (root)**, and save.
4. Wait for the GitHub Pages deployment to finish and verify the live pages.

Production URL:

https://dalton-cyber.github.io/dalton-braddock-author-site/

`.nojekyll` tells Pages to serve these files directly. Deployment requires no secrets. The site does not change repository Pages settings automatically.

## Search and sharing

Every page has a unique title and meta description, canonical URL, Open Graph metadata, a local social image, and author structured data. The books page includes four `Book` records in an `ItemList`. `robots.txt` permits crawling and advertises `sitemap.xml`. No publication dates, ISBNs, prices, reviews, awards, or unsupported plot details are asserted.

After deployment:

1. Add the production URL as a **URL-prefix property** in Google Search Console.
2. Verify ownership using Google's provided method. For an HTML verification file, place the exact supplied file in the repository root; alternatively, add Google's supplied verification meta tag.
3. Submit `sitemap.xml` and inspect the home and books URLs. Request indexing after the deployment is publicly accessible.

Search engines decide indexing and ranking; metadata does not guarantee either. If using a custom domain later, update canonical URLs, `og:url`, `og:image`, JSON-LD IDs/URLs, `robots.txt`, `sitemap.xml`, and the validation script's `BASE` constant consistently. Add a `CNAME` file only for a domain you control.

## Content and source notes

Author: **Dalton Braddock**. Book titles were supplied by the author. Product and author URLs below were supplied directly during implementation and normalized to remove tracking parameters:

| Title                          | Section          | Amazon                               |
| ------------------------------ | ---------------- | ------------------------------------ |
| The Isles of Calgannor         | Novels           | https://www.amazon.com/dp/B0FSYGCNVH |
| The Knife Between              | Novels           | https://www.amazon.com/dp/B0FP8F921C |
| Mystery of the Missing Antlers | Children's books | https://www.amazon.com/dp/B0FN6Z3F5V |
| The Tide That Turned           | Children's books | https://www.amazon.com/dp/B0FLVLGMK6 |

Amazon author page: https://www.amazon.com/stores/Dalton-Braddock/author/B0FLZZ7MCL

The two children's titles are grouped under _Braddock Wild Life Adventures_, as identified by the supplied product URLs. The other two titles are presented in the novels section. The Amazon pages could not be independently fetched in the development environment because outbound access was denied. The supplied product links are genuine author-provided destinations, but availability and editions must be checked on Amazon before publication.

No approved detailed biography, author portrait, plot descriptions, public email address, or original cover files were provided. The biography therefore uses only confirmed bibliography information. Book displays use original CSS title artwork, explicitly identified as artwork rather than published covers. Replace them with licensed, author-approved cover files when available, using descriptive `alt` text, image dimensions, and optimized local images. Do not use guessed cover URLs or placeholder purchase links.

## Updating the collection

Keep titles and purchase links consistent between the home page, books page, biography, and books JSON-LD. When adding pages, update the navigation, sitemap, and `PAGES` in `scripts/check_site.py`. Add genuine contact details only with the author's approval. This site has no contact backend or form that could silently discard messages.

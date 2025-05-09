# Blog Post Creation Workflow (Eleventy)

This document outlines the steps to create a new blog post now that the site uses the Eleventy Static Site Generator (SSG).

## Process

1.  **Create a New Markdown File:**
    *   Navigate to the `blog/posts/` directory in your project.
    *   Create a new file with a descriptive name and the `.md` extension (e.g., `my-new-post-title.md`). Use hyphens for spaces in the filename.

2.  **Add Front Matter:**
    *   At the very top of the new file, add YAML front matter enclosed in triple dashes (`---`).
    *   **Required Fields:**
        *   `title`: "Your Post Title Here" (Enclose in quotes)
        *   `layout`: `post.liquid` (Specifies the template file in `_includes/`)
        *   `tags`: `posts` (Crucial for including the post in the blog list)
        *   `date`: "YYYY-MM-DD" (e.g., "2024-09-15")
    *   **Required/Recommended for Content Quality:**
        *   `description`: "A brief summary of the post for SEO and excerpts."
        *   `category`: "The Category Name" (e.g., "Workout Guides", "HIIT Fundamentals". Should match categories used in `blog/index.liquid` filtering.)
        *   `featured_image`: "/assets/blog/your-image-name.jpg" (Path relative to the site root - **See Image Handling below**)
        *   `image_alt`: "Descriptive alt text for the featured image."

    *   **Example Front Matter:**
        ```yaml
        ---
        title: "My Awesome New HIIT Workout"
        description: "Learn this amazing workout routine that targets full body strength."
        date: "2024-08-20"
        featured_image: "/assets/blog/new-workout-cover.jpg"
        image_alt: "Person performing the new workout exercise"
        layout: "post.liquid"
        tags: "posts"
        category: "Workout Guides"
        ---
        ```

3.  **Write Content in Markdown:**
    *   Below the closing `---` of the front matter, write the actual blog post content using standard Markdown syntax.
    *   **Goal:** Create informative, engaging, and SEO-friendly content based on the topic (referencing `blog-post-ideas.md` and `seo-strategy.md`).
    *   **Structure:** Use headings (`##`, `###`), lists (`*`, `1.`), bold/italics, etc., to structure the content logically.
    *   **Keywords:** Naturally incorporate target keywords identified in the SEO strategy.
    *   **App Integration:** Where relevant, mention how the Peak Interval app can be used in relation to the post's topic (e.g., specific timer settings, features).
    *   **CTAs:** Include relevant Calls to Action, potentially using the styled `cta-box` HTML structure (see below).
    *   **Quality:** Ensure high content quality, accuracy, and adherence to editorial guidelines.
    *   **HTML:** You can include raw HTML within the Markdown for complex elements like the styled CTA boxes, custom divs (like `mistake-box`, `glossary-term`), figures, etc. Eleventy will pass this through directly.
        ```html
        <div class="cta-box">
            <h3>Check this out!</h3>
            <p>Some content.</p>
            <a href="https://apps.apple.com/us/app/peak-interval-hiit-timer/id6741055716" class="cta-button">Download Peak Interval</a>
        </div>
        ```

4.  **Image Handling:**
    *   **Source Images:** Find high-quality, relevant images (e.g., from stock photo sites like Unsplash, Pexels, or custom graphics).
    *   **Optimize Images:** Before adding, resize and compress images for web use to ensure fast page loading times. Tools like TinyPNG or Squoosh can help.
    *   **Save Images:** Place the optimized images in the `/assets/blog/` directory (or your designated image folder).
    *   **Update Front Matter:** Replace the placeholder path in the `featured_image` front matter with the correct path to your new image (e.g., `featured_image: "/assets/blog/actual-image-name.jpg"`).
    *   **Add Alt Text:** Ensure the `image_alt` field provides a meaningful description of the image.
    *   **Content Images:** Use standard Markdown `![Alt text](/path/to/image.jpg)` or HTML `<img>` tags for images within the post body.

5.  **Preview:**
    *   Run the Eleventy development server: `npx @11ty/eleventy --serve`
    *   Open `http://localhost:8080/blog/` in your browser.
    *   Check the blog list for the new post.
    *   Navigate to the full post page and carefully review the content, formatting, images, and links.

6.  **Update Tracking:**
    *   Open the `blog-post-ideas.md` file.
    *   Find the corresponding blog post idea in the list.
    *   Mark it as completed by adding `[DONE]` at the end of the line.
    *   This helps track which blog posts have been published and which ideas are still available for future content.

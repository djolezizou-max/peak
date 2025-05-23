# Blog Post Creation Workflow (Eleventy)

This document outlines the steps to create a new blog post now that the site uses the Eleventy Static Site Generator (SSG).

## Process

1.  **Create a New Markdown File:**
    *   Navigate to the `blog/posts/` directory in your project.
    *   Create a new file with a descriptive name and the `.md` extension (e.g., `my-new-post-title.md`). Use hyphens for spaces in the filename.

2.  **Generate a Featured Image with OpenAI:**
    *   Use our custom script to generate a high-quality, relevant image for your blog post using OpenAI's image generation API.
    *   Run the script with a detailed prompt that describes the desired image:
        ```bash
        ./generate_blog_image.sh "Detailed description of the image you want, including style details like 'photorealistic'" "filename-for-image.jpg"
        ```
    *   The script will automatically:
        *   Generate the image using AI
        *   Save it to the correct location in `/assets/blog/`
        *   Provide the path to use in your front matter
    *   Example:
        ```bash
        ./generate_blog_image.sh "A person performing high-intensity interval training exercises outdoors with mountains in the background, photorealistic fitness photography" "hiit-nature-workout.jpg"
        ```

3.  **Add Front Matter:**
    *   At the very top of the new file, add YAML front matter enclosed in triple dashes (`---`).
    *   **Required Fields:**
        *   `title`: "Your Post Title Here" (Enclose in quotes)
        *   `layout`: `post.liquid` (Specifies the template file in `_includes/`)
        *   `tags`: `posts` (Crucial for including the post in the blog list)
        *   `date`: "YYYY-MM-DD" (e.g., "2024-09-15")
    *   **Required/Recommended for Content Quality:**
        *   `description`: "A brief summary of the post for SEO and excerpts."
        *   `category`: "The Category Name" (e.g., "Workout Guides", "HIIT Fundamentals". Should match categories used in `blog/index.liquid` filtering.)
        *   `featured_image`: "/assets/blog/your-image-name.jpg" (Use the path provided by the image generation script)
        *   `image_alt`: "Descriptive alt text for the featured image that matches the content of the AI-generated image."

    *   **Example Front Matter:**
        ```yaml
        ---
        title: "Outdoor HIIT Workouts: Taking Your Intervals Into Nature"
        description: "Discover the benefits of outdoor HIIT workouts and learn how to create effective interval training sessions using natural environments and minimal equipment."
        date: "2025-05-11"
        featured_image: "/assets/blog/outdoor-hiit-nature.jpg"
        image_alt: "Person performing high-intensity interval training exercises in a scenic natural outdoor setting with mountains and trees"
        layout: "post.liquid"
        tags: "posts"
        category: "Workout Guides"
        ---
        ```

4.  **Write Content in Markdown:**
    *   Below the closing `---` of the front matter, write the actual blog post content using standard Markdown syntax.
    *   **Goal:** Create informative, engaging, and SEO-friendly content based on the topic (referencing `blog-post-ideas.md` and `seo-strategy.md`).
    *   **Structure:** Use headings (`##`, `###`), lists (`*`, `1.`), bold/italics, etc., to structure the content logically.
    *   **Content Flow Best Practices:**
        * **Narrative paragraphs:** Prioritize well-crafted paragraphs (3-5 sentences) for most content. Develop ideas fully with proper transitions between thoughts.
        * **Bullet point moderation:** Use bullet points sparingly and strategically for:
            - Lists that truly need to be itemized
            - Key points that need visual separation
            - Technical specifications or quick reference information
        * **Paragraph-to-bullet ratio:** Aim for at least 3-4 paragraphs between each bullet point list
        * **Contextual framing:** Always introduce bullet points with a proper explanatory paragraph
        * **Follow-up explanation:** Consider adding detailed paragraphs after important bullet points to expand on key ideas
    *   **Content Variety:** Balance your content with:
        * Narrative paragraphs (primary content structure)
        * Occasional bullet points (for truly list-worthy content)
        * Descriptive examples
        * Short anecdotes or scenarios
        * Analogies to clarify complex concepts
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

5.  **Additional Images (If Needed):**
    *   For any additional images within the post content, you can either:
        *   Generate more AI images using the same script with different prompts and filenames
        *   Use standard Markdown `![Alt text](/path/to/image.jpg)` or HTML `<img>` tags to include these images in your post
    *   Example for generating a secondary image:
        ```bash
        ./generate_blog_image.sh "A specific HIIT exercise being performed in a park, side angle view, photorealistic" "hiit-exercise-demo.jpg"
        ```
    *   Then include it in your post:
        ```markdown
        ![Person demonstrating proper HIIT exercise form](/assets/blog/hiit-exercise-demo.jpg)
        ```

6.  **Preview:**
    *   Run the Eleventy development server: `npx @11ty/eleventy --serve`
    *   Open `http://localhost:8080/blog/` in your browser.
    *   Check the blog list for the new post.
    *   Navigate to the full post page and carefully review the content, formatting, images, and links.

7.  **Update Tracking:**
    *   Open the `blog-post-ideas.md` file.
    *   Find the corresponding blog post idea in the list.
    *   Mark it as completed by adding `[DONE]` at the end of the line.
    *   This helps track which blog posts have been published and which ideas are still available for future content.

## Tips for Effective AI Image Generation

1. **Be Highly Specific in Prompts:**
   * Describe the scene, subjects, actions, environment, and style
   * Include details like "photorealistic fitness photography" for consistent style
   * Mention specific equipment, locations, or elements relevant to the post topic

2. **Align Images with Content:**
   * The image should clearly represent the main topic of the blog post
   * For workout posts, include descriptions of the exercises being performed
   * For concept posts, visualize the key principles being discussed

3. **Multiple People Synchronization:**
   * **IMPORTANT:** When prompts include multiple people, ensure they are all performing the same exercise in perfect synchronization
   * Specify "all performing the same exercise simultaneously" or "all doing identical movements in sync"
   * Avoid prompts that could result in different people doing different exercises
   * Example: "Group of people all performing jumping jacks simultaneously" instead of "Group of people doing various exercises"

4. **Image Sizes and Quality:**
   * The script generates 1024x1024 pixel images by default
   * These are already optimized for web use
   * No additional compression is necessary for AI-generated images

5. **Troubleshooting:**
   * If an image doesn't match your expectations, try running the script again with a more detailed prompt
   * Check the `assets/blog/` directory to confirm the image was saved correctly
   * Ensure the image path in the front matter exactly matches the filename used in the script

const { DateTime } = require("luxon");

module.exports = function(eleventyConfig) {

  // Clean the output directory before each build
  eleventyConfig.setUseGitIgnore(false);
  
  // Ignore all markdown files at the root of the project
  eleventyConfig.ignores.add("*.md");
  
  // Pass through static assets
  eleventyConfig.addPassthroughCopy("assets");
  eleventyConfig.addPassthroughCopy("favicon.ico");
  eleventyConfig.addPassthroughCopy("app_icon.png");
  eleventyConfig.addPassthroughCopy("robots.txt");
  // IndexNow verification key. Must stay reachable at the site root or every
  // IndexNow ping is rejected (see Scripts/marketing/indexnow_ping.py).
  eleventyConfig.addPassthroughCopy("bc78c3ae8d93a7d9bcb54ddaa9c837bd.txt");

  // Strip trailing slash (except for root "/") so canonical URLs match
  // Vercel's trailingSlash: false routing.
  eleventyConfig.addFilter("stripTrailingSlash", (url) => {
    if (!url || url === "/") return url;
    return url.endsWith("/") ? url.slice(0, -1) : url;
  });

  // Add slugify filter
  const slugify = require("slugify");
  eleventyConfig.addFilter("slugify", (str) => {
    if (!str) return;
    return slugify(str, {
      lower: true,
      strict: true,
      remove: /[*+~.()\'"!:@]/g
    });
  });

  // A page's real last-modified date is the later of its own date and the last
  // sitewide template change, because editing a layout rewrites every page that
  // uses it. Without this, posts advertise a 2023 lastmod after their rendered
  // HTML changed, and Google deprioritises recrawling them.
  eleventyConfig.addFilter("maxDate", (a, b) => {
    if (!a) return b;
    if (!b) return a;
    return a > b ? a : b;
  });

  // Date formatting filter (for sitemap)
  eleventyConfig.addLiquidFilter("htmlDateString", (dateObj) => {
    // Check if dateObj is valid and not null
    if (!dateObj || !(dateObj instanceof Date) || isNaN(dateObj)) {
      // Return current date or a placeholder if the input date is invalid
      return DateTime.now().toISODate(); 
    }
    return DateTime.fromJSDate(dateObj, {zone: 'utc'}).toISODate();
  });

  // Generate category pages
  eleventyConfig.addCollection("categoryPages", function(collectionApi) {
    // Get all posts
    const posts = collectionApi.getFilteredByTag("posts");
    
    // Extract unique categories
    const categories = new Set();
    posts.forEach(post => {
      if (post.data.category) {
        categories.add(post.data.category);
      }
    });
    
    // Create category pages
    return Array.from(categories).map(category => {
      return {
        category: category,
        slug: slugify(category, {
          lower: true,
          strict: true,
          remove: /[*+~.()\'"!:@]/g
        })
      };
    });
  });

  // Set custom directories for input, output, includes, and data
  // These are relative to the project root
  return {
    // Control which files Eleventy will process
    // e.g.: *.md, *.njk, *.html, *.liquid
    templateFormats: [
      "md",
      "liquid",
      "html",
    ],

    // Pre-process *.md files with: (default: `liquid`)
    markdownTemplateEngine: "liquid",

    // Pre-process *.html files with: (default: `liquid`)
    htmlTemplateEngine: "liquid",

    // Directory structure (defaults are shown)
    dir: {
      input: ".", // Process files from the project root
      includes: "_includes", // Folder for layouts, partials, etc.
      data: "_data", // Folder for global data files
      output: "_site" // Where the generated site will live
    }
  };
}; 
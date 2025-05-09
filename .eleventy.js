const { DateTime } = require("luxon");

module.exports = function(eleventyConfig) {

  // Pass through static assets
  eleventyConfig.addPassthroughCopy("assets");
  eleventyConfig.addPassthroughCopy("favicon.ico");
  eleventyConfig.addPassthroughCopy("app_icon.png");

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

  // Date formatting filter (for sitemap)
  eleventyConfig.addLiquidFilter("htmlDateString", (dateObj) => {
    // Check if dateObj is valid and not null
    if (!dateObj || !(dateObj instanceof Date) || isNaN(dateObj)) {
      // Return current date or a placeholder if the input date is invalid
      return DateTime.now().toISODate(); 
    }
    return DateTime.fromJSDate(dateObj, {zone: 'utc'}).toISODate();
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
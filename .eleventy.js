module.exports = function(eleventyConfig) {
  // Passthrough copy for assets and admin
  eleventyConfig.addPassthroughCopy({ "assets": "assets" });
  eleventyConfig.addPassthroughCopy({ "admin": "admin" });

  // Watch CSS and JS for live reload
  eleventyConfig.addWatchTarget("assets/styles.css");
  eleventyConfig.addWatchTarget("assets/image-viewer.js");

  return {
    dir: {
      input: "src",
      output: "_site",
      includes: "_includes",
      layouts: "_includes/layouts"
    },
    // Enable deep merge for data if needed
    dataTemplateEngine: "njk",
    htmlTemplateEngine: "njk",
    markdownTemplateEngine: "njk"
  };
};

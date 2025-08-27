module.exports = function(eleventyConfig) {
  // Passthrough copy for assets and admin
  eleventyConfig.addPassthroughCopy({ "assets": "assets" });
  eleventyConfig.addPassthroughCopy({ "admin": "admin" });

  // Watch CSS and JS for live reload
  eleventyConfig.addWatchTarget("assets/styles.css");
  eleventyConfig.addWatchTarget("assets/image-viewer.js");

  // HTML-transform för att lägga till klasser på bilder
  eleventyConfig.addTransform("image-classes", function(content, outputPath) {
    if (outputPath && outputPath.endsWith(".html")) {
      // Lägg till klasser på alla bilder i artiklar
      content = content.replace(
        /<p><img([^>]+)><\/p>/g,
        '<p class="image-container"><img$1 class="article-image"></p>'
      );
      
      // Hantera fall där bilden inte är i en p-tag
      content = content.replace(
        /<img([^>]+)(?<!class="[^"]*")>/g,
        '<img$1 class="article-image">'
      );
    }
    return content;
  });



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

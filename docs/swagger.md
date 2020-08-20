<div id="swagger-ui"></div>

<script src="wagger-ui-bundle.js"></script>
<script src="wagger-ui-standalone-preset.js"></script>

<script>
window.onload = function() {
  const ui = SwaggerUIBundle({
    url: "https://github.com/greenbird/piri/blob/master/mapmallow/schema.json",
    dom_id: '#swagger-ui',
    presets: [
      SwaggerUIBundle.presets.apis,
      SwaggerUIStandalonePreset
    ]
  })

  window.ui = ui
}
</script>

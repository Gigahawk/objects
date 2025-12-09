<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Objects</title>

  <style>
    /* Make the page a column flex container and remove default margins */
    html, body {
      height: 100%;
      margin: 0;
      box-sizing: border-box;
    }
    body {
      display: flex;
      flex-direction: column;
      min-height: 100vh;
    }

    /* Keep the select at its natural height and let the iframe fill the rest */
    #model {
      margin: 12px;
      max-width: 100%;
    }

    iframe {
      flex: 1 1 auto; /* fill remaining vertical space */
      width: 100%;
      border: 0;
      display: block;
    }
  </style>
</head>

<body>
  <select name="model" id="model">
  % for model in models.splitlines():
    <option value="${model}">${model}</option>
  % endfor
  </select>

  <iframe src="https://gigahawk.github.io/Online3DViewer/website/" title="description"></iframe> 

  <script>
    // Update iframe src when the select changes and initialize on DOM ready
    (function() {
      var select = document.getElementById('model');
      var frame = document.querySelector('iframe');

      if (!select || !frame) return;

      function updateFrame() {
        // If value is a relative/path or full URL, it will be used as-is.
        frame.src = 'https://gigahawk.github.io/Online3DViewer/website/#model=https://gigahawk.github.io/objects/' + select.value;
      }

      // Update on change
      select.addEventListener('change', updateFrame);

      // Initialize iframe to current selection on load
      document.addEventListener('DOMContentLoaded', function() {
        updateFrame();
      });
    })();
  </script>

</body>
</html>

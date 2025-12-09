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
      margin: 0;
      max-width: 100%;
    }

    iframe {
      flex: 1 1 auto; /* fill remaining vertical space */
      width: 100%;
      border: 0;
      display: block;
    }

    /* Controls container for select + download button */
    .controls {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 12px;
    }

    #download {
      display: inline-block;
      padding: 6px 10px;
      background: #0078d4;
      color: #fff;
      text-decoration: none;
      border-radius: 4px;
      font-size: 14px;
    }
    #download[aria-disabled="true"] {
      opacity: 0.5;
      pointer-events: none;
    }

    /* Built-from link: push to the right of the controls */
    #built-from {
      margin-left: auto;
      color: #666;
      text-decoration: none;
      font-size: 13px;
      padding: 6px 8px;
    }
    #built-from:hover {
      text-decoration: underline;
    }
  </style>

  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script>

  <link href="https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css" rel="stylesheet" />
  <script src="https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.min.js"></script>
</head>

<body>
  <!-- controls: select + download button -->
  <div class="controls">
    <select name="model" id="model">
    % for model in models.splitlines():
      <option value="${model}">${model}</option>
    % endfor
    </select>

    <a id="download" href="#" download>Download</a>

    <a id="built-from" href="https://github.com/Gigahawk/objects/commit/${gitsha}">Built from commit ${gitsha[0:7]}</a>
  </div>

  <iframe id="viewer" src="https://gigahawk.github.io/Online3DViewer/website/" title="description"></iframe> 

  <script>
    $(document).ready(function() {

      function objectUrlFor(modelPath) {
        return 'https://gigahawk.github.io/objects/' + modelPath;
      }

      function viewerUrlFor(modelPath) {
        // viewer expects a full URL after "model=" in the hash
        var objUrl = objectUrlFor(modelPath);
        // Suprisingly you cannot encode the url in the model param
        //return 'https://gigahawk.github.io/Online3DViewer/website/#model=' + encodeURIComponent(objUrl);
        return 'https://gigahawk.github.io/Online3DViewer/website/#model=' + objUrl;

      }

      $('#model').select2();

      function updateAll(e) {
        console.log(e);
        var val = $("#model").val();
        console.log("Setting target model to " + val);
        $("#viewer").attr('src', viewerUrlFor(val));
        $("#download").attr('href', objectUrlFor(val));
        // Use the last segment as filename if possible
        try {
          var parts = val.split('/');
          var filename = parts[parts.length - 1] || 'download';
          $("#download").attr('download', filename);
          $("#download").removeAttr('aria-disabled');
        } catch (e) {
          $("#download").attr('aria-disabled', 'true');
        }
      }

      $('#model').on("change", updateAll);

      updateAll();

    });
  </script>

</body>
</html>

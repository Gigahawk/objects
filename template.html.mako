<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Objects</title>
</head>

<body>
  <select name="model" id="model">
  % for model in models.splitlines():
    <option value="${model}">${model}</option>
  % endfor
  </select>

  <iframe src="https://gigahawk.github.io/Online3DViewer/website/" title="description"></iframe> 

</body>
</html>

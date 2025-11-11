4. To tell browsers how to encode chars on your page, set the `charset` to `utf-8`.  `utf-8` is a universal character set that includes almost every character from all human languages.
Inside the `head` element, nest a `meta` element with the attribute `charset` set to `utf-8`. Remember that `meta` elements are self-closing, and do not need a closing tag.
```html
  <head>
    <title>Colored Markers</title>
    <meta charset="utf-8">
</head>
```

5. You can have multiple self-closing `meta` elements on a web page. Each `meta` element adds information about the page that cannot be expressed by other HTML elements.

Add another self-closing `meta` element within the `head`. Give it a `name` attribute set to `viewport` and a `content` attribute set to `width=device-width, initial-scale=1.0` so your page looks the same on all devices.
```html
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Colored Markers</title>
</head>
```
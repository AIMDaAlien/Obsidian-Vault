---
tags: [css, freecodecamp]
created: 2025-09-15
publish: true
---
These are my own study notes following the freeCodeCamp Responsive Web Design certification course "Learn CSS Colors by Building a Set of Colored Markers" at https://www.freecodecamp.org/learn/ .

# CSS Colors and Box Model - Colored Markers

## Page setup and the head

Every page starts the way any HTML page does: a doctype and an `html` element with a language.

```html
<!DOCTYPE html>
<html lang="en">
</html>
```

Inside `html` I nest a `head` and, right after it, a `body`. The `title` element goes in the `head`. It gives search engines extra information about the page, and it also shows up in the browser's title bar and in the tab itself. Even a tab that is not currently open shows the title text when I hover over it.

```html
<head>
  <title>Colored Markers</title>
</head>
```

## Meta elements

`meta` elements are self-closing, so they need no closing tag, and a page can have several. Each one adds information about the page that no other HTML element can express.

The first sets the character encoding. `utf-8` is a universal character set covering almost every character from every human language.

```html
<meta charset="utf-8">
```

The second is the viewport meta element, which uses `name` and `content` attributes so the page looks the same on all devices.

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

## Linking an external stylesheet

This project keeps its styles in an external CSS file, `styles.css`, which has to be linked before it takes effect. A `link` element goes inside the `head`, with `rel` set to `stylesheet` and `href` pointing at the file.

```html
<link rel="stylesheet" href="styles.css">
```

## Structuring the page and the markers

Content lives in the `body`. I start with an `h1` reading "CSS Color Markers".

Next I need elements that will eventually become the colored markers. Below the `h1` I add a `div` with the class `container`, and inside it a `div` with the class `marker`.

```html
<div class="container">
  <div class="marker"></div>
</div>
```

Once one marker works, adding more is just a matter of putting two more `div` elements with the class `marker` inside the container, so there are three in total.

## Styling the heading

To center the heading, I target the `h1` and set `text-align` to `center`. This is the same pattern used earlier to right-align a paragraph, just with a different value.

```css
h1 {
  text-align: center;
}
```

## Color keywords

One simple way to color an element is a color keyword such as `black`, `cyan`, or `yellow`. I target the `marker` class and set `background-color`.

```css
.marker {
  background-color: red;
}
```

## Size and the box model

An empty `div` has no height by default, because there is no content to push it open. So the marker has to be given explicit dimensions with the `height` and `width` properties.

```css
.marker {
  background-color: red;
  height: 25px;
  width: 200px;
}
```

### Centering with the margin shorthand

Earlier I set the margin of each side separately with properties like `margin-top` and `margin-left`. The `margin` shorthand sets several sides at once. Giving it a single value of `auto` sets top, right, bottom, and left margins all to `auto`, which centers the marker horizontally on the page.

```css
margin: auto;
```

### Two-value margin

With three separate marker `div` elements stacked directly together, they read as one big rectangle, so they need space between them. When `margin` has two values, the first sets `margin-top` and `margin-bottom`, and the second sets `margin-left` and `margin-right`. Using `10px auto` gives each marker 10px of vertical space while keeping it horizontally centered.

```css
margin: 10px auto;
```

## Complete result

The course material I followed stops partway through the project, so this is the page as it stands: three markers, all still red.

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <link rel="stylesheet" href="styles.css">
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Colored Markers</title>
  </head>
  <body>
    <h1>CSS Color Markers</h1>
    <div class="container">
      <div class="marker"></div>
      <div class="marker"></div>
      <div class="marker"></div>
    </div>
  </body>
</html>
```

```css
h1 {
  text-align: center;
}

.marker {
  width: 200px;
  height: 25px;
  background-color: red;
  margin: 10px auto;
}
```

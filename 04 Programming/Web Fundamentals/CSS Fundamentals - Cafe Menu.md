---
tags: [css, freecodecamp]
created: 2025-09-15
publish: true
---

These are my own study notes from the Responsive Web Design certification on [freeCodeCamp](https://www.freecodecamp.org/learn/), working through the project "Learn Basic CSS by Building a Cafe Menu".

# CSS Fundamentals - Cafe Menu

The project builds a one-page menu for a made-up place called Camper Cafe. I start from an empty file and end with a centered, styled menu with coffees, desserts, dividers, icons and a footer. Everything below is grouped by idea rather than by the order I met it.

## HTML skeleton and page structure

Every page starts from the same boilerplate: a `<!DOCTYPE html>` declaration, then an `html` element carrying `lang="en"`. Inside it goes a `head` for information that is not shown on the page, and a `body` for what is.

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <title>Cafe Menu</title>
  </head>
  <body></body>
</html>
```

The `title` is only one of several head elements that help search engines and browser tabs. Another is a self-closing `meta` element with `charset="utf-8"`, which tells the browser how to decode characters. A second `meta` with `name="viewport"` and `content="width=device-width, initial-scale=1.0"` makes the page look about the same on a phone as on a desktop.

Inside `body`, the content lives in a `main` element. It holds an `h1` with the cafe name in capitals (CAMPER CAFE) and a `p` saying `Est. 2020`. The menu is split in two with `section` elements, one for coffee and one for desserts, each opening with an `h2`. A later `footer` element sits after `main` for extra info.

Each menu entry is an `article`, which is meant for a small bundle of related content. Mine holds two `p` elements, the flavor and its price. I started with French Vanilla at 3.00 and filled in the remaining coffees. The desserts section uses the same pattern: Donut, Cherry Pie, Cheesecake and Cinnamon Roll.

The footer has a `p` containing an anchor (`a`) with the text "Visit our website", then a second `p` with the address. Adding `target="_blank"` opens the link in a new tab.

```html
<footer>
  <p><a href="https://www.freecodecamp.org" target="_blank">Visit our website</a></p>
  <p>123 Free Code Camp Drive</p>
</footer>
```

For layout purposes I also wrapped everything in a `div`. Unlike the content elements, `div` exists mainly to group things for design. All the other body content moved inside it.

## Adding CSS and linking a stylesheet

CSS first went inside a `style` element in the `head`, written as a selector followed by braces containing property and value pairs. That works, but since there would be many more rules, it is cleaner to keep them in a separate `styles.css` file. I moved the rules over (without the `style` tags), deleted the `style` element, and the centered text snapped back to the left, which proved the styles were no longer applied.

To reconnect them, a self-closing `link` goes in the head with `rel="stylesheet"` and an `href` pointing at the file.

```html
<link rel="stylesheet" href="styles.css" />
```

Once the text centered again I knew the link worked. A comment in CSS is wrapped in `/* ... */`, which is handy for switching a declaration off temporarily and for labeling parts of the file.

```css
/* background-color: burlywood; */
```

## Selectors

The first selectors were type selectors, which target every element of a kind. `h1 { text-align: center; }` centers all headings of that level. Repeating the same declaration for `h1`, `h2` and `p` is wasteful, so I combined them into a selector list, separated by commas.

```css
h1, h2, p {
  text-align: center;
}
```

A class selector is a name with a dot in front of it and is applied by putting a matching `class` attribute on an element. I turned the `div` rule into `.menu` and added `class="menu"` to the div. Classes are more precise than type selectors and can be reused on many elements. I used them throughout: `flavor`, `price`, `dessert`, `item`, `established`, `address`, `bottom-line`.

A descendant selector targets elements nested inside another. `.item p` matches every `p` anywhere inside an element with the class `item`.

```css
.item p {
  display: inline-block;
}
```

Classes can also share one rule through a list. When the dessert names needed the same look as the coffee flavors, I added `.dessert` to the existing rule instead of duplicating it:

```css
.flavor, .dessert {
  text-align: left;
  width: 75%;
}
```

## Text styling

Text alignment is controlled with `text-align`. I used `left` on the flavor and dessert names and `right` on the prices, which sets up a classic menu look.

Fonts come from `font-family`. Setting `sans-serif` on `body` changes all text, since the property is inherited. Then only the headings get `Impact`. A comma-separated fallback, such as `serif` after Impact, is used if the first choice is not installed.

```css
body { font-family: sans-serif; }

h1, h2 {
  font-family: Impact, serif;
}
```

To italicize the "Est. 2020" line I made an `.established` class with `font-style: italic` and applied it to that paragraph.

```css
.established {
  font-style: italic;
}
```

Heading sizes are browser defaults unless overridden, so I set them myself with `font-size`: 40px for `h1` and 30px for `h2`. Menu items got 18px and the footer text 14px. Since `.item p` already existed, the 18px just went into that same rule.

## Colors and backgrounds

`background-color` takes a named color. I tried `brown` on the body first, but the text was hard to read, so I switched to `burlywood`. Then, to see how the `div` behaved alone, I commented out the body color and gave the background to the div instead, which showed the menu box clearly.

Later the body got a coffee-beans picture through `background-image` with a `url(...)` value, replacing the plain color.

```css
body {
  background-image: url(https://example.com/beans.jpg);
}
```

## The box model, width and spacing

An element's size can be set with `width`, either in pixels or as a percentage of its parent. I began with `300px` on the div, then switched to `80%` of the body so it scales. A `max-width` of `500px` stops it growing too wide on large screens, which was making the coffee names sit far from their prices.

Margin is invisible space outside an element. Setting `margin-left` and `margin-right` to `auto` centers a block horizontally inside its parent.

Padding is space inside the element, between its edge and its content. I first set the four sides one at a time, then collapsed them into the shorthand `padding: 20px`. The body also got `padding: 20px` to leave room around the whole menu.

```css
.menu {
  width: 80%;
  max-width: 500px;
  background-color: burlywood;
  margin-left: auto;
  margin-right: auto;
  padding: 20px;
}
```

Vertical margins were used for fine tuning. The lines of menu items looked too far apart, so `.item p` got `margin-top` and `margin-bottom` of `5px`. The `h1` had a default top margin that made the top space differ from the bottom, so I set `margin-top: 0` and trimmed `margin-bottom` to `15px`. The address paragraph had the opposite problem: an `.address` class with `margin-bottom: 5px` made the space below it match the top.

After the last `hr` the gap looked smaller than at the top, so a `.bottom-line` class with `margin-top: 25px` added space. I applied the class to the second `hr`.

```css
.bottom-line {
  margin-top: 25px;
}
```

Margins may also be negative. Pulling images upward by using `margin-top: -25px` was an easy way to tighten the gap between a heading and its icon, easier than changing the heading margin.

## Layout: putting flavor and price on one line

`p` elements are block level, so each takes the full width of its parent and they stack. To put flavor and price on the same line I made them behave like inline elements with `display: inline-block` through the `.item p` rule. Inline-block boxes are only as wide as their content, so the prices did not stay at the far right. Giving each class a `width` of `50%` seemed the answer, but the second paragraph wrapped to the next line.

The cause is the whitespace in the HTML. Two inline-block elements on separate lines have a small space between them, which pushes the total over 100%. I tried `49%` each as a test, which worked but left a gap at the right of the price. The real fix was to remove the whitespace by writing the two `p` tags directly next to each other in the markup, and then going back to `50%`.

```html
<article class="item">
  <p class="flavor">French Vanilla</p><p class="price">3.00</p>
</article>
```

I repeated this for every article, adding the `item` class and the `flavor` or `dessert` and `price` classes. When I narrowed the preview, long flavor names wrapped, because the left side only had half the space. Since prices are short, I changed the widths to `75%` for the flavor and `25%` for the price.

## Dividers and borders

An `hr` element draws a horizontal divider and is self-closing. I placed one between the "Est. 2020" paragraph and the first section, and another between `main` and the footer. By default it is a thin grey line, so I styled its `height` and `background-color`.

The grey edges visible around it are its borders. Setting `border-color` to the same brown hides them.

```css
hr {
  height: 2px;
  background-color: brown;
  border-color: brown;
}
```

The default `border-width` is `1px` on every side, so the visible thickness is the height plus top and bottom borders. With a height of `3px` the line came to `5px`, thicker than intended. Dropping the height to `2px` gives a total of `4px`.

## Images

An `img` element needs a `src` and an `alt` describing it for screen readers and for when the image fails to load. I put a coffee icon under the Coffee heading ("coffee icon") and a pie icon under Desserts ("pie icon"). The menu had a lot of text, and the pictures lighten it.

Images are inline by default, so they did not center like the headings. Making them `display: block` and using auto side margins centered them. The negative top margin from above then closed the gap under each heading.

```css
img {
  display: block;
  margin-left: auto;
  margin-right: auto;
  margin-top: -25px;
}
```

## Links and pseudo-classes

A pseudo-class selector styles an element in a certain state, attached to the selector with a colon. For links the default colors are blue for unvisited and purple for visited. A plain `a` rule with `color: black` makes every link the same color regardless.

The state selectors are `a:visited` (already seen), `a:hover` (mouse over it) and `a:active` (being clicked). I first tried grey, brown and white to see the effect, then settled on a palette matching the black and brown theme: black when visited, brown on hover, and brown while pressed.

```css
a:visited {
  color: black;
}

a:hover {
  color: brown;
}

a:active {
  color: brown;
}
```

I also left a `/*FOOTER*/` comment before the footer rules to keep the stylesheet organized.

## Complete result

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta charset="utf-8" />
    <title>Cafe Menu</title>
    <link href="styles.css" rel="stylesheet" />
  </head>
  <body>
    <div class="menu">
      <main>
        <h1>CAMPER CAFE</h1>
        <p class="established">Est. 2020</p>
        <hr>
        <section>
          <h2>Coffee</h2>
          <img src="https://example.com/coffee.jpg" alt="coffee icon">
          <article class="item">
            <p class="flavor">French Vanilla</p><p class="price">3.00</p>
          </article>
          <article class="item">
            <p class="flavor">Caramel Macchiato</p><p class="price">3.75</p>
          </article>
          <article class="item">
            <p class="flavor">Pumpkin Spice</p><p class="price">3.50</p>
          </article>
          <article class="item">
            <p class="flavor">Hazelnut</p><p class="price">4.00</p>
          </article>
          <article class="item">
            <p class="flavor">Mocha</p><p class="price">4.50</p>
          </article>
        </section>
        <section>
          <h2>Desserts</h2>
          <img src="https://example.com/pie.jpg" alt="pie icon">
          <article class="item">
            <p class="dessert">Donut</p><p class="price">1.50</p>
          </article>
          <article class="item">
            <p class="dessert">Cherry Pie</p><p class="price">2.75</p>
          </article>
          <article class="item">
            <p class="dessert">Cheesecake</p><p class="price">3.00</p>
          </article>
          <article class="item">
            <p class="dessert">Cinnamon Roll</p><p class="price">2.50</p>
          </article>
        </section>
      </main>
      <hr class="bottom-line">
      <footer>
        <p><a href="https://www.freecodecamp.org" target="_blank">Visit our website</a></p>
        <p class="address">123 Free Code Camp Drive</p>
      </footer>
    </div>
  </body>
</html>
```

```css
body {
  background-image: url(https://example.com/beans.jpg);
  font-family: sans-serif;
  padding: 20px;
}

h1, h2, p {
  text-align: center;
}

h1, h2 {
  font-family: Impact, serif;
}

h1 {
  font-size: 40px;
  margin-top: 0;
  margin-bottom: 15px;
}

h2 {
  font-size: 30px;
}

.menu {
  width: 80%;
  max-width: 500px;
  background-color: burlywood;
  margin-left: auto;
  margin-right: auto;
  padding: 20px;
}

.established {
  font-style: italic;
}

.flavor, .dessert {
  text-align: left;
  width: 75%;
}

.price {
  text-align: right;
  width: 25%;
}

.item p {
  display: inline-block;
  margin-top: 5px;
  margin-bottom: 5px;
  font-size: 18px;
}

hr {
  height: 2px;
  background-color: brown;
  border-color: brown;
}

.bottom-line {
  margin-top: 25px;
}

img {
  display: block;
  margin-left: auto;
  margin-right: auto;
  margin-top: -25px;
}

/*FOOTER*/
footer {
  font-size: 14px;
}

a {
  color: black;
}

a:visited {
  color: black;
}

a:hover {
  color: brown;
}

a:active {
  color: brown;
}

.address {
  margin-bottom: 5px;
}
```

---
tags: [html, freecodecamp]
created: 2025-09-15
publish: true
---

My notes from freeCodeCamp's Responsive Web Design certification course, "Learn HTML by Building a Cat Photo App" (https://www.freecodecamp.org/learn/).

# HTML Fundamentals - CatPhotoApp

These notes follow one small project, a cat photo page, built up piece by piece. I have grouped them by topic instead of by the order I built things in.

## Elements, tags and attributes

An HTML element is usually an opening tag like `<h1>` and a closing tag like `</h1>`, with the content in between. Some elements, such as `img` and `input`, have no content and use a single self-closing tag.

Attributes are extra words inside the opening tag that change how the element behaves. They take the form `name="value"`, and their order does not matter. A few attributes are boolean: you just write the word (for example `required` or `checked`) with a space around it and give it no value.

An `id` attribute identifies one specific element, so its value must be unique across the whole page.

Comments let me leave messages for myself without changing what the browser shows. Anything inside one is inactive:

```html
<!-- TODO: Add link to cat photos -->
```

When elements sit inside other elements this is called nesting. Nested elements are indented two spaces further than their parent, which keeps the code readable.

## Document structure

Every page starts with a doctype declaration so the browser follows industry-wide standards. The whole page lives inside the `html` element, and the `lang` attribute says which language the page is written in. All other elements are descendants of `html`.

```html
<!DOCTYPE html>
<html lang="en">
```

Inside `html` there are two parts. The `body` holds everything that is rendered on the page. The `head` holds information about the page. The `title` element in the head sets the text shown in the browser tab or title bar. A `meta` tag with `charset="UTF-8"` tells the browser which character encoding to use.

```html
<head>
  <meta charset="UTF-8">
  <title>CatPhotoApp</title>
</head>
```

## Headings and paragraphs

The `h1` to `h6` elements show how important the content below them is. A lower number means higher importance, so `h2` ranks under `h1`. A page should have only one `h1`, and lower-ranked headings go beneath higher ones. Adding a lower-ranked heading such as an `h3` after an `h2` implies a new subsection.

```html
<h1>CatPhotoApp</h1>
<h2>Cat Photos</h2>
```

The `p` element makes a paragraph of text.

```html
<p>See more cat photos in our gallery.</p>
```

## Text emphasis

The `em` element emphasizes a word, and `strong` marks text as strongly important or urgent.

```html
<figcaption>Cats <em>love</em> lasagna.</figcaption>
<figcaption>Cats <strong>hate</strong> other cats.</figcaption>
```

## Images

An `img` element embeds an image and has no closing tag. Its `src` attribute is the image URL. By itself, an empty `img` shows nothing.

Every image should also have an `alt` attribute. Screen readers read it out, and it is displayed if the image fails to load.

```html
<img src="https://example.com/cat.jpg" alt="A cute orange cat lying on its back.">
```

## Links

The anchor element `a` links to another page, and `href` holds the destination. The text between the opening and closing tags becomes the clickable link text. An anchor with no text shows nothing.

```html
<a href="https://freecatphotoapp.com">link to cat pictures</a>
```

Anchors can wrap just a few words inside a larger element, so a single phrase in a paragraph can become the link. That made my separate link below the paragraph redundant, so I deleted it.

Setting `target="_blank"` on the anchor opens the link in a new tab.

```html
<p>See more <a target="_blank" href="https://freecatphotoapp.com">cat photos</a> in our gallery.</p>
```

Other content can be a link too, not just text. Wrapping an image in an anchor makes the image clickable.

```html
<a href="https://freecatphotoapp.com"><img src="https://example.com/cat.jpg" alt="A cute orange cat lying on its back."></a>
```

## Semantic grouping

HTML5 has elements that label the areas of a page. They make the markup easier to read and help with search engine optimization (SEO) and accessibility.

`main` marks the main content of the page. I put the `h1`, `h2`, comment and `p` inside it, which is the nesting described above.

```html
<main>
  <h1>CatPhotoApp</h1>
</main>
```

`section` splits the content into thematic parts. I wrapped the cat photos content in one before adding more content, then added a second and a third section below it for the lists and the form. Each section starts with its own `h2`.

```html
<section>
  <h2>Cat Lists</h2>
</section>
```

`footer` goes after `main` and holds closing information for the page. Mine has a paragraph with a link in it.

```html
<footer>
  <p>No Copyright - <a href="https://www.freecodecamp.org">freeCodeCamp.org</a></p>
</footer>
```

## Figures and captions

`figure` represents self-contained content, such as an image, and lets me associate it with a caption. The caption goes in a `figcaption` element, placed after the image inside the figure.

```html
<figure>
  <img src="https://example.com/lasagna.jpg" alt="A slice of lasagna on a plate.">
  <figcaption>Cats <em>love</em> lasagna.</figcaption>
</figure>
```

## Lists

An unordered list is a `ul`, and each item inside it is an `li` (list item). On its own an empty `ul` shows nothing. Items appear with bullet points.

```html
<ul>
  <li>cat nip</li>
  <li>laser pointers</li>
  <li>lasagna</li>
</ul>
```

An ordered list `ol` is written the same way, but its items are numbered when displayed.

```html
<ol>
  <li>flea treatment</li>
  <li>thunder</li>
  <li>other cats</li>
</ol>
```

I used these under `h3` headings, with a figure placed after each list.

## Forms

A `form` element collects information from users. Its `action` attribute says where the form data gets sent.

```html
<form action="https://freecatphotoapp.com/submit-cat-photo"></form>
```

### Text inputs

The `input` element collects data in several ways and, like `img`, is self-closing. The `type` attribute picks the kind of input, for example `text`, `password`, `radio`, `checkbox`, or a file picker. A `type="text"` input creates a text field.

For the data to reach the location in `action`, the field needs a `name` attribute that labels the value being submitted. `placeholder` shows a hint about what to enter, and the boolean `required` attribute stops the form being submitted while the field is empty.

```html
<input type="text" name="catphotourl" placeholder="cat photo URL" required>
```

### Buttons

The `button` element makes a clickable button. With no attributes, clicking it submits the form to the `action` location. I still add `type="submit"` so the intent is explicit instead of relying on defaults.

```html
<button type="submit">Submit</button>
```

Inputs and buttons are inline elements, so they sit next to each other rather than on separate lines, even when written on separate lines in the source.

### Radio buttons

Radio buttons suit questions where only one answer is allowed out of several options.

```html
<input type="radio"> Indoor
```

To make only one button in a group selectable, every radio button in the group must share the same `name` value. Otherwise both can be selected at once.

Submitted form data is built from `name` and `value`. Without a `value`, the data just says something like `indoor-outdoor=on`, which tells me nothing when there are several buttons. So I give each radio button a `value`, conveniently the same as its `id`.

### Labels

A `label` ties an input to its text, which helps assistive technology and makes clicking the text select the input. There are two ways. One is wrapping the input and its text in the label:

```html
<label><input id="indoor" type="radio" name="indoor-outdoor" value="indoor"> Indoor</label>
```

The other is to wrap only the text in a label and give it a `for` attribute that matches the input's `id`:

```html
<input id="loving" type="checkbox"> <label for="loving">Loving</label>
```

### Checkboxes

Checkboxes are for questions that can have more than one answer. They are created with `type="checkbox"`. Related checkboxes share one `name` (here `personality`), which makes it easier for a server to process them, and each gets its own `id`, `for` label and `value`. As with radio buttons, `value` is optional but good practice.

```html
<input id="lazy" type="checkbox" name="personality" value="lazy"> <label for="lazy">Lazy</label>
```

### Default selection

The boolean `checked` attribute makes a checkbox or radio button selected by default. I used it on the first radio button and the first checkbox.

### Grouping inputs

`fieldset` groups related inputs and labels. It is a block-level element, so it starts on a new line. Its `legend` is a caption that explains what the group is asking.

```html
<fieldset>
  <legend>What's your cat's personality?</legend>
</fieldset>
```

## Complete result

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <title>CatPhotoApp</title>
  </head>
  <body>
    <main>
      <h1>CatPhotoApp</h1>

      <section>
        <h2>Cat Photos</h2>
        <!-- TODO: Add link to cat photos -->
        <p>See more <a target="_blank" href="https://freecatphotoapp.com">cat photos</a> in our gallery.</p>
        <a href="https://freecatphotoapp.com"><img src="https://example.com/cat.jpg" alt="A cute orange cat lying on its back."></a>
      </section>

      <section>
        <h2>Cat Lists</h2>
        <h3>Things cats love:</h3>
        <ul>
          <li>cat nip</li>
          <li>laser pointers</li>
          <li>lasagna</li>
        </ul>
        <figure>
          <img src="https://example.com/lasagna.jpg" alt="A slice of lasagna on a plate.">
          <figcaption>Cats <em>love</em> lasagna.</figcaption>
        </figure>
        <h3>Top 3 things cats hate:</h3>
        <ol>
          <li>flea treatment</li>
          <li>thunder</li>
          <li>other cats</li>
        </ol>
        <figure>
          <img src="https://example.com/cats.jpg" alt="Five cats looking around a field.">
          <figcaption>Cats <strong>hate</strong> other cats.</figcaption>
        </figure>
      </section>

      <section>
        <h2>Cat Form</h2>
        <form action="https://freecatphotoapp.com/submit-cat-photo">
          <fieldset>
            <legend>Is your cat an indoor or outdoor cat?</legend>
            <label><input id="indoor" type="radio" name="indoor-outdoor" value="indoor" checked> Indoor</label>
            <label><input id="outdoor" type="radio" name="indoor-outdoor" value="outdoor"> Outdoor</label>
          </fieldset>
          <fieldset>
            <legend>What's your cat's personality?</legend>
            <input id="loving" type="checkbox" name="personality" value="loving" checked> <label for="loving">Loving</label>
            <input id="lazy" type="checkbox" name="personality" value="lazy"> <label for="lazy">Lazy</label>
            <input id="energetic" type="checkbox" name="personality" value="energetic"> <label for="energetic">Energetic</label>
          </fieldset>
          <input type="text" name="catphotourl" placeholder="cat photo URL" required>
          <button type="submit">Submit</button>
        </form>
      </section>
    </main>

    <footer>
      <p>No Copyright - <a href="https://www.freecodecamp.org">freeCodeCamp.org</a></p>
    </footer>
  </body>
</html>
```

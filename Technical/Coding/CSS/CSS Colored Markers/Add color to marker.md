11. One way to add color to an element is to use a *color* *keyword*, like `black,cyan, or yellow`.
Here's how to target the class `freecodecamp`: 
![[Pasted image 20230621220540.png]]
```css
.marker {
  background-color: red;
}
```

12. Since the marker `div` element has no content in it, it doesn't have any height by default.
In your `.marker` CSS rule, set the `height` property to `25px` and the `width` property to `200px`.
```css
.marker {
  background-color: red;
  height: 25px;
  width: 200px;
}
```

13. Your marker would look better if it was centered on the page. An easy way to do that is with the `margin` shorthand property.

In the last project, you set the margin area of elements separately with properties like `margin-top` and `margin-left`. The `margin` shorthand property makes it easy to set multiple margin areas at the same time.

**To center your marker on the page, set its `margin` property to `auto`. This sets `margin-top`, `margin-right`, `margin-bottom`, and `margin-left` all to `auto`.**

```css
.marker {
  width: 200px;
  height: 25px;
  background-color: red;
  margin: auto;
}
```
14. Now that you've made one marker centered with color, time to add other markers.
In the `container div`, add two more div elements and give them each a class of `marker`.
```html
    <div class="container">
      <div class="marker"> </div>
        <div class="marker"> </div>
          <div class="marker"> </div>
</div>
```

15. While you have three separate marker `div` elements, they look like one big rectangle. You should add some space between them to make it easier to see each element.

When the shorthand `margin` property has two values, it sets `margin-top` and `margin-bottom` to the first value, and `margin-left` and `margin-right` to the second value.

In your `.marker` CSS rule, set the `margin` property to `10px auto`.
```css
.marker {
  width: 200px;
  height: 25px;
  background-color: red;
  margin: 10px auto;
}
```

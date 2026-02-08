8. As a reminder, here's how to target a paragraph element and align it to the right:  [[Step 10,11]]
![[Pasted image 20230621215642.png]]
Create a new CSS rule that targets the `h1`, and set its `text-align` to center.
```css
h1 {
  text-align: center;
}
```

9. Now you'll add some elements that you'll eventually style into color markers.

First, within the `body` element, add a `div` element and set its `class` attribute to `container`. Make sure the `div` element is below the `h1` element. 
```html
  <body>
    <h1>CSS Color Markers</h1>
    <div class="container"></div>
</body>
```

10. Next, within the div element, add another div element and give it a class of `marker`. 
```html
  <body>
    <h1>CSS Color Markers</h1>
    <div class="container"> <div class="marker"></div>
    </div>
</body>
```
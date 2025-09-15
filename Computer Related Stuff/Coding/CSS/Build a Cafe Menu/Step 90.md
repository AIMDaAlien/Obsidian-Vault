Add one last image under the `Desserts` heading using the url `https://cdn.freecodecamp.org/curriculum/css-cafe/pie.jpg`. Give the image an `alt` value of `pie icon`.
```html
<h2>Desserts</h2>
<img src="https://cdn.freecodecamp.org/curriculum/css-cafe/pie.jpg" alt="pie icon">
```


91. It would be nice if the vortical space between the `h2` and their associated icons was smaller. `h2` have default top and bottom margin space, so you could change the bottom margin of the `h2` elements to say 0 or another number. 

There's an easier way, simply add a negative top margin to the `img` elements to pull them up from their current positions. Negative values are created using a `-` in front of the value. To complete this project, use a negative top margin of `25px` in the `img` type selector.

```css
img {
  display: block;
  margin-left: auto;
  margin-right: auto;
  margin-top: -25px;
}
```




#Web
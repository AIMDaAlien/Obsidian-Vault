`label` elements are used to help associate the text for an `input` element with `input` itself (for assistive tech like screen readers). 
For example, `<label><input type="radio"> cat</label>` makes it so clicking the word `cat` also selects the corresponding radio button.

Nest your `radio` button inside a `label` element.

```html
<label> 
<input type="radio" name="location" value="indoor" checked> Indoor </label>
```

#Web
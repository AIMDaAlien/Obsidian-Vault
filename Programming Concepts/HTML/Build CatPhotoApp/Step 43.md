Even though you added your button below the text input, they appear next to each other on the page. That's because both `input` and `button` elements are *inline elements*, which don't appear on new lines. 

The button will submit the form by default. However, relying on default behavior might confuse. Add `type` attribute with the value `submit` to the button to make it clear that it is a submit button.

```html
<button type="submit">Submit</button>
```



#Web

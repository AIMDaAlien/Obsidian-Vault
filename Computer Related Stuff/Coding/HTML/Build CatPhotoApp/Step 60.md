Like radio buttons, form data for selected checkboxes are `name` / `value` attribute pairs. While the `value` attribute is optional, it's best practice to include it with any checkboxes or radio buttons on the page.

Add a `value` attribute to each checkbox. For convenience, set each checkbox's `value` attribute to the same value as its `id` attribute.

```html
          <fieldset>

            <legend>Is your cat an indoor or outdoor cat?</legend>

            <label><input id="indoor" type="radio" name="indoor-outdoor" value="indoor"> Indoor</label>

            <label><input id="outdoor" type="radio" name="indoor-outdoor" value="outdoor"> Outdoor</label>

          </fieldset>

          <fieldset>

            <legend>What's your cat's personality?</legend>

            <input id="loving" type="checkbox" name="personality" value="loving"> <label for="loving">Loving</label>

            <input id="lazy" type="checkbox" name="personality" value="lazy"> <label for="lazy">Lazy</label>

            <input id="energetic" type="checkbox" name="personality" value="energetic"> <label for="energetic"> Energetic</label>

          </fieldset>
```


#Web
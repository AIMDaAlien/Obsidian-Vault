In order to make a checkbox checked or radio button selected by default, you need to add the `checked` attribute to it. There's no need to set a value to the `checked` attribute. Instead, just add the word `checked` to the `input` element, making sure there is space between it and other attributes.

Make the first radio button and the first checkbox selected by default.

```html
         <fieldset>

            <legend>Is your cat an indoor or outdoor cat?</legend>

            <label><input id="indoor" type="radio" name="indoor-outdoor" value="indoor" checked> Indoor</label>

            <label><input id="outdoor" type="radio" name="indoor-outdoor" value="outdoor"> Outdoor</label>

          </fieldset>

          <fieldset>

            <legend>What's your cat's personality?</legend>

            <input id="loving" type="checkbox" name="personality" value="loving" checked> <label for="loving">Loving</label>

            <input id="lazy" type="checkbox" name="personality" value="lazy"> <label for="lazy">Lazy</label>

            <input id="energetic" type="checkbox" name="personality" value="energetic"> <label for="energetic"> Energetic</label>

          </fieldset>
```
![[Pasted image 20230616221435.png]]



#Web
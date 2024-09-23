/*
```javascript
*/
const firstone = ea.getViewSelectedElements()[0].y;
for (let i = 0; i < ea.getViewSelectedElements().length; i++) {
  console.log(ea.getViewSelectedElements()[i]);
  console.log(ea.getViewSelectedElements()[i].y);
  console.log(firstone);
  ea.getViewSelectedElements()[i].y = firstone;
}

const spacing = 1500;
const rectangles = ea.getViewSelectedElements()
for (let i = 0; i < rectangles.length - 1; i++) {
  const firstRectangle = rectangles[i];
  for (let j = i + 1; j < rectangles.length; j++) {
    const secondRectangle = rectangles[j];

    for (let k = secondRectangle.x; k < firstRectangle.x + firstRectangle.width; k = k + 1) {
      if (k + secondRectangle.width > firstRectangle.x) {
        secondRectangle.x = firstRectangle.x + firstRectangle.width + spacing;
        break;
      }
    }
  }
}

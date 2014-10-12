/**
 * Welcome to Pebble.js!
 *
 * This is where you write your app.
 */

var UI = require('ui');
var Vector2 = require('vector2');
var ajax = require('ajax');

var slide = 1;
var url = 'http://104.131.83.142';

var main = new UI.Card({
  title: 'Slidemaster',
  body: 'Slide ' + slide
});

main.show();

main.on('click', function(e) {
  slide += e.button == 'up' ? 1 : -1;
  main.body('Slide ' + slide);
  ajax(
    {
      url: url + (e.button == 'up' ? '/next' : '/previous')
    },
    function(data) {
      main.body('Slide ' + slide);
    }
  );
});

/*main.on('click', 'up', function(e) {
  var menu = new UI.Menu({
    sections: [{
      items: [{
        title: 'Pebble.js',
        icon: 'images/menu_icon.png',
        subtitle: 'Can do Menus'
      }, {
        title: 'Second Item',
        subtitle: 'Subtitle Text'
      }]
    }]
  });
  menu.on('select', function(e) {
    console.log('Selected item #' + e.itemIndex + ' of section #' + e.sectionIndex);
    console.log('The item is titled "' + e.item.title + '"');
  });
  menu.show();
});*/

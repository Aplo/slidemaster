/**
 * Welcome to Pebble.js!
 *
 * This is where you write your app.
 */

var UI = require('ui');
var Vector2 = require('vector2');
var ajax = require('ajax');

var slide = 1;
var url = 'http://sm.aplo.io';

/*var main = new UI.Card({
  title: 'Slidemaster',
  body: 'Slide ' + slide
});

main.show();*/

var main = new UI.Menu();

var titles = [];
var ids = [];
ajax(
  {
    url: url + '/files',
    type: 'json'
  },
  function(data) {
    for (var i = 0; i < data.items.length; i++) {
      if (data.items[i].mimeType == 'application/vnd.google-apps.presentation') {
        var title = data.items[i].title;
        titles.push({
          title: title,
        });
        ids.push(data.items[i].id);
      }
    }
    main = new UI.Menu({
      sections: [{
        items: titles
      }]
    });
    
    main.on('select', function(e) {
      console.log(titles[e.itemIndex].title);
      var uid = Math.random().toString(36).substr(2, 4);
      var sid = ids[e.itemIndex];
      var card = new UI.Card({
        title: titles[e.itemIndex].title,
        body: 'id: ' + uid + '\nSlide 1'
      });
      ajax(
        {
          url: url + '/create?uid=' + uid + '&sid=' + sid
        }
      );
      card.show();
    });
    
    main.show();
  }
);

/*main.on('click', function(e) {
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
});*/

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

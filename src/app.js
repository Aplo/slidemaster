/**
 * Welcome to Pebble.js!
 *
 * This is where you write your app.
 */

var UI = require('ui');
var Vector2 = require('vector2');
var ajax = require('ajax');

var url = 'http://sm.aplo.io';

var splash = new UI.Window();
var textfield = new UI.Text({
  position: new Vector2(0, 50),
  size: new Vector2(144, 30),
  font: 'gothic-24-bold',
  text: 'Loading...',
  textAlign: 'center'
});
splash.add(textfield);
splash.show();

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
      var slide = 1;
      
      console.log(titles[e.itemIndex].title);
      var uid = Math.random().toString(36).substr(2, 4);
      var sid = ids[e.itemIndex];
      var card = new UI.Card({
        title: titles[e.itemIndex].title,
        body: 'id: ' + uid + '\nSlide: 1'
      });
      ajax(
        {
          url: url + '/create?uid=' + uid + '&sid=' + sid
        }
      );
      
      card.on('click', function(ev) {
        if (ev.button == 'up') {
          slide += 1;
        } else if (ev.button == 'select') {
          slide = 1;
        } else if (ev.button == 'select') {
          slide -= 1;
        }
        
        card.body('id: ' + uid + '\nSlide: ' + slide);
        ajax(
          {
            url: url + '/page?uid=' + uid + '&page=' + slide
          }
        );
      });
      
      card.show();
    });
    
    main.show();
    splash.hide();
  }
);

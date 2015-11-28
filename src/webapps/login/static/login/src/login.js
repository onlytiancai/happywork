define(function(require, exports, module) {
    var Backbone = require('backbone');
    var Router = require('./router')

    var init = function(container){
        new Router({container:container});
        Backbone.history.start();
    };

    module.exports = {init: init};

});

define(function(require, exports, module) {
    var Backbone = require('backbone');
    var Cookie = require('cookie');
    var login_view = require('./views/login_view');
    var user_view = require('./views/user_view');

    var router = Backbone.Router.extend({
        initialize: function(option){
            this.container = option.container;
        },
        routes: {
            '': 'index',
        },
        index: function(){
            if (Cookie.get("sessionid") == undefined){
                this.container.html(new login_view().el);
            }else{
                this.container.html(new user_view().el);
            }
        }
    });

    module.exports = router;
});

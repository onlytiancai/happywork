define(function(require, exports, module) {
    var tpl = require('../templates/user.tpl');
    var alert_tpl = require('../templates/alert.tpl');
    var Backbone = require('backbone'),
        Mustache = require('mustache'),
        _ = require('underscore'),
        $ = require('jquery');

    var showmessage = function(message){
        $('.show-message').append(Mustache.render(alert_tpl, {message: message}));
    };

    var view = Backbone.View.extend({
        events: {
            "click .btn-logout": "logout"
        },
        initialize: function(options){
            _.bindAll(this, 'render');
            _.bindAll(this, 'logout');
            var that = this;
            $.getJSON('userinfo', function(result){
                that.model = result.data;
                that.render(); 
            });
        },
        render: function(){
            $(this.el).html(Mustache.render(tpl, this.model));
            return this;
        },
        logout: function(e){
            var that = this;
            $.ajax({
                type: 'POST',
                dataType: 'json',
                url: 'logout',
                success: function(result){
                    if (result.code == 200) {
                        location.reload();
                    }else{
                        showmessage([result.code, ':', result.message].join(''));
                    }
                },
                error: function(xhr, ajaxOpt, error){
                    showmessage([xhr.status, ':', error, '\r\n'].join(''));
                }
            }); 
        }
    });

    module.exports = view;
});

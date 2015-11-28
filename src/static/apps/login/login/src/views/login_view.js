define(function(require, exports, module) {
    require('./login.css');

    var tpl = require('../templates/login.tpl');
    var alert_tpl = require('../templates/alert.tpl');
    var Backbone = require('backbone'),
        Mustache = require('mustache'),
        _ = require('underscore'),
        $ = require('jquery');

    var showmessage = function(message){
        $('.show-message').html(Mustache.render(alert_tpl, {message: message}));
    };


    var view = Backbone.View.extend({
        events: {
            "click .btn-login": "login",
        },
        initialize: function(options){
            _.bindAll(this, 'render');
            _.bindAll(this, 'login');
            var that = this;
            this.render();
        },
        render: function(){
            $(this.el).html(Mustache.render(tpl, this.model));
            return this;
        },
        login: function(e){
            var that = this;
            $.ajax({
                type: 'POST',
                dataType: 'json',
                url: 'login',
                data: $('.form-signin').serializeArray(),
                success: function(result){
                    if (result.code == 200) {
                        location.href = '/';
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

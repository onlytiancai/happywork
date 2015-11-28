define("#luffy/1.0.0/router-debug", ["./views/operators_view-debug", "./views/apps_view-debug", "./views/hosts_view-debug", "./views/tasks_view-debug", "backbone-debug", "mustache-debug", "underscore-debug", "jquery-debug"], function(require, exports, module) {
    var Backbone = require('backbone-debug');
    var operators_view = require('./views/operators_view-debug');
    var apps_view = require('./views/apps_view-debug');
    var hosts_view = require('./views/hosts_view-debug');
    var tasks_view = require('./views/tasks_view-debug');

    var router = Backbone.Router.extend({
        initialize: function(option){
            this.container = option.container;
        },
        routes: {
            '': 'operators',
            'operators': 'operators',
            'apps/:operator': 'apps',
            'hosts/:operator/:app': 'hosts',
            'tasks/:operator/:app/:hosts': 'tasks',
        },
        operators: function(){
            this.container.html(new operators_view().el);
        },
        apps: function(operator){
            this.container.html(new apps_view({operator:operator}).el);
        },
        hosts: function(operator, app){
            this.container.html(new hosts_view({operator: operator, app: app}).el);
        },
        tasks: function(operator, app, hosts){
            this.container.html(new tasks_view({operator: operator, app: app, hosts:hosts}).el);
        }
    });

    module.exports = router;
});

define("#luffy/1.0.0/views/operators_view-debug", ["backbone-debug", "mustache-debug", "underscore-debug", "jquery-debug"], function(require, exports, module) {
    var tpl = '<h3>请选择您要执行的操作</h3> {{#operators}} <h5>{{group}}</h5> <ul> {{#operators}} <li><a href="javascript:void(0)" operator="{{name}}">{{description}}</a></li> {{/operators}} </ul> {{/operators}}';
    var Backbone = require('backbone-debug'),
        Mustache = require('mustache-debug'),
        _ = require('underscore-debug'),
        $ = require('jquery-debug');


    var view = Backbone.View.extend({
        events: {
            "click ul li a": "next_step",
        },
        initialize: function(){
            _.bindAll(this, 'render');
            var that = this;

            $.getJSON('luffy_config', function(data){
                that.model = data;
                that.render();
            }); 
        },
        render: function(){
            $(this.el).html(Mustache.render(tpl, this.model));
            return this;
        },
        next_step: function(e){
            location.href = '#/apps/'+$(e.target).attr('operator'); 
        }
    });

    module.exports = view;
});

define("#luffy/1.0.0/views/apps_view-debug", ["backbone-debug", "mustache-debug", "underscore-debug", "jquery-debug"], function(require, exports, module) {
    var tpl = '<h3>请选择要操作的应用</h3> <ul> {{#apps}} <li><a href="javascript:void(0)">{{.}}</a></li> {{/apps}} </ul> <button type="button" class="btn back">上一步</button>';
    var Backbone = require('backbone-debug'),
        Mustache = require('mustache-debug'),
        _ = require('underscore-debug'),
        $ = require('jquery-debug');


    var view = Backbone.View.extend({
        events: {
            "click ul li a": "next_step",
            "click .back": "goback",
        },
        initialize: function(options){
            this.operator = options.operator;

            _.bindAll(this, 'render');
            _.bindAll(this, 'next_step');

            var that = this;

            $.getJSON('luffy_config', function(data){
                that.model = data;
                that.render();
            }); 
        },
        render: function(){
            $(this.el).html(Mustache.render(tpl, this.model));
            return this;
        },
        next_step: function(e){
            location.href = '#/hosts/' + this.operator + '/' + $(e.target).text(); 
        },
        goback: function(){
            history.back();
        }
    });

    module.exports = view;
});

define("#luffy/1.0.0/views/hosts_view-debug", ["backbone-debug", "mustache-debug", "underscore-debug", "jquery-debug"], function(require, exports, module) {
    var tpl = '<h3>请选择主机</h3> <div class="alert hide"> <button type="button" class="close" data-dismiss="alert">×</button> <span></span> </div> {{#hosts}} <label class="checkbox"><input type="checkbox" value="{{ip}}">{{name}}:{{ip}}</label> {{/hosts}} <button type="button" class="btn back">上一步</button> <button type="button" class="btn next btn-primary">下一步</button>';
    var Backbone = require('backbone-debug'),
        Mustache = require('mustache-debug'),
        _ = require('underscore-debug'),
        $ = require('jquery-debug');


    var view = Backbone.View.extend({
        events: {
            "click .next": "next_step",
            "click .back": "goback",
        },
        initialize: function(options){
            this.operator = options.operator;
            this.app = options.app;

            _.bindAll(this, 'render');
            _.bindAll(this, 'next_step');

            var that = this;

            $.getJSON('luffy_config', function(data){
                that.model = data;
                that.render();
            }); 
        },
        render: function(){
            $(this.el).html(Mustache.render(tpl, this.model));
            return this;
        },
        next_step: function(e){
            var hosts = [];
            $('input:checked').each(function(){
                hosts.push($(this).val());
            });
            if(hosts.length < 1){
                this.$('.alert span').html('请选择主机。')
                this.$('.alert').show();
                return;
            }
            location.href = '#/tasks/' + this.operator + '/' + this.app +'/'+ hosts.join(','); 
        },
        goback: function(){
            history.back();
        }
    });

    module.exports = view;
});

define("#luffy/1.0.0/views/tasks_view-debug", ["backbone-debug", "mustache-debug", "underscore-debug", "jquery-debug"], function(require, exports, module) {
    var tpl = '<h3>请确认操作</h3> <ul> <li>执行操作：{{operator}}</li> <li>进行操作的应用：{{app}}</li> <li>进行操作的主机：{{#hosts}}{{.}}, {{/hosts}}</li> <li>其它参数：<input class="other_args" type="text"/></li> </ul> <button type="button" class="btn back">上一步</button> <button type="button" class="btn next btn-primary">确认执行</button> <pre class="results"></pre>';
    var Backbone = require('backbone-debug'),
        Mustache = require('mustache-debug'),
        _ = require('underscore-debug'),
        $ = require('jquery-debug');


    var view = Backbone.View.extend({
        events: {
            "click .next": "excute",
            "click .back": "goback",
        },
        initialize: function(options){
            this.model = options;
            this.model.hosts = this.model.hosts.split(',');

            _.bindAll(this, 'render');
            _.bindAll(this, 'excute');

            this.render()

        },
        render: function(){
            $(this.el).html(Mustache.render(tpl, this.model));
            return this;
        },
        excute: function(e){
            var that = this;
            that.$('.results').empty();
            _.each(this.model.hosts, function(host){
                var url = 'run/' + host + '/' + that.model.operator;
                var args = [that.model.app];
                var other_args = this.$('.other_args').val();
                if (other_args)
                    args.push(other_args)
                args = {args: args.join(',')};
                $.post(url, args, function(result){
                    that.$('.results').append(result);
                }); 
            });
        },
        goback: function(){
            history.back();
        }
    });

    module.exports = view;
});

define("#luffy/1.0.0/luffy-debug", ["./router-debug", "./views/operators_view-debug", "./views/apps_view-debug", "./views/hosts_view-debug", "./views/tasks_view-debug", "backbone-debug", "mustache-debug", "underscore-debug", "jquery-debug"], function(require, exports, module) {
    var Backbone = require('backbone-debug');
    var Router = require('./router-debug')

    var init = function(container){
        new Router({container:container});
        Backbone.history.start();
    };

    Luffy = {init: init}
    module.exports = Luffy;

});

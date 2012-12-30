define(function(require, exports, module) {
    var Backbone = require('backbone');
    var _ = require('underscore');
    var moment = require('moment');
    var Cookie = require('cookie');
    require('./moment-zh-cn.js');
    
    moment.lang('zh-cn');

    var tpl = require('./index.html');
    $('.main-body').html(tpl);

    require('./bootstrap-datepicker/js/bootstrap-datepicker.js')
    require('./bootstrap-datepicker/js/locales/bootstrap-datepicker.zh-CN.js')
    require('./bootstrap-datepicker/css/datepicker.css')

    $('body').click(function(){
        $("a[rel=popover]") .popover('hide');
    });
    

    // An example Backbone application contributed by
    // [Jérôme Gravel-Niquet](http://jgn.me/). This demo uses a simple
    // [LocalStorage adapter](backbone-localstorage.js)
    // to persist Backbone models within your browser.

    // Load the application once the DOM is ready, using `jQuery.ready`:
    $(function(){
        var message_template = _.template($('#message-template').html());
        var show_message = function(type, message){
            var model = {type: type, message: message};
            $('.message-container').append(message_template(model));
        };

        if (Cookie.get('sessionid') == undefined){
            show_message('alert', '您正在使用演示版，所有数据将公开现实，登陆后才能保存自己的待办信息。');
        }
        // Todo Model
        // ----------

        // Our basic **Todo** model has `title`, `order`, and `done` attributes.
        var Todo = Backbone.Model.extend({

            // Default attributes for the todo item.
            defaults: function() {
                return {
                    title: "empty todo...",
                    order: Todos.nextOrder(),
                    done: false,
                    archived: false
               };
            },

            // Ensure that each todo created has `title`.
            initialize: function() {
                if (!this.get("title")) {
                    this.set({"title": this.defaults.title});
                }
            },

            // Toggle the `done` state of this todo item.
            toggle: function() {
                var done = !this.get("done"); 
                if (done){
                    var archivetime = moment().day(1).format("YYYY-MM-DD");
                    var donetime = moment().format("YYYY-MM-DD HH:mm:ss");
                    this.save({done: done, donetime: donetime,archived: true, archivetime:archivetime});
                }else{
                    this.save({done: done, archived: false});
                }
            },
            setStart: function(){
                var starttime = moment().local().format("YYYY-MM-DD HH:mm:ss");
                this.save({started: true, starttime: starttime});
            },
            setdeadline: function(date){
                var deadlinetime= moment(date).local().hours(0).minutes(0).format("YYYY-MM-DD HH:mm:ss");
                this.save({deadlinetime: deadlinetime});
            },


            // Remove this Todo from *localStorage* and delete its view.
            clear: function() {
                this.destroy();
            }
        });

        // Todo Collection
        // ---------------

        // The collection of todos is backed by *localStorage* instead of a remote
        // server.
        var TodoList = Backbone.Collection.extend({

            // Reference to this collection's model.
            model: Todo,

            // Save all of the todo items under the `"todos"` namespace.
            //localStorage: new Store("todos-backbone"),
            url: 'todos',

            // Filter down the list of all todo items that are finished.
            done: function() {
                return this.filter(function(todo){ return todo.get('done') });
            },

            // Filter down the list to only todo items that are still not finished.
            remaining: function() {
                return this.without.apply(this, this.done());
            },

            // We keep the Todos in sequential order, despite being saved by unordered
            // GUID in the database. This generates the next order number for new items.
            nextOrder: function() {
                if (!this.length) return 1;
                return this.last().get('order') + 1;
            },

            // Todos are sorted by their original insertion order.
            comparator: function(todo) {
                return todo.get('order');
            }

        });

        // Create our global collection of **Todos**.
        var Todos = new TodoList;

        // Todo Item View
        // --------------

        // The DOM element for a todo item...
        var TodoView = Backbone.View.extend({

            //... is a list tag.
            tagName:  "li",

            // Cache the template function for a single item.
            template: _.template($('#item-template').html()),

            // The DOM events specific to an item.
            events: {
                "click .toggle"   : "toggleDone",
                "dblclick .view"  : "edit",
                "click a.destroy" : "clear",
                "click a.setstart" : "setstart",
                "click a.setdeadline" : "showdatepicker",
                "keypress .edit"  : "updateOnEnter",
                "blur .edit"      : "close",
                "click .operation": "operation",
                "click .popover": "stopPropagation",
                "changeDate .setdeadline": "setdeadline"
            },

            // The TodoView listens for changes to its model, re-rendering. Since there's
            // a one-to-one correspondence between a **Todo** and a **TodoView** in this
            // app, we set a direct reference on the model for convenience.
            initialize: function() {
                this.model.bind('change', this.render, this);
                this.model.bind('change:archived', this.remove, this);
                this.model.bind('destroy', this.remove, this);
            },
            operation: function(e){
                $("a[rel=popover]").each(function(){
                    if (e.target != this)
                        $(this).popover('hide');
                });

                this.$('.setdeadline').datepicker({language:'zh-CN', todayBtn: 'linked'});
                e.preventDefault();
                e.stopPropagation();
            },
            setstart: function(){
                this.model.setStart();
            },
            showdatepicker: function(e){
                e.preventDefault();
            },
            setdeadline: function(ev){
                $(ev.target).datepicker('hide');
                this.model.setdeadline(ev.date);
            },
            stopPropagation: function(e){
                e.stopPropagation();
            },

            // Re-render the titles of the todo item.
            render: function() {
                var model = this.model.toJSON();
                model.statusline =  '';
                if (model.done){
                    model.statusline =  '完成于' + moment(model.donetime, 'YYYY-MM-DD HH:mm:ss').fromNow();
                }else if (model.deadlinetime){
                    model.statusline =  '最后期限是' + moment(model.deadlinetime, 'YYYY-MM-DD HH:mm:ss').format('L');
                }else if (model.started){
                    model.statusline =  '已经开始了' + moment(model.starttime, 'YYYY-MM-DD HH:mm:ss').fromNow().replace('前','');
                }else{
                    if (model.createtime){
                        model.statusline =  '创建于' + moment(model.createtime, 'YYYY-MM-DD HH:mm:ss').fromNow();
                    }
                }
                model.deadlinetime = model.deadlinetime ? moment(model.deadlinetime, 'YYYY-MM-DD HH:mm:ss').format('YYYY-MM-DD') : moment().format('YYYY-MM-DD');
                model.show_archived = app.show_archived;
                this.$el.html(this.template(model));
                this.$el.toggleClass('done', this.model.get('done'));
                this.input = this.$('.edit');
                return this;
            },

            // Toggle the `"done"` state of the model.
            toggleDone: function() {
                this.model.toggle();
            },

            // Switch this view into `"editing"` mode, displaying the input field.
            edit: function() {
                this.$el.addClass("editing");
                this.input.focus();
            },

            // Close the `"editing"` mode, saving changes to the todo.
            close: function() {
                var value = this.input.val();
                if (!value) this.clear();
                this.model.save({title: value});
                this.$el.removeClass("editing");
            },

            // If you hit `enter`, we're through editing the item.
            updateOnEnter: function(e) {
                if (e.keyCode == 13) this.close();
            },

            // Remove the item, destroy the model.
            clear: function() {
                this.model.clear();
            },

            

        });

        // The Application
        // ---------------

        // Our overall **AppView** is the top-level piece of UI.
        var AppView = Backbone.View.extend({

            // Instead of generating a new element, bind to the existing skeleton of
            // the App already present in the HTML.
            el: $("#todoapp"),

            // Our template for the line of statistics at the bottom of the app.
            statsTemplate: _.template($('#stats-template').html()),
            navTemplate: _.template($('#todo-nav-template').html()),

            // Delegated events for creating new items, and clearing completed ones.
            events: {
                "keypress #new-todo":  "createOnEnter",
                "click .archived-bar .thisweek": "thisweek_archived",
                "click .archived-bar .preweek": "preweek_archived",
                "click .archived-bar .nextweek": "nextweek_archived"
            },

            // At initialization we bind to the relevant events on the `Todos`
            // collection, when items are added or changed. Kick things off by
            // loading any preexisting todos that might be saved in *localStorage*.
            initialize: function(options) {
                this.input = this.$("#new-todo");

                Todos.bind('add', this.addOne, this);
                Todos.bind('reset', this.addAll, this);
                Todos.bind('all', this.render, this);
                Todos.bind('remove', this.render, this);

                this.footer = this.$('footer');
                this.main = $('#main');

            },
            thisweek_archived: function(){
                var day = moment().day(1).format("YYYY-MM-DD");
                location.href = '#tag/' + this.tag + '/archived/' + day;
            },
            preweek_archived: function(){
                var day = moment(this.day).subtract('w', 1).format("YYYY-MM-DD");
                location.href = '#tag/' + this.tag + '/archived/' + day;
            },
            nextweek_archived: function(){
                var day = moment(this.day).add('w', 1).format("YYYY-MM-DD");
                location.href = '#tag/' + this.tag + '/archived/' + day;
            },

            // Re-rendering the App just means refreshing the statistics -- the rest
            // of the app doesn't change.
            render: function() {
                var done = Todos.done().length;
                var remaining = Todos.remaining().length;

                $('.todo-nav').html(this.navTemplate({tag: app.tag, archived:app.show_archived}));
                if (app.show_archived){
                    $('#new-todo').hide();
                    $('.archived-bar').show();
                }else{
                    $('#new-todo').show();
                    $('.archived-bar').hide();
                }

                
                if (!this.show_archived){
                    $('.todo-info').html('您正在查看当前的待办事项');
                }else{
                    $('.todo-info').html('您正在查看('+this.day+')这周的已完成事项');
                    this.footer.hide();
                }

                if (Todos.length) {
                    this.main.show();
                    if (!this.show_archived){
                        this.footer.show();
                        this.footer.html(this.statsTemplate({done: done, remaining: remaining}));
                    }
                } else {
                    this.main.hide();
                    this.footer.hide();
                }

                $("a[rel=popover]").popover({html: true});
            },

            // Add a single todo item to the list by creating a view for it, and
            // appending its element to the `<ul>`.
            addOne: function(todo) {
                var view = new TodoView({model: todo});
                this.$("#todo-list").append(view.render().el);
            },

            // Add all items in the **Todos** collection at once.
            addAll: function() {
                this.$("#todo-list").empty();
                Todos.each(this.addOne);
            },

            // If you hit return in the main input field, create new **Todo** model,
            // persisting it to *localStorage*.
            createOnEnter: function(e) {
                if (e.keyCode != 13) return;
                if (!this.input.val()) return;

                Todos.create({title: this.input.val(), tag: this.tag, createtime:null, donetime:null, started:false});
                this.input.val('');
            },

        });

        var TagList = Backbone.Collection.extend({
            url: 'tags'
        });

        var Tags = new TagList();

        var TagsView = Backbone.View.extend({
            el: $(".todo-tags"),
            events: {
                "keypress .new-tag":  "newTag"
            },
            initialize: function(options) {
                Tags.bind('all', this.render, this);
                Tags.fetch();
            },
            newTag: function(e){
                if (e.keyCode != 13) return;
                Tags.create({tag:this.$('.new-tag').val()});
                this.$('.new-tag').val('');
            },
            render: function(){
                $(this.$('.nav-list')).empty();
                $(this.$('.nav-list')).append('<li class="nav-header">待办分类</li>');
                $(this.$('.nav-list')).append('<li  '+ ('all' == app.tag ? 'class="active"' : '') +'><a href="#tag/all">全部</a></li>');
                Tags.each(function(tag){
                    tag = tag.get('tag');
                    $(this.$('.nav-list')).append('<li '+ (tag == app.tag ? 'class="active"' : '') +'><a class="tag" href="#tag/'+tag+'">'+tag+'</a></li>');
                });
            }
        });
        
        var tagsView = new TagsView();
        var app = new AppView();
        var Router = Backbone.Router.extend({
            routes: {
                '': 'index',
                'tag/:tag': 'index',
                'tag/:tag/archived': 'archived',
                'tag/:tag/archived/:day': 'archived'
            },
            index: function(tag){
                tag = tag || 'all'
                app.tag = tag;
                app.show_archived = false;
                tagsView.render();

                var args = {archived:0};
                if (tag != 'all') args.tag = tag;
                Todos.fetch({data: args});
            },
            archived: function(tag, day){
                tag = tag || 'all';
                day = day ||  moment().day(1).format("YYYY-MM-DD")
                app.tag = tag;
                app.day = day;
                app.show_archived = true;
                tagsView.render();

                var args = {archived: 1, archivetime: day};
                if (tag != 'all') args.tag = tag;
                Todos.fetch({data: args});
            }
        });

        new Router();
        Backbone.history.start();
    });
});

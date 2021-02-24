Vue.component('item-list', {
    delimiters: ["[[", "]]"],
    props: ['board', 'render', 'del_board'],
    template: "<div class='item'><h3>[[board.title]]</h3><p class='content'>[[board.content]]</p><button class='edit' v-on:click.self='render(board.title, board.content)'>Edit</button><button class='delete' v-on:click.self='del_board(board.title)'>Delete</button></div>"
});

var list = new Vue({
    delimiters: ["[[", "]]"],
    el: "#list",
    data: {
        Boards: JSON.parse('{{values|safe}}')
    },
    methods:{
        render: function render(title, content){
            var data = [];
            lines = content.split("/c");
            for(var i = 0; i < lines.length-1; i++){
                var dict = {};
                dict["id"] = i;
                dict["text"] = lines[i];
                data.push(dict);
            }
            axios.post('/resume', {
    title: title, content: data}).then(response => window.location.href = "{{url_for('main')}}");
    },
    del_board: function del_board(title){
        axios.post('/delete', {title:title}).then(window.location.href = "{{url_for('boards_user')}}");
    }
    }
});

var connect = new Vue({
    delimiters:["[[", "]]"],
    el: "#connect",
    data: {
        text : "Connect",
        user_name: "{{given_name}}",
        logged: "{{logged}}"
    },
    methods: {
      login: function login(){
        window.location.href = "{{url_for('login_screen')}}";
      }
    }
  });

  function update_info(){
    if(connect.logged == 1){
        connect.text = "Hi, " + connect.user_name;
    }
  }

update_info();
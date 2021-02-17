var menu = new Vue({
    delimiters:["[[", "]]"],
    el: "#menu",
    data:{
      title: "{{title}}",
      content: "",
      logged:"{{logged}}"
    },
    methods:{
      save:  function save () {
        this.title = document.getElementById("title").value;

        for(var i = 0; i < lst.List.length; i++){
          this.content += lst.List[i].text + "/c";
        }

        var data = [];

        for(var i = 0; i < lst.List.length; i++){
          var dict = {};
          dict.id = lst.List[i].id;
          dict.text = lst.List[i].text.replace(/\\/g, "|");
          console.log(lst.List[i].id);
          console.log(lst.List[i].text);
          data.push(dict);
        }

        cleaned = this.content.replace(/\\/g, "|");
  
        axios.post('/update', {
        title: this.title, content:cleaned, data:data});
    },
    board_list: function board_list(){
      window.location.href = "{{url_for('boards_user')}}";
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
        }else{
            document.getElementById("save").style.display = "none";
            document.getElementById("myBoards").style.display = "none";
            document.getElementById("login_message").style.display = "block";
        }
      }
    
    update_info();
  
    Vue.component('todo-item', {
      delimiters:["[[", "]]"],
      props: ['todo', 'selected_id', 'update', 'del_element'],
      template: "<div class='container' v-on:click.self='update(todo.id)'><div id='output' class='output' value='item.text'></div><button class='remove' v-on:click='del_element(todo.id)'>Remove</button><button class='edit' v-on:click='update(todo.id)'>Edit</button></div>"
    });
    
    var lst = new Vue({
      delimiters:["[[", "]]"],
      el: '#lst',
      data: {
        List: JSON.parse('{{content|safe}}'),
        selected_id: 0,
      },
      methods: {      update: function update(id){
              this.selected_id = id;
              render.selected_id = id;
              document.getElementById("input").value = this.List[id]["text"].split("|").join("\\");
    
              document.getElementById("input").focus();
    
              let divs = document.getElementsByClassName("container");
    
              for(let i = 0; i < divs.length; i++){
                if(i == id){
                  divs[i].style.border = "3px solid black";
                }else{
                  divs[i].style.border = "1px solid grey";
                }
              }
    
          },
          add: function add(){
              var size = this.List.length;
              this.List.push({id:size, text:""});
              this.selected_id = size;
              document.getElementById("input").value = "";
          },
          del_element: function del_element(id){
            let index;
            for(var i = 0; i < this.List.length; i++){
              if(this.List[i]["id"] == id){
                  index = i;
              }
            }
    
            this.List = this.List.slice(0, index).concat(this.List.slice(index+1, this.List.length));
    
            console.log(index);
    
            for(var i = index; i < this.List.length; i++){
                console.log("Antes:" + this.List[i]["id"]);
                this.List[i]["id"] += -1;
                console.log("Depois:" +  this.List[i]["id"]);
            }
            
            update = document.getElementsByClassName("output");
    
            for(var i = 0; i < update.length -1; i++){
                update[i].innerHTML = this.List[i]["text"].split("|").join("\\");
            }
            
            MathJax.typeset();
            
          }
      }
    });
    
    function set_values(){
      values = document.getElementsByClassName("output");
    
      dic = JSON.parse('{{content|safe}}');
    
      for(var i = 0; i < values.length; i++){
        var cleaned = lst.List[i]["text"].split("|").join("\\");
        values[i].innerHTML = cleaned;
      }
    }
    
    set_values();
    
    var render = new Vue({
      delimiters: ["[[", "]]"],
      el: "#render",
      data: {
          selected_id : lst.selected_id,
          current_text: ""
      },
      methods:{
        convert: function convert() {
        
        //
        //  Get the TeX input
        //
        var input = document.getElementById("input").value.trim();
  
        output = document.getElementsByClassName('output')[lst.selected_id];
  
        output.innerHTML = input;
  
        lst.List[lst.selected_id]["text"] = input;
  
        MathJax.typeset();
      }
      }
  });

  function after_load(){

    document.getElementsByClassName("container")[0].style.border = "3px solid black";
    document.getElementById("input").focus();
    if(menu.title == "None"){
      menu.title = "";
    }
  }
var request = new XMLHttpRequest();
var url = location.href;
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
request.onerror = () =>{
    console.log('Error occurred');
};

function send_request(method, body){
    request.open(method, url);
    request.setRequestHeader('Content-Type', 'charset=UTF-8');
    request.setRequestHeader('X-CSRFToken', csrftoken);
    request.send(body);
}


const todo_list = document.querySelector('.todo-list');
const remove = document.querySelectorAll('.remove');
const add = document.querySelector('.add');

add.addEventListener('click', (event) =>{
    item = document.querySelector('.todo-list-input').value;
    if (item){
        request.onload = () => {
            location.reload();
            console.log(`Task with text ${item} was created.`);
        };
        send_request('POST', `text=${item}`);
    }
});

todo_list.addEventListener('change', (event) => {
    var target = event.target;
    var state = '';
    pk = target.closest('li').getAttribute('value');
    body = `pk=${pk}&completed=`;
    if (!target.getAttribute('checked')){
        body += 'true';
        state = true;
        target.closest('li').classList.add('completed');
    }else{
        body += 'false';
        state = false;
        target.closest('li').classList.remove('completed');
    }
    request.onload = () => {
            location.reload();
            console.log(`Task with pk ${pk} was changed to ${state}`);
    };
    send_request('PUT', body);
    
});

remove.forEach((currentValue) =>{
    currentValue.addEventListener('click', (event) => {
        target = event.target
        pk = target.closest('li').getAttribute('value');
        body = `pk=${pk}`;
        request.onload = () => {
            location.reload();
            console.log(`Task with pk ${pk} was deleted`);
        };
        send_request('DELETE', body);
    });
});

var debugging = false;
function debug(obj){
	if (debugging){
		console.log(obj);
	}
}

var baseURL = 'https://watchparty.ignaciopardo.repl.co/';

var title = localStorage.getItem('title');
var platform = localStorage.getItem('platform');
var url;

var usr = localStorage.getItem('usr');
var pas = localStorage.getItem('pas');

if (window.location.href.includes('redirect_signin')){
	const queryString = window.location.search;
	const urlParams = new URLSearchParams(queryString);
	usr = urlParams.get('usr')
	pas = urlParams.get('pas')
}
debug({usr, pas});
var signed = false;
var initial = true;
var first = false;

var login_div;
var main_div;

var usr_txt;
var pas_txt;
var o_usr;

var signout_btn;
var signin_btn;
var signup_btn;
var add_btn;
var remove_btn;

document.addEventListener('DOMContentLoaded', function () {
	document.body.style.overflowY = 'hidden';

	url =	encodeURIComponent(window.location.href.replaceAll('/', '|').replaceAll(':', ';'));
	signout_btn = document.getElementsByClassName('signout_btn')[0];
	signin_btn = document.getElementsByClassName('signin_btn')[0];
	signup_btn = document.getElementsByClassName('signup_btn')[0];
	add_btn = document.getElementsByClassName('add_btn')[0];
	remove_btn = document.getElementsByClassName('remove_btn')[0];
	

	signout_btn.addEventListener('click', signout);
	signin_btn.addEventListener('click', _signin);
	signup_btn.addEventListener('click', signup);
	add_btn.addEventListener('click', add);
	remove_btn.addEventListener('click', remove);


	login_div = document.getElementsByClassName('login')[0];
	main_div = document.getElementsByClassName('main')[0];
	usr_txt = document.getElementsByClassName('usr_txt')[0];
	pas_txt = document.getElementsByClassName('pas_txt')[0];
	o_usr = document.getElementsByClassName('new_friend_txt')[0];

	main_div.hidden = true;
	
	first = true;
	signin();

});

function _signin(){
	get_usr_pas();
	if (usr == null || pas == null || usr == 'null' || pas == 'null' || usr == '' || pas == '' ){
		alert('invalid username or password');
	}
	else{
		first = false;
		signin();
	}
}

function get_usr_pas(){
		usr = encodeURIComponent(usr_txt.value);
		pas = pas_txt.value;
		if (pas != ''){
			var md = forge.md.sha256.create();
			md.update(pas);
			pas = encodeURIComponent(md.digest().toHex());
		}
	
}

function hide_show_inputs(){
	if (login_div.hidden){
		document.body.style.overflowY = 'hidden';
	}
	else{
		document.body.style.overflowY = 'visible';
	}
	login_div.hidden = !login_div.hidden;
	main_div.hidden = !login_div.hidden;
}

function string_validate(){
	get_usr_pas();
	if (pas != null && usr != null){
		return true
	}
	else{
		//Alert
		alert('invalid username or password');
		return false
	}
}

function signup(){
	if (string_validate()){
		fetch(baseURL+'new/'+usr+'/'+pas)
			.then(response => response.json())
			.then(data => signup_response(data));
	}
}

function signup_response(data){
	if(data.response){
		hide_show_inputs();
		localStorage.setItem('usr', usr);
		localStorage.setItem('pas', pas);
		signed = true;
		update_np(data.np)
		debug({usr, pas})
	}
	else{
		//Alert
		alert(data.description);
	}
}

function l(r){
	debug(r)
	return r.json()
}

function signin(){
	fetch(baseURL+'validate/'+usr+'/'+pas)
			.then(response => l(response))
			.then(data => signin_response(data));
}

function signin_response(data){
	debug(data);
	if(data.response){
		hide_show_inputs();
		localStorage.setItem('usr',usr);
		localStorage.setItem('pas',pas);
		debug({usr, pas});
		signed = true;
		debug(data.data.np)
		update_np(data.data.np);
		load_friends();
	}
	else{
		if(!first){
			alert(data.description);
		}
	}
}

function load_friends(){
	fetch(baseURL+'get_friends_np/'+usr+'/'+pas)
				.then(response => response.json())
				.then(data => display_friends_np(data));
}

function display_friends_np(data){
	debug(data);
	if (Object.entries(data.data).length == 0){
		document.getElementsByClassName('friends')[0].innerHTML = '<div class="no_friends"><img class="no_friends_img" src="https://watchparty.ignaciopardo.repl.co/static/icons/no_friends.svg"></div>';
	}
	else{
		document.getElementsByClassName('friends')[0].innerHTML = '';
		for (let [key, value] of Object.entries(data.data)) {
			debug(key, value);
			if (value['platform'] == null || value['platform'] == '' || value['platform'] == 'null'){
				document.getElementsByClassName('friends')[0].innerHTML += '<a class="np_item_clickable" href="'+value['url']+'"><div class="strip np_item"><div class="item_platform"></div><div class="item_text"><div class="item_username">'+key+'</div><div class="item_title">'+value['title']+'</div></div></div></a>';
			}
			else{
				var img = value['platform']
				if (window.location.href.includes('white')){
					img += '-owhite'
				}
				document.getElementsByClassName('friends')[0].innerHTML += '<a class="np_item_clickable" href="'+value['url']+'"><div class="strip np_item"><div class="item_platform"><img class="platform_img" src="https://watchparty.ignaciopardo.repl.co/static/icons/'+img+'.svg"></div><div class="item_text"><div class="item_username">'+key+'</div><div class="item_title">'+value['title']+'</div></div></div></a>';
			}
		}
	}
}


function signout(){
	hide_show_inputs();
	usr = null;
	pas = null;
	localStorage.setItem('usr',usr);
	localStorage.setItem('pas',pas);
	pas_txt.value = '';
	signed = false;
	document.getElementsByClassName('friends')[0].innerHTML = '<div class="no_friends"><img class="no_friends_img" src="https://watchparty.ignaciopardo.repl.co/static/icons/no_friends.svg"></div>';
	document.getElementsByClassName('me')[0].innerHTML = '';
}


function add(){
	if (o_usr.value != ''){
		fetch(baseURL+'add/'+usr+'/'+pas+'/'+o_usr.value)
			.then(response => response.json())
			.then(data => load_friends());
	}
	o_usr.value = '';
}
function remove(){
	if (o_usr.value != ''){
		fetch(baseURL+'remove/'+usr+'/'+pas+'/'+o_usr.value)
			.then(response => response.json())
			.then(data => load_friends());
	}
	o_usr.value = '';
}

function update_np(data){
	if (data['platform'] == null || data['platform'] == '' || data['platform'] == 'null')
		document.getElementsByClassName('me')[0].innerHTML = '<center><div class="me_name">'+usr+'</div><div class="me_content"><div class="me_np_platform"></div><div class="me_np_divider"></div><div class="me_np_title">'+data['title']+'</div></div></center>';
	else
		var img = data['platform']
		if (window.location.href.includes('white')){
			img += '-owhite'
		}
		document.getElementsByClassName('me')[0].innerHTML = '<center><div class="me_name">'+usr+'</div><div class="me_content"><div class="me_np_platform"><img src="https://watchparty.ignaciopardo.repl.co/static/icons/'+img+'.svg"></div><div class="me_np_divider"></div><div class="me_np_title">'+data['title']+'</div></div></center>';
}

function update(){
	fetch(baseURL+'update_np/'+usr+'/'+pas+'/'+title+'/'+url+'/'+platform)
	  .then(response => response.json())
	  .then(data => update_np(data));
}
function retrieve_np(){
	fetch(baseURL+'retrieve_np/'+usr+'/'+pas)
	  .then(response => response.json())
	  .then(data => update_np(data));
}

setInterval(timed_loop, 5000);

var pretitle;
function timed_loop(){
	if (signed){
		load_friends();
		retrieve_np();
	}
}

debug({title, url})
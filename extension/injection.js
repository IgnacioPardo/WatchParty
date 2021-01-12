//var baseURL = '"+baseURL+"';
var cors_workarround = 'https://mighty-citadel-72323.herokuapp.com/';//'https://cors-anywhere.herokuapp.com/';
var baseURL = cors_workarround + 'https://watchparty.ignaciopardo.repl.co/';
var title = '';
var platform = '';
var url = encodeURIComponent(window.location.href.replaceAll('/', '|').replaceAll(':', ';'));
if (localStorage.getItem('url') != null)
	localStorage.setItem('url', url);
var usr = localStorage.getItem('usr');
var pas = localStorage.getItem('pas');

if(url.includes('disneyplus')){document.addEventListener('mouseover', read, false);}

function read(){
	if (url.includes('disneyplus')){
		if (document.getElementsByClassName('title-field').length != 0){
			title = encodeURIComponent(document.getElementsByClassName('title-field')[0].innerHTML + ' ' + document.getElementsByClassName('subtitle-field')[0].innerHTML);
			platform = encodeURIComponent('disney');
		}
	}
	else if (url.includes('netflix') && url.includes('watch')){
		title = encodeURIComponent(document.getElementsByClassName('ellipsize-text')[0].childNodes[0].innerHTML + ' ' + document.getElementsByClassName('ellipsize-text')[0].childNodes[1].innerHTML + ' ' + document.getElementsByClassName('ellipsize-text')[0].childNodes[2].innerHTML);
		platform = encodeURIComponent('netflix');
	}
	else if (url.includes('hbogo')){
		title = encodeURIComponent(document.getElementsByClassName('contentTitle')[0].innerHTML);
		platform = encodeURIComponent('hbogo');
	}
	else if (url.includes('youtube') && url.includes('watch')) {
		title = encodeURIComponent(navigator.mediaSession.metadata.artist + ' | ' + navigator.mediaSession.metadata.title);
		platform = encodeURIComponent('youtube');
	} 
	else if (url.includes('spotify')) {
		title = encodeURIComponent(navigator.mediaSession.metadata.artist + ' | ' + navigator.mediaSession.metadata.title);
		platform = encodeURIComponent('spotify');
	}
	else if (url.includes('twitch')){
		title = encodeURIComponent(document.getElementsByClassName('tw-c-text-base tw-font-size-4 tw-line-height-heading tw-semibold tw-title')[0].innerText + ' | ' +  document.getElementsByClassName('tw-ellipsis tw-line-clamp-2 tw-strong tw-word-break-word')[0].innerText);
		platform = encodeURIComponent('twitch');
	}
	else if (url.includes('flow')) {
		title = encodeURIComponent(document.getElementsByClassName('title truncate')[0].innerHTML);
		platform = encodeURIComponent('flow');
	}
	else if (url.includes('crunchyroll')) {
		title = encodeURIComponent(document.getElementsByClassName('ellipsis')[0].innerText);
		platform = encodeURIComponent('crunchyroll');
	}
	else if (url.includes('pluto')) {
		if (url.includes('series')){
			title = encodeURIComponent(document.getElementsByClassName('Overlay__episode-sc-1vplhvo-11 hyLpf')[0].innerHTML.split("&nbsp;")[0] + ' | ' + document.getElementsByClassName('Overlay__title-sc-1vplhvo-14 kSPZyl')[0].innerText);
		}
		else{
			title = encodeURIComponent(document.getElementsByClassName('Overlay__title-sc-1vplhvo-14 kSPZyl')[0].innerText);
		}
		
		platform = encodeURIComponent('pluto');
	}
	else if ('mediaSession' in navigator) {
		if (navigator.mediaSession.metadata){
			title = encodeURIComponent(navigator.mediaSession.metadata.artist + ' | ' + navigator.mediaSession.metadata.title);
			platform = encodeURIComponent('unknown');
		}
	}
	else{
		return null
	}

	url = encodeURIComponent(window.location.href.replaceAll('/', '|').replaceAll(':', ';'));
	
	usr = localStorage.getItem('usr');
	pas = localStorage.getItem('pas');

	return {title, url, platform, usr, pas};
}
function update(_title, _url, _platform, _usr, _pas){
	if (_title != '' && _title != null && _url != '' && _url != null && _platform != '' && _platform != null && _usr != '' && _pas != ''){
		fetch(baseURL+'update_np/'+_usr+'/'+_pas+'/'+_title+'/'+_url+'/'+_platform)
		  .then(response => response.json())
		  .then(data => none(data));
	}
}
function none(data) {
	return null
}

document.addEventListener('DOMContentLoaded', function () {
	result = read();
	update(result.title, result.url, result.platform, result.usr, result.pas);
	localStorage.setItem('url', url);
});

setInterval(timed_loop, 5000);

function timed_loop(){
	/*if (encodeURIComponent(window.location.href.replaceAll('/', '|').replaceAll(':', ';')) != localStorage.getItem('url')){
		console.log('reading ...');
		result = read();
		update(result.title, result.url, result.platform, result.usr, result.pas);
		localStorage.setItem('url', url);
		console.log('done');
	}*/
	result = read();
	update(result.title, result.url, result.platform, result.usr, result.pas);
	localStorage.setItem('url', url);
		
}
read();